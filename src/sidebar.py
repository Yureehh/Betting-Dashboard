import pandas as pd
import streamlit as st

from commons import SINGLE_VERTICAL_SPACE

START_DATE = pd.Timestamp("2024-08-01")


def render_sidebar(data: pd.DataFrame, pending: bool = False) -> pd.DataFrame:
    """
    Render the sidebar for filtering the bets ledger.

    Args:
        data (pd.DataFrame): The DataFrame containing the bets ledger.
        pending (bool): If True, filters out results for pending bets.

    Returns:
        pd.DataFrame: Filtered DataFrame based on sidebar inputs.
    """
    if data.empty:
        st.sidebar.warning("No data available to filter.")
        return data

    # Sidebar for filters
    st.sidebar.markdown(SINGLE_VERTICAL_SPACE, unsafe_allow_html=True)
    st.sidebar.title("**Filters**")

    # Date filters
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input("**Start date**", value=START_DATE)
    with col2:
        end_date = st.date_input("**End date**", value=None)

    # Apply date filters
    if start_date:
        data = data[data["Date"] >= pd.Timestamp(start_date)]

    if end_date:
        data = data[data["Date"] <= pd.Timestamp(end_date)]

    if bet_types := st.sidebar.multiselect(
        "**Bet Type**", sorted(data["Type"].unique())
    ):
        data = data[data["Type"].isin(bet_types)]

    if leagues := st.sidebar.multiselect("**League**", sorted(data["League"].unique())):
        data = data[data["League"].isin(leagues)]

    if teams := st.sidebar.multiselect("**Team**", sorted(data["Team"].unique())):
        data = data[data["Team"].isin(teams)]

    # Bet result filter (only if not pending)
    if not pending:
        if bet_results := st.sidebar.multiselect(
            "**Bet Result**", sorted(data["Result"].unique())
        ):
            data = data[data["Result"].isin(bet_results)]

    return data
