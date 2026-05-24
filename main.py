import pandas as pd 
import matplotlib.pyplot as plt 
from scipy.stats import shapiro 
from typing import cast 
from scipy import stats 
from reliability.Fitters import Fit_Weibull_2P 
import numpy as np 

def load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    # Clean spaces 
    df.columns = df.columns.str.strip() 

    return df 

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

def weibull_percentile_life(beta: float, eta: float, percentile: float) -> float:
    """
    Calcula la vida Bx para una distribucion Weibull 2P. 

    percentile = probabilidad acumulada de falla 
    Ejemplo:
    0.10 -> B10 
    0.01 -> B1 
    0.0001 -> B0.01 
    """
    return eta * (-np.log(1 - percentile)) **(1 / beta)

def bootstrap_b_life(series: pd.Series, percentile: float, confidence: float, n_bootstrap: int = 500) -> tuple[float, float, float]:
    data =series.values
    estimates = []

    for _ in range(n_bootstrap):
        sample = np.random.choice(data, size=len(data), replace=True)

        try: 
            fit = Fit_Weibull_2P(
                    failures=sample, 
                    show_probability_plot=False, 
                    print_results=False
                    )
            beta= fit.beta
            eta = fit.alpha 

            bx = weibull_percentile_life(beta, eta, percentile) 
            estimates.append(bx) 
        except Exception:
            continue 
    estimates = np.array(estimates)
    estimate = np.median(estimates)
    alpha = 1 - confidence 
    lower = np.quantile(estimates, alpha /2) 
    upper = np.quantile(estimates, 1 - alpha /2) 

    return estimate, lower, upper 


def weibull_analysis(series: pd.Series) -> None:
    print("\nWeibull Analysis")
    print("------------------")

    try:
        confidence = float(input("Nivel de confianza, ejemplo 0.60 0 0.90: "))
        percentiles = [ 0.50, 0.10, 0.01, 0.001, 0.0001 ]

        if not 0 < confidence < 1:
            print("El nivel de confianza debe estar entre 0 y 1")
            return 

        fit = Fit_Weibull_2P(
                failures=series.values, 
                show_probability_plot=True, 
                print_results=True, 
                CI=confidence
                )
        beta = fit.beta 
        eta = fit.alpha 
         
        print("\nEstimacion de vida por percentil")
        print("----------------------------------")
        print(f"Confianza seleccionada: {confidence * 100:1f}%")

        print("\nTable B-life")
        print("--------------")
                
        for p in percentiles:
            bx_life = weibull_percentile_life(beta = beta, eta = eta, percentile = p)
            boot_estimate, lower, upper = bootstrap_b_life(series = series, percentile = p, confidence = confidence, n_bootstrap = 500)

            print(
                    f"B{p * 100:.4f} ->"
                    f"Estimate: {bx_life:.4f} h |"
                    f"Lower {confidence * 100: .0f}%: {lower:.4f} h |"
                    f"Upper {confidence * 100: .0f}%: {upper:.4f} h"
                    ) 
      
    except Exception as e:
        print(f"Error en Weibull Analysis: {e}")


def plot_histogram(series: pd.Series, column: str) -> None:
    plt.hist(series, bins=8, edgecolor="black")
    plt.title(f"Histograma - {column}")
    plt.xlabel(column)
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()

def qq_plot(series: pd.Series, column: str) -> None:
    plt.figure()
    stats.probplot(series, dist ="norm", plot=plt)
    plt.title(f"Q-Q Plot - {column}")
    plt.grid(True)
    plt.show()

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
    qq_plot(series, column)
    weibull_analysis(series)

if __name__ == "__main__":
    main() 
