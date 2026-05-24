"""Histogram plotting utilities."""

import matplotlib.pyplot as plt
import pandas as pd


def plot_histogram(series: pd.Series, column: str) -> None:
    """Display a histogram for the selected numeric column."""

    plt.hist(series, bins=8, edgecolor="black")
    plt.title(f"Histograma - {column}")
    plt.xlabel(column)
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()
