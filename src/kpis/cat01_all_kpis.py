#!/usr/bin/env python3
import csv
from pathlib import Path
from collections import Counter

INPUT_EVENTS = "data/processed/events_enriched.csv"
OUT_ACTIVITY = "data/kpis/kpi_activity.csv"
OUT_PERSISTENCE = "data/kpis/kpi_persistence.csv"
OUT_TENSION = "data/kpis/kpi_tension.csv"
OUT_VOLATILITY = "data/kpis/kpi_volatility.csv"
OUT_RISK = "data/kpis/kpi_risk.csv"

def kpi_activity():
    counter = Counter()
    with open(INPUT_EVENTS, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            day = row["timestamp"][:10]
            if day:
                counter[day] += 1
    Path("data/kpis").mkdir(parents=True, exist_ok=True)
    with open(OUT_ACTIVITY, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "events"])
        for d, c in sorted(counter.items()):
            writer.writerow([d, c])
    print(f"[KPI] Actividad → {OUT_ACTIVITY}")
    return counter

def kpi_persistence(activity):
    days = sorted(activity.keys())
    streaks = []
    streak = 0
    prev = None
    for d in days:
        if prev is None:
            streak = 1
        else:
            streak = streak + 1 if d > prev else 1
        streaks.append((d, streak))
        prev = d
    with open(OUT_PERSISTENCE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "persistence"])
        for d, s in streaks:
            writer.writerow([d, s])
    print(f"[KPI] Persistencia → {OUT_PERSISTENCE}")

WEIGHTS_TENSION = {
    "security": 3,
    "mobility": 2,
    "environment": 2,
    "politics": 1,
    "other": 0
}

def kpi_tension():
    tension = Counter()
    with open(INPUT_EVENTS, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            day = row["timestamp"][:10]
            cat = row["category"]
            tension[day] += WEIGHTS_TENSION.get(cat, 0)
    with open(OUT_TENSION, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "tension"])
        for d, score in sorted(tension.items()):
            writer.writerow([d, score])
    print(f"[KPI] Tensión → {OUT_TENSION}")
    return tension

def kpi_volatility(activity):
    rows = sorted(activity.items())
    out = []
    prev = None
    for d, e in rows:
        if prev is None:
            out.append((d, 0))
        else:
            out.append((d, abs(e - prev)))
        prev = e
    with open(OUT_VOLATILITY, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "volatility"])
        for d, v in out:
            writer.writerow([d, v])
    print(f"[KPI] Volatilidad → {OUT_VOLATILITY}")

WEIGHTS_RISK = {
    "security": 5,
    "environment": 3,
    "mobility": 2,
    "politics": 1,
    "other": 0
}

def kpi_risk():
    risk = Counter()
    with open(INPUT_EVENTS, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            day = row["timestamp"][:10]
            cat = row["category"]
            risk[day] += WEIGHTS_RISK.get(cat, 0)
    with open(OUT_RISK, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "risk"])
        for d, score in sorted(risk.items()):
            writer.writerow([d, score])
    print(f"[KPI] Riesgo → {OUT_RISK}")

if __name__ == "__main__":
    Path("data/kpis").mkdir(parents=True, exist_ok=True)
    activity = kpi_activity()
    kpi_persistence(activity)
    kpi_tension()
    kpi_volatility(activity)
    kpi_risk()
    print("\n[OK] Todos los KPIs generados correctamente.\n")
