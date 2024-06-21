import pandas as pd
import plotly.express as px
import streamlit as st

from src.commons import load_bets
from src.setup import setup
from src.sidebar import render_sidebar

break_line = "<br><br>"


def render_metrics(data):
    """Display metrics for the total number of bets, winrate, profit, and ROI."""
    # Metrics
    total_bets = len(data)
    total_wins = len(data[data["Result"] == "W"])
    total_winrate = (total_wins / total_bets) * 100
    total_profit = data["Profit"].sum()
    total_roi = (total_profit / data["Wager"].sum()) * 100

    # Display metrics in four columns
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Bets", total_bets)
    with col2:
        st.metric("Total Winrate %", f"{total_winrate:.2f}%")
    with col3:
        st.metric("Total Profit (Units)", f"{total_profit:.2f}")
    with col4:
        st.metric("Total ROI %", f"{total_roi:.2f}%")

    st.markdown(break_line, unsafe_allow_html=True)


def render_bet_df(data):
    """Display the bets ledger in a DataFrame."""
    st.write("### Bets Ledger")
    st.dataframe(data, hide_index=True)
    st.markdown(break_line, unsafe_allow_html=True)


def render_profit_timeline(data):
    """Display a line chart showing the profit timeline."""
    chart_name = "### Profit Timeline"
    x_axis = "Month"
    y_axis = "Profit"

    # Ensure 'Date' is in datetime format
    data["Date"] = pd.to_datetime(data["Date"])

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

    # Calculate the range for the y-axis
    min_profit = monthly_profit[y_axis].min() * 0.9
    max_profit = monthly_profit[y_axis].max() * 1.1

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
        yaxis={"range": [min_profit, max_profit]},  # Extend range slightly
        width=1000,  # Adjust width to make plot wider
    )

    # Display the Plotly chart in Streamlit
    st.write(chart_name)
    st.plotly_chart(fig)
    st.markdown(break_line, unsafe_allow_html=True)


def render_summary_table(data):
    """Display a summary table with the total number of bets, wins, losses, draws, profit, winrate, and ROI."""
    # Summary table
    summary_table = (
        data.groupby("League")
        .agg(
            Total_Bets=("Date", "count"),
            Total_Wins=("Result", lambda x: (x == "W").sum()),
            Total_Losses=("Result", lambda x: (x == "L").sum()),
            Total_Draws=("Result", lambda x: (x == "D").sum()),
            Total_Profit=("Profit", "sum"),
            Total_Wager=("Wager", "sum"),
        )
        .reset_index()
    )

    # Compute additional columns
    summary_table["Winrate %"] = (
        summary_table["Total_Wins"] / summary_table["Total_Bets"]
    ) * 100
    summary_table["ROI %"] = (
        summary_table["Total_Profit"] / summary_table["Total_Wager"]
    ) * 100

    st.table(summary_table)


if __name__ == "__main__":
    """
    Main function to render the Streamlit dashboard.
    """
    setup("Yureeh Betting Dashboard", "📈")

    data = load_bets()

    # Capture the filtered data from the sidebar
    filtered_data = render_sidebar(data)

    # Use the filtered data in the rendering functions
    render_metrics(filtered_data)

    # Plot the profit timeline
    render_profit_timeline(filtered_data)

    # Display the filtered data in a table
    render_bet_df(filtered_data)

    # render_summary_table(filtered_data)

# # Pie Chart: % of Bets by League using Plotly
# bets_by_league = data["League"].value_counts().reset_index()
# bets_by_league.columns = ["League", "Count"]
# fig = px.pie(bets_by_league, values="Count", names="League", title="% of Bets by League")
# st.plotly_chart(fig)

# # ROI % by Wager Type
# roi_by_wager = data.groupby("Type")["Profit"].sum() / data.groupby("Type")["Wager"].sum()
# st.bar_chart(roi_by_wager)

# # Win % by Odds
# win_by_odds = data[data["Result"] == "W"].groupby("Odds").size() / data.groupby("Odds").size() * 100
# st.bar_chart(win_by_odds)

# # Win % by League
# win_by_league = data[data["Result"] == "W"].groupby("League").size() / data.groupby("League").size() * 100
# st.bar_chart(win_by_league)
