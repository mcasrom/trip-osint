#!/usr/bin/env python3
import subprocess

def run(cmd):
    print(f"\n=== Ejecutando: {cmd} ===")
    subprocess.run(cmd, shell=True, check=True)

# 1. INGEST
run("python3 src/ingest/ingest_rss.py")

# 2. NORMALIZE
run("python3 src/normalize/normalize_events.py")

# 3. ENRICH
run("python3 src/enrich/enrich_events.py")

# 4. KPIS (archivo único)
run("python3 src/kpis/cat01_all_kpis.py")

print("\n[OK] Pipeline COMPLETO ejecutado sin errores.\n")
