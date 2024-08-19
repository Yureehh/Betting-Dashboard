import pandas as pd
import plotly.express as px
import streamlit as st

from commons import VERTICAL_SPACE, load_bets, setup
from sidebar import render_sidebar


def calculate_metrics(data):
    """
    Calculate metrics such as total bets, winrate, profit, and ROI.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.

    Returns:
        dict: A dictionary containing calculated metrics.
    """
    total_bets = len(data)
    total_wins = len(data[data["Result"] == "W"])
    total_winrate = (total_wins / total_bets) * 100 if total_bets > 0 else 0
    total_profit = data["Profit"].sum()
    total_wager = data["Wager"].sum()
    total_roi = (total_profit / total_wager) * 100 if total_wager > 0 else 0

    return {
        "total_bets": total_bets,
        "total_wager": round(total_wager, 2),
        "total_winrate": round(total_winrate, 2),
        "total_profit": round(total_profit, 2),
        "total_roi": round(total_roi, 2),
    }


def render_metrics(metrics):
    """
    Display metrics for the total number of bets, winrate, profit, and ROI.

    Args:
        metrics (dict): A dictionary containing calculated metrics.
    """
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Bets", metrics["total_bets"])
    with col2:
        st.metric("Units Wagered", metrics["total_wager"])
    with col3:
        st.metric("Winrate %", f"{metrics['total_winrate']}%")
    with col4:
        st.metric("Profit (Units)", f"{metrics['total_profit']}")
    with col5:
        st.metric("ROI %", f"{metrics['total_roi']}%")

    st.markdown(VERTICAL_SPACE, unsafe_allow_html=True)


def render_bet_df(data):
    """
    Display the bets ledger in a DataFrame.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.
    """
    st.write("### Bets Ledger")
    data["Date"] = data["Date"].dt.date
    data = data.sort_values(by="Date", ascending=False)
    st.dataframe(data, hide_index=True)
    st.markdown(VERTICAL_SPACE, unsafe_allow_html=True)


def render_profit_timeline(data):
    """
    Display a line chart showing the profit timeline.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.
    """
    chart_name = "### Profit Timeline"
    x_axis = "Month"
    y_axis = "Profit (Units)"

    data["Date"] = pd.to_datetime(data["Date"])

    # Group by month and sum profits
    monthly_profit = data.resample("ME", on="Date")["Profit"].sum().reset_index()
    monthly_profit.columns = [x_axis, y_axis]

    # Create a separate column for month in string format for display
    monthly_profit["Month_str"] = monthly_profit[x_axis].dt.strftime("%Y-%m")

    # Compute display range for x-axis
    min_date = monthly_profit[x_axis].min() - pd.DateOffset(months=1)
    max_date = monthly_profit[x_axis].max() + pd.DateOffset(months=1)

    # Create the Plotly figure
    fig = px.line(
        monthly_profit,
        x=x_axis,
        y=y_axis,
        markers=True,
    )

    fig.update_layout(
        xaxis_title=None,
        yaxis_title=y_axis,
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
    st.markdown(VERTICAL_SPACE, unsafe_allow_html=True)


def calculate_roi_by_wager_type(data):
    """
    Calculate ROI by wager type and count the number of bets per type.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.

    Returns:
        pd.DataFrame: DataFrame containing ROI and count of bets per wager type.
    """
    roi_by_wager = data.groupby("Type").agg(
        {"Profit": "sum", "Wager": "sum", "Result": "count"}
    )
    roi_by_wager["ROI"] = round(
        (roi_by_wager["Profit"] / roi_by_wager["Wager"]) * 100, 2
    )
    roi_by_wager = roi_by_wager.reset_index()
    roi_by_wager.rename(columns={"Result": "Bets Count"}, inplace=True)
    return roi_by_wager


def create_roi_bar_chart(roi_data):
    """
    Create a horizontal bar chart for ROI by wager type.

    Args:
        roi_data (pd.DataFrame): DataFrame containing ROI and bet count per wager type.

    Returns:
        plotly.graph_objects.Figure: The bar chart figure.
    """
    roi_data["color"] = roi_data["ROI"].apply(
        lambda x: "#00CC96" if x > 0 else "#FF6692"
    )

    fig = px.bar(
        roi_data,
        x="ROI",
        y="Type",
        orientation="h",
        labels={"Type": "Wager Type", "ROI": "ROI %"},
        color="color",
        color_discrete_map={"#00CC96": "#00CC96", "#FF6692": "#FF6692"},
        text="ROI",  # Display the ROI percentage on the bars
        hover_data={
            "Type": False,  # Disable wager type in hover
            "color": False,  # Disable color in hover
            "ROI": False,  # Format ROI as percentage
            "Bets Count": True,  # Show bet counts
        },
    )

    fig.update_traces(texttemplate="%{x:.2f}%", textposition="outside")
    fig.update_layout(showlegend=False, yaxis=dict(autorange="reversed"))
    fig.update_traces(marker={"line": {"width": 1, "color": "DarkSlateGrey"}})
    return fig


def render_roi_by_wager_type(roi_data):
    """
    Display the ROI by wager type chart.

    Args:
        roi_data (pd.DataFrame): The data frame containing the bets ledger.
    """
    fig = create_roi_bar_chart(roi_data)
    st.write("### ROI by Wager Type")
    st.plotly_chart(fig)
    st.markdown(VERTICAL_SPACE, unsafe_allow_html=True)


if __name__ == "__main__":
    setup("Yureeh Betting Dashboard")

    data = load_bets()

    if not data.empty:
        filtered_data = render_sidebar(data)

        metrics = calculate_metrics(filtered_data)
        render_metrics(metrics)

        render_profit_timeline(filtered_data)

        render_bet_df(filtered_data)

        roi_data = calculate_roi_by_wager_type(filtered_data)
        render_roi_by_wager_type(roi_data)

        st.markdown("<hr>", unsafe_allow_html=True)
    else:
        st.error("Failed to load data. Please check the data source.")
