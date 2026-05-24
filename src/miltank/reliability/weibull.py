"""Weibull fitting and B-life estimation utilities."""

import numpy as np
import pandas as pd
from reliability.Fitters import Fit_Weibull_2P

from miltank.models import WeibullBResult
from miltank.reliability.data_prep import split_failure_and_censored

def weibull_percentile_life(beta: float, eta: float, percentile: float) -> float:
    """Compute Weibull life for a given cumulative failure percentile."""

    return eta * (-np.log(1 - percentile)) ** (1 / beta)


def bootstrap_b_life(
    series: pd.Series, percentile: float, confidence: float, n_bootstrap: int = 500
) -> tuple[float, float, float]:
    """Estimate B-life and confidence bounds via bootstrap resampling."""

    data = series.values
    estimates = []

    for _ in range(n_bootstrap):
        sample = np.random.choice(data, size=len(data), replace=True)
        try:
            fit = Fit_Weibull_2P(
                failures=sample,
                show_probability_plot=False,
                print_results=False,
            )
            beta = fit.beta
            eta = fit.alpha
            bx = weibull_percentile_life(beta, eta, percentile)
            estimates.append(bx)
        except Exception:
            continue

    estimates_array = np.array(estimates)
    if estimates_array.size == 0:
        raise ValueError("Bootstrap produced no valid Weibull samples")

    estimate = float(np.median(estimates_array))
    alpha = 1 - confidence
    lower = float(np.quantile(estimates_array, alpha / 2))
    upper = float(np.quantile(estimates_array, 1 - alpha / 2))
    return estimate, lower, upper

def bootstrap_b_life_censored(
        failures: np.ndarray,
        right_censored: np.ndarray, 
        percentile: float, 
        confidence: float, 
        n_bootstrap: int = 500, 
        ) -> tuple[float, float, float]:
    """Bootstrap B-life estimates for right-censored Weibull data."""

    estimates = []

    for _ in range(n_bootstrap):
        try:
            boot_failures = np.random.choice(
                    failures, 
                    size = len(failures),
                    replace = True, 
                    )
            boot_censored = np.random.choice(
                    right_censored, 
                    size=len(right_censored),
                    replace=True, 
                    )
            fit  = Fit_Weibull_2P(
                    failures = boot_failures, 
                    right_censored =boot_censored, 
                    show_probability_plot=False, 
                    print_results=False, 
                    )
            beta = fit.beta 
            eta = fit.alpha 

            bx = weibull_percentile_life(
                    beta=beta, 
                    eta=eta, 
                    percentile = percentile,
                    )
            estimates.append(bx) 

        except Exception:
            continue 

    estimates = np.array(estimates)
    estimate = np.median(estimates) 

    alpha = 1 - confidence

    lower = np.quantile(estimates, alpha /2) 
    upper = np.quantile(estimates, 1 - alpha /2) 

    return estimate, lower, upper 

def weibull_analysis(
    series: pd.Series,
    confidence: float,
    percentiles: list[float] | None = None,
    n_bootstrap: int = 500,
    show_probability_plot: bool = True,
    print_fit_results: bool = True,
) -> list[WeibullBResult]:
    """Fit a 2-parameter Weibull model and return B-life estimates."""

    if not 0 < confidence < 1:
        raise ValueError("Confidence level must be between 0 and 1")

    if percentiles is None:
        percentiles = [0.50, 0.10, 0.01, 0.001, 0.0001]

    fit = Fit_Weibull_2P(
        failures=series.values,
        show_probability_plot=show_probability_plot,
        print_results=print_fit_results,
        CI=confidence,
    )
    beta = fit.beta
    eta = fit.alpha

    results: list[WeibullBResult] = []
    for p in percentiles:
        bx_life = weibull_percentile_life(beta=beta, eta=eta, percentile=p)
        _, lower, upper = bootstrap_b_life(
            series=series,
            percentile=p,
            confidence=confidence,
            n_bootstrap=n_bootstrap,
        )
        results.append(
            WeibullBResult(
                percentile=p,
                estimate_hours=float(bx_life),
                lower_hours=lower,
                upper_hours=upper,
            )
        )

    return results


def weibull_analysis_censored(
        df: pd.DataFrame,
        time_col: str, 
        event_col: str, 
        confidence: float, 
        ) -> None:
    """Fit Weibull with right-censored data and print B-life results."""

    percentiles = [ 0.50, 0.10, 0.01, 0.001, 0.0001 ]

    failures, right_censored = split_failure_and_censored(
            df=df, 
            time_col = time_col, 
            event_col = event_col,
            )

    print("\nWeibull Analysis with Right Censored Data")
    print("-------------------------------------------")
    print(f"Failures: {len(failures)}")
    print(f"Right censored: {len(right_censored)}")
    print(f"Confidence: {confidence * 100:.1f}%")

    fit = Fit_Weibull_2P(
            failures = failures, 
            right_censored = right_censored, 
            show_probability_plot = True, 
            print_results = True, 
            CI = confidence, 
            )

    beta = fit.beta 
    eta = fit.alpha 

    print("\nTable B-life")
    print("--------------")

    for p in percentiles:
        estimate, lower, upper = bootstrap_b_life_censored(
                failures=failures, 
                right_censored=right_censored,
                percentile=p,
                confidence=confidence,
                n_bootstrap=500,
                )
        print(
                f"B{p * 100:.4f} ->"
                f"Estimate: {estimate:.4f} h|"
                f"Lower {confidence * 100:.0f}% {lower:.4f} h |"
                f"Upper {confidence * 100:.0f}% {upper:.4f} h"
        )
