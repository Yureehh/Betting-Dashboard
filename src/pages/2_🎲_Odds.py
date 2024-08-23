import pandas as pd
import plotly.express as px
import streamlit as st

from commons import (
    BLUE_COLOR,
    DOUBLE_VERTICAL_SPACE,
    GREEN_COLOR,
    RED_COLOR,
    render_horizontal_line,
    setup_and_load_bets,
)
from sidebar import render_sidebar

ODDS_GROUP_STR = "Odds Group"
PAGE_NAME = "Stats by Odds"


def group_odds(odds: float) -> str:
    """
    Group odds into specified ranges.

    Args:
        odds (float): The odds value to be grouped.

    Returns:
        str: The odds group as a string.
    """
    if odds < 1.5:
        return "1.00 - 1.49"
    elif odds < 2.0:
        return "1.50 - 1.99"
    elif odds < 2.5:
        return "2.00 - 2.49"
    elif odds < 3.0:
        return "2.50 - 2.99"
    else:
        return ">= 3.00"


def plot_bet_number_percentage(data: pd.DataFrame) -> None:
    """
    Plot a pie chart of bet number percentage by odds group.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.
    """
    st.write("### Bets Percentage by Odds Group")
    bet_counts = data[ODDS_GROUP_STR].value_counts().reset_index()
    bet_counts.columns = [ODDS_GROUP_STR, "Bets Count"]
    bet_counts = bet_counts.sort_values(ODDS_GROUP_STR)

    fig = px.pie(
        bet_counts,
        values="Bets Count",
        names=ODDS_GROUP_STR,
    )

    fig.update_layout(
        yaxis=dict(autorange="reversed"),
        showlegend=True,
        autosize=True,
        legend=dict(orientation="v", x=1.1, y=0.5),
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown(DOUBLE_VERTICAL_SPACE, unsafe_allow_html=True)


def plot_profit_by_odds(data: pd.DataFrame) -> None:
    """
    Plot profit by odds group.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.
    """
    st.write("### Profit by Odds Group")
    profit_by_odds = (
        data.groupby(ODDS_GROUP_STR)
        .agg({"Profit": "sum"})
        .reset_index()
        .assign(
            Bets_Count=lambda df: data[ODDS_GROUP_STR]
            .value_counts()
            .reindex(df[ODDS_GROUP_STR])
            .values,
            Profit=lambda df: df["Profit"].round(2),
        )
        .sort_values(by=ODDS_GROUP_STR)
    )

    fig = px.bar(
        profit_by_odds,
        x="Profit",
        y=ODDS_GROUP_STR,
        orientation="h",
        labels={ODDS_GROUP_STR: "", "Profit": "Profit (Units)"},
        color=profit_by_odds["Profit"].apply(
            lambda x: GREEN_COLOR if x > 0 else RED_COLOR
        ),
        color_discrete_map={GREEN_COLOR: GREEN_COLOR, RED_COLOR: RED_COLOR},
        text="Profit",
        hover_data={"Profit": False, "Bets_Count": True, ODDS_GROUP_STR: False},
    )
    fig.update_traces(
        texttemplate="%{text}",
        textposition="outside",
        marker={"line": {"width": 1, "color": "DarkSlateGrey"}},
    )
    fig.update_layout(showlegend=False, yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(DOUBLE_VERTICAL_SPACE, unsafe_allow_html=True)


def plot_winrate_by_odds(data: pd.DataFrame) -> None:
    """
    Plot winrate by odds group.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.
    """
    st.write("### Winrate by Odds Group")
    winrate_by_odds = (
        data.assign(Win=lambda df: df["Result"].apply(lambda x: 1 if x == "W" else 0))
        .groupby(ODDS_GROUP_STR)
        .agg({"Win": "mean"})
        .reset_index()
        .assign(
            Bets_Count=lambda df: data[ODDS_GROUP_STR]
            .value_counts()
            .reindex(df[ODDS_GROUP_STR])
            .values,
            Winrate=lambda df: (df["Win"] * 100).round(2),
        )
        .sort_values(by=ODDS_GROUP_STR)
    )

    fig = px.bar(
        winrate_by_odds,
        x="Winrate",
        y=ODDS_GROUP_STR,
        orientation="h",
        labels={ODDS_GROUP_STR: "", "Winrate": "Winrate %"},
        color_discrete_sequence=[BLUE_COLOR],  # Darker blue for winrate
        text="Winrate",
        hover_data={"Winrate": False, "Bets_Count": True, ODDS_GROUP_STR: False},
    )
    fig.update_traces(
        texttemplate="%{text}%",
        textposition="outside",
        marker={"line": {"width": 1, "color": "DarkSlateGrey"}},
    )
    fig.update_layout(showlegend=False, yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(DOUBLE_VERTICAL_SPACE, unsafe_allow_html=True)


def plot_roi_by_odds(data: pd.DataFrame) -> None:
    """
    Plot ROI by odds group.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.
    """
    st.write("### ROI by Odds Group")
    roi_by_odds = (
        data.groupby(ODDS_GROUP_STR)
        .agg({"Profit": "sum", "Wager": "sum"})
        .reset_index()
        .assign(
            Bets_Count=lambda df: data[ODDS_GROUP_STR]
            .value_counts()
            .reindex(df[ODDS_GROUP_STR])
            .values,
            ROI=lambda df: ((df["Profit"] / df["Wager"]) * 100).round(2),
        )
        .sort_values(by=ODDS_GROUP_STR)
    )

    fig = px.bar(
        roi_by_odds,
        x="ROI",
        y=ODDS_GROUP_STR,
        orientation="h",
        labels={ODDS_GROUP_STR: "", "ROI": "ROI %"},
        color=roi_by_odds["ROI"].apply(lambda x: GREEN_COLOR if x > 0 else RED_COLOR),
        color_discrete_map={GREEN_COLOR: GREEN_COLOR, RED_COLOR: RED_COLOR},
        text="ROI",
        hover_data={"ROI": False, "Bets_Count": True, ODDS_GROUP_STR: False},
    )
    fig.update_traces(
        texttemplate="%{text}%",
        textposition="outside",
        marker={"line": {"width": 1, "color": "DarkSlateGrey"}},
    )
    fig.update_layout(showlegend=False, yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(DOUBLE_VERTICAL_SPACE, unsafe_allow_html=True)


if __name__ == "__main__":

    data = setup_and_load_bets(PAGE_NAME)

    if not data.empty:
        filtered_data = render_sidebar(data)
        filtered_data[ODDS_GROUP_STR] = filtered_data["Odds"].apply(group_odds)

        plot_bet_number_percentage(filtered_data)
        plot_profit_by_odds(filtered_data)
        plot_winrate_by_odds(filtered_data)
        plot_roi_by_odds(filtered_data)

        render_horizontal_line()
    else:
        st.error("Failed to load data. Please check the data source.")
