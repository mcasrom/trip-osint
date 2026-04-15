"""
tabs/numbeo_tab.py — Coste de vida por país (Numbeo scraping)
No requiere API key. Usa el endpoint público de Numbeo.
"""
import streamlit as st
import requests
from bs4 import BeautifulSoup

# Mapeo pais_nombre → slug Numbeo (nombre en URL)
NUMBEO_SLUG = {
    "Alemania":               "Germany",
    "Francia":                "France",
    "Italia":                 "Italy",
    "Reino Unido":            "United-Kingdom",
    "Turquía":                "Turkey",
    "Portugal":               "Portugal",
    "Grecia":                 "Greece",
    "México":                 "Mexico",
    "Colombia":               "Colombia",
    "Argentina":              "Argentina",
    "Estados Unidos":         "United-States",
    "Japón":                  "Japan",
    "India":                  "India",
    "Tailandia":              "Thailand",
    "China":                  "China",
    "Marruecos":              "Morocco",
    "Egipto":                 "Egypt",
    "Australia":              "Australia",
    "Austria":                "Austria",
    "Bélgica":                "Belgium",
    "Países Bajos":           "Netherlands",
    "Suiza":                  "Switzerland",
    "Polonia":                "Poland",
    "República Checa":        "Czech-Republic",
    "Suecia":                 "Sweden",
    "Noruega":                "Norway",
    "Dinamarca":              "Denmark",
    "Irlanda":                "Ireland",
    "Croacia":                "Croatia",
    "Hungría":                "Hungary",
    "Rumanía":                "Romania",
    "Georgia":                "Georgia",
    "Ucrania":                "Ukraine",
    "Emiratos Árabes Unidos": "United-Arab-Emirates",
    "Arabia Saudí":           "Saudi-Arabia",
    "Israel":                 "Israel",
    "Jordania":               "Jordan",
    "Corea del Sur":          "South-Korea",
    "Singapur":               "Singapore",
    "Vietnam":                "Vietnam",
    "Indonesia":              "Indonesia",
    "Malasia":                "Malaysia",
    "Nepal":                  "Nepal",
    "Kenia":                  "Kenya",
    "Tanzania":               "Tanzania",
    "Sudáfrica":              "South-Africa",
    "Ghana":                  "Ghana",
    "Canadá":                 "Canada",
    "Brasil":                 "Brazil",
    "Chile":                  "Chile",
    "Perú":                   "Peru",
    "Cuba":                   "Cuba",
    "Rep. Dominicana":        "Dominican-Republic",
    "Ecuador":                "Ecuador",
    "Nueva Zelanda":          "New-Zealand",
    "Rusia":                  "Russia",
    "Filipinas":              "Philippines",
    "Irán":                   "Iran",
    "Pakistán":               "Pakistan",
    "Afganistán":             "Afghanistan",
    "Argelia":                "Algeria",
    "Bolivia":                "Bolivia",
    "Venezuela":              "Venezuela",
    "Costa Rica":             "Costa-Rica",
    "Guatemala":              "Guatemala",
}

# Categorías de interés para viajeros
CATEGORIAS = {
    "🍽 Restaurantes": [
        "Meal, Inexpensive Restaurant",
        "Meal for 2 People, Mid-range Restaurant, Three-course",
        "McMeal at McDonalds (or Equivalent Combo Meal)",
        "Domestic Beer (0.5 liter draught)",
        "Imported Beer (0.33 liter bottle)",
        "Cappuccino (regular)",
        "Water (0.33 liter bottle)",
    ],
    "🛒 Mercado": [
        "Milk (regular), (1 liter)",
        "Loaf of Fresh White Bread (500g)",
        "Rice (white), (1 kg)",
        "Eggs (regular) (12)",
        "Water (1.5 liter bottle)",
        "Bottle of Wine (Mid-Range)",
        "Domestic Beer (0.5 liter bottle)",
    ],
    "🚌 Transporte": [
        "One-way Ticket (Local Transport)",
        "Monthly Pass (Regular Price)",
        "Taxi Start (Normal Tariff)",
        "Taxi 1km (Normal Tariff)",
        "Gasoline (1 liter)",
    ],
    "🏨 Alojamiento": [
        "Apartment (1 bedroom) in City Centre",
        "Apartment (1 bedroom) Outside of Centre",
        "Hotel Room (1 person, mid-range)",
    ],
    "💊 Salud": [
        "Antibiotics (1 course)",
        "Short visit to private doctor",
    ],
}


