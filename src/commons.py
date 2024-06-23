import pandas as pd
import streamlit as st

from utils.paths import BETS_PATH

# Suppress SettingWithCopyWarning warnings
pd.options.mode.chained_assignment = None

BREAK_LINE = "<br><br>"


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
            "About": "Public ledger of my betting activity.\nTwitter: @Yureehwastaken",
        },
        page_icon=page_icon,
    )
    apply_custom_styles()
    st.title(page_title)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)


def apply_custom_styles():
    """
    Apply custom CSS styles to the Streamlit page.
    """
    st.markdown(
        """
        <style>
            html, body, div, span, applet, object, iframe,
            h1, h2, h3, h4, h5, h6, p, blockquote, pre,
            a, abbr, acronym, address, big, cite, code,
            del, dfn, em, img, ins, kbd, q, s, samp,
            small, strike, strong, sub, sup, tt, var,
            b, u, i, center,
            dl, dt, dd, ol, ul, li,
            fieldset, form, label, legend,
            table, caption, tbody, tfoot, thead, tr, th, td,
            article, aside, canvas, details, embed,
            figure, figcaption, footer, header, hgroup,
            menu, nav, output, ruby, section, summary,
            time, mark, audio, video,
            .main .block-container, [class*="css"] {
                font-family: 'Source Code Pro', monospace;
            }

            h1, .main .block-container {
                font-family: 'Source Code Pro', monospace;
            }

            .main .block-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 2rem;
            }
            .stMetric {
                text-align: center;
            }
            .block-container table {
                margin-top: 2rem;
            }
            .footer {
                position: fixed;
                left: 0;
                bottom: 0;
                width: 100%;
                background-color: #f1f1f1;
                text-align: center;
                padding: 1rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def compute_profit(row):
    """
    Compute the profit for each bet.

    Args:
        row (pd.Series): A row of the DataFrame containing bet information.

    Returns:
        float: The computed profit for the bet.
    """
    if row["Result"] == "W":
        return row["Wager"] * (row["Odds"] - 1)
    elif row["Result"] == "L":
        return -row["Wager"]
    else:  # Draw
        return 0


def load_bets():
    """
    Load the bets ledger CSV file and compute additional columns.

    Returns:
        pd.DataFrame: A DataFrame with the bet data and computed columns.
    """
    try:
        # Load the CSV file
        #  TODO: read it from s3
        data = pd.read_csv(BETS_PATH)
    except FileNotFoundError:
        st.error("The bets ledger file was not found. Please check the path.")
        return pd.DataFrame()
    except pd.errors.EmptyDataError:
        st.error("The bets ledger file is empty.")
        return pd.DataFrame()

    # Select only the required columns
    data = data[
        [
            "Date",
            "Team",
            "League",
            "Game",
            "Type",
            "Sportbook",
            "Bet",
            "Result",
            "Odds",
            "Wager",
        ]
    ]

    # Convert 'Date' to datetime
    data["Date"] = pd.to_datetime(data["Date"])

    # Compute the 'To_Win' column
    data["To_Win"] = data["Wager"] * (data["Odds"] - 1)

    # Compute the 'Profit' column
    data["Profit"] = data.apply(compute_profit, axis=1)

    # Compute the ROI column
    data["ROI"] = (data["Profit"] / data["Wager"] * 100).apply(
        lambda x: f"{str(round(x, 2))}%"
    )

    return data
