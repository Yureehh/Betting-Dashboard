import streamlit as st

from src.commons import load_bets
from src.setup import setup
from src.sidebar import render_sidebar


def render_charts(data):
    """Display charts for profit by sportsbook, odds, and league."""
    profit_by_sportsbook = data.groupby("Sportbook")["Profit"].sum()
    st.bar_chart(profit_by_sportsbook)

    profit_by_odds = data.groupby("Odds")["Profit"].sum()
    st.bar_chart(profit_by_odds)

    profit_by_league = data.groupby("League")["Profit"].sum()
    st.bar_chart(profit_by_league)


if __name__ == "__main__":
    setup(
        "Betting Charts",
        "📈",
    )
    data = load_bets()
    render_sidebar(data)

    render_charts(data)
