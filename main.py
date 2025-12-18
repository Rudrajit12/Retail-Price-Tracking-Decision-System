from fetch_products_gsheets import fetch_products_from_gsheets
from scraper import run_scraper
from compare_prices import run_comparison
from upload_gsheets import upload_outputs_to_gsheets
import os

# -----------------------------
# GLOBAL CONFIGURATION
# -----------------------------
#GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
GOOGLE_SHEET_ID = "1A8HCLYpR5RNopFxVJJ_a5-Dkj-isXzB7Ql6TFJA7Ca4"
SERVICE_ACCOUNT_FILE = "service_account.json"


def main():
    """
    Orchestrates the entire Reliance Digital pricing pipeline.

    Execution flow:
    1. Fetch products from Google Sheets
    2. Scrape prices from Reliance, Amazon, Flipkart
    3. Compare Reliance pricing vs market
    4. Upload results back to Google Sheets
    """

    print("\n🚀 Starting Reliance Digital Pricing Intelligence Pipeline\n")

    # Step 1: Fetch product URLs & metadata
    print("⏳ Fetching products from Google Sheets...\n")
    fetch_products_from_gsheets(
        spreadsheet_id=GOOGLE_SHEET_ID,
        service_account_file=SERVICE_ACCOUNT_FILE
    )

    # Step 2: Scrape prices and stock status
    print("\n⏳ Scraping product prices and stock status...\n")
    run_scraper()

    # Step 3: Compare Reliance pricing vs market
    print("\n⏳ Comparing Reliance Digital Prices vs Market...\n")
    run_comparison()

    # Step 4: Publish outputs to Google Sheets
    print("\n⏳ Uploading outputs to Google Sheets...\n")
    upload_outputs_to_gsheets(
        spreadsheet_id=GOOGLE_SHEET_ID,
        service_account_file=SERVICE_ACCOUNT_FILE
    )

    print("\n✅ Pipeline executed successfully!\n")


# Entry point
if __name__ == "__main__":
    main()
