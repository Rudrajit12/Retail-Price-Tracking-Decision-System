# 🛒 Retail Price Tracking & Repricing Decision System

### *Competitor Pricing Intelligence for Reliance Digital*

> **An end-to-end automated pricing intelligence pipeline that monitors competitor prices (Amazon & Flipkart), compares them against Reliance Digital, and generates actionable repricing insights via an automated dashboard.**

---

## 🚀 Project Overview

In highly competitive electronics retail, **pricing decisions must be data-driven and fast**.
Even small delays in reacting to competitor price changes can lead to **lost sales or margin erosion**.

This project simulates a **real-world Retail Analyst role at Reliance Digital**, where the goal is to:

* Continuously monitor competitor prices
* Identify under-pricing and over-pricing situations
* Detect stock-based pricing opportunities
* Provide **clear repricing recommendations** through a live dashboard

---

## 🎯 Business Problem

Reliance Digital sells electronics across multiple categories (mobiles, laptops, accessories).
Competitors like **Amazon and Flipkart** frequently change prices and stock availability.

### Key challenges:

* Prices fluctuate multiple times a day
* Manual monitoring is not scalable
* Delayed response impacts revenue and market share
* Stock-outs by competitors create pricing opportunities

---

## 💡 Solution Approach

This system builds a **fully automated pricing intelligence pipeline** that:

1. **Scrapes competitor prices & stock**
2. **Normalizes and logs pricing data**
3. **Compares Reliance Digital prices vs market**
4. **Generates repricing recommendations**
5. **Updates a live Google Sheets dashboard**
6. **Runs automatically on a schedule**

---

## 🧩 System Architecture

```
Google Sheets (Products Master)
        ↓
Local Automated Scraper (Python)
        ↓
Price Log (CSV)
        ↓
Pricing Comparison Engine
        ↓
Actionable Insights (CSV)
        ↓
Google Sheets Dashboard
```

> ⚠️ Scraping is executed locally (or via scheduler) to avoid bot-blocking from e-commerce sites.
> Analytics & dashboards remain fully automated.

---

## ⚙️ Tech Stack

| Layer           | Tools                               |
| --------------- | ----------------------------------- |
| Language        | Python                              |
| Scraping        | Playwright, Requests, BeautifulSoup |
| Data Processing | Pandas, NumPy                       |
| Storage         | CSV, Google Sheets                  |
| Automation      | Windows Task Scheduler              |
| Visualization   | Google Sheets Dashboard             |
| Version Control | Git & GitHub                        |

---

## 📂 Project Structure

```
Retail-Price-Tracking-Decision-System/
│
├── fetch_products_gsheets.py     # Fetch product URLs from Google Sheets
├── scraper.py                   # Amazon, Flipkart & Reliance Digital scrapers
├── compare_prices.py            # Pricing gap & repricing logic
├── upload_gsheets.py            # Upload outputs to Google Sheets
├── main.py                      # End-to-end pipeline runner
├── run_pipeline.bat             # Scheduler entry point (Windows)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🔍 Key Features

### ✅ Multi-Site Price Monitoring

* Amazon
* Flipkart
* Reliance Digital

### ✅ Robust Scraping Logic

* Playwright-based scraping for JS-heavy sites
* Graceful failure handling
* Partial data tolerance (real-world behavior)

### ✅ Intelligent Pricing Analysis

* Market minimum price detection
* Price gap & % difference calculation
* Stock-based pricing opportunities
* Clear **“Who Should Reprice?”** recommendation

### ✅ Automated Dashboard Updates

* Live Google Sheets dashboard
* No manual intervention required
* Historical price logging

---

## 📊 Pricing Intelligence Logic (Example)

| Scenario                      | Insight                       |
| ----------------------------- | ----------------------------- |
| Reliance price > Market min   | Consider price reduction      |
| Reliance price < Market min   | Opportunity to improve margin |
| Amazon OOS, Reliance In-Stock | Reliance can increase price   |
| Minimal gap (<5%)             | Maintain current price        |

---

## 🖥 Dashboard (Google Sheets)

The dashboard provides:

* Current prices by retailer
* Price gaps vs competitors
* Repricing recommendations
* Stock opportunity flags

Designed for:

* Retail Analysts
* Pricing Managers
* Category Managers

---

## 🔄 Automation Strategy

### Why NOT GitHub Actions for Scraping?

* GitHub runner IPs are aggressively blocked by e-commerce websites
* Leads to partial or inconsistent data

### Chosen Approach (Industry-Realistic)

* **Local scheduled scraping** (trusted IP)
* **Fully automated pipeline execution**
* **Dashboard always stays updated**

> This mirrors how real retail analytics teams handle competitor intelligence.

---

## ▶️ How to Run Locally

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### 2️⃣ Configure credentials

* Add `service_account.json` (not committed)
* Share Google Sheet with service account email

### 3️⃣ Run pipeline

```bash
python main.py
```

---

## ⏰ Automation (Windows)

Pipeline is automated using **Windows Task Scheduler**:

* Daily scheduled execution
* Automatic dashboard refresh
* Execution logs stored locally

---

## 📈 Business Impact

* Enables **faster pricing decisions**
* Improves margin optimization
* Identifies stock-based opportunities
* Reduces manual monitoring effort
* Scales to hundreds of SKUs

---

## 🧠 Skills Demonstrated

* Retail & consumer analytics
* Competitor pricing strategy
* Web scraping under real-world constraints
* Data pipeline design
* Automation & scheduling
* Business-driven analytics storytelling

---

## 🔮 Future Enhancements

* Add email / Slack alerts
* Integrate historical trend analysis
* Category-level pricing recommendations
* Cloud VM deployment
* Proxy-based scraping for scale

---

## 👤 Author

**Rudrajit Bhattacharyya**

Data Analyst | Retail & Consumer Analytics

* 📍 Bengaluru, India
* 🔗 [LinkedIn](https://www.linkedin.com/in/rudrajitb/)
* 💻 [GitHub](https://github.com/Rudrajit12)

---
