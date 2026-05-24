"""Interactive command-line workflow for exploratory reliability analysis."""

import pandas as pd

from miltank.io.csv_loader import get_numeric_series, load_csv
from miltank.plots.histogram import plot_histogram
from miltank.plots.qqplot import qq_plot
from miltank.reliability.weibull import weibull_analysis, weibull_analysis_censored
from miltank.stats.descriptive import describe_series, normality_test


def show_columns(df: pd.DataFrame) -> None:
    """Print available DataFrame columns with positional indexes."""

    print("\nAvailable columns:")
    for i, col in enumerate(df.columns):
        print(f"[{i}] {col}")


def print_descriptive_stats(series: pd.Series, column: str) -> None:
    """Calculate and print descriptive statistics for a selected column."""

    result = describe_series(series, column)
    print("\nSummary Statistics")
    print("--------------------")
    print(f"Column: {result.column}")
    print(f"Count: {result.count:.4f}")
    print(f"Mean: {result.mean:.4f}")
    print(f"Standard deviation: {result.std:.4f}")
    print(f"Minimum: {result.minimum:.4f}")
    print(f"Maximum: {result.maximum:.4f}")
    print(f"P25: {result.p25:.4f}")
    print(f"Median: {result.median:.4f}")
    print(f"P75: {result.p75:.4f}")


def print_normality_test(series: pd.Series) -> None:
    """Run and print a Shapiro-Wilk normality test report."""

    print("\nShapiro-Wilk Normality Test")
    print("-----------------------------")
    result = normality_test(series)

    if result is None:
        print("There are not enough values to run the test.")
        return

    print(f"Statistics: {result.statistic:.4f}")
    print(f"P-value: {result.p_value:.4f}")

    if result.is_normal:
        print("Result: Data appears to follow a normal distribution.")
    else:
        print("Result: Data does not appear to follow a normal distribution.")


def resolve_column_input(df: pd.DataFrame, raw_value: str) -> str:
    """Resolve user input to a column name using name or index."""

    value = raw_value.strip()

    if value in df.columns:
        return str(value)

    if value.isdigit():
        index = int(value)
        if 0 <= index < len(df.columns):
            return str(df.columns[index])

    raise ValueError(
        f"Column '{raw_value}' not found. Use a valid column name or index from the list."
    )


def run() -> None:
    """Execute the end-to-end CLI flow from CSV loading to Weibull output."""

    path = input("CSV file path: ").strip()
    df = load_csv(path)
    show_columns(df)

    index = int(input("\nChoose the column index: "))
    column = str(df.columns[index])

    series = get_numeric_series(df, column)

    print_descriptive_stats(series, column)
    print_normality_test(series)
    plot_histogram(series, column)
    qq_plot(series, column)
    
    use_censored = input("Use right-censored data? [y/n]: ").strip().lower() 

    if use_censored == 'y':
        time_col = resolve_column_input(
            df, input("Time column (name or index), e.g. time_h or 0: ")
        )
        event_col = resolve_column_input(
            df, input("Event column (name or index), e.g. event or 1: ")
        )
        confidence = float(input("Confidence level, e.g. 0.60 or 0.90: "))

        weibull_analysis_censored(
                df = df, 
                time_col = time_col, 
                event_col = event_col,
                confidence = confidence,
                )
    else:
        print("\nWeibull Analysis")
        print("------------------")
        try:
            confidence_raw = input("Confidence level, e.g. 0.60 or 0.90: ").strip()
            confidence = float(confidence_raw.replace(",", "."))
            results = weibull_analysis(series=series, confidence=confidence, n_bootstrap=500)

            print("\nLife estimation by percentile")
            print("-------------------------------")
            print(f"Selected confidence: {confidence * 100:.1f}%")
            print("\nTable B-life")
            print("--------------")
            for item in results:
                print(
                    f"B{item.percentile * 100:.4f} ->"
                    f"Estimate: {item.estimate_hours:.4f} h |"
                    f"Lower {confidence * 100: .0f}%: {item.lower_hours:.4f} h |"
                    f"Upper {confidence * 100: .0f}%: {item.upper_hours:.4f} h"
                )
        except Exception as e:
            print(f"Error in Weibull analysis: {e}")
