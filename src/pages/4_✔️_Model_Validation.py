import json

# Caching for efficiency
from functools import lru_cache

import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image

from commons import VERTICAL_SPACE, get_latest_date, load_bets, setup
from paths import (
    ACCURACY_OVER_SAMPLES_PATH,
    HISTORICAL_ACCURACY_PATH,
    LEAGUE_ACCURACIES_PATH,
    MODEL_METRICS_PATH,
)
from sidebar import render_sidebar


@lru_cache(maxsize=32)
def load_json(file_path):
    """
    Load JSON data from a file.

    Args:
        file_path (str or Path): Path to the JSON file.

    Returns:
        dict: Parsed JSON data.
    """
    with open(file_path) as f:
        return json.load(f)


@lru_cache(maxsize=32)
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
    metric_columns = st.columns(4)
    for i, (key, value) in enumerate(metrics.items()):
        metric_columns[i].metric(key.capitalize(), f"{value:.2%}")
    st.markdown(VERTICAL_SPACE, unsafe_allow_html=True)


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
    st.markdown(VERTICAL_SPACE, unsafe_allow_html=True)


def display_league_accuracies(league_accuracies):
    """
    Display league accuracies as a sorted horizontal bar chart.

    Args:
        league_accuracies (dict): Dictionary containing league accuracies.
    """
    st.write("### League Accuracies in Test Set")

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
    st.markdown(VERTICAL_SPACE, unsafe_allow_html=True)


if __name__ == "__main__":
    setup(f"Model Validation - Updated {get_latest_date(MODEL_METRICS_PATH)}")

    data = load_bets()

    if not data.empty:
        filtered_data = render_sidebar(data)

        # Load and display model metrics
        display_metrics(load_json(MODEL_METRICS_PATH))

        # Plot historical accuracy
        plot_image(
            "Historical Accuracy",
            HISTORICAL_ACCURACY_PATH,
            "Historical Accuracy Over Time",
        )

        # Plot accuracy over samples
        plot_image(
            "Accuracy Over Samples",
            ACCURACY_OVER_SAMPLES_PATH,
            "Accuracy Over Different Sample Sizes",
        )

        # Load and display league accuracies
        league_accuracies = load_json(LEAGUE_ACCURACIES_PATH)
        display_league_accuracies(league_accuracies)

        st.markdown("<hr>", unsafe_allow_html=True)
    else:
        st.error("Failed to load data. Please check the data source.")

# import json
# import pandas as pd
# import plotly.express as px
# import streamlit as st
# from PIL import Image

# from paths import (
#     ACCURACY_OVER_SAMPLES_PATH,
#     HISTORICAL_ACCURACY_PATH,
#     LEAGUE_ACCURACIES_PATH,
#     MODEL_METRICS_PATH,
# )
# from commons import VERTICAL_SPACE, get_latest_date, load_bets, setup
# from sidebar import render_sidebar
# from s3_utils import load_json_from_s3, load_image_from_s3

# def display_metrics(metrics_path=None, bucket_name=None, s3_key=None):
#     """
#     Display model metrics, supporting both local and S3 sources.

#     Args:
#         metrics_path (str or Path, optional): Path to the local JSON metrics file.
#         bucket_name (str, optional): The name of the S3 bucket.
#         s3_key (str, optional): The object key in the S3 bucket.
#     """
#     st.write("### Model Metrics")

#     if bucket_name and s3_key:
#         metrics = load_json_from_s3(bucket_name, s3_key)
#     else:
#         metrics = load_json(metrics_path)

#     metric_columns = st.columns(4)
#     for i, (key, value) in enumerate(metrics.items()):
#         metric_columns[i].metric(key.capitalize(), f"{value:.2%}")
#     st.markdown(VERTICAL_SPACE, unsafe_allow_html=True)

# def plot_image(title, image_path=None, caption="", bucket_name=None, s3_key=None):
#     """
#     Plot an image with a title and caption, supporting both local and S3 sources.

#     Args:
#         title (str): The title of the plot.
#         image_path (str or Path, optional): Path to the local image file.
#         caption (str): Caption for the image.
#         bucket_name (str, optional): The name of the S3 bucket.
#         s3_key (str, optional): The object key in the S3 bucket.
#     """
#     st.write(f"### {title}")

#     if bucket_name and s3_key:
#         image = load_image_from_s3(bucket_name, s3_key)
#     else:
#         image = load_image(image_path)

#     st.image(image, caption=caption)
#     st.markdown(VERTICAL_SPACE, unsafe_allow_html=True)

# def display_league_accuracies(league_accuracies):
#     """
#     Display league accuracies as a sorted horizontal bar chart.

#     Args:
#         league_accuracies (dict): Dictionary containing league accuracies.
#     """
#     st.write("### League Accuracies")

#     league_acc_df = pd.DataFrame.from_dict(
#         league_accuracies, orient="index"
#     ).reset_index()
#     league_acc_df.columns = ["League", "Count", "Accuracy"]
#     league_acc_df["Accuracy"] = league_acc_df["Accuracy"].apply(
#         lambda x: round(x * 100, 2)
#     )
#     league_acc_df = league_acc_df.sort_values(by="Accuracy", ascending=False)

#     fig = px.bar(
#         league_acc_df,
#         x="Accuracy",
#         y="League",
#         orientation="h",
#         text="Accuracy",
#         labels={"League": "", "Accuracy": "Accuracy %"},
#     )

#     fig.update_traces(
#         texttemplate="%{text:.2f}%",
#         textposition="outside",
#         marker={"line": {"width": 1, "color": "DarkSlateGrey"}},
#     )
#     fig.update_layout(
#         showlegend=False,
#         margin=dict(l=0, r=0, t=0, b=0),
#         yaxis=dict(autorange="reversed"),
#     )

#     st.plotly_chart(fig, use_container_width=True)
#     st.markdown(VERTICAL_SPACE, unsafe_allow_html=True)

# if __name__ == "__main__":
#     setup(f"Model Validation - Updated {get_latest_date(MODEL_METRICS_PATH)}")

#     data = load_bets()

#     if not data.empty:
#         filtered_data = render_sidebar(data)

#         # Load and display model metrics
#         display_metrics(
#             metrics_path=MODEL_METRICS_PATH,
#             bucket_name="your-bucket-name",
#             s3_key="path/to/metrics.json",
#         )

#         # Plot historical accuracy
#         plot_image(
#             "Historical Accuracy",
#             image_path=HISTORICAL_ACCURACY_PATH,
#             caption="Historical Accuracy Over Time",
#             bucket_name="your-bucket-name",
#             s3_key="path/to/historical_accuracy.png",
#         )

#         # Plot accuracy over samples
#         plot_image(
#             "Accuracy Over Samples",
#             image_path=ACCURACY_OVER_SAMPLES_PATH,
#             caption="Accuracy Over Different Sample Sizes",
#             bucket_name="your-bucket-name",
#             s3_key="path/to/accuracy_over_samples.png",
#         )

#         # Load and display league accuracies
#         league_accuracies = load_json(
#             file_path=LEAGUE_ACCURACIES_PATH,
#             bucket_name="your-bucket-name",
#             s3_key="path/to/league_accuracies.json",
#         )
#         display_league_accuracies(league_accuracies)

#         st.markdown("<hr>", unsafe_allow_html=True)
#     else:
#         st.error("Failed to load data. Please check the data source.")
