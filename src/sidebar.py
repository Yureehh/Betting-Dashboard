import pandas as pd
import streamlit as st

START_DATE = pd.Timestamp("2024-08-01")


def render_sidebar(data, pending=False):
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
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
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

    if leagues := st.sidebar.multiselect("**League**", data["League"].unique()):
        data = data[data["League"].isin(leagues)]

    if teams := st.sidebar.multiselect("**Team**", data["Team"].unique()):
        data = data[data["Team"].isin(teams)]

    if bet_types := st.sidebar.multiselect("**Bet Type**", data["Type"].unique()):
        data = data[data["Type"].isin(bet_types)]

    # Bet result filter (only if not pending)
    if not pending:
        if bet_results := st.sidebar.multiselect(
            "**Bet Result**", data["Result"].unique()
        ):
            data = data[data["Result"].isin(bet_results)]

    return data
