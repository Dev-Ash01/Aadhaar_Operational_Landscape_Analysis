"""
Data cleaning and standardization module for Aadhaar analysis.
"""

import pandas as pd
import numpy as np
import glob
import re
from pathlib import Path
from .config import (
    ENROLLMENT_DIR, DEMOGRAPHIC_DIR, BIOMETRIC_DIR, CLEANED_DATA_DIR,
    REQUIRED_COLUMNS, STATE_STANDARDIZATION_MAP, CANONICAL_STATES_UT
)


def _state_key(x: str) -> str:
    """Convert state name to lowercase key for standardization."""
    x = "" if x is None else str(x)
    x = x.strip().lower()
    x = re.sub(r"\s+", " ", x)
    x = x.replace(".", "")
    return x


def standardize_state_value(x: str) -> str:
    """
    Maps all spelling / legacy variants to ONE canonical Indian state/UT.
    Never invents new states.
    """
    k = _state_key(x)
    if not k:
        return np.nan

    if k in STATE_STANDARDIZATION_MAP:
        return STATE_STANDARDIZATION_MAP[k]

    k2 = _state_key(k.replace("&", "and"))
    if k2 in STATE_STANDARDIZATION_MAP:
        return STATE_STANDARDIZATION_MAP[k2]

    candidate = k.title()
    if candidate in CANONICAL_STATES_UT:
        return candidate

    return np.nan


def load_and_combine_csvs(glob_pattern: str, required_cols: list, stream_name: str) -> pd.DataFrame:
    """Load and combine CSV files from a directory."""
    files = sorted(glob.glob(glob_pattern))
    if not files:
        raise FileNotFoundError(f"No CSV files found for {stream_name} at {glob_pattern}")

    dfs = []
    for fp in files:
        df = pd.read_csv(fp)
        df.columns = [c.strip() for c in df.columns]
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            raise ValueError(f"{stream_name}: {fp} missing {missing}")
        dfs.append(df[required_cols].copy())

    combined = pd.concat(dfs, ignore_index=True)
    combined["stream"] = stream_name
    return combined


def clean_data():
    """Clean and standardize all data streams."""
    print("Loading and cleaning data...")

    # Load raw data
    enrollment = load_and_combine_csvs(
        str(ENROLLMENT_DIR / "*.csv"), REQUIRED_COLUMNS["enrollment"], "enrollment"
    )
    demographic = load_and_combine_csvs(
        str(DEMOGRAPHIC_DIR / "*.csv"), REQUIRED_COLUMNS["demographic"], "demographic"
    )
    biometric = load_and_combine_csvs(
        str(BIOMETRIC_DIR / "*.csv"), REQUIRED_COLUMNS["biometric"], "biometric"
    )

    # Apply state standardization
    for df, name in [(enrollment, "enrollment"), (demographic, "demographic"), (biometric, "biometric")]:
        df["state_raw"] = df["state"]
        df["state"] = df["state"].apply(standardize_state_value)
        print(f"✓ {name}: {len(df)} rows, {df['state'].nunique(dropna=True)} unique states")

    # Parse dates
    for df in [enrollment, demographic, biometric]:
        df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
        df["month"] = df["date"].dt.to_period("M")

    # Save cleaned data as Parquet
    enrollment.to_parquet(CLEANED_DATA_DIR / "enrollment_cleaned.parquet")
    demographic.to_parquet(CLEANED_DATA_DIR / "demographic_cleaned.parquet")
    biometric.to_parquet(CLEANED_DATA_DIR / "biometric_cleaned.parquet")

    print(f"✓ Cleaned data saved to {CLEANED_DATA_DIR}")
    return enrollment, demographic, biometric


if __name__ == "__main__":
    clean_data()