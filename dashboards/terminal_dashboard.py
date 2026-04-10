#!/usr/bin/env python3
import csv
from pathlib import Path

FILES = {
    "Actividad": "data/kpis/kpi_activity.csv",
    "Tensión": "data/kpis/kpi_tension.csv",
    "Riesgo": "data/kpis/kpi_risk.csv",
    "Persistencia": "data/kpis/kpi_persistence.csv",
    "Volatilidad": "data/kpis/kpi_volatility.csv",
}

def read_csv(path):
    rows = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            headers = next(reader)
            for r in reader:
                rows.append(r)
        return headers, rows
    except FileNotFoundError:
        return None, None

def print_table(title, headers, rows):
    print("\n" + "=" * 60)
    print(f"{title}")
    print("=" * 60)

    if headers is None:
        print("No data.\n")
        return

    col_widths = [max(len(str(x)) for x in col) for col in zip(headers, *rows)]

    header_line = " | ".join(h.ljust(w) for h, w in zip(headers, col_widths))
    print(header_line)
    print("-" * len(header_line))

    for r in rows:
        print(" | ".join(c.ljust(w) for c, w in zip(r, col_widths)))

def main():
    print("\nOSINT DASHBOARD (Terminal)\n")

    for title, path in FILES.items():
        headers, rows = read_csv(path)
        print_table(title, headers, rows)

    print("\n[OK] Dashboard generado en terminal.\n")

if __name__ == "__main__":
    main()
