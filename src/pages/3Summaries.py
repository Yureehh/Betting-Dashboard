import streamlit as st

from src.commons import BREAK_LINE, load_bets, setup
from src.sidebar import render_sidebar


def render_profit_table(data):
    """
    Render a table showing profit by bet type and league.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.
    """
    st.write("### Profit")
    profit_table = data.pivot_table(
        values="Profit", index="Type", columns="League", aggfunc="sum", fill_value=0
    )
    profit_table = profit_table.round(2)
    st.dataframe(profit_table)
    st.markdown(BREAK_LINE, unsafe_allow_html=True)


def render_bet_count_table(data):
    """
    Render a table showing the number of bets by bet type and league.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.
    """
    st.write("### Bets Count")
    bet_count_table = data.pivot_table(
        values="Date", index="Type", columns="League", aggfunc="count", fill_value=0
    )
    st.dataframe(bet_count_table)
    st.markdown(BREAK_LINE, unsafe_allow_html=True)


def render_total_wager_table(data):
    """
    Render a table showing the total wager by bet type and league.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.
    """
    st.write("### Total Wager")
    wager_table = data.pivot_table(
        values="Wager", index="Type", columns="League", aggfunc="sum", fill_value=0
    )
    wager_table = wager_table.round(2)
    st.dataframe(wager_table)
    st.markdown(BREAK_LINE, unsafe_allow_html=True)


def render_average_odds_table(data):
    """
    Render a table showing the average odds by bet type and league.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.
    """
    st.write("### Average Odds")
    odds_table = data.pivot_table(
        values="Odds", index="Type", columns="League", aggfunc="mean", fill_value=0
    )
    odds_table = odds_table.round(2)
    st.dataframe(odds_table)
    st.markdown(BREAK_LINE, unsafe_allow_html=True)


def render_win_rate_table(data):
    """
    Render a table showing the win rate by bet type and league.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.
    """
    st.write("### Win Rate")
    data.loc[:, "Win"] = data["Result"].apply(lambda x: 1 if x == "W" else 0)
    win_rate_table = data.pivot_table(
        values="Win", index="Type", columns="League", aggfunc="mean", fill_value=0
    )
    win_rate_table = (win_rate_table * 100).round(2)
    st.dataframe(win_rate_table)
    st.markdown(BREAK_LINE, unsafe_allow_html=True)


if __name__ == "__main__":
    setup("Summaries by Bet and League", "⭕")

    data = load_bets()

    if not data.empty:
        filtered_data = render_sidebar(data)

        render_profit_table(filtered_data)
        render_bet_count_table(filtered_data)
        render_win_rate_table(filtered_data)
        render_total_wager_table(filtered_data)
        render_average_odds_table(filtered_data)

        st.markdown("<hr>", unsafe_allow_html=True)
    else:
        st.error("Failed to load data. Please check the data source.")
