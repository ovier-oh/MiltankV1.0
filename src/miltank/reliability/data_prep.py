"""Data preparation helpers for censored reliability analysis."""

import pandas as pd 
import numpy as np 

def split_failure_and_censored(
        df: pd.DataFrame, 
        time_col: str, 
        event_col: str, 
        ) -> tuple[np.ndarray, np.ndarray]:
    """
    Split observations into failures and right-censored arrays.

    event = 1 means failure.
    event = 0 means right-censored (suspended).
    """
    if time_col not in df.columns: 
        raise ValueError(f"Column '{time_col}' not found")

    if event_col not in df.columns:
        raise ValueError(f"Column '{event_col}' not found")

    clean_df = df[[time_col, event_col]].copy()
    clean_df[time_col] = pd.to_numeric(clean_df[time_col], errors="coerce")
    clean_df[event_col] = pd.to_numeric(clean_df[event_col], errors="coerce")
    clean_df = clean_df.dropna() 

    failures = clean_df[clean_df[event_col] == 1][time_col].values 
    right_censored = clean_df[clean_df[event_col] == 0][time_col].values 

    if len(failures) == 0:
        raise ValueError("No failure data found. You need at least one event = 1")

    return failures, right_censored
