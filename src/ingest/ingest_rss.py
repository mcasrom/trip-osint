#!/usr/bin/env python3
import feedparser
import yaml
import csv
from pathlib import Path

CONFIG_PATH = "config/sources.yml"
OUTPUT_PATH = "data/raw/rss_events.csv"

def load_sources():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

def ingest_rss():
    sources = load_sources().get("rss", [])
    rows = []

    for src in sources:
        if not src.get("enabled", False):
            continue

        feed = feedparser.parse(src["url"])
        for entry in feed.entries:
            rows.append({
                "source": src["name"],
                "title": entry.get("title", ""),
                "summary": entry.get("summary", ""),
                "published": entry.get("published", ""),
            })

    Path("data/raw").mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "title", "summary", "published"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"[INGEST] {len(rows)} eventos guardados en {OUTPUT_PATH}")

if __name__ == "__main__":
    ingest_rss()
