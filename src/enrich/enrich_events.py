#!/usr/bin/env python3
import csv
import yaml
from pathlib import Path

INPUT_PATH = "data/processed/events_normalized.csv"
OUTPUT_PATH = "data/processed/events_enriched.csv"
TAXONOMY_PATH = "config/taxonomy.yml"

def load_taxonomy():
    with open(TAXONOMY_PATH, "r") as f:
        return yaml.safe_load(f)

def classify(text, taxonomy):
    text = text.lower()
    for category, data in taxonomy["categories"].items():
        for kw in data["keywords"]:
            if kw in text:
                return category
    return "other"

def enrich():
    taxonomy = load_taxonomy()
    rows_out = []

    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            category = classify(row["title"] + " " + row["summary"], taxonomy)
            row["category"] = category
            rows_out.append(row)

    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["source", "title", "summary", "timestamp", "category"]
        )
        writer.writeheader()
        writer.writerows(rows_out)

    print(f"[ENRICH] {len(rows_out)} eventos enriquecidos → {OUTPUT_PATH}")

if __name__ == "__main__":
    enrich()
