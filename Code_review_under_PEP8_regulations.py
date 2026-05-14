import os

import ipytest
import matplotlib.pyplot as plt
import pandas as pd
import pytest
import seaborn as sns


def prepare_smartphone_data(file_path):
    """
    Prepare smartphone data for visualization and analysis.

    Transformations applied:
        - Keep only columns required for analysis
        - Remove rows with missing battery_capacity or os values
        - Convert price values to dollar amounts

    :param file_path: Path to the raw smartphone CSV file
    :return: Cleaned pandas DataFrame
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"File containing smartphone data not found at path: {file_path}"
        )

    raw_data = pd.read_csv(file_path)

    columns_to_keep = [
        "brand_name",
        "os",
        "price",
        "avg_rating",
        "processor_speed",
        "battery_capacity",
        "screen_size",
    ]

    cleaned_data = raw_data.loc[:, columns_to_keep]

    # Remove rows with missing required values
    cleaned_data = cleaned_data.dropna(
        subset=["battery_capacity", "os"]
    )

    # Convert price to dollars
    cleaned_data["price"] = cleaned_data["price"] / 100

    return cleaned_data


# Call the function
cleaned_data = prepare_smartphone_data("./data/smartphones.csv")


def column_to_label(column_name):
    """
    Convert a DataFrame column name into a plot-friendly label.

    :param column_name: Original column name
    :return: Formatted label string
    """

    if isinstance(column_name, str):
        return " ".join(column_name.split("_")).title()

    raise TypeError(
        "Please make sure to pass a value of type 'str'."
    )


def visualize_versus_price(clean_data, x):
    """
    Create a scatterplot showing the relationship between
    a selected feature and smartphone price.

    :param clean_data: Cleaned smartphone DataFrame
    :param x: Column name to plot on the x-axis
    :return: None
    """

    sns.scatterplot(
        x=x,
        y="price",
        data=clean_data,
        hue="os",
    )

    # Use reusable helper function (DRY principle)
    plt.xlabel(column_to_label(x))
    plt.ylabel("Price ($)")

    plt.title(f"{column_to_label(x)} vs. Price")


# Call the visualization function
visualize_versus_price(
    cleaned_data,
    "processor_speed",
)


# Configure ipytest
ipytest.config.rewrite_asserts = True
__file__ = "notebook.ipynb"


# Create fixture
@pytest.fixture()
def clean_smartphone_data():
    return prepare_smartphone_data(
        "./data/smartphones.csv"
    )


def test_nan_values(clean_smartphone_data):
    """
    Ensure there are no missing values in
    battery_capacity or os columns.
    """

    assert (
        clean_smartphone_data["battery_capacity"]
        .isnull()
        .sum()
        == 0
    )

    assert (
        clean_smartphone_data["os"]
        .isnull()
        .sum()
        == 0
    )


ipytest.run("-qq")