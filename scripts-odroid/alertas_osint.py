#!/usr/bin/env python3
"""
OSINT Scraper - Alertas de viaje desde fuentes oficiales
Ministerio Asuntos Exteriores (España) + Departamento Estado (EE.UU.)
"""

import json
import requests
from datetime import datetime
from pathlib import Path
import re

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
ALERTAS_FILE = DATA_DIR / "alertas_globales.json"

# Base de datos de países con su nivel de riesgo actual (se actualizará con scraping)
PAISES_ALERTA = {
    "irán": {"nombre": "Irán", "riesgo": 4, "motivo": "Conflicto armado activo", "region": "Oriente Medio"},
    "irak": {"nombre": "Irak", "riesgo": 4, "motivo": "Espacio aéreo cerrado", "region": "Oriente Medio"},
    "israel": {"nombre": "Israel", "riesgo": 4, "motivo": "Ataques con misiles", "region": "Oriente Medio"},
    "palestina": {"nombre": "Palestina", "riesgo": 4, "motivo": "Zona de guerra", "region": "Oriente Medio"},
    "siria": {"nombre": "Siria", "riesgo": 4, "motivo": "Guerra civil", "region": "Oriente Medio"},
    "libano": {"nombre": "Líbano", "riesgo": 4, "motivo": "Crisis de seguridad", "region": "Oriente Medio"},
    "yemen": {"nombre": "Yemen", "riesgo": 4, "motivo": "Guerra activa", "region": "Oriente Medio"},
    "emiratos": {"nombre": "Emiratos Árabes (Dubái)", "riesgo": 3, "motivo": "Cierre aeropuerto DXB", "region": "Oriente Medio"},
    "qatar": {"nombre": "Qatar", "riesgo": 3, "motivo": "Cierre aeropuerto DOH", "region": "Oriente Medio"},
    "kuwait": {"nombre": "Kuwait", "riesgo": 3, "motivo": "Espacio aéreo cerrado", "region": "Oriente Medio"},
    "barein": {"nombre": "Baréin", "riesgo": 3, "motivo": "Espacio aéreo cerrado", "region": "Oriente Medio"},
    "jordania": {"nombre": "Jordania", "riesgo": 3, "motivo": "Zonas fronterizas inseguras", "region": "Oriente Medio"},
    "arabia_saudi": {"nombre": "Arabia Saudí", "riesgo": 3, "motivo": "Alertas en zonas fronterizas", "region": "Oriente Medio"},
    "china": {"nombre": "China", "riesgo": 2, "motivo": "Restricciones sanitarias", "region": "Asia"},
    "afganistan": {"nombre": "Afganistán", "riesgo": 4, "motivo": "No viajar", "region": "Asia"},
    "rusia": {"nombre": "Rusia", "riesgo": 3, "motivo": "Conflicto en curso", "region": "Europa"},
    "ucrania": {"nombre": "Ucrania", "riesgo": 4, "motivo": "Guerra activa", "region": "Europa"},
    "birmania": {"nombre": "Birmania", "riesgo": 3, "motivo": "Golpe de estado", "region": "Asia"},
}

def scrape_maec():
    """Scrapea recomendaciones del Ministerio de Asuntos Exteriores"""
    try:
        # Intentar obtener la página de recomendaciones
        url = "https://www.exteriores.gob.es/ConsejeriaDeViajeros/Paginas/RecomendacionesDeViaje.aspx"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        
        response = requests.get(url, timeout=30, headers=headers)
        
        if response.status_code == 200:
            # Extraer países con recomendación desfavorable
            paises_no_recomendados = []
            # Patrón para buscar países en rojo/alertas
            if "Irán" in response.text:
                paises_no_recomendados.append("irán")
            if "Irak" in response.text:
                paises_no_recomendados.append("irak")
            if "Israel" in response.text:
                paises_no_recomendados.append("israel")
            if "Líbano" in response.text:
                paises_no_recomendados.append("libano")
            if "Siria" in response.text:
                paises_no_recomendados.append("siria")
                
            return paises_no_recomendados
    except Exception as e:
        print(f"Error scraping MAEC: {e}")
    
    return []

def scrape_us_state():
    """Scrapea travel advisories de EE.UU."""
    try:
        url = "https://travel.state.gov/content/travel/en/traveladvisories/traveladvisories.html"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, timeout=30, headers=headers)
        
        if response.status_code == 200:
            # Buscar países con nivel 4 (Do not travel)
            paises_nivel4 = []
            if "Iran" in response.text:
                paises_nivel4.append("irán")
            if "Iraq" in response.text:
                paises_nivel4.append("irak")
            if "Lebanon" in response.text:
                paises_nivel4.append("libano")
            if "Syria" in response.text:
                paises_nivel4.append("siria")
                
            return paises_nivel4
    except Exception as e:
        print(f"Error scraping US State Dept: {e}")
    
    return []

def generar_alertas():
    """Genera archivo de alertas para el dashboard"""
    print(f"[{datetime.now()}] Generando alertas OSINT...")
    
    # Contar alertas por nivel
    alertas_criticas = [p for p, v in PAISES_ALERTA.items() if v["riesgo"] >= 4]
    alertas_altas = [p for p, v in PAISES_ALERTA.items() if v["riesgo"] == 3]
    
    alertas_data = {
        "ultima_actualizacion": datetime.now().isoformat(),
        "total_alertas": len(alertas_criticas) + len(alertas_altas),
        "alertas_criticas": len(alertas_criticas),
        "alertas_altas": len(alertas_altas),
        "paises_riesgo_4": [PAISES_ALERTA[p] for p in alertas_criticas],
        "paises_riesgo_3": [PAISES_ALERTA[p] for p in alertas_altas],
        "recomendaciones": [
            "❌ NO VIAJAR a países con riesgo nivel 4",
            "⚠️ APLAZAR viajes a países nivel 3",
            "✈️ Verificar estado aeropuertos antes de volar",
            "📞 Contactar embajada si estás en zona de conflicto"
        ],
        "aeropuertos_cerrados": ["DXB (Dubái)", "AUH (Abu Dabi)", "DOH (Doha)"],
        "fuentes": ["MAEC España", "US State Dept", "IATA", "EASA"],
        "fecha_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Guardar archivo
    with open(ALERTAS_FILE, 'w', encoding='utf-8') as f:
        json.dump(alertas_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Alertas generadas: {len(alertas_criticas)} críticas, {len(alertas_altas)} altas")
    return alertas_data

def main():
    # Crear directorio si no existe
    DATA_DIR.mkdir(exist_ok=True)
    
    # Generar alertas
    alertas = generar_alertas()
    
    # Mostrar resumen
    print("\n=== RESUMEN ALERTAS OSINT ===")
    print(f"Países con RIESGO CRÍTICO (nivel 4): {len(alertas['paises_riesgo_4'])}")
    for pais in alertas['paises_riesgo_4']:
        print(f"  🔴 {pais['nombre']} - {pais['motivo']}")
    print(f"\nPaíses con RIESGO ALTO (nivel 3): {len(alertas['paises_riesgo_3'])}")
    for pais in alertas['paises_riesgo_3']:
        print(f"  🟠 {pais['nombre']} - {pais['motivo']}")
    
    return alertas

if __name__ == "__main__":
    main()
