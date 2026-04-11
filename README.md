# 🌍 TripOSINT — Inteligencia para viajeros

> Dashboard OSINT de inteligencia táctica para viajeros: alertas de seguridad, meteorología en tiempo real, tipo de cambio, requisitos de entrada, prensa local y checklists personalizadas por destino y motivo de viaje.

[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=flat-square&logo=streamlit)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-00d4aa?style=flat-square)](LICENSE)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-Apoya%20el%20proyecto-FF5E5B?style=flat-square&logo=ko-fi)](https://ko-fi.com/mcasrom)

---

## 📋 Descripción

**TripOSINT** es una herramienta de inteligencia de fuentes abiertas (OSINT) orientada al viajero, desarrollada como parte del ecosistema **SIEG** (Sistema de Inteligencia Estratégica Global). Agrega y presenta en un único dashboard toda la información crítica que un viajero necesita antes y durante un desplazamiento internacional.

### ¿Qué problema resuelve?

La información pre-viaje está dispersa en decenas de fuentes: el MAEC para alertas de seguridad, bancos para el tipo de cambio, portales de salud para vacunas, apps de meteorología para el tiempo... TripOSINT centraliza todo eso en un dashboard táctico de estilo oscuro, accesible desde cualquier navegador, desplegable en local o en la nube.

---

## 🗂️ Estructura del proyecto

```
trip-osint/
│
├── app.py                    # Entrada principal — Streamlit app
├── requirements.txt          # Dependencias Python
├── README.md                 # Este archivo
│
├── config/
│   ├── __init__.py
│   └── paises.py             # Catálogo de países (~25 campos por país)
│
└── tabs/
    ├── __init__.py
    ├── maec_tab.py           # Alertas y nivel de riesgo MAEC
    ├── meteo_tab.py          # Meteorología en tiempo real (Open-Meteo)
    ├── divisa_tab.py         # Tipo de cambio en tiempo real
    ├── requisitos_tab.py     # Requisitos de entrada (visa, documentos)
    ├── salud_tab.py          # Vacunas y recomendaciones OMS
    ├── prensa_tab.py         # Prensa local vía RSS (feedparser)
    ├── checklist_tab.py      # Checklists personalizadas por motivo
    └── info_tab.py           # Info general, contactos, enchufes, etc.
```

---

## 🔧 Instalación

### Requisitos previos

- Python 3.10+
- Git

### Instalación local (Linux / DietPi / Odroid)

```bash
# Clonar el repositorio
git clone https://github.com/mcasrom/trip-osint.git
cd trip-osint

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Arrancar
streamlit run app.py --server.port 8060 --server.address 0.0.0.0
```

Accede en el navegador: `http://localhost:8060` o `http://<ip-local>:8060`

### Arranque en background (Odroid / servidor)

```bash
nohup streamlit run app.py \
  --server.port 8060 \
  --server.address 0.0.0.0 \
  > ~/trip-osint/trip-osint.log 2>&1 &
echo $! > ~/trip-osint/trip-osint.pid
```

Para detenerlo:

```bash
kill $(cat ~/trip-osint/trip-osint.pid)
```

### Despliegue en Streamlit Cloud

1. Fork o clona este repositorio en tu cuenta de GitHub
2. Ve a [share.streamlit.io](https://share.streamlit.io)
3. Selecciona el repo, rama `main`, archivo `app.py`
4. Deploy

---

## 🌐 APIs utilizadas

| API | Uso | Autenticación | Coste |
|-----|-----|---------------|-------|
| [Open-Meteo](https://open-meteo.com) | Meteorología actual + forecast 7 días | Sin API key | Gratis |
| [Open-Meteo Geocoding](https://open-meteo.com/en/docs/geocoding-api) | Geocodificación de capitales | Sin API key | Gratis |
| [ExchangeRate-API](https://exchangerate-api.com) | Tipos de cambio EUR base | Sin API key (free tier) | Gratis |
| RSS feeds (feedparser) | Prensa local de cada país | Sin API key | Gratis |

Ninguna API requiere registro ni API key en su tier gratuito. TripOSINT funciona completamente offline con datos de fallback si no hay conexión.

---

## 📊 Metodología OSINT

TripOSINT aplica principios OSINT estándar al dominio del viaje:

### Fuentes primarias
- **MAEC** (Ministerio de Asuntos Exteriores, España): niveles de riesgo y alertas oficiales
- **OMS / WHO**: recomendaciones sanitarias y de vacunación por destino
- **Open-Meteo**: datos meteorológicos de modelos globales (ERA5, GFS, ECMWF)

### Fuentes secundarias
- **RSS de medios locales**: prensa del país de destino para contexto geopolítico en tiempo real
- **OSAC** (US Dept. of State, Overseas Security Advisory Council): alertas de seguridad
- **ExchangeRate-API**: datos financieros de mercado

### Procesamiento
Los datos se agregan por país y se presentan con:
- **Codificación por colores** según nivel de riesgo (verde → rojo → negro)
- **Recomendaciones contextuales** según motivo del viaje (turismo, negocios, sanitario...)
- **Checklists dinámicas** que se adaptan al destino y motivo
- **Cache inteligente**: meteo 1h, divisas 1h, RSS 15 min (evita throttling)

### Limitaciones conocidas
- Datos MAEC hardcodeados — no hay API pública del MAEC para alertas en tiempo real
- Niveles de riesgo requieren actualización manual cuando el MAEC los modifica
- Feeds RSS pueden no estar disponibles para todos los países (fallback por región)
- Tipo de cambio con 1h de lag respecto al mercado interbancario

---

## 🗺️ Países soportados (v2.0)

| Región | Países |
|--------|--------|
| Europa | Alemania, Francia, Italia, Reino Unido, Turquía, Portugal, Grecia |
| América | México, Colombia, Argentina, Estados Unidos |
| Asia | Japón, India, Tailandia, China |
| África | Marruecos, Egipto |
| Oceanía | Australia |

Añadir un país nuevo es tan sencillo como añadir una entrada al diccionario `PAISES` en `config/paises.py` siguiendo la plantilla existente.

---

## ➕ Añadir un país nuevo

Copia esta plantilla en `config/paises.py`:

```python
"NombrePaís": {
    "region": "Europa",          # Europa | América | Asia | África | Oceanía
    "emoji": "🏳️",
    "capital": "Capital",
    "moneda_nombre": "Euro",
    "moneda_codigo": "EUR",      # Código ISO 4217
    "nivel_riesgo_maec": 1,      # 1 (sin riesgo) → 5 (desaconsejado)
    # Meteo (obtener en maps.google.com → coordenadas)
    "lat": 0.0, "lon": 0.0,
    "timezone": "Europe/Madrid", # https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
    # Info
    "idioma": "Español",
    "idioma_oficial": "Español",
    "enchufes": "Tipo F",
    "voltaje": "230V",
    "frecuencia": "50Hz",
    "internet_calidad": "Buena",
    "conduccion_lado": "Derecha",
    "distancia_sistema": "Métrico",
    # Contactos
    "telefono_emergencias": "112",
    "telefono_policia": "112",
    "telefono_embajada_es": "+XX XXX XXX XXX",
    "url_maec": "https://www.exteriores.gob.es/...",
    # Entrada
    "visa_espana": "No requerida",
    "pasaporte_o_dni": "DNI válido",
    # Salud
    "vacunas_recomendadas": ["Hepatitis A"],
    "vacunas_obligatorias": [],
    "riesgo_salud": "Bajo",
    "riesgo_malaria": "Ninguno",
    "notas_salud": "",
    # Cívico
    "notas_civicas": "",
    "requisitos_especiales": [],
    "alertas_maec": [],
    # Prensa RSS
    "fuentes_prensa": [
        {"nombre": "Medio 1", "url": "https://medio.com/rss.xml", "idioma": "ES"},
    ],
},
```

---

## 🔄 Roadmap

- [ ] Integración con API oficial IATA para requisitos de entrada en tiempo real
- [ ] Mapa interactivo de riesgo por zonas dentro del país (Folium)
- [ ] Alertas Telegram al cambiar nivel de riesgo MAEC
- [ ] Exportación de briefing pre-viaje a PDF
- [ ] Modo offline completo con datos cacheados en SQLite
- [ ] Más países (objetivo: top 50 destinos desde España)
- [ ] Internacionalización EN/ES

---

## 🤝 Contribuir

1. Fork del repositorio
2. Crea una rama: `git checkout -b feature/nuevo-pais`
3. Añade tu contribución (nuevo país, fix, mejora)
4. Pull Request con descripción clara

Las contribuciones más valoradas son **nuevos países** con todos los campos completos y **feeds RSS** verificados.

---

## ☕ Apoya el proyecto

TripOSINT es software libre desarrollado en tiempo libre. Si te resulta útil:

[![Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/mcasrom)

---

## 📄 Licencia

MIT License — Copyright © 2026 **M. Castillo** (mcasrom)

Puedes usar, modificar y distribuir este software libremente, manteniendo la atribución al autor original.

---

## 📬 Contacto

- **Email**: [mybloggingnotes@gmail.com](mailto:mybloggingnotes@gmail.com)
- **GitHub**: [@mcasrom](https://github.com/mcasrom)
- **Ko-fi**: [ko-fi.com/mcasrom](https://ko-fi.com/mcasrom)
- **SIEG Portal**: [mcasrom.github.io/sieg-osint](https://mcasrom.github.io/sieg-osint)

---

<div align="center">
<sub>Parte del ecosistema SIEG · Sistema de Inteligencia Estratégica Global</sub>
</div>
