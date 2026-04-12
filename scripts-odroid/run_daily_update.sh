#!/bin/bash
# TripOSINT — Daily Update
# Ruta: /home/dietpi/trip-osint/scripts-odroid/run_daily_update.sh
# Cron: 0 6 * * *
set -euo pipefail

PROJ=/home/dietpi/trip-osint
VENV=$PROJ/venv
LOCK=/tmp/trip_osint_update.lock

ts() { date '+%Y-%m-%d %H:%M:%S'; }

exec 200>$LOCK
flock -n 200 || { echo "$(ts) [SKIP] instancia en curso"; exit 0; }

echo ""
echo "$(ts) ════ TripOSINT daily update ════"

source $VENV/bin/activate
echo "$(ts) [OK]  venv"

# Actualizar dependencias
pip install -q -r $PROJ/requirements.txt 2>/dev/null \
    && echo "$(ts) [OK]  requirements" \
    || echo "$(ts) [WARN] pip (no crítico)"

# Git pull
cd $PROJ
git pull origin main --quiet 2>/dev/null \
    && echo "$(ts) [OK]  git pull" \
    || echo "$(ts) [WARN] git pull (sin cambios o sin red)"

# Health check: paises.py carga OK
python3 -c "
import sys; sys.path.insert(0,'$PROJ')
from config.paises import PAISES
print('$(ts) [OK]  PAISES: {} países'.format(len(PAISES)))
" 2>&1

# Limpiar logs >30 días
find $PROJ/logs -name "*.log" -mtime +30 -delete 2>/dev/null \
    && echo "$(ts) [OK]  logs rotados"

# Estado sistema
RAM=$(free -m | awk 'NR==2{print $3}')
DISK=$(df -h / | awk 'NR==2{print $5}')
echo "$(ts) [SYS] RAM:${RAM}MB DISCO:${DISK}"

echo "$(ts) ════ Update OK ════"
