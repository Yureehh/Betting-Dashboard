import pandas as pd
import streamlit as st


def render_sidebar(data):
    """Render the sidebar for filtering the bets ledger."""
    # Sidebar for filters
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    st.sidebar.title("**Filters**")

    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input("**Start date**", value=None)
    with col2:
        end_date = st.date_input("**End date**", value=None)

    if start_date:
        data = data[data["Date"] >= pd.Timestamp(start_date)]

    if end_date:
        data = data[data["Date"] <= pd.Timestamp(end_date)]

    # League filter
    leagues = st.sidebar.multiselect("**League**", data["League"].unique())
    if leagues:
        data = data[data["League"].isin(leagues)]

    # Team filter
    teams = st.sidebar.multiselect("**Team**", data["Team"].unique())
    if teams:
        data = data[data["Team"].isin(teams)]

    # Bet type filter
    bet_types = st.sidebar.multiselect("**Bet Type**", data["Type"].unique())
    if bet_types:
        data = data[data["Type"].isin(bet_types)]

    # Bet Result filter
    bet_results = st.sidebar.multiselect("**Bet Result**", data["Result"].unique())
    if bet_results:
        data = data[data["Result"].isin(bet_results)]

    return data