def _fetch_numbeo(slug):
    url = f"https://www.numbeo.com/cost-of-living/country_result.jsp?country={slug}"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code != 200:
            return {}, f"http_{r.status_code}"
        soup = BeautifulSoup(r.text, "html.parser")
        data = {}
        # Tabla principal de precios
        table = soup.find("table", {"class": "data_wide_table"})
        if not table:
            return {}, "no_table"
        for row in table.find_all("tr"):
            cols = row.find_all("td")
            if len(cols) >= 2:
                item = cols[0].get_text(strip=True)
                price_td = cols[1].get_text(strip=True)
                # Limpiar: "1,200.50 $" → float
                import re
                nums = re.findall(r"[\d,]+\.?\d*", price_td.replace(",", ""))
                currency_sym = re.findall(r"[€$£¥₩₹]|[A-Z]{3}", price_td)
                if nums:
                    try:
                        data[item] = {
                            "price": float(nums[0]),
                            "currency": currency_sym[0] if currency_sym else "$",
                            "raw": price_td,
                        }
                    except Exception:
                        pass
        return data, "ok"
    except Exception as e:
        return {}, str(e)


def render(pais, pais_nombre, lang="es"):
    L = {
        "title":    {"es": "💰 Coste de vida",
                     "en": "💰 Cost of Living"},
        "subtitle": {"es": "Precios de referencia para viajeros (fuente: Numbeo)",
                     "en": "Reference prices for travelers (source: Numbeo)"},
        "noslug":   {"es": f"⚠ Sin datos Numbeo para **{pais_nombre}**.",
                     "en": f"⚠ No Numbeo data for **{pais_nombre}**."},
        "error":    {"es": "Error consultando Numbeo",
                     "en": "Error querying Numbeo"},
        "nodata":   {"es": "Sin datos disponibles para esta categoría.",
                     "en": "No data available for this category."},
        "source":   {"es": "Fuente: Numbeo.com — precios orientativos, pueden variar",
                     "en": "Source: Numbeo.com — indicative prices, may vary"},
        "item":     {"es": "Concepto", "en": "Item"},
        "price":    {"es": "Precio",   "en": "Price"},
        "link":     {"es": "Ver país completo en Numbeo →",
                     "en": "View full country on Numbeo →"},
    }
    t = lambda k: L.get(k, {}).get(lang, L.get(k, {}).get("es", k))

    st.markdown(f"### {t('title')}")
    st.caption(t("subtitle"))

    slug = NUMBEO_SLUG.get(pais_nombre)
    if not slug:
        st.warning(t("noslug"))
        return

    with st.spinner("Consultando Numbeo..."):
        data, status = _fetch_numbeo(slug)

    if status != "ok" or not data:
        st.error(f"{t('error')}: {status}")
        return

    # Métricas rápidas (3 precios clave)
    meal   = data.get("Meal, Inexpensive Restaurant", {})
    beer   = data.get("Domestic Beer (0.5 liter draught)", {})
    taxi   = data.get("One-way Ticket (Local Transport)", {})
    hotel  = data.get("Apartment (1 bedroom) in City Centre", {})

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🍽 Menú barato",
                f"{meal.get('price','—')} {meal.get('currency','')}" if meal else "—")
    col2.metric("🍺 Cerveza local",
                f"{beer.get('price','—')} {beer.get('currency','')}" if beer else "—")
    col3.metric("🚌 Transporte",
                f"{taxi.get('price','—')} {taxi.get('currency','')}" if taxi else "—")
    col4.metric("🏨 Aparto/mes",
                f"{hotel.get('price','—')} {hotel.get('currency','')}" if hotel else "—")

    st.markdown("---")

    # Tabs por categoría
    cat_names = list(CATEGORIAS.keys())
    cat_tabs  = st.tabs(cat_names)

    for tab, (cat_label, items) in zip(cat_tabs, CATEGORIAS.items()):
        with tab:
            rows = []
            for item in items:
                if item in data:
                    d = data[item]
                    rows.append((item, f"{d['price']:.2f} {d['currency']}"))
            if not rows:
                st.info(t("nodata"))
                continue
            for item, price in rows:
                st.markdown(f"""
                <div style='display:flex;justify-content:space-between;align-items:center;
                     background:#0d1a2a;border:1px solid #1e2d40;border-radius:5px;
                     padding:8px 14px;margin-bottom:4px;font-family:JetBrains Mono;font-size:12px'>
                    <span style='color:#c8d8e8'>{item}</span>
                    <span style='color:#00d4aa;font-weight:700'>{price}</span>
                </div>
                """, unsafe_allow_html=True)

    # Link directo
    numbeo_url = f"https://www.numbeo.com/cost-of-living/country_result.jsp?country={slug}"
    st.markdown(f"""
    <div style='margin-top:16px'>
        <a href='{numbeo_url}' target='_blank'
           style='color:#00d4aa;font-family:JetBrains Mono;font-size:12px'>
            {t('link')}
        </a>
    </div>
    """, unsafe_allow_html=True)

    st.caption(t("source"))
