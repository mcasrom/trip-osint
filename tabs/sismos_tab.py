"""
tabs/sismos_tab.py — Sismos recientes por país (USGS API)
"""
import streamlit as st
import requests
from datetime import datetime, timezone
try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

COUNTRY_TZ = {
    "Alemania":               "Europe/Berlin",
    "Francia":                "Europe/Paris",
    "Italia":                 "Europe/Rome",
    "Reino Unido":            "Europe/London",
    "Turquía":                "Europe/Istanbul",
    "Portugal":               "Europe/Lisbon",
    "Grecia":                 "Europe/Athens",
    "México":                 "America/Mexico_City",
    "Colombia":               "America/Bogota",
    "Argentina":              "America/Argentina/Buenos_Aires",
    "Estados Unidos":         "America/New_York",
    "Japón":                  "Asia/Tokyo",
    "India":                  "Asia/Kolkata",
    "Tailandia":              "Asia/Bangkok",
    "China":                  "Asia/Shanghai",
    "Marruecos":              "Africa/Casablanca",
    "Egipto":                 "Africa/Cairo",
    "Australia":              "Australia/Sydney",
    "Austria":                "Europe/Vienna",
    "Bélgica":                "Europe/Brussels",
    "Países Bajos":           "Europe/Amsterdam",
    "Suiza":                  "Europe/Zurich",
    "Polonia":                "Europe/Warsaw",
    "República Checa":        "Europe/Prague",
    "Suecia":                 "Europe/Stockholm",
    "Noruega":                "Europe/Oslo",
    "Dinamarca":              "Europe/Copenhagen",
    "Irlanda":                "Europe/Dublin",
    "Croacia":                "Europe/Zagreb",
    "Hungría":                "Europe/Budapest",
    "Rumanía":                "Europe/Bucharest",
    "Georgia":                "Asia/Tbilisi",
    "Ucrania":                "Europe/Kiev",
    "Emiratos Árabes Unidos": "Asia/Dubai",
    "Arabia Saudí":           "Asia/Riyadh",
    "Israel":                 "Asia/Jerusalem",
    "Jordania":               "Asia/Amman",
    "Corea del Sur":          "Asia/Seoul",
    "Singapur":               "Asia/Singapore",
    "Vietnam":                "Asia/Ho_Chi_Minh",
    "Indonesia":              "Asia/Jakarta",
    "Malasia":                "Asia/Kuala_Lumpur",
    "Nepal":                  "Asia/Kathmandu",
    "Kenia":                  "Africa/Nairobi",
    "Tanzania":               "Africa/Dar_es_Salaam",
    "Sudáfrica":              "Africa/Johannesburg",
    "Ghana":                  "Africa/Accra",
    "Canadá":                 "America/Toronto",
    "Brasil":                 "America/Sao_Paulo",
    "Chile":                  "America/Santiago",
    "Perú":                   "America/Lima",
    "Cuba":                   "America/Havana",
    "Rep. Dominicana":        "America/Santo_Domingo",
    "Ecuador":                "America/Guayaquil",
    "Nueva Zelanda":          "Pacific/Auckland",
    "Rusia":                  "Europe/Moscow",
    "Filipinas":              "Asia/Manila",
    "Irán":                   "Asia/Tehran",
    "Pakistán":               "Asia/Karachi",
    "Afganistán":             "Asia/Kabul",
    "Argelia":                "Africa/Algiers",
    "Bolivia":                "America/La_Paz",
    "Venezuela":              "America/Caracas",
    "Costa Rica":             "America/Costa_Rica",
    "Guatemala":              "America/Guatemala",
}

def _get_tz(pais_nombre):
    iana = COUNTRY_TZ.get(pais_nombre, "UTC")
    try:
        return ZoneInfo(iana), iana
    except Exception:
        return __import__("datetime").timezone.utc, "UTC"

