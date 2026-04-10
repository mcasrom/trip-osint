#!/usr/bin/env python3
import csv
from pathlib import Path
from collections import Counter

INPUT_PATH = "data/processed/events_enriched.csv"
OUTPUT_PATH = "data/kpis/kpi_activity.csv"

def kpi_activity():
    Path("data/kpis").mkdir(parents=True, exist_ok=True)

    counter = Counter()

    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            day = row["timestamp"][:10]
            if day:
                counter[day] += 1

    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "events"])
        for day, count in sorted(counter.items()):
            writer.writerow([day, count])

    print(f"[KPI] KPI de actividad generado → {OUTPUT_PATH}")

if __name__ == "__main__":
    kpi_activity()
