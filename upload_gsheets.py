import pandas as pd
import gspread
import json
import numpy as np
from google.oauth2.service_account import Credentials


def upload_csv_to_sheet(sheet, df, tab_name):
    """
    Upload a Pandas DataFrame to a specific Google Sheets tab.

    This function:
    - Creates the tab if it doesn't exist
    - Clears existing data if it does
    - Safely converts NaN / inf values (Google Sheets does not accept them)
    - Uploads data row-by-row

    Parameters:
    - sheet: gspread Spreadsheet object
    - df (pd.DataFrame): Data to upload
    - tab_name (str): Target tab name
    """

    # Create or clear the worksheet
    try:
        worksheet = sheet.worksheet(tab_name)
        worksheet.clear()
    except:
        worksheet = sheet.add_worksheet(
            title=tab_name,
            rows=5000,
            cols=50
        )

    # Replace NaN / inf values (JSON-safe conversion)
    df_clean = df.replace([np.nan, np.inf, -np.inf], "")

    # Prepare rows for Google Sheets API
    rows = [df_clean.columns.tolist()]
    for _, row in df_clean.iterrows():
        rows.append([str(x) if x != "" else "" for x in row.tolist()])

    # Upload to Google Sheets
    worksheet.update(rows)

    print(f"Uploaded data to tab: {tab_name}")


def upload_outputs_to_gsheets(
    spreadsheet_id: str,
    service_account_file: str,
    price_log_csv: str = "price_log.csv",
    comparison_csv: str = "price_comparison_results.csv",
    products_csv: str = "products_master.csv",
):
    """
    Upload all pipeline outputs to Google Sheets.

    This function uploads:
    - Products master
    - Price log (raw scraped data)
    - Reliance vs Market pricing comparison

    Parameters:
    - spreadsheet_id (str): Google Sheet ID
    - service_account_file (str): Path to service_account.json
    - price_log_csv (str): Path to price_log.csv
    - comparison_csv (str): Path to comparison CSV
    - products_csv (str): Path to products master CSV
    """

    # Full Sheets access required for writing
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]

    # Authenticate Google Sheets
    creds = Credentials.from_service_account_file(
        service_account_file, scopes=scopes
    )
    client = gspread.authorize(creds)

    # Open target spreadsheet
    sheet = client.open_by_key(spreadsheet_id)

    # Load CSV outputs
    df_log = pd.read_csv(price_log_csv)
    df_comp = pd.read_csv(comparison_csv)
    df_products = pd.read_csv(products_csv)

    # Upload each dataset to its respective tab
    upload_csv_to_sheet(sheet, df_products, "products")
    upload_csv_to_sheet(sheet, df_log, "price_log")
    upload_csv_to_sheet(sheet, df_comp, "price_comparison_results")

    print("\n All outputs uploaded to Google Sheets successfully!")
