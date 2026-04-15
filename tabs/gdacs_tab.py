"""
tabs/gdacs_tab.py — Alertas de desastres globales (GDACS RSS feed)
No requiere API key. Feed público: https://www.gdacs.org/xml/rss.xml
Tipos: TC (tifón/ciclón), EQ (terremoto), FL (inundación),
       VO (volcán), DR (sequía), WF (incendio forestal)
"""
import streamlit as st
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

# Namespace GDACS en el feed RSS
NS = {
    "gdacs": "http://www.gdacs.org",
    "geo":   "http://www.w3.org/2003/01/geo/wgs84_pos#",
    "dc":    "http://purl.org/dc/elements/1.1/",
}

GDACS_FEED = "https://www.gdacs.org/xml/rss.xml"

# Tipos de evento GDACS → etiqueta + color
EVENT_META = {
    "TC": ("🌀 Ciclón/Tifón",      "#7c4dff"),
    "EQ": ("🌋 Terremoto",         "#ff9100"),
    "FL": ("🌊 Inundación",        "#00bcd4"),
    "VO": ("🔥 Volcán",            "#ff5722"),
    "DR": ("🏜 Sequía",            "#ffd600"),
    "WF": ("🔥 Incendio forestal", "#ff6d00"),
}

# Alert level → color
ALERT_COLOR = {
    "Green":  "#00e676",
    "Orange": "#ff9100",
    "Red":    "#ff1744",
}

# Países → timezone IANA (mismo dict que sismos, subset útil + extras)
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
        return timezone.utc, "UTC"


def _fetch_gdacs():
    """Descarga y parsea el feed RSS de GDACS. Devuelve lista de dicts."""
    try:
        r = requests.get(GDACS_FEED, timeout=15,
                         headers={"User-Agent": "trip-osint/1.0"})
        if r.status_code != 200:
            return [], f"http_{r.status_code}"
        root = ET.fromstring(r.content)
        channel = root.find("channel")
        if channel is None:
            return [], "no_channel"
        items = []
        for item in channel.findall("item"):
            def g(tag, ns=None):
                el = item.find(tag) if ns is None else item.find(tag, ns)
                return (el.text or "").strip() if el is not None else ""

            alert_level = g("gdacs:alertlevel", NS)
            event_type  = g("gdacs:eventtype",  NS)
            country     = g("gdacs:country",    NS)
            todate      = g("gdacs:todate",      NS)
            severity    = g("gdacs:severity",    NS)  # descripción textual
            population  = g("gdacs:population",  NS)
            lat         = g("geo:lat",  NS)
            lon         = g("geo:long", NS)
            title       = g("title")
            link        = g("link")
            pub_date    = g("pubDate")

            # Parsear fecha pubDate  "Thu, 10 Apr 2025 12:00:00 GMT"
            dt = None
            for fmt in ("%a, %d %b %Y %H:%M:%S %Z", "%a, %d %b %Y %H:%M:%S %z"):
                try:
                    dt = datetime.strptime(pub_date, fmt)
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
                    break
                except Exception:
                    pass

            items.append({
                "title":       title,
                "event_type":  event_type,
                "alert_level": alert_level,
                "country":     country,
                "severity":    severity,
                "population":  population,
                "lat":         lat,
                "lon":         lon,
                "link":        link,
                "dt":          dt,
            })
        return items, "ok"
    except Exception as e:
        return [], str(e)


def _filter_by_country(items, pais_nombre):
    """
    Filtra por país. Comparación case-insensitive parcial
    porque GDACS usa nombres en inglés.
    """
    pais_lower = pais_nombre.lower()
    # Traducciones ES→EN para matching
    TRANS = {
        "japón": "japan", "méxico": "mexico", "turquía": "turkey",
        "italia": "italy", "grecia": "greece", "perú": "peru",
        "filipinas": "philippines", "nueva zelanda": "new zealand",
        "estados unidos": "united states", "canadá": "canada",
        "colombia": "colombia", "ecuador": "ecuador",
        "marruecos": "morocco", "argelia": "algeria",
        "kenia": "kenya", "irán": "iran", "pakistán": "pakistan",
        "afganistán": "afghanistan", "rusia": "russia",
        "brasil": "brazil", "tailandia": "thailand",
        "españa": "spain", "etiopía": "ethiopia", "sudán": "sudan",
    }
    search = TRANS.get(pais_lower, pais_lower)
    return [i for i in items if search in (i.get("country") or "").lower()]


