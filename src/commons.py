from typing import Optional

import gspread
import pandas as pd
import pyperclip
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials

HORIZONTAL_LINE = "<hr>"
SINGLE_VERTICAL_SPACE = "<br>"
DOUBLE_VERTICAL_SPACE = "<br><br>"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1rrBtklorbir3zrsHkzTAFlmahxu_S9Gnyrg1RQhRtHw/edit?usp=drive_link"
GREEN_COLOR = "#00CC96"
RED_COLOR = "#FF6692"
BLUE_COLOR = "#0057B8"
REFERRAL_LINK = "https://thunderpick.io?r=ORACLE_BETS"
REFERRAL_CODE = "ORACLE_BETS"
REFERRAL_COPY = "🚀 **Join ThunderPick now to claim your deposit bonus!**"
REFERRAL_BUTTON = f"📢 **Click to Copy Referral Code:** '_{REFERRAL_CODE}_'"
REFERRAL_BUTTON_TOOLTIP = "Copied Referral to Clipboard"
ABOUT_TEXT = "Public ledger of LoL Oracle betting activity.\nTwitter: @Oracle_Betss"
PREMIUM_STRING = "Premium"


def setup(page_title: str, page_icon: Optional[str] = None) -> None:
    """
    Setup the Streamlit page with the given title and icon.

    Args:
        page_title (str): The title of the Streamlit page.
        page_icon (Optional[str]): The icon for the Streamlit page.
    """
    st.set_page_config(
        page_title="LoL Oracle",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "About": ABOUT_TEXT,
        },
        page_icon=page_icon,
    )
    st.title(page_title)
    st.markdown(SINGLE_VERTICAL_SPACE, unsafe_allow_html=True)
    render_referral_section()
    st.markdown(HORIZONTAL_LINE, unsafe_allow_html=True)
    st.markdown(SINGLE_VERTICAL_SPACE, unsafe_allow_html=True)


def render_referral_section() -> None:
    """
    Renders the referral section with a button to go to the referral link and another to copy the referral code.
    """

    if st.button(REFERRAL_COPY, key="referral_link", type="primary"):
        st.write(
            f'<meta http-equiv="refresh" content="0; url={REFERRAL_LINK}" />',
            unsafe_allow_html=True,
        )

    if st.button(REFERRAL_BUTTON, key="referral_code", type="secondary"):
        pyperclip.copy(REFERRAL_CODE)
        st.success(REFERRAL_BUTTON_TOOLTIP, icon="✔️")


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
    profit = profit.mask(loss_condition, -bets_df["Wager"])
    profit = profit.mask(bets_df["Result"] == "Draw", 0)
    return profit


@st.cache_data(ttl=300)  # Cache the data for 5 minutes
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

        # Fix private key formatting issue
        if not creds_dict["private_key"].endswith("\n-----END PRIVATE KEY-----\n"):
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
    bets_df["ROI"] = ((bets_df["Profit"] / bets_df["Wager"]) * 100).round(2).astype(
        str
    ) + "%"

    # Ensure 'Premium' column is the last column in the DataFrame if it exists
    if PREMIUM_STRING in bets_df.columns:
        bets_df = bets_df[
            [col for col in bets_df.columns if col != PREMIUM_STRING] + [PREMIUM_STRING]
        ]

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
