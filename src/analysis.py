"""
Analysis module for Aadhaar operational data.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from .config import CLEANED_DATA_DIR, ANALYSIS_DIR, STREAMS


def load_and_filter_data(start_date, end_date):
    """Load cleaned data and filter by date range."""
    print(f"Loading data for period: {start_date.date()} to {end_date.date()}")

    enrollment = pd.read_parquet(CLEANED_DATA_DIR / "enrollment_cleaned.parquet")
    demographic = pd.read_parquet(CLEANED_DATA_DIR / "demographic_cleaned.parquet")
    biometric = pd.read_parquet(CLEANED_DATA_DIR / "biometric_cleaned.parquet")

    # Filter by date
    enrollment = enrollment[(enrollment['date'] >= start_date) & (enrollment['date'] <= end_date)]
    demographic = demographic[(demographic['date'] >= start_date) & (demographic['date'] <= end_date)]
    biometric = biometric[(biometric['date'] >= start_date) & (biometric['date'] <= end_date)]

    print(f"Filtered data: {len(enrollment)} enrollment, {len(demographic)} demographic, {len(biometric)} biometric records")
    return enrollment, demographic, biometric


def analyze_geographic_concentration(enrollment, demographic, biometric):
    """Analyze geographic concentration at state level."""
    print("Analyzing geographic concentration...")

    results = {}

    for df, name, cols in [
        (enrollment, "enrollment", ['age_0_5', 'age_5_17', 'age_18_greater']),
        (demographic, "demographic", ['demo_age_5_17', 'demo_age_17_']),
        (biometric, "biometric", ['bio_age_5_17', 'bio_age_17_'])
    ]:
        state_analysis = df.groupby('state').agg({
            'date': 'count',
            **{col: 'sum' for col in cols}
        }).rename(columns={'date': 'total_records'}).sort_values('total_records', ascending=False)

        state_analysis['percentage'] = (state_analysis['total_records'] / state_analysis['total_records'].sum() * 100).round(2)
        state_analysis['cumulative_pct'] = state_analysis['percentage'].cumsum().round(2)

        results[f"{name}_state_analysis"] = state_analysis
        print(f"✓ {name}: Top 5 states represent {state_analysis.head(5)['percentage'].sum():.1f}%")

    return results


def analyze_temporal_patterns(enrollment, demographic, biometric):
    """Analyze temporal patterns and seasonality."""
    print("Analyzing temporal patterns...")

    results = {}

    for df, name in [(enrollment, "enrollment"), (demographic, "demographic"), (biometric, "biometric")]:
        monthly = df.groupby('month').size().reset_index(name='records')
        monthly['month'] = monthly['month'].astype(str)
        monthly['percentage'] = (monthly['records'] / monthly['records'].sum() * 100).round(2)

        results[f"{name}_temporal_analysis"] = monthly
        print(f"✓ {name}: Peak month is {monthly.loc[monthly['records'].idxmax(), 'month']} with {monthly['records'].max()} records")

    return results


def run_analysis(start_date, end_date):
    """Run all analyses and save results."""
    # Load and filter data
    enrollment, demographic, biometric = load_and_filter_data(start_date, end_date)

    # Run analyses
    geo_results = analyze_geographic_concentration(enrollment, demographic, biometric)
    temporal_results = analyze_temporal_patterns(enrollment, demographic, biometric)

    # Combine results
    all_results = {**geo_results, **temporal_results}

    # Save to CSV
    for name, df in all_results.items():
        df.to_csv(ANALYSIS_DIR / f"{name}.csv", index=True)
        print(f"✓ Saved {name}.csv")

    print(f"Analysis complete! Results saved to {ANALYSIS_DIR}")
    return all_results