def render(pais, pais_nombre, lang="es"):
    L = {
        "title":     {"es": "🚨 Alertas de desastres (GDACS)",
                      "en": "🚨 Disaster Alerts (GDACS)"},
        "subtitle":  {"es": "Feed en tiempo real del Sistema Global de Alertas de Desastres",
                      "en": "Real-time feed from the Global Disaster Alert and Coordination System"},
        "filter":    {"es": "Filtrar por tipo de evento", "en": "Filter by event type"},
        "all":       {"es": "Todos",                      "en": "All"},
        "nodata":    {"es": f"✅ Sin alertas activas para **{pais_nombre}** en el feed GDACS actual.",
                      "en": f"✅ No active alerts for **{pais_nombre}** in current GDACS feed."},
        "global":    {"es": "Mostrando alertas globales (sin filtro por país)",
                      "en": "Showing global alerts (no country filter)"},
        "error":     {"es": "Error al consultar GDACS", "en": "Error querying GDACS"},
        "severity":  {"es": "Severidad",   "en": "Severity"},
        "affected":  {"es": "Afectados",   "en": "Affected pop."},
        "date":      {"es": "Fecha",       "en": "Date"},
        "localtime": {"es": "Hora local",  "en": "Local time"},
        "tz_label":  {"es": "Huso horario","en": "Time zone"},
        "source":    {"es": "Fuente: GDACS — gdacs.org | Actualización: en tiempo real",
                      "en": "Source: GDACS — gdacs.org | Updates: real-time"},
        "no_tz":     {"es": "UTC (país sin huso definido)", "en": "UTC (country TZ undefined)"},
    }
    t = lambda k: L.get(k, {}).get(lang, L.get(k, {}).get("es", k))

    st.markdown(f"### {t('title')}")
    st.caption(t("subtitle"))

    # Huso horario del país
    local_tz, iana_tz = _get_tz(pais_nombre)
    utc_offset = datetime.now(tz=local_tz).strftime("%z")
    utc_fmt = f"UTC{utc_offset[:3]}:{utc_offset[3:]}" if len(utc_offset) == 5 else "UTC"
    tz_display = f"🕐 {t('tz_label')}: `{iana_tz}` ({utc_fmt})"
    if iana_tz == "UTC":
        tz_display = f"🕐 {t('no_tz')}"
    st.caption(tz_display)

    with st.spinner("Consultando GDACS..."):
        all_items, status = _fetch_gdacs()

    if status != "ok" and not all_items:
        st.error(f"{t('error')}: {status}")
        return

    # Filtrar por país
    country_items = _filter_by_country(all_items, pais_nombre)
    show_global = len(country_items) == 0

    if show_global:
        st.info(t("global"))
        display_items = all_items[:20]
    else:
        display_items = country_items

    if not display_items:
        st.success(t("nodata"))
        return

    # Filtro tipo evento
    tipos_presentes = sorted(set(i["event_type"] for i in display_items if i["event_type"]))
    tipo_labels = {k: EVENT_META.get(k, (k, "#4a6080"))[0] for k in tipos_presentes}
    opciones = [t("all")] + [tipo_labels.get(k, k) for k in tipos_presentes]
    sel = st.selectbox(t("filter"), opciones, key="gdacs_tipo")

    if sel != t("all"):
        tipo_sel = next((k for k, v in tipo_labels.items() if v == sel), None)
        display_items = [i for i in display_items if i["event_type"] == tipo_sel]

    # Métricas resumen
    n_red    = sum(1 for i in display_items if (i["alert_level"] or "").lower() == "red")
    n_orange = sum(1 for i in display_items if (i["alert_level"] or "").lower() == "orange")
    n_green  = sum(1 for i in display_items if (i["alert_level"] or "").lower() == "green")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total alertas", len(display_items))
    col2.metric("🔴 Rojo",       n_red)
    col3.metric("🟠 Naranja",    n_orange)
    col4.metric("🟢 Verde",      n_green)

    st.markdown("---")

    # Cards
    for item in display_items:
        ev_label, ev_color = EVENT_META.get(item["event_type"], (item["event_type"], "#4a6080"))
        al_color = ALERT_COLOR.get(item["alert_level"], "#4a6080")
        al_label = item["alert_level"] or "—"

        # Fechas
        fecha_utc   = "—"
        fecha_local = "—"
        if item["dt"]:
            dt_utc = item["dt"].astimezone(timezone.utc)
            dt_loc = item["dt"].astimezone(local_tz)
            fecha_utc   = dt_utc.strftime("%d/%m/%Y %H:%M UTC")
            fecha_local = dt_loc.strftime("%d/%m/%Y %H:%M") + f" ({iana_tz})"

        country_str  = f"&nbsp;·&nbsp;<span style='color:#c8d8e8'>{item['country']}</span>" if item["country"] else ""
        severity_str = f"<br><span style='color:#8a9bac;font-size:11px'>{item['severity']}</span>" if item["severity"] else ""
        pop_str      = f"&nbsp;·&nbsp;<span style='color:#ffd600'>👥 {item['population']}</span>" if item["population"] else ""
        link_str     = f"<a href='{item['link']}' target='_blank' style='color:#00d4aa;text-decoration:none;float:right'>→ GDACS</a>" if item["link"] else ""

        st.markdown(f"""
        <div style='background:#0d1a2a;border:1px solid #1e2d40;border-left:3px solid {al_color};
             border-radius:6px;padding:10px 14px;margin-bottom:8px;font-family:JetBrains Mono;font-size:12px'>
            <span style='color:{ev_color};font-weight:700'>{ev_label}</span>
            &nbsp;·&nbsp;<span style='color:{al_color};font-weight:700'>● {al_label}</span>
            {country_str}
            {pop_str}
            {link_str}
            <br>
            <span style='color:#c8d8e8'>{item['title']}</span>
            {severity_str}
            <br>
            <span style='color:#4a6080'>🌐 {fecha_utc}</span>
            &nbsp;·&nbsp;<span style='color:#00d4aa'>🕐 {fecha_local}</span>
        </div>
        """, unsafe_allow_html=True)

    st.caption(t("source"))
