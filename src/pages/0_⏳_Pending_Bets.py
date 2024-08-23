import pandas as pd
import streamlit as st

from commons import DOUBLE_VERTICAL_SPACE, render_horizontal_line, setup_and_load_bets
from sidebar import render_sidebar

PAGE_NAME = "Pending Bets"
MISSING_DATA_MESSAGE = "No data available. Please check the data source."


def render_pending_bets_df(pending_bets_df: pd.DataFrame) -> None:
    """
    Display the pending bets in a DataFrame.

    Args:
        pending_bets_df (pd.DataFrame): The DataFrame containing the pending bets.
    """
    if pending_bets_df.empty:
        st.write("No pending bets to display.")
    else:
        st.write("### Pending Bets")
        pending_bets_df["Date"] = pending_bets_df["Date"].dt.date
        pending_bets_df = pending_bets_df.sort_values(by="Date", ascending=False)
        st.dataframe(pending_bets_df, hide_index=True)
        st.markdown(DOUBLE_VERTICAL_SPACE, unsafe_allow_html=True)


def main() -> None:
    """
    Main function to set up the page and render the pending bets.
    """

    all_bets_df = setup_and_load_bets(PAGE_NAME, pending=True)

    if all_bets_df.empty:
        st.error(MISSING_DATA_MESSAGE)
    else:
        filtered_bets_df = render_sidebar(all_bets_df, pending=True)
        render_pending_bets_df(filtered_bets_df)
        render_horizontal_line()


if __name__ == "__main__":
    main()
