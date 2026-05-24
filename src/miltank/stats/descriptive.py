"""Statistical helpers for descriptive metrics and normality checks."""

import pandas as pd
from scipy.stats import shapiro

from miltank.models import DescriptiveStats, NormalityResult


def describe_series(series: pd.Series, column: str) -> DescriptiveStats:
    """Compute descriptive statistics for a numeric series."""

    return DescriptiveStats(
        column=column,
        count=float(series.count()),
        mean=float(series.mean()),
        std=float(series.std()),
        minimum=float(series.min()),
        maximum=float(series.max()),
        p25=float(series.quantile(0.25)),
        median=float(series.median()),
        p75=float(series.quantile(0.75)),
    )


def normality_test(series: pd.Series) -> NormalityResult | None:
    """Run Shapiro-Wilk test and return None when data is insufficient."""

    if len(series) < 3:
        return None

    statistic, p_value = shapiro(series)
    alpha = 0.05
    return NormalityResult(
        statistic=float(statistic),
        p_value=float(p_value),
        is_normal=bool(p_value > alpha),
    )
