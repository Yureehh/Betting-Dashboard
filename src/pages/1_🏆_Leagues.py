import plotly.express as px
import streamlit as st

from commons import VERTICAL_SPACE, load_bets, setup
from sidebar import render_sidebar


def plot_bet_number_percentage(data):
    """
    Plot a pie chart of bet number percentage by league.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.
    """
    st.write("### Bet Number Percentage by League")
    bet_counts = data["League"].value_counts().reset_index()
    bet_counts.columns = ["League", "Count"]
    fig = px.pie(
        bet_counts,
        values="Count",
        names="League",
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(VERTICAL_SPACE, unsafe_allow_html=True)


def plot_profit_by_league(data):
    """
    Plot profit by league.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.
    """
    st.write("### Profit by League")
    profit_by_league = data.groupby("League")["Profit"].sum().reset_index()
    profit_by_league["Profit"] = profit_by_league["Profit"].round(2)
    profit_by_league = profit_by_league.sort_values(
        by="Profit", ascending=False
    )  # Optimize sorting for display
    fig = px.bar(
        profit_by_league,
        x="Profit",
        y="League",
        orientation="h",
        labels={"League": "", "Profit": "Profit (Units)"},
        color=profit_by_league["Profit"].apply(
            lambda x: "#00CC96" if x > 0 else "#FF6692"
        ),
        color_discrete_map={"#00CC96": "#00CC96", "#FF6692": "#FF6692"},
        text="Profit",
    )
    fig.update_traces(texttemplate="%{text}", textposition="outside")
    fig.update_layout(showlegend=False, yaxis=dict(autorange="reversed"))
    fig.update_traces(marker={"line": {"width": 1, "color": "DarkSlateGrey"}})
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(VERTICAL_SPACE, unsafe_allow_html=True)


def plot_winrate_by_league(data):
    """
    Plot winrate by league.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.
    """
    st.write("### Winrate by League")
    data["Win"] = data["Result"].apply(lambda x: 1 if x == "W" else 0)
    winrate_by_league = data.groupby("League")["Win"].mean().reset_index()
    winrate_by_league["Winrate"] = (winrate_by_league["Win"] * 100).round(2)
    winrate_by_league = winrate_by_league.sort_values(
        by="Winrate", ascending=False
    )  # Optimize sorting for display
    fig = px.bar(
        winrate_by_league,
        x="Winrate",
        y="League",
        orientation="h",
        labels={"League": "", "Winrate": "Winrate %"},
        color_discrete_sequence=["#0057B8"],  # Darker blue for winrate
        text="Winrate",
    )
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    fig.update_layout(showlegend=False, yaxis=dict(autorange="reversed"))
    fig.update_traces(marker={"line": {"width": 1, "color": "DarkSlateGrey"}})
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(VERTICAL_SPACE, unsafe_allow_html=True)


def plot_roi_by_league(data):
    """
    Plot ROI by league.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.
    """
    st.write("### ROI by League")
    roi_by_league = data.groupby("League").agg({"Profit": "sum", "Wager": "sum"})
    roi_by_league["ROI"] = (
        (roi_by_league["Profit"] / roi_by_league["Wager"]) * 100
    ).round(2)
    roi_by_league = roi_by_league.reset_index()
    roi_by_league = roi_by_league.sort_values(
        by="ROI", ascending=False
    )  # Optimize sorting for display
    fig = px.bar(
        roi_by_league,
        x="ROI",
        y="League",
        orientation="h",
        labels={"League": "", "ROI": "ROI %"},
        color=roi_by_league["ROI"].apply(lambda x: "#00CC96" if x > 0 else "#FF6692"),
        color_discrete_map={"#00CC96": "#00CC96", "#FF6692": "#FF6692"},
        text="ROI",
    )
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    fig.update_layout(showlegend=False, yaxis=dict(autorange="reversed"))
    fig.update_traces(marker={"line": {"width": 1, "color": "DarkSlateGrey"}})
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(VERTICAL_SPACE, unsafe_allow_html=True)


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
