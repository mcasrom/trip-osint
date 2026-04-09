#!/bin/bash
cd /home/odroid/trip-osint
python3 scripts-odroid/scrape_all.py
git add data/
git commit -m "Update $(date +%Y-%m-%d)" || echo "Sin cambios"
git push origin main
