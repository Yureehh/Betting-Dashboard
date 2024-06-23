import pandas as pd
import streamlit as st


def render_sidebar(data):
    """
    Render the sidebar for filtering the bets ledger.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.

    Returns:
        pd.DataFrame: Filtered data frame based on sidebar inputs.
    """
    # Sidebar for filters
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    st.sidebar.title("**Filters**")

    # Date filters
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input("**Start date**", value=None)
    with col2:
        end_date = st.date_input("**End date**", value=None)

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

    if bet_results := st.sidebar.multiselect("**Bet Result**", data["Result"].unique()):
        data = data[data["Result"].isin(bet_results)]

    return data
