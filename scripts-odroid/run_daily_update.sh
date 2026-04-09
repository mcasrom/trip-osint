#!/bin/bash
# Script maestro que se ejecuta diariamente a las 00:00
# Actualiza todos los datos OSINT y sube a GitHub

echo "=== TRIP-OSINT DAILY UPDATE ==="
echo "Iniciado: $(date)"

cd /home/dietpi/trip-osint

# 1. Ejecutar scraper de destinos
echo "📊 Scraping destinos..."
python3 scripts-odroid/scrape_all.py

# 2. Ejecutar scraper de alertas OSINT
echo "🚨 Scraping alertas OSINT..."
python3 scripts-odroid/alertas_osint.py

# 3. Copiar JSONs a docs/data para GitHub Pages
echo "📁 Copiando datos a docs/data..."
mkdir -p docs/data
cp data/*.json docs/data/

# 4. Commit y push a GitHub
echo "📤 Subiendo a GitHub..."
git add data/ docs/data/
git commit -m "Actualización automática $(date +%Y-%m-%d_%H:%M:%S)" || echo "Sin cambios"
git push origin main

echo "=== COMPLETADO: $(date) ==="
