import plotly.express as px
import streamlit as st

from commons import BLUE_COLOR, GREEN_COLOR, RED_COLOR, VERTICAL_SPACE, load_bets, setup
from sidebar import render_sidebar

ODDS_GROUP_STR = "Odds Group"


def group_odds(odds):
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


def plot_bet_number_percentage(data):
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
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(VERTICAL_SPACE, unsafe_allow_html=True)


def plot_profit_by_odds(data):
    """
    Plot profit by odds group.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.
    """
    st.write("### Profit by Odds Group")
    profit_by_odds = data.groupby(ODDS_GROUP_STR).agg({"Profit": "sum"}).reset_index()
    profit_by_odds["Bets Count"] = (
        data[ODDS_GROUP_STR]
        .value_counts()
        .reindex(profit_by_odds[ODDS_GROUP_STR])
        .values
    )
    profit_by_odds["Profit"] = profit_by_odds["Profit"].round(2)
    profit_by_odds = profit_by_odds.sort_values(by=ODDS_GROUP_STR)
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
        hover_data={"Profit": False, "Bets Count": True, ODDS_GROUP_STR: False},
    )
    fig.update_traces(texttemplate="%{text}", textposition="outside")
    fig.update_layout(showlegend=False, yaxis=dict(autorange="reversed"))
    fig.update_traces(marker={"line": {"width": 1, "color": "DarkSlateGrey"}})
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(VERTICAL_SPACE, unsafe_allow_html=True)


def plot_winrate_by_odds(data):
    """
    Plot winrate by odds group.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.
    """
    st.write("### Winrate by Odds Group")
    data["Win"] = data["Result"].apply(lambda x: 1 if x == "W" else 0)
    winrate_by_odds = data.groupby(ODDS_GROUP_STR).agg({"Win": "mean"}).reset_index()
    winrate_by_odds["Bets Count"] = (
        data[ODDS_GROUP_STR]
        .value_counts()
        .reindex(winrate_by_odds[ODDS_GROUP_STR])
        .values
    )
    winrate_by_odds["Winrate"] = (winrate_by_odds["Win"] * 100).round(2)
    winrate_by_odds = winrate_by_odds.sort_values(ODDS_GROUP_STR)
    fig = px.bar(
        winrate_by_odds,
        x="Winrate",
        y=ODDS_GROUP_STR,
        orientation="h",
        labels={ODDS_GROUP_STR: "", "Winrate": "Winrate %"},
        color_discrete_sequence=[BLUE_COLOR],  # Darker blue for winrate
        text="Winrate",
        hover_data={"Winrate": False, "Bets Count": True, ODDS_GROUP_STR: False},
    )
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    fig.update_layout(showlegend=False, yaxis=dict(autorange="reversed"))
    fig.update_traces(marker={"line": {"width": 1, "color": "DarkSlateGrey"}})
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(VERTICAL_SPACE, unsafe_allow_html=True)


def plot_roi_by_odds(data):
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
    )
    roi_by_odds["Bets Count"] = (
        data[ODDS_GROUP_STR].value_counts().reindex(roi_by_odds[ODDS_GROUP_STR]).values
    )
    roi_by_odds["ROI"] = ((roi_by_odds["Profit"] / roi_by_odds["Wager"]) * 100).round(2)
    roi_by_odds = roi_by_odds.sort_values(ODDS_GROUP_STR)
    fig = px.bar(
        roi_by_odds,
        x="ROI",
        y=ODDS_GROUP_STR,
        orientation="h",
        labels={ODDS_GROUP_STR: "", "ROI": "ROI %"},
        color=roi_by_odds["ROI"].apply(lambda x: GREEN_COLOR if x > 0 else RED_COLOR),
        color_discrete_map={GREEN_COLOR: GREEN_COLOR, RED_COLOR: RED_COLOR},
        text="ROI",
        hover_data={"ROI": False, "Bets Count": True, ODDS_GROUP_STR: False},
    )
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    fig.update_layout(showlegend=False, yaxis=dict(autorange="reversed"))
    fig.update_traces(marker={"line": {"width": 1, "color": "DarkSlateGrey"}})
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(VERTICAL_SPACE, unsafe_allow_html=True)


# The line `# from paths import (` is a commented-out import statement in Python. It is used to
# indicate that the code previously had an import statement from a module named `paths`, but it has
# been commented out and not currently in use.

if __name__ == "__main__":
    setup("Stats by Odds")

    data = load_bets()

    if not data.empty:
        filtered_data = render_sidebar(data)

        filtered_data[ODDS_GROUP_STR] = filtered_data["Odds"].apply(group_odds)

        plot_bet_number_percentage(filtered_data)
        plot_profit_by_odds(filtered_data)
        plot_winrate_by_odds(filtered_data)
        plot_roi_by_odds(filtered_data)

        st.markdown("<hr>", unsafe_allow_html=True)
    else:
        st.error("Failed to load data. Please check the data source.")
