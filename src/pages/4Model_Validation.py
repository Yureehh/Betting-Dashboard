import json

import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image

from src.commons import BREAK_LINE, load_bets, setup
from src.sidebar import render_sidebar
from utils.paths import (
    ACCURACY_OVER_SAMPLES,
    HISTORICAL_ACCURACY,
    LEAGUE_ACCURACIES,
    MODEL_METRICS,
)

# TODO: Retrieve the model validations from S3


def load_json(file_path):
    """
    Load JSON data from a file.

    Args:
        file_path (str or Path): Path to the JSON file.

    Returns:
        dict: Parsed JSON data.
    """
    with open(file_path) as f:
        data = json.load(f)
    return data


def load_image(image_path):
    """
    Load an image from a file.

    Args:
        image_path (str or Path): Path to the image file.

    Returns:
        PIL.Image.Image: Loaded image.
    """
    return Image.open(image_path)


def display_metrics(metrics):
    """
    Display model metrics in a row.

    Args:
        metrics (dict): Dictionary containing model metrics.
    """
    st.write("### Model Metrics")
    cols = st.columns(4)
    cols[0].metric("Accuracy", f"{metrics['accuracy']:.2%}")
    cols[1].metric("Precision", f"{metrics['precision']:.2%}")
    cols[2].metric("Recall", f"{metrics['recall']:.2%}")
    cols[3].metric("F1 Score", f"{metrics['f1']:.2%}")
    st.markdown(BREAK_LINE, unsafe_allow_html=True)


def plot_image(title, image_path, caption):
    """
    Plot an image with a title and caption.

    Args:
        title (str): The title of the plot.
        image_path (str or Path): Path to the image file.
        caption (str): Caption for the image.
    """
    st.write(f"### {title}")
    image = load_image(image_path)
    st.image(image, caption=caption)
    st.markdown(BREAK_LINE, unsafe_allow_html=True)


def display_league_accuracies(league_accuracies):
    """
    Display league accuracies as a sorted horizontal bar chart.

    Args:
        league_accuracies (dict): Dictionary containing league accuracies.
    """
    st.write("### League Accuracies")

    # Convert dictionary to DataFrame and sort by Accuracy in descending order
    league_acc_df = pd.DataFrame.from_dict(
        league_accuracies, orient="index"
    ).reset_index()
    league_acc_df.columns = ["League", "Count", "Accuracy"]
    league_acc_df["Accuracy"] = league_acc_df["Accuracy"].apply(
        lambda x: round(x * 100, 2)
    )
    league_acc_df = league_acc_df.sort_values(by="Accuracy", ascending=False)

    # Create bar chart using Plotly
    fig = px.bar(
        league_acc_df,
        x="Accuracy",
        y="League",
        orientation="h",
        text="Accuracy",
        labels={"League": "", "Accuracy": "Accuracy %"},
    )

    # Customize traces and layout
    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
        marker={"line": {"width": 1, "color": "DarkSlateGrey"}},
    )
    fig.update_layout(
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0),
        yaxis=dict(autorange="reversed"),
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(BREAK_LINE, unsafe_allow_html=True)


if __name__ == "__main__":
    setup("Model Validation", "✔️")

    data = load_bets()

    if not data.empty:
        filtered_data = render_sidebar(data)

        # Load and display model metrics
        display_metrics(load_json(MODEL_METRICS))

        # Plot historical accuracy
        plot_image(
            "Historical Accuracy", HISTORICAL_ACCURACY, "Historical Accuracy Over Time"
        )

        # Plot accuracy over samples
        plot_image(
            "Accuracy Over Samples",
            ACCURACY_OVER_SAMPLES,
            "Accuracy Over Different Sample Sizes",
        )

        # Load and display league accuracies
        league_accuracies = load_json(LEAGUE_ACCURACIES)
        display_league_accuracies(league_accuracies)

        st.markdown("<hr>", unsafe_allow_html=True)
    else:
        st.error("Failed to load data. Please check the data source.")