def _bbox(pais):
    """
    Bounding box aproximado por país [minlat, maxlat, minlon, maxlon]
    y timezone IANA para mostrar hora local.
    Returns: (bbox_list, iana_tz_string) o (None, "UTC")
    """
    DATA = {
        "Japón":          ([24, 46, 122, 154],   "Asia/Tokyo"),
        "Indonesia":      ([-11, 6, 95, 141],    "Asia/Jakarta"),
        "México":         ([14, 33, -118, -86],  "America/Mexico_City"),
        "Chile":          ([-56, -17, -76, -66], "America/Santiago"),
        "Turquía":        ([36, 42, 26, 45],     "Europe/Istanbul"),
        "Turkey":         ([36, 42, 26, 45],     "Europe/Istanbul"),
        "Italia":         ([37, 47, 6, 19],      "Europe/Rome"),
        "Grecia":         ([35, 42, 20, 30],     "Europe/Athens"),
        "Perú":           ([-18, -1, -82, -68],  "America/Lima"),
        "India":          ([8, 37, 68, 98],      "Asia/Kolkata"),
        "China":          ([18, 53, 73, 135],    "Asia/Shanghai"),
        "Filipinas":      ([4, 21, 116, 128],    "Asia/Manila"),
        "Nueva Zelanda":  ([-47, -34, 166, 178], "Pacific/Auckland"),
        "Australia":      ([-44, -10, 113, 154], "Australia/Sydney"),
        "Estados Unidos": ([24, 50, -125, -66],  "America/New_York"),
        "Canadá":         ([42, 70, -141, -52],  "America/Toronto"),
        "Colombia":       ([-5, 13, -79, -66],   "America/Bogota"),
        "Ecuador":        ([-5, 2, -82, -75],    "America/Guayaquil"),
        "Argentina":      ([-55, -22, -74, -53], "America/Argentina/Buenos_Aires"),
        "Bolivia":        ([-23, -9, -70, -57],  "America/La_Paz"),
        "Venezuela":      ([0, 13, -74, -59],    "America/Caracas"),
        "Costa Rica":     ([8, 12, -86, -82],    "America/Costa_Rica"),
        "Guatemala":      ([13, 18, -92, -88],   "America/Guatemala"),
        "Nepal":          ([26, 31, 80, 89],     "Asia/Kathmandu"),
        "Irán":           ([25, 40, 44, 64],     "Asia/Tehran"),
        "Pakistán":       ([23, 38, 60, 78],     "Asia/Karachi"),
        "Afganistán":     ([29, 39, 60, 75],     "Asia/Kabul"),
        "Rusia":          ([41, 77, 26, 180],    "Europe/Moscow"),
        "Marruecos":      ([27, 36, -14, -1],    "Africa/Casablanca"),
        "Argelia":        ([18, 38, -9, 12],     "Africa/Algiers"),
        "Kenia":          ([-5, 5, 33, 42],      "Africa/Nairobi"),
        "Tanzania":       ([-12, -1, 29, 41],    "Africa/Dar_es_Salaam"),
    }
    entry = DATA.get(pais)
    if entry:
        return entry[0], entry[1]
    return None, "UTC"


ALERT_COLOR = {
    "green":  ("#00e676", "🟢 Verde"),
    "yellow": ("#ffd600", "🟡 Amarillo"),
    "orange": ("#ff9100", "🟠 Naranja"),
    "red":    ("#ff1744", "🔴 Rojo"),
}


def _fetch_sismos(pais, minmag=4.0, limit=10):
    bbox, _ = _bbox(pais)
    params = {
        "format":       "geojson",
        "minmagnitude": minmag,
        "limit":        limit,
        "orderby":      "time",
    }
    if bbox:
        params["minlatitude"]  = bbox[0]
        params["maxlatitude"]  = bbox[1]
        params["minlongitude"] = bbox[2]
        params["maxlongitude"] = bbox[3]
    else:
        return None, "sin_bbox"
    try:
        r = requests.get(
            "https://earthquake.usgs.gov/fdsnws/event/1/query",
            params=params, timeout=10
        )
        if r.status_code == 200:
            return r.json().get("features", []), "ok"
        return [], f"http_{r.status_code}"
    except Exception as e:
        return [], str(e)


