
"""
Aadhaar Operational Landscape Analysis - Main CLI
===============================================

Usage:
    python main.py                # Run full pipeline (clean + analyze)
    python main.py clean          # Clean and prepare data only
    python main.py analyze        # Run analysis on cleaned data only

Options:
    --start-date YYYY-MM-DD       Start date for analysis (default: 2025-01-01)
    --end-date YYYY-MM-DD         End date for analysis (default: 2026-01-19)
"""

import argparse
from datetime import datetime
from src.data_cleaning import clean_data
from src.analysis import run_analysis


def main():
    parser = argparse.ArgumentParser(description="Aadhaar Operational Analysis")
    parser.add_argument("command", nargs='?', choices=["clean", "analyze"],
                       help="Command to run (optional, runs both if not specified)")
    parser.add_argument("--start-date", default="2025-01-01",
                       help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", default="2026-01-19",
                       help="End date (YYYY-MM-DD)")

    args = parser.parse_args()

    start_date = datetime.fromisoformat(args.start_date)
    end_date = datetime.fromisoformat(args.end_date)

    print(f"Aadhaar Analysis - {'FULL PIPELINE' if not args.command else args.command.upper()}")
    print(f"Date range: {start_date.date()} to {end_date.date()}")
    print("=" * 50)

    if args.command == "clean":
        print("Step 1: Data Cleaning")
        clean_data()

    elif args.command == "analyze":
        print("Step 2: Analysis")
        run_analysis(start_date, end_date)

    else:
        print("Running full pipeline: clean and analyze")
        print("Step 1: Data Cleaning")
        clean_data()
        print("\nStep 2: Analysis")
        run_analysis(start_date, end_date)

    print("\n✅ Done!")


if __name__ == "__main__":
    main()