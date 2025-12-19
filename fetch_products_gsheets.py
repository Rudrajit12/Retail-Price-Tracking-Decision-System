import pandas as pd
import gspread
from google.oauth2.service_account import Credentials


def fetch_products_from_gsheets(
    spreadsheet_id: str,
    service_account_file: str,
    products_tab: str = "products",
    output_csv: str = "products_master.csv"
):
    """
    Fetch product master data from Google Sheets and save it as a CSV.

    This function:
    - Authenticates using a Google service account
    - Reads the specified 'products' tab
    - Converts it into a Pandas DataFrame
    - Saves it locally as products_master.csv

    Parameters:
    - spreadsheet_id (str): Google Sheet ID
    - service_account_file (str): Path to service_account.json
    - products_tab (str): Name of the tab containing product URLs
    - output_csv (str): Output CSV filename

    Returns:
    - pd.DataFrame: Loaded products DataFrame
    """

    # Required scope to read Google Sheets
    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

    # Authenticate using service account
    creds = Credentials.from_service_account_file(
        service_account_file, scopes=scopes
    )
    client = gspread.authorize(creds)

    # Open the spreadsheet and the products tab
    sheet = client.open_by_key(spreadsheet_id)
    worksheet = sheet.worksheet(products_tab)

    # Fetch all rows as list of dictionaries
    records = worksheet.get_all_records()
    df = pd.DataFrame(records)

    # Safety check: products tab should not be empty
    if df.empty:
        raise ValueError("Products tab is empty in Google Sheets")

    # Save locally as CSV for downstream steps
    df.to_csv(output_csv, index=False)

    print(f"Products fetched from Google Sheets: {output_csv}")

    return df
