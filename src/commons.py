import os
from datetime import datetime

import gspread
import pandas as pd
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials

VERTICAL_SPACE = "<br><br>"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1rrBtklorbir3zrsHkzTAFlmahxu_S9Gnyrg1RQhRtHw"
CREDENTIALS_FILE = "lol-oracle-google-credentials.json"


def setup(page_title, page_icon=""):
    """
    Setup the Streamlit page with the given title and icon.

    Args:
        page_title (str): The title of the Streamlit page.
        page_icon (str): The icon for the Streamlit page.
    """
    st.set_page_config(
        page_title=page_title,
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "About": "Public ledger of my betting activity.\nTwitter: @Yureehwastaken"
        },
        page_icon=page_icon,
    )
    apply_custom_styles()
    st.title(page_title)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)


def apply_custom_styles():
    """
    Apply custom CSS styles to the Streamlit page by loading from an external CSS file.
    """
    with open("styles/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def compute_profit(data):
    """
    Compute the profit for each bet using vectorized operations.

    Args:
        data (pd.DataFrame): The DataFrame containing bet information.

    Returns:
        pd.Series: A Series with the computed profit for each bet.
    """
    profit = data["Wager"] * (data["Odds"] - 1)
    profit[data["Result"].isin(["L", "Loss", "Lose"])] = -data["Wager"]
    profit[data["Result"] == "Draw"] = 0
    return profit


def load_bets_from_google_sheet(credentials_file, sheet_url):
    """
    Load bets data from Google Sheets.

    Args:
        sheet_url (str): The URL of the Google Sheets document.
        credentials_file (str): The path to the JSON credentials file.

    Returns:
        pd.DataFrame: DataFrame containing the bets data.
    """
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
    client = gspread.authorize(creds)

    # Open the Google Sheet by URL
    sheet = client.open_by_url(sheet_url).sheet1  # Assumes data is in the first sheet

    # Extract data into a DataFrame
    data = sheet.get_all_records()
    return pd.DataFrame(data)


def process_bets_data(data):
    """
    Process the loaded bets data by computing additional columns.

    Args:
        data (pd.DataFrame): The DataFrame containing the loaded bet data.

    Returns:
        pd.DataFrame: The processed DataFrame.
    """
    if data.empty:
        return data

    data = data.dropna()
    data["Date"] = pd.to_datetime(data["Date"])
    data["To_Win"] = data["Wager"] * (data["Odds"] - 1)
    data["Profit"] = compute_profit(data)
    data["ROI"] = (data["Profit"] / data["Wager"] * 100).round(2).astype(str) + "%"
    return data


def load_bets():
    """
    Load and process the bets ledger data from Google Sheets.

    Returns:
        pd.DataFrame: The processed bets ledger DataFrame.
    """
    try:
        data = load_bets_from_google_sheet(CREDENTIALS_FILE, SHEET_URL)
        return process_bets_data(data)
    except FileNotFoundError:
        st.error("The Google credentials file was not found. Please check the path.")
        return pd.DataFrame()
    except gspread.exceptions.SpreadsheetNotFound:
        st.error("The Google Sheet was not found. Please check the URL.")
        return pd.DataFrame()


def get_latest_date(filepath):
    """
    Get the latest modification date of a file.

    Args:
        filepath (str): The file path to check.

    Returns:
        str: The last modification date formatted as 'YYYY-MM-DD'.
    """
    modified_time = os.path.getmtime(filepath)
    return datetime.fromtimestamp(modified_time).strftime("%Y-%m-%d")
