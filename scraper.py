import pandas as pd
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from datetime import datetime
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-IN,en;q=0.9",
}

# ---------------- AMAZON SCRAPER ----------------
def scrape_amazon(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        page.goto(url, timeout=90000)
        page.wait_for_timeout(8000)  # wait for JS price

        price = None
        selectors = [
            "span.a-price-whole",
            "span.a-offscreen",
            "#priceblock_ourprice",
            "#priceblock_dealprice",
            "#corePrice_feature_div span.a-price-whole",
        ]

        for sel in selectors:
            element = page.query_selector(sel)
            if element:
                raw = element.inner_text().strip()
                price = (
                    raw.replace(",", "")
                       .replace("₹", "")
                       .replace("\n", "")
                       .replace(".", "")
                       .strip()
                )
                if price.isdigit():
                    break

        # STOCK
        stock = "Unknown"
        try:
            s = page.query_selector("#availability span")
            if s:
                stock = s.inner_text().strip()
        except:
            pass

        browser.close()
        return price, stock


# ---------------- FLIPKART SCRAPER ----------------
def scrape_flipkart(url):
    """
    Scrape Flipkart price and stock using Playwright.
    Reliable in CI/CD environments.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url, timeout=60000)
            page.wait_for_timeout(6000)  # allow JS to render

            html = page.content()
            browser.close()

        soup = BeautifulSoup(html, "html.parser")

        # -------- PRICE --------
        price = None
        selectors = [
            "._30jeq3",
            "._16Jk6d",
            "._3I9_wc",
            ".Nx9bqj",
            "div._25b18c ._30jeq3",
            "div.hZ3P6w.bnqy13"
        ]

        for sel in selectors:
            elem = soup.select_one(sel)
            if elem:
                price = (
                    elem.get_text(strip=True)
                    .replace("₹", "")
                    .replace(",", "")
                )
                break

        # -------- STOCK --------
        stock = "In Stock"
        stock_elem = soup.select_one("._16FRp0")
        if stock_elem:
            stock = stock_elem.get_text(strip=True)

        # -------- BLOCK DETECTION --------
        if not price:
            if "captcha" in soup.text.lower() or "verify" in soup.text.lower():
                return None, "Blocked by Flipkart"
            return None, "Price not found"

        return price, stock

    except Exception as e:
        print(f"Flipkart Playwright error: {e}")
        return None, "Error"

# ---------------- RELIANCE DIGITAL SCRAPER ----------------
def scrape_reliance(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=60000)

            # wait for main content to load
            page.wait_for_selector("h1", timeout=60000)
            time.sleep(2)

            # ✅ FINAL STOCK LOGIC (TEXT-BASED)
            page_text = page.inner_text("body").lower()
            if "currently unavailable" in page_text:
                stock = "Out of Stock"
            else:
                stock = "In Stock"

            html = page.content()
            browser.close()

        soup = BeautifulSoup(html, "html.parser")

        # -------- PRICE --------
        price = None
        price_tag = soup.select_one("div[class*='price']")
        if price_tag:
            price = (
                price_tag.get_text(strip=True)
                .replace("₹", "")
                .replace(",", "")
                .replace("\n", "")
                .replace(".00", "")
                .strip()
            )

        return price, stock

    except Exception as e:
        print("Reliance Digital scraper error:", e)
        return None, "Error"


# ---------------- MAIN SCRAPER FUNCTION ----------------
def run_scraper():
    print("Running scrapers...")
    df = pd.read_csv("products_master.csv")

    results = []

    for _, row in df.iterrows():
        print(f"Scraping: {row['product_name']} | {row['site']}")
        
        try:
            if row["site"].lower() == "amazon":
                price, stock = scrape_amazon(row["url"])

            elif row["site"].lower() == "flipkart":
                price, stock = scrape_flipkart(row["url"])

            elif row["site"].lower() == "reliance digital":
                price, stock = scrape_reliance(row["url"])
            else:
                price, stock = None, "Unsupported"

        except Exception as e:
            print(f"Scraping failed for {row['site']} | {row['product_name']}: {e}")
            price, stock = None, "Error"

        results.append([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            row["product_id"],
            row["product_name"],
            row["site"],
            price,
            stock
        ])
        
        time.sleep(1.5)

    # Save output
    log_df = pd.DataFrame(results, columns=[
        "timestamp", "product_id", "product_name", "site", "price", "stock"
    ])

    log_df.to_csv("price_log.csv", index=False)
    print("\n Scraping complete! Saved to price_log.csv\n")
