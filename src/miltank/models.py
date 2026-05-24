"""Typed data models used across the project."""

from dataclasses import dataclass


@dataclass
class DescriptiveStats:
    """Container for common descriptive statistics of one numeric column."""

    column: str
    count: float
    mean: float
    std: float
    minimum: float
    maximum: float
    p25: float
    median: float
    p75: float


@dataclass
class NormalityResult:
    """Result of the Shapiro-Wilk normality test."""

    statistic: float
    p_value: float
    is_normal: bool


@dataclass
class WeibullBResult:
    """Weibull B-life estimate and confidence interval for one percentile."""

    percentile: float
    estimate_hours: float
    lower_hours: float
    upper_hours: float
