"""Q-Q plot helpers for normality visualization."""

import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats


def qq_plot(series: pd.Series, column: str) -> None:
    """Display a Q-Q plot against a normal distribution."""

    plt.figure()
    stats.probplot(series, dist="norm", plot=plt)
    plt.title(f"Q-Q Plot - {column}")
    plt.grid(True)
    plt.show()
