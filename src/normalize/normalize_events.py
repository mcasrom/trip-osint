#!/usr/bin/env python3
import csv
from pathlib import Path
from datetime import datetime

INPUT_PATH = "data/raw/rss_events.csv"
OUTPUT_PATH = "data/processed/events_normalized.csv"

def normalize_timestamp(ts):
    try:
        return datetime.strptime(ts, "%a, %d %b %Y %H:%M:%S %Z").isoformat()
    except:
        return ""

def normalize():
    Path("data/processed").mkdir(parents=True, exist_ok=True)

    rows_out = []

    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows_out.append({
                "source": row["source"],
                "title": row["title"].strip(),
                "summary": row["summary"].strip(),
                "timestamp": normalize_timestamp(row["published"]),
            })

    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "title", "summary", "timestamp"])
        writer.writeheader()
        writer.writerows(rows_out)

    print(f"[NORMALIZE] {len(rows_out)} eventos normalizados → {OUTPUT_PATH}")

if __name__ == "__main__":
    normalize()
