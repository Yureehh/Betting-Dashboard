import pandas as pd
import plotly.express as px
import streamlit as st

from commons import (
    BLUE_COLOR,
    DOUBLE_VERTICAL_SPACE,
    GREEN_COLOR,
    RED_COLOR,
    load_bets,
    setup,
)
from sidebar import render_sidebar


def plot_bet_number_percentage(data: pd.DataFrame) -> None:
    """
    Plot a pie chart of bet number percentage by league.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.
    """
    st.write("### Bets Percentage by League")
    bet_counts = data["League"].value_counts().reset_index()
    bet_counts.columns = ["League", "Bets Count"]
    bet_counts = bet_counts.sort_values("League")  # Sort alphabetically
    fig = px.pie(
        bet_counts,
        values="Bets Count",
        names="League",
    )
    fig.update_layout(
        showlegend=True,
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(DOUBLE_VERTICAL_SPACE, unsafe_allow_html=True)


def plot_profit_by_league(data: pd.DataFrame) -> None:
    """
    Plot profit by league.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.
    """
    st.write("### Profit by League")
    profit_by_league = (
        data.groupby("League")
        .agg({"Profit": "sum"})
        .reset_index()
        .assign(
            Bets_Count=lambda df: data["League"]
            .value_counts()
            .reindex(df["League"])
            .values,
            Profit=lambda df: df["Profit"].round(2),
        )
        .sort_values("League")
    )

    fig = px.bar(
        profit_by_league,
        x="Profit",
        y="League",
        orientation="h",
        labels={"League": "", "Profit": "Profit (Units)"},
        color=profit_by_league["Profit"].apply(
            lambda x: GREEN_COLOR if x > 0 else RED_COLOR
        ),
        color_discrete_map={GREEN_COLOR: GREEN_COLOR, RED_COLOR: RED_COLOR},
        text="Profit",
        hover_data={"Profit": False, "Bets_Count": True, "League": False},
    )
    fig.update_traces(
        texttemplate="%{text}",
        textposition="outside",
        marker={"line": {"width": 1, "color": "DarkSlateGrey"}},
    )
    fig.update_layout(showlegend=False, yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(DOUBLE_VERTICAL_SPACE, unsafe_allow_html=True)


def plot_winrate_by_league(data: pd.DataFrame) -> None:
    """
    Plot winrate by league.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.
    """
    st.write("### Winrate by League")
    winrate_by_league = (
        data.assign(Win=lambda df: df["Result"].apply(lambda x: 1 if x == "W" else 0))
        .groupby("League")
        .agg({"Win": "mean"})
        .reset_index()
        .assign(
            Bets_Count=lambda df: data["League"]
            .value_counts()
            .reindex(df["League"])
            .values,
            Winrate=lambda df: (df["Win"] * 100).round(2),
        )
        .sort_values("League")
    )

    fig = px.bar(
        winrate_by_league,
        x="Winrate",
        y="League",
        orientation="h",
        labels={"League": "", "Winrate": "Winrate %"},
        color_discrete_sequence=[BLUE_COLOR],  # Darker blue for winrate
        text="Winrate",
        hover_data={"Winrate": False, "Bets_Count": True, "League": False},
    )
    fig.update_traces(
        texttemplate="%{text}%",
        textposition="outside",
        marker={"line": {"width": 1, "color": "DarkSlateGrey"}},
    )
    fig.update_layout(showlegend=False, yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(DOUBLE_VERTICAL_SPACE, unsafe_allow_html=True)


def plot_roi_by_league(data: pd.DataFrame) -> None:
    """
    Plot ROI by league.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.
    """
    st.write("### ROI by League")
    roi_by_league = (
        data.groupby("League")
        .agg({"Profit": "sum", "Wager": "sum"})
        .reset_index()
        .assign(
            Bets_Count=lambda df: data["League"]
            .value_counts()
            .reindex(df["League"])
            .values,
            ROI=lambda df: (df["Profit"] / df["Wager"] * 100).round(2),
        )
        .sort_values("League")
    )

    fig = px.bar(
        roi_by_league,
        x="ROI",
        y="League",
        orientation="h",
        labels={"League": "", "ROI": "ROI %"},
        color=roi_by_league["ROI"].apply(lambda x: GREEN_COLOR if x > 0 else RED_COLOR),
        color_discrete_map={GREEN_COLOR: GREEN_COLOR, RED_COLOR: RED_COLOR},
        text="ROI",
        hover_data={"Bets_Count": True},
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
    setup("Stats by League")

    data = load_bets()

    if not data.empty:
        filtered_data = render_sidebar(data)
        plot_bet_number_percentage(filtered_data)
        plot_profit_by_league(filtered_data)
        plot_winrate_by_league(filtered_data)
        plot_roi_by_league(filtered_data)
        st.markdown("<hr>", unsafe_allow_html=True)
    else:
        st.error("Failed to load data. Please check the data source.")
