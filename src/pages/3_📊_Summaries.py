import streamlit as st

from commons import VERTICAL_SPACE, load_bets, setup
from sidebar import render_sidebar


def render_table(data, values, index, columns, aggfunc, title, round_digits=2):
    """
    General function to render a table using Streamlit, displaying aggregated data.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.
        values (str): The column to aggregate.
        index (str): The column to group by for the rows.
        columns (str): The column to group by for the columns.
        aggfunc (str or function): The aggregation function (e.g., 'sum', 'mean', 'count').
        title (str): The title of the table to display.
        round_digits (int): The number of decimal places to round the results. Default is 2.
    """
    st.write(f"### {title}")
    table = data.pivot_table(
        values=values, index=index, columns=columns, aggfunc=aggfunc, fill_value=0
    )
    table = table.round(round_digits)
    st.dataframe(table)
    st.markdown(VERTICAL_SPACE, unsafe_allow_html=True)


def render_profit_table(data):
    """
    Render a table showing profit by bet type and league.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.
    """
    render_table(
        data,
        values="Profit",
        index="Type",
        columns="League",
        aggfunc="sum",
        title="Profit (Units)",
    )


def render_bet_count_table(data):
    """
    Render a table showing the number of bets by bet type and league.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.
    """
    render_table(
        data,
        values="Date",
        index="Type",
        columns="League",
        aggfunc="count",
        title="Bets Count (#)",
    )


def render_total_wager_table(data):
    """
    Render a table showing the total wager by bet type and league.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.
    """
    render_table(
        data,
        values="Wager",
        index="Type",
        columns="League",
        aggfunc="sum",
        title="Total Wager (Units)",
    )


def render_average_odds_table(data):
    """
    Render a table showing the average odds by bet type and league.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.
    """
    render_table(
        data,
        values="Odds",
        index="Type",
        columns="League",
        aggfunc="mean",
        title="Average Bet Odds",
    )


def render_win_rate_table(data):
    """
    Render a table showing the win rate by bet type and league.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.
    """
    data["Win"] = data["Result"].apply(lambda x: 1 if x == "W" else 0)
    render_table(
        data,
        values="Win",
        index="Type",
        columns="League",
        aggfunc="mean",
        title="Win Rate (%)",
        round_digits=2,
    )


if __name__ == "__main__":
    setup("Summaries by Bet and League")

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
