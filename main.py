import pandas as pd 
import matplotlib.pyplot as plt 
from scipy.stats import shapiro 
from typing import cast 

def load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def show_columns(df: pd.DataFrame) -> None: 
    print("\nColumn availables:")
    for i, col in enumerate(df.columns):
        print(f"[{i}] {col}")


def get_numeric_series(df: pd.DataFrame, column: str) -> pd.Series:
    s = cast(pd.Series, df[column])
    return pd.to_numeric(s, errors="coerce").dropna()

def describe_column(series: pd.Series, column: str) -> None: 
    print("\nSummary Stadistics")
    print("--------------------")
    print(f"Column: {column}")
    print(f"Quantity: {series.count():.4f}")
    print(f"Mean: {series.mean():.4f}")
    print(f"Standard deviation: {series.std():.4f}")
    print(f"Minimum: {series.min():.4f}")
    print(f"Maximum: {series.max():.4f}")
    print(f"P25: {series.quantile(0.25):.4f}")
    print(f"Median: {series.median():.4f}")
    print(f"P75: {series.quantile(0.75):.4f}")

def plot_histogram(series: pd.Series, column: str) -> None:
    plt.hist(series, bins=8, edgecolor="black")
    plt.title(f"Histograma - {column}")
    plt.xlabel(column)
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()


def normality_test(series: pd.Series) -> None:
    print("\nShapiro-Wilk normality Test")
    print("-----------------------------")

    if len(series) < 3:
        print("There aren't enough values for test")
        return 

    statistic, p_value = shapiro(series)

    print(f"Statistics: {statistic:.4f}")
    print(f"P-value: {p_value:.4f}")

    alpha = 0.05 

    if p_value > alpha: 
        print("Result: Data show a behaviour normal distribution")
    else:
        print("Result: Data show a behaviour no normal distribuiton")


def main():
    path = input("Path of CSV: ").strip() 

    df = load_csv(path)
    show_columns(df) 

    index = int(input("\nChoose numer of column: "))
    column: str = cast(str, df.columns[index])

    series = get_numeric_series(df, column)

    describe_column(series, column)
    normality_test(series)
    plot_histogram(series, column)

if __name__ == "__main__":
    main() 
