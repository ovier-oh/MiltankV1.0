"""Utilities to load CSV data and extract numeric series."""

import pandas as pd
from typing import cast


def load_csv(path: str) -> pd.DataFrame:
    """Load a CSV file and normalize column names by trimming spaces."""

    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    return df


def get_numeric_series(df: pd.DataFrame, column: str) -> pd.Series:
    """Convert a DataFrame column to numeric values and drop invalid rows."""

    s = cast(pd.Series, df[column])
    return pd.to_numeric(s, errors="coerce").dropna()
