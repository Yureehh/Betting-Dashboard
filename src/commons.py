import os
from datetime import datetime
from typing import Optional

import gspread
import pandas as pd
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials

VERTICAL_SPACE = "<br><br>"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1rrBtklorbir3zrsHkzTAFlmahxu_S9Gnyrg1RQhRtHw/edit?usp=drive_link"
GREEN_COLOR = "#00CC96"
RED_COLOR = "#FF6692"
BLUE_COLOR = "#0057B8"


def setup(page_title: str, page_icon: Optional[str] = ""):
    """
    Setup the Streamlit page with the given title and icon.

    Args:
        page_title (str): The title of the Streamlit page.
        page_icon (Optional[str]): The icon for the Streamlit page.
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
    css_file_path = "styles/styles.css"
    if os.path.exists(css_file_path):
        with open(css_file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"Custom styles not applied. '{css_file_path}' file not found.")


def compute_profit(bets_df: pd.DataFrame) -> pd.Series:
    """
    Compute the profit for each bet using vectorized operations.

    Args:
        bets_df (pd.DataFrame): The DataFrame containing bet information.

    Returns:
        pd.Series: A Series with the computed profit for each bet.
    """
    profit = bets_df["Wager"] * (bets_df["Odds"] - 1)
    loss_condition = bets_df["Result"].isin(["L", "Loss", "Lose"])
    profit.loc[loss_condition] = -bets_df["Wager"]
    profit.loc[bets_df["Result"] == "Draw"] = 0
    return profit


@st.cache_data(ttl=60 * 5)  # Cache the data for 5 minutes
def load_bets_from_google_sheet(sheet_url: str) -> pd.DataFrame:
    """
    Load bets data from Google Sheets.

    Args:
        sheet_url (str): The URL of the Google Sheets document.

    Returns:
        pd.DataFrame: DataFrame containing the bets data.
    """
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]

        # Load credentials from Streamlit secrets
        creds_dict = dict(st.secrets["gspread_credentials"])

        # Fix private key formatting issue (if needed)
        creds_dict["private_key"] += "\n-----END PRIVATE KEY-----\n"

        # Load credentials directly from the dictionary
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)

        # Open the Google Sheet by URL
        sheet = client.open_by_url(
            sheet_url
        ).sheet1  # Assumes data is in the first sheet

        # Extract data into a DataFrame
        bets_data = sheet.get_all_records()
        return pd.DataFrame(bets_data).replace("", pd.NA)

    except gspread.exceptions.SpreadsheetNotFound:
        st.error("The Google Sheet was not found. Please check the URL.")
    except gspread.exceptions.APIError as e:
        st.error(f"API Error: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

    return pd.DataFrame()


def process_bets_data(bets_df: pd.DataFrame, pending: bool = False) -> pd.DataFrame:
    """
    Process the loaded bets data by computing additional columns.

    Args:
        bets_df (pd.DataFrame): The DataFrame containing the loaded bet data.
        pending (bool): If True, filter to only pending bets.

    Returns:
        pd.DataFrame: The processed DataFrame.
    """
    if bets_df.empty:
        return bets_df

    bets_df = (
        bets_df[bets_df["Result"].isna()].copy() if pending else bets_df.dropna().copy()
    )
    bets_df["Date"] = pd.to_datetime(bets_df["Date"], errors="coerce")
    bets_df["To_Win"] = bets_df["Wager"] * (bets_df["Odds"] - 1)
    bets_df["Profit"] = compute_profit(bets_df)
    bets_df["ROI"] = (bets_df["Profit"] / bets_df["Wager"] * 100).round(2).astype(
        str
    ) + "%"

    # Ensure 'Premium' column is the last column in the DataFrame if it exists
    if "Premium" in bets_df.columns:
        cols = [col for col in bets_df.columns if col != "Premium"] + ["Premium"]
        bets_df = bets_df.loc[:, cols]

    return bets_df


def load_bets(pending: bool = False) -> pd.DataFrame:
    """
    Load and process the bets ledger data from Google Sheets.

    Args:
        pending (bool): If True, only pending bets will be returned.

    Returns:
        pd.DataFrame: The processed bets ledger DataFrame.
    """
    bets_df = load_bets_from_google_sheet(SHEET_URL)
    return process_bets_data(bets_df, pending)


def get_latest_date(filepath: str) -> str:
    """
    Get the latest modification date of a file.

    Args:
        filepath (str): The file path to check.

    Returns:
        str: The last modification date formatted as 'YYYY-MM-DD'.
    """
    try:
        modified_time = os.path.getmtime(filepath)
        return datetime.fromtimestamp(modified_time).strftime("%Y-%m-%d")
    except FileNotFoundError:
        st.error(f"File not found: {filepath}")
        return ""  # Return empty string if file is not found
