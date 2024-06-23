import plotly.express as px
import streamlit as st

from src.commons import break_line, load_bets
from src.setup import setup
from src.sidebar import render_sidebar


def group_odds(odds):
    """Group odds into specified ranges."""
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
    """Plot pie chart of bet number percentage given odds group."""
    st.write("### Bet Number Percentage by Odds Group")
    bet_counts = data["Odds Group"].value_counts().reset_index()
    bet_counts.columns = ["Odds Group", "Count"]
    fig = px.pie(
        bet_counts,
        values="Count",
        names="Odds Group",
    )
    st.plotly_chart(fig)
    st.markdown(break_line, unsafe_allow_html=True)


def plot_profit_by_odds(data):
    """Plot profit by odds."""
    st.write("### Profit by Odds")
    profit_by_odds = data.groupby("Odds Group")["Profit"].sum().reset_index()
    profit_by_odds["Profit"] = profit_by_odds["Profit"].round(2)
    fig = px.bar(
        profit_by_odds,
        x="Profit",
        y="Odds Group",
        orientation="h",
        labels={"Odds Group": "", "Profit": "Profit (Units)"},
        color=profit_by_odds["Profit"].apply(
            lambda x: "#00CC96" if x > 0 else "#FF6692"
        ),
        color_discrete_map={"#00CC96": "#00CC96", "#FF6692": "#FF6692"},
        text="Profit",
    )
    fig.update_traces(texttemplate="%{text}", textposition="outside")
    fig.update_layout(showlegend=False)
    fig.update_traces(marker={"line": {"width": 1, "color": "DarkSlateGrey"}})
    st.plotly_chart(fig)
    st.markdown(break_line, unsafe_allow_html=True)


def plot_winrate_by_odds(data):
    """Plot winrate by odds."""
    st.write("### Winrate by Odds")
    data["Win"] = data["Result"].apply(lambda x: 1 if x == "W" else 0)
    winrate_by_odds = data.groupby("Odds Group")["Win"].mean().reset_index()
    winrate_by_odds["Winrate"] = (winrate_by_odds["Win"] * 100).round(2)
    fig = px.bar(
        winrate_by_odds,
        x="Winrate",
        y="Odds Group",
        orientation="h",
        labels={"Odds Group": "", "Winrate": "Winrate %"},
        color=winrate_by_odds["Winrate"].apply(
            lambda x: "#00CC96" if x > 50 else "#FF6692"
        ),
        color_discrete_map={"#00CC96": "#00CC96", "#FF6692": "#FF6692"},
        text="Winrate",
    )
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    fig.update_layout(showlegend=False)
    fig.update_traces(marker={"line": {"width": 1, "color": "DarkSlateGrey"}})
    st.plotly_chart(fig)
    st.markdown(break_line, unsafe_allow_html=True)


def plot_roi_by_odds(data):
    """Plot ROI by odds."""
    st.write("### ROI by Odds")
    roi_by_odds = data.groupby("Odds Group").agg({"Profit": "sum", "Wager": "sum"})
    roi_by_odds["ROI"] = ((roi_by_odds["Profit"] / roi_by_odds["Wager"]) * 100).round(2)
    roi_by_odds = roi_by_odds.reset_index()
    fig = px.bar(
        roi_by_odds,
        x="ROI",
        y="Odds Group",
        orientation="h",
        labels={"Odds Group": "", "ROI": "ROI %"},
        color=roi_by_odds["ROI"].apply(lambda x: "#00CC96" if x > 0 else "#FF6692"),
        color_discrete_map={"#00CC96": "#00CC96", "#FF6692": "#FF6692"},
        text="ROI",
    )
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    fig.update_layout(showlegend=False)
    fig.update_traces(marker={"line": {"width": 1, "color": "DarkSlateGrey"}})
    st.plotly_chart(fig)
    st.markdown(break_line, unsafe_allow_html=True)


if __name__ == "__main__":
    setup("Stats by Odds", "📈")

    data = load_bets()

    filtered_data = render_sidebar(data)

    filtered_data["Odds Group"] = filtered_data["Odds"].apply(group_odds)

    plot_bet_number_percentage(filtered_data)
    plot_profit_by_odds(filtered_data)
    plot_winrate_by_odds(filtered_data)
    plot_roi_by_odds(filtered_data)

    st.markdown("<hr>", unsafe_allow_html=True)
