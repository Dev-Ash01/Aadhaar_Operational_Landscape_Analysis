"""
Configuration settings for Aadhaar Analysis
"""

import os
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# Data paths
DATA_DIR = PROJECT_ROOT / "data"
ENROLLMENT_DIR = DATA_DIR / "enrollment_folder"
DEMOGRAPHIC_DIR = DATA_DIR / "demographic_updates_folder"
BIOMETRIC_DIR = DATA_DIR / "biometric_updates_folder"

# Output paths
OUTPUT_DIR = PROJECT_ROOT / "output"
CLEANED_DATA_DIR = OUTPUT_DIR / "cleaned_data"
ANALYSIS_DIR = OUTPUT_DIR / "analysis_results"

# Ensure directories exist
for dir_path in [CLEANED_DATA_DIR, ANALYSIS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# State standardization map
STATE_STANDARDIZATION_MAP = {
    # Andaman & Nicobar
    "andaman & nicobar islands": "Andaman and Nicobar Islands",
    "andaman and nicobar islands": "Andaman and Nicobar Islands",
    "andaman & nicobar": "Andaman and Nicobar Islands",
    "andaman nicobar": "Andaman and Nicobar Islands",

    # Dadra & Daman (merged UT)
    "dadra & daman": "Dadra and Nagar Haveli and Daman and Diu",
    "dadra and daman": "Dadra and Nagar Haveli and Daman and Diu",
    "dadra & nagar haveli": "Dadra and Nagar Haveli and Daman and Diu",
    "dadra and nagar haveli": "Dadra and Nagar Haveli and Daman and Diu",
    "daman & diu": "Dadra and Nagar Haveli and Daman and Diu",
    "daman and diu": "Dadra and Nagar Haveli and Daman and Diu",
    "dadra nagar haveli": "Dadra and Nagar Haveli and Daman and Diu",

    # Jammu & Kashmir
    "jammu & kashmir": "Jammu and Kashmir",
    "jammu and kashmir": "Jammu and Kashmir",
    "jammu kashmir": "Jammu and Kashmir",

    # Common spelling issues
    "west bangal": "West Bengal",
    "west bengel": "West Bengal",
    "westbengal": "West Bengal",

    "orissa": "Odisha",
    "pondicherry": "Puducherry",
    "puducheri": "Puducherry",
    "telengana": "Telangana",
    "uttranchal": "Uttarakhand",
    "new delhi": "Delhi",
    "leh": "Ladakh",

    # Administrative aggregates (invalid as states)
    "india": None,
    "all india": None,
    "total": None,
    "all states": None,
}

# Canonical states/UTs
CANONICAL_STATES_UT = {
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
    "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya",
    "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim",
    "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand",
    "West Bengal", "Andaman and Nicobar Islands", "Chandigarh",
    "Dadra and Nagar Haveli and Daman and Diu", "Delhi", "Jammu and Kashmir",
    "Ladakh", "Lakshadweep", "Puducherry",
}

# Required columns for each stream
REQUIRED_COLUMNS = {
    "enrollment": ["date", "state", "district", "pincode", "age_0_5", "age_5_17", "age_18_greater"],
    "demographic": ["date", "state", "district", "pincode", "demo_age_5_17", "demo_age_17_"],
    "biometric": ["date", "state", "district", "pincode", "bio_age_5_17", "bio_age_17_"],
}

# Analysis streams
STREAMS = ["enrollment", "demographic", "biometric"]
COLORS = {"enrollment": "#2E86AB", "demographic": "#A23B72", "biometric": "#F18F01"}