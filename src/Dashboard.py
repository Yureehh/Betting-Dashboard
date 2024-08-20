import pandas as pd
import plotly.express as px
import streamlit as st

from commons import (
    DOUBLE_VERTICAL_SPACE,
    GREEN_COLOR,
    HORIZONTAL_LINE,
    RED_COLOR,
    SINGLE_VERTICAL_SPACE,
    load_bets,
    setup,
)
from sidebar import render_sidebar

WIN_SYMBOL = "W"
PAGE_NAME = "LoL Oracle Betting Dashboard"


def calculate_metrics(data: pd.DataFrame) -> dict:
    """
    Calculate metrics such as total bets, winrate, profit, and ROI.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.

    Returns:
        dict: A dictionary containing calculated metrics.
    """
    total_bets = len(data)
    total_wins = data["Result"].eq(WIN_SYMBOL).sum()
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


def render_metrics(metrics: dict) -> None:
    """
    Display metrics for the total number of bets, winrate, profit, and ROI.

    Args:
        metrics (dict): A dictionary containing calculated metrics.
    """
    st.write("### Overview")
    st.markdown(SINGLE_VERTICAL_SPACE, unsafe_allow_html=True)

    cols = st.columns(5)
    metrics_labels = [
        "Total Bets",
        "Units Wagered",
        "Winrate %",
        "Profit (Units)",
        "ROI %",
    ]
    metrics_values = [
        metrics["total_bets"],
        metrics["total_wager"],
        f"{metrics['total_winrate']}%",
        metrics["total_profit"],
        f"{metrics['total_roi']}%",
    ]

    for col, label, value in zip(cols, metrics_labels, metrics_values):
        col.metric(label, value)

    st.markdown(DOUBLE_VERTICAL_SPACE, unsafe_allow_html=True)


def render_profit_timeline(data: pd.DataFrame) -> None:
    """
    Display a line chart showing the profit timeline.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.
    """
    chart_name = "### Profit Timeline"
    x_axis = "Month"
    y_axis = "Profit (Units)"

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
        margin=dict(t=40, b=40),
        width=1000,  # Adjust width to make plot wider
    )

    st.write(chart_name)
    st.plotly_chart(fig)
    st.markdown(DOUBLE_VERTICAL_SPACE, unsafe_allow_html=True)


def render_bet_df(data: pd.DataFrame) -> None:
    """
    Display the bets ledger in a DataFrame.

    Args:
        data (pd.DataFrame): The data frame containing the bets ledger.
    """
    st.write("### Bets Ledger")
    st.markdown(SINGLE_VERTICAL_SPACE, unsafe_allow_html=True)

    data["Date"] = data["Date"].dt.date
    data = data.sort_values(by="Date", ascending=False)

    st.dataframe(data, hide_index=True)
    st.markdown(DOUBLE_VERTICAL_SPACE, unsafe_allow_html=True)


def calculate_roi_by_wager_type(data: pd.DataFrame) -> pd.DataFrame:
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
    return roi_by_wager.reset_index().rename(columns={"Result": "Bets Count"})


def create_roi_bar_chart(roi_data: pd.DataFrame):
    """
    Create a horizontal bar chart for ROI by wager type.

    Args:
        roi_data (pd.DataFrame): DataFrame containing ROI and bet count per wager type.

    Returns:
        plotly.graph_objects.Figure: The bar chart figure.
    """
    roi_data["color"] = roi_data["ROI"].apply(
        lambda x: GREEN_COLOR if x > 0 else RED_COLOR
    )

    fig = px.bar(
        roi_data,
        x="ROI",
        y="Type",
        orientation="h",
        labels={"Type": "Wager Type", "ROI": "ROI %"},
        color="color",
        color_discrete_map={GREEN_COLOR: GREEN_COLOR, RED_COLOR: RED_COLOR},
        text="ROI",
        hover_data={
            "Type": False,
            "color": False,
            "ROI": False,
            "Bets Count": True,
        },
    )

    fig.update_traces(
        texttemplate="%{x:.2f}%",
        textposition="outside",
        marker={"line": {"width": 1, "color": "DarkSlateGrey"}},
    )
    fig.update_layout(showlegend=False, yaxis=dict(autorange="reversed"))
    return fig


def render_roi_by_wager_type(roi_data: pd.DataFrame) -> None:
    """
    Display the ROI by wager type chart.

    Args:
        roi_data (pd.DataFrame): The data frame containing the bets ledger.
    """
    st.write("### ROI by Wager Type")
    st.plotly_chart(create_roi_bar_chart(roi_data))
    st.markdown(DOUBLE_VERTICAL_SPACE, unsafe_allow_html=True)


if __name__ == "__main__":
    setup(PAGE_NAME)

    data = load_bets()

    if not data.empty:
        filtered_data = render_sidebar(data)

        render_metrics(calculate_metrics(filtered_data))
        render_profit_timeline(filtered_data)
        render_bet_df(filtered_data)
        render_roi_by_wager_type(calculate_roi_by_wager_type(filtered_data))

        st.markdown(HORIZONTAL_LINE, unsafe_allow_html=True)
    else:
        st.error("Failed to load data. Please check the data source.")
