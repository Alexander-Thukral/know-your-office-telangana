#!/usr/bin/env python3
"""
Preprocess TELANGANA_MSTR CSV → kyo_data.json for the Know Your Office dashboard.

Usage:
    python3 preprocess_data.py                  # One-time conversion
    python3 preprocess_data.py --watch          # Watch CSV for changes and auto-regenerate
    python3 preprocess_data.py --csv other.csv  # Use a different CSV file
"""
import argparse
import glob
import json
import os
import sys
import time
from datetime import datetime

import pandas as pd

# --- Configuration ---
DEFAULT_CSV_PATTERN = "TELANGANA_MSTR_*.csv"
OUTPUT_JSON = "kyo_data.json"
WATCH_INTERVAL_SECONDS = 30

# Short keys to reduce JSON size (each key repeated 154K times)
# The dashboard maps these back to display names.
KEY_MAP = {
    "OFFICE NAME": "a",
    "EST_ID": "b",
    "PAN": "c",
    "EST_NAME": "d",
    "INCROP_ADDRESS1": "e",
    "INCROP_ADDRESS2": "f",
    "INCROP_CITY": "g",
    "INCROP_DIST": "h",
    "INCROP_PIN": "i",
    "COVER_DATE": "j",
    "EXEMPTION_STATUS_NAME": "k",
    "ENF_TASK_ID": "l",
    "ACC_TASK_ID": "m",
    "UANS": "n",
    "DSC": "o",
    "ESN": "p",
    "F5A": "q",
    "PRIMARY_EMAIL": "r",
}

EXPECTED_COLUMNS = list(KEY_MAP.keys())


def find_csv(csv_path=None):
    """Find the CSV file to process."""
    if csv_path:
        if os.path.exists(csv_path):
            return csv_path
        print(f"❌ Specified CSV not found: {csv_path}")
        sys.exit(1)

    matches = sorted(glob.glob(DEFAULT_CSV_PATTERN))
    if not matches:
        print(f"❌ No CSV matching '{DEFAULT_CSV_PATTERN}' found in current directory.")
        sys.exit(1)
    chosen = max(matches, key=os.path.getmtime)
    return chosen


def preprocess(csv_path):
    """Read CSV, clean data, write compact JSON. Returns True on success."""
    print(f"\n{'='*60}")
    print(f"📄 Processing: {csv_path}")
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")

    try:
        df = pd.read_csv(csv_path, dtype=str, low_memory=False)
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return False

    initial_rows = len(df)
    print(f"📊 Raw rows: {initial_rows:,}")

    # Remove junk rows (header duplicates + trailing blanks)
    header_mask = df["EST_ID"].eq("EST_ID") | df["EST_ID"].isna()
    df = df[~header_mask].reset_index(drop=True)
    removed = initial_rows - len(df)
    if removed:
        print(f"🧹 Removed {removed} junk/empty rows")

    # Clean text: strip whitespace, replace NaN placeholders with empty string
    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace({"nan": "", "None": "", "NaN": ""})

    missing = set(EXPECTED_COLUMNS) - set(df.columns)
    if missing:
        print(f"⚠️  Warning: Missing columns: {missing}")

    final_rows = len(df)
    print(f"✅ Clean rows: {final_rows:,}")

    # Rename columns to short keys for compact JSON
    df_compact = df[EXPECTED_COLUMNS].rename(columns=KEY_MAP)

    # Build JSON: { "keys": {short: long, ...}, "data": [{...}, ...] }
    output = {
        "keys": {v: k for k, v in KEY_MAP.items()},
        "data": df_compact.to_dict(orient="records"),
    }

    output_path = os.path.join(os.path.dirname(csv_path) or ".", OUTPUT_JSON)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, separators=(",", ":"))

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"💾 Output: {output_path} ({size_mb:.1f} MB)")

    # Quick stats
    if "OFFICE NAME" in df.columns:
        offices = df["OFFICE NAME"].value_counts()
        print(f"\n📋 Offices:")
        for office, count in offices.items():
            if office:
                print(f"   {office}: {count:,}")

    print(f"\n✅ Done! Dashboard-ready JSON generated.\n")
    return True


def watch_mode(csv_path):
    """Watch the CSV file for changes and auto-regenerate JSON."""
    print(f"\n👁️  Watch mode: monitoring '{csv_path}'")
    print(f"   Checking every {WATCH_INTERVAL_SECONDS}s. Press Ctrl+C to stop.\n")

    # Initial preprocessing
    preprocess(csv_path)
    last_mtime = os.path.getmtime(csv_path)

    try:
        while True:
            time.sleep(WATCH_INTERVAL_SECONDS)
            try:
                current_mtime = os.path.getmtime(csv_path)
                if current_mtime != last_mtime:
                    print(f"\n🔄 Change detected in {csv_path}!")
                    preprocess(csv_path)
                    last_mtime = current_mtime
            except FileNotFoundError:
                print(f"⚠️  File {csv_path} not found, waiting...")
    except KeyboardInterrupt:
        print("\n\n👋 Watch mode stopped.")


def main():
    parser = argparse.ArgumentParser(description="Preprocess EPFO CSV for Know Your Office dashboard")
    parser.add_argument("--csv", type=str, default=None,
                        help="Path to CSV file (default: auto-detect TELANGANA_MSTR_*.csv)")
    parser.add_argument("--watch", action="store_true",
                        help="Watch CSV for changes and auto-regenerate JSON")
    args = parser.parse_args()

    csv_path = find_csv(args.csv)
    print(f"📎 Using CSV: {csv_path}")

    if args.watch:
        watch_mode(csv_path)
    else:
        preprocess(csv_path)


if __name__ == "__main__":
    main()
