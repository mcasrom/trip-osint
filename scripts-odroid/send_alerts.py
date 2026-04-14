#!/usr/bin/env python3
"""
TripOSINT — Alertas Telegram
Detecta cambios en nivel_riesgo_maec y notifica via Telegram.
Cron sugerido: 0 9 * * * (diario 09:00)
"""
import json
import os
import sys
import requests
from datetime import datetime

# ── Config ────────────────────────────────────────────────────────────────────
TELEGRAM_TOKEN   = os.environ.get("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "-1003764932977")
SNAPSHOT_FILE    = os.path.join(os.path.dirname(__file__), "../data/riesgo_snapshot.json")
PROJ             = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def log(msg):
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {msg}")

def send_telegram(msg):
    if not TELEGRAM_TOKEN:
        log("[WARN] TELEGRAM_TOKEN no configurado — mensaje no enviado")
        return False
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    r = requests.post(url, json={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg,
        "parse_mode": "HTML"
    }, timeout=10)
    return r.status_code == 200

def load_paises():
    sys.path.insert(0, PROJ)
    from config.paises import PAISES
    return {k: v.get("nivel_riesgo_maec", 1) for k, v in PAISES.items()}

def load_snapshot():
    if not os.path.exists(SNAPSHOT_FILE):
        return {}
    with open(SNAPSHOT_FILE) as f:
        return json.load(f)

def save_snapshot(data):
    os.makedirs(os.path.dirname(SNAPSHOT_FILE), exist_ok=True)
    with open(SNAPSHOT_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

NIVELES = {1:"🟢 BAJO", 2:"🟡 MODERADO", 3:"🟠 ALTO", 4:"🔴 MUY ALTO", 5:"⛔ EXTREMO"}

def main():
    log("═══ TripOSINT alertas MAEC ═══")
    actual   = load_paises()
    anterior = load_snapshot()

    if not anterior:
        save_snapshot(actual)
        log(f"[OK] Snapshot inicial creado — {len(actual)} países")
        return

    cambios = []
    for pais, nivel in actual.items():
        prev = anterior.get(pais)
        if prev is None:
            cambios.append((pais, None, nivel, "nuevo"))
        elif prev != nivel:
            cambios.append((pais, prev, nivel, "cambio"))

    eliminados = [p for p in anterior if p not in actual]
    for p in eliminados:
        cambios.append((p, anterior[p], None, "eliminado"))

    if not cambios:
        log("[OK] Sin cambios de riesgo detectados")
        save_snapshot(actual)
        return

    log(f"[ALERTA] {len(cambios)} cambio(s) detectado(s)")
    lines = ["🌍 <b>TripOSINT — Cambios de Riesgo MAEC</b>", f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}", ""]

    for pais, prev, nuevo, tipo in cambios:
        if tipo == "cambio":
            direccion = "⬆️" if nuevo > prev else "⬇️"
            lines.append(f"{direccion} <b>{pais}</b>: {NIVELES.get(prev,'?')} → {NIVELES.get(nuevo,'?')}")
        elif tipo == "nuevo":
            lines.append(f"🆕 <b>{pais}</b>: {NIVELES.get(nuevo,'?')}")
        elif tipo == "eliminado":
            lines.append(f"🗑 <b>{pais}</b>: eliminado del catálogo")

    lines += ["", "🔗 triposint.streamlit.app"]
    msg = "\n".join(lines)

    if send_telegram(msg):
        log("[OK] Telegram enviado")
    else:
        log("[WARN] Telegram falló")

    save_snapshot(actual)
    log("═══ Alertas OK ═══")

if __name__ == "__main__":
    main()