def render(pais, pais_nombre, lang="es"):
    L = {
        "title":    {"es": "🌋 Sismos recientes",        "en": "🌋 Recent Earthquakes"},
        "minmag":   {"es": "Magnitud mínima",            "en": "Minimum magnitude"},
        "limit":    {"es": "Nº de resultados",           "en": "Number of results"},
        "nobbox":   {"es": f"⚠ Sin cobertura sísmica definida para **{pais_nombre}**.",
                     "en": f"⚠ No seismic coverage defined for **{pais_nombre}**."},
        "nodata":   {"es": "✅ Sin sismos recientes con los filtros seleccionados.",
                     "en": "✅ No recent earthquakes with selected filters."},
        "mag":      {"es": "Magnitud", "en": "Magnitude"},
        "place":    {"es": "Lugar",    "en": "Location"},
        "date":     {"es": "Fecha",    "en": "Date"},
        "alert":    {"es": "Alerta",   "en": "Alert"},
        "tsunami":  {"es": "Tsunami",  "en": "Tsunami"},
        "source":   {"es": "Fuente: USGS Earthquake Hazards Program — earthquake.usgs.gov",
                     "en": "Source: USGS Earthquake Hazards Program — earthquake.usgs.gov"},
        "error":    {"es": "Error consultando USGS",  "en": "Error querying USGS"},
        "fallback": {"es": "⚠ País sin cobertura bbox — mostrando sismos globales M≥5.5",
                     "en": "⚠ Country without bbox — showing global M≥5.5 earthquakes"},
        "localtime":{"es": "Hora local",  "en": "Local time"},
        "tz_label": {"es": "Huso horario","en": "Time zone"},
    }
    t = lambda k: L.get(k, {}).get(lang, L.get(k, {}).get("es", k))

    st.markdown(f"### {t('title')}")

    # Obtener timezone del país
    local_tz, iana_tz = _get_tz(pais_nombre)
    try:
        local_tz = ZoneInfo(iana_tz)
    except Exception:
        local_tz = timezone.utc
        iana_tz = "UTC"

    # Mostrar huso horario como info
    utc_offset = datetime.now(tz=local_tz).strftime("%z")
    utc_fmt = f"UTC{utc_offset[:3]}:{utc_offset[3:]}" if len(utc_offset) == 5 else "UTC"
    st.caption(f"🕐 {t('tz_label')}: `{iana_tz}` ({utc_fmt})")

    col1, col2 = st.columns(2)
    with col1:
        minmag = st.slider(t("minmag"), 2.0, 8.0, 4.0, 0.5, key="sismos_minmag")
    with col2:
        limit = st.slider(t("limit"), 5, 50, 15, 5, key="sismos_limit")

    with st.spinner("Consultando USGS..."):
        features, status = _fetch_sismos(pais_nombre, minmag, limit)

    if status == "sin_bbox":
        st.warning(t("nobbox"))
        st.info(t("fallback"))
        # Fallback global sin bbox
        try:
            r = requests.get(
                "https://earthquake.usgs.gov/fdsnws/event/1/query",
                params={"format": "geojson", "minmagnitude": 5.5,
                        "limit": 10, "orderby": "time"},
                timeout=10
            )
            features = r.json().get("features", []) if r.status_code == 200 else []
            status = "ok"
        except Exception as e:
            st.error(str(e))
            return

    if status != "ok" and not features:
        st.error(f"{t('error')}: {status}")
        return

    if not features:
        st.success(t("nodata"))
        return

    # Métricas resumen
    mags = [f["properties"].get("mag", 0) or 0 for f in features]
    tsunamis = sum(1 for f in features if f["properties"].get("tsunami"))
    col1, col2, col3 = st.columns(3)
    col1.metric(f"Total M≥{minmag}", len(features))
    col2.metric("Magnitud máxima", f"M{max(mags):.1f}" if mags else "—")
    col3.metric("Alertas tsunami", tsunamis)

    # Cards
    for f in features:
        p = f["properties"]
        ts = (p.get("time") or 0) / 1000
        dt_utc   = datetime.fromtimestamp(ts, tz=timezone.utc)
        dt_local = datetime.fromtimestamp(ts, tz=local_tz)
        fecha_utc   = dt_utc.strftime("%d/%m/%Y %H:%M UTC")
        fecha_local = dt_local.strftime("%d/%m/%Y %H:%M") + f" ({iana_tz})"
        mag = p.get("mag") or 0
        mag_color = "#00e676" if mag < 5 else "#ffd600" if mag < 6 else "#ff9100" if mag < 7 else "#ff1744"
        alerta = p.get("alert") or ""
        color_alerta, label_alerta = ALERT_COLOR.get(alerta, ("#4a6080", "—"))
        url = p.get("url", "#")
        tsunami_html = "&nbsp;·&nbsp;<span style='color:#ff9100'>⚠️ Tsunami</span>" if p.get("tsunami") else ""
        alerta_html  = f"&nbsp;·&nbsp;<span style='color:{color_alerta}'>{label_alerta}</span>" if alerta else ""

        st.markdown(f"""
        <div style='background:#0d1a2a;border:1px solid #1e2d40;border-left:3px solid {mag_color};
             border-radius:6px;padding:10px 14px;margin-bottom:6px;font-family:JetBrains Mono;font-size:12px'>
            <span style='color:{mag_color};font-weight:700;font-size:14px'>M{mag:.1f}</span>
            &nbsp;·&nbsp;<span style='color:#c8d8e8'>{p.get('place','N/D')}</span>
            {tsunami_html}{alerta_html}
            <br>
            <span style='color:#4a6080'>🌐 {fecha_utc}</span>
            &nbsp;·&nbsp;<span style='color:#00d4aa'>🕐 {fecha_local}</span>
            &nbsp;<a href='{url}' target='_blank' style='color:#00d4aa;text-decoration:none;float:right'>→ USGS</a>
        </div>
        """, unsafe_allow_html=True)

    st.caption(t("source"))
