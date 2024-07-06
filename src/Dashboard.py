import pandas as pd
import plotly.express as px
import streamlit as st

from src.commons import BREAK_LINE, load_bets, setup
from src.sidebar import render_sidebar


def render_metrics(data):
    """
    Display metrics for the total number of bets, winrate, profit, and ROI.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.
    """
    # Calculate metrics
    total_bets = len(data)
    total_wins = len(data[data["Result"] == "W"])
    total_winrate = (total_wins / total_bets) * 100 if total_bets > 0 else 0
    total_profit = data["Profit"].sum()
    total_roi = (
        (total_profit / data["Wager"].sum()) * 100 if data["Wager"].sum() > 0 else 0
    )

    # Display metrics in four columns
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric(r"\# Bets", total_bets)
    with col2:
        st.metric("Units Wagered", data["Wager"].sum())
    with col3:
        st.metric("Winrate %", f"{total_winrate:.2f}%")
    with col4:
        st.metric("Profit (Units)", f"{total_profit:.2f}")
    with col5:
        st.metric("ROI %", f"{total_roi:.2f}%")

    st.markdown(BREAK_LINE, unsafe_allow_html=True)


def render_bet_df(data):
    """
    Display the bets ledger in a DataFrame.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.
    """
    st.write("### Bets Ledger")
    data["Date"] = data["Date"].dt.date
    st.dataframe(data, hide_index=True)
    st.markdown(BREAK_LINE, unsafe_allow_html=True)


def render_profit_timeline(data):
    """
    Display a line chart showing the profit timeline.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.
    """
    chart_name = "### Profit Timeline"
    x_axis = "Month"
    y_axis = "Profit"

    data.loc[:, "Date"] = pd.to_datetime(data["Date"])

    # Group by month and sum profits
    monthly_profit = data.resample("ME", on="Date")["Profit"].sum().reset_index()
    monthly_profit.columns = [x_axis, y_axis]

    # Create a copy of the 'Month' column in datetime format for range calculation
    monthly_profit["Month_dt"] = monthly_profit["Month"]

    # Convert 'Month' to string format for consistent labeling
    monthly_profit["Month"] = monthly_profit["Month_dt"].dt.strftime("%Y-%m")

    # Calculate the range for the x-axis
    min_date = monthly_profit["Month_dt"].min() - pd.DateOffset(months=2)
    max_date = monthly_profit["Month_dt"].max() + pd.DateOffset(months=1)

    # Create a Plotly figure
    fig = px.line(monthly_profit, x="Month", y=y_axis)

    # Update the layout to include axis titles and wider plot
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Profit (Units)",
        xaxis={
            "tickformat": "%Y-%m",
            "dtick": "M1",  # Ensure one tick per month
            "range": [min_date, max_date],  # Extend range slightly
            "tickmode": "linear",
        },
        width=1000,  # Adjust width to make plot wider
    )

    st.write(chart_name)
    st.plotly_chart(fig)
    st.markdown(BREAK_LINE, unsafe_allow_html=True)


def render_roi_by_wager_type(data):
    """
    Display a horizontal bar chart showing the ROI by wager type with conditional coloring.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.
    """
    roi_by_wager = data.groupby("Type").agg({"Profit": "sum", "Wager": "sum"})
    roi_by_wager["ROI"] = round(
        (roi_by_wager["Profit"] / roi_by_wager["Wager"]) * 100, 2
    )
    roi_by_wager = roi_by_wager.reset_index()

    roi_by_wager["color"] = roi_by_wager["ROI"].apply(
        lambda x: "#00CC96" if x > 0 else "#FF6692"
    )

    fig = px.bar(
        roi_by_wager,
        x="ROI",
        y="Type",
        orientation="h",
        labels={"Type": "Wager Type", "ROI": "ROI %"},
        color="color",
        color_discrete_map={"#00CC96": "#00CC96", "#FF6692": "#FF6692"},
        text="ROI",
    )

    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    fig.update_layout(showlegend=False, yaxis=dict(autorange="reversed"))
    fig.update_traces(marker={"line": {"width": 1, "color": "DarkSlateGrey"}})

    st.write("### ROI by Wager Type")
    st.plotly_chart(fig)
    st.markdown(BREAK_LINE, unsafe_allow_html=True)


if __name__ == "__main__":
    setup("Yureeh Betting Dashboard", "📈")

    data = load_bets()

    if not data.empty:
        filtered_data = render_sidebar(data)
        print(filtered_data.columns)
        render_metrics(filtered_data)
        render_profit_timeline(filtered_data)
        render_bet_df(filtered_data)
        render_roi_by_wager_type(filtered_data)

        st.markdown("<hr>", unsafe_allow_html=True)
    else:
        st.error("Failed to load data. Please check the data source.")
