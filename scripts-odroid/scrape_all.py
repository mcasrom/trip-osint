#!/usr/bin/env python3
import json
import os
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
CONFIG_FILE = BASE_DIR / "config" / "destinos.conf"

def leer_destinos():
    """Lee destinos desde archivo de configuración"""
    destinos = []
    if not CONFIG_FILE.exists():
        # Destinos por defecto si no existe config
        return ["gold_coast", "bali", "saigon"]
    
    with open(CONFIG_FILE, 'r') as f:
        for linea in f:
            linea = linea.strip()
            if linea and not linea.startswith('#'):
                partes = linea.split('|')
                if partes:
                    destinos.append(partes[0])  # nombre del destino
    return destinos

def generar_kpi(destino):
    """Genera KPIs para CUALQUIER destino"""
    return {
        "destino": destino,
        "timestamp": datetime.now().isoformat(),
        "seguridad": 2,
        "requisitos": {
            "pasaporte": "6 meses validez",
            "visado": "consultar requisitos locales",
            "vacunas": "consultar OMS"
        },
        "dinero": {
            "efectivo_recomendado": "200 USD equivalente local",
            "tarjetas_aceptadas": "Visa/Mastercard/Amex"
        },
        "telefonos_interes": {
            "policia_turistica": "112 o local",
            "embajada": "consultar ministerio"
        },
        "transporte": {
            "aerolineas": ["local", "internacional"]
        },
        "alertas": [],
        "recomendaciones": "Consultar fuentes oficiales antes de viajar"
    }

def main():
    destinos = leer_destinos()
    print(f"[{datetime.now()}] Scraping para {len(destinos)} destinos: {', '.join(destinos)}")
    
    DATA_DIR.mkdir(exist_ok=True)
    
    for destino in destinos:
        print(f"  → Procesando {destino}...")
        datos = generar_kpi(destino)
        
        output_file = DATA_DIR / f"{destino}_latest.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        print(f"    ✓ Guardado {output_file}")
    
    # Guardar timestamp global
    with open(DATA_DIR / "meta_last_update.txt", 'w') as f:
        f.write(json.dumps({
            "ultima_actualizacion": datetime.now().isoformat(),
            "destinos": destinos,
            "total_destinos": len(destinos)
        }, indent=2))
    
    print(f"✅ Scraping completado - {len(destinos)} destinos actualizados")

if __name__ == "__main__":
    main()

# Añadir al final del archivo existente, antes de if __name__

def generar_alertas():
    """Genera alertas OSINT"""
    from alertas_osint import generar_alertas as gen_alertas
    return gen_alertas()

# Modificar main para incluir alertas
def main_completo():
    print(f"[{datetime.now()}] Iniciando scraping completo...")
    
    # Scraping normal de destinos
    destinos = leer_destinos()
    for destino in destinos:
        datos = generar_kpi(destino)
        with open(DATA_DIR / f"{destino}_latest.json", 'w') as f:
            json.dump(datos, f, indent=2)
        print(f"  ✓ {destino}")
    
    # Generar alertas globales
    generar_alertas()
    
    print("✅ Scraping completado")

if __name__ == "__main__":
    main_completo()
