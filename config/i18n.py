"""
config/i18n.py — Internacionalización ES/EN TripOSINT
"""

STRINGS = {
    # ── App general ───────────────────────────────────────────────────────────
    "app_title": {
        "es": "TripOSINT — Inteligencia para viajeros",
        "en": "TripOSINT — Travel Intelligence Dashboard",
    },
    "app_subtitle": {
        "es": "Inteligencia para viajeros v2.0",
        "en": "Travel Intelligence v2.0",
    },
    "app_tagline": {
        "es": "Viaja con inteligencia, no con suerte",
        "en": "Travel smart, not blind",
    },
    "app_source": {
        "es": "▸ INTELIGENCIA DE VIAJE · OSINT · FUENTES OFICIALES",
        "en": "▸ TRAVEL INTELLIGENCE · OSINT · OFFICIAL SOURCES",
    },
    # ── Sidebar ───────────────────────────────────────────────────────────────
    "sidebar_region": {
        "es": "🌐 Región",
        "en": "🌐 Region",
    },
    "sidebar_all": {
        "es": "Todas",
        "en": "All",
    },
    "sidebar_country": {
        "es": "✈ País de destino",
        "en": "✈ Destination country",
    },
    "sidebar_motive": {
        "es": "🎯 Motivo del viaje",
        "en": "🎯 Purpose of travel",
    },
    "sidebar_motives": {
        "es": ["Turismo", "Trabajo / Negocios", "Familiar", "Estudios", "Sanitario"],
        "en": ["Tourism", "Work / Business", "Family", "Studies", "Medical"],
    },
    "sidebar_share": {
        "es": "🔗 Compartir este destino",
        "en": "🔗 Share this destination",
    },
    "sidebar_summary": {
        "es": "RESUMEN DESTINO",
        "en": "DESTINATION SUMMARY",
    },
    "sidebar_coffee": {
        "es": "☕ Invítame a un café",
        "en": "☕ Buy me a coffee",
    },
    "sidebar_contact": {
        "es": "✉ Contacto",
        "en": "✉ Contact",
    },
    "sidebar_lang": {
        "es": "🌐 Idioma / Language",
        "en": "🌐 Idioma / Language",
    },
    # ── Riesgo MAEC ───────────────────────────────────────────────────────────
    "risk_labels": {
        "es": {
            1: ("🟢", "Sin riesgo especial"),
            2: ("🟡", "Precaución"),
            3: ("🟠", "Alta precaución"),
            4: ("🔴", "No recomendado"),
            5: ("⛔", "Desaconsejado totalmente"),
        },
        "en": {
            1: ("🟢", "No special risk"),
            2: ("🟡", "Caution advised"),
            3: ("🟠", "High caution"),
            4: ("🔴", "Not recommended"),
            5: ("⛔", "Travel strongly discouraged"),
        },
    },
    # ── Tabs principales ──────────────────────────────────────────────────────
    "tab_security": {
        "es": "🛡️ Seguridad",
        "en": "🛡️ Security",
    },
    "tab_health": {
        "es": "🏥 Salud & Entrada",
        "en": "🏥 Health & Entry",
    },
    "tab_destination": {
        "es": "🌍 Destino",
        "en": "🌍 Destination",
    },
    "tab_intel": {
        "es": "📡 Inteligencia",
        "en": "📡 Intelligence",
    },
    "tab_tools": {
        "es": "🛠️ Herramientas",
        "en": "🛠️ Tools",
    },
    # ── Subtabs ───────────────────────────────────────────────────────────────
    "subtab_risk_global": {
        "es": "🌐 Riesgo Global",
        "en": "🌐 Global Risk",
    },
    "subtab_maec": {
        "es": "🚨 Alertas MAEC",
        "en": "🚨 MAEC Alerts",
    },
    "subtab_health": {
        "es": "🏥 Salud & OMS",
        "en": "🏥 Health & WHO",
    },
    "subtab_entry": {
        "es": "📋 Requisitos entrada",
        "en": "📋 Entry requirements",
    },
    "subtab_info": {
        "es": "ℹ️ Info & Contactos",
        "en": "ℹ️ Info & Contacts",
    },
    "subtab_meteo": {
        "es": "🌤️ Meteorología",
        "en": "🌤️ Weather",
    },
    "subtab_currency": {
        "es": "💱 Divisa & Cambio",
        "en": "💱 Currency & Exchange",
    },
    "subtab_press": {
        "es": "📰 Prensa local",
        "en": "📰 Local press",
    },
    "subtab_checklist": {
        "es": "✅ Checklists",
        "en": "✅ Checklists",
    },
    "subtab_export": {
        "es": "📄 Export PDF",
        "en": "📄 Export PDF",
    },
    "subtab_methodology": {
        "es": "🔬 Metodología & Fuentes",
        "en": "🔬 Methodology & Sources",
    },
    # ── Header info ───────────────────────────────────────────────────────────
    "header_capital": {
        "es": "Capital",
        "en": "Capital",
    },
    "header_region": {
        "es": "Región",
        "en": "Region",
    },
    "header_currency": {
        "es": "Moneda",
        "en": "Currency",
    },
    "header_language": {
        "es": "Idioma",
        "en": "Language",
    },
    "header_plugs": {
        "es": "Enchufes",
        "en": "Power plugs",
    },
    "header_driving": {
        "es": "Conducción",
        "en": "Driving side",
    },
    "header_motive": {
        "es": "Motivo",
        "en": "Purpose",
    },
    "header_risk": {
        "es": "Riesgo MAEC",
        "en": "MAEC Risk",
    },
    # ── SEO meta por país ─────────────────────────────────────────────────────
    "seo_title": {
        "es": "{pais} — Guía OSINT para viajeros · TripOSINT",
        "en": "{pais} — OSINT Travel Intelligence Guide · TripOSINT",
    },
    "seo_description": {
        "es": "Información de inteligencia actualizada para viajar a {pais}: alertas MAEC, requisitos de entrada, salud, seguridad, clima y divisas. Fuentes oficiales.",
        "en": "Up-to-date travel intelligence for {pais}: MAEC alerts, entry requirements, health, security, weather and currency. Official sources.",
    },
    "seo_keywords": {
        "es": "viajar a {pais}, seguridad {pais}, requisitos entrada {pais}, alertas MAEC {pais}, visa {pais}, vacunas {pais}, OSINT viajeros",
        "en": "travel to {pais}, {pais} safety, {pais} entry requirements, {pais} travel alerts, {pais} visa, {pais} vaccines, travel OSINT",
    },
}

def t(key, lang="es", **kwargs):
    """Helper: devuelve string traducido con formato opcional."""
    val = STRINGS.get(key, {}).get(lang, STRINGS.get(key, {}).get("es", key))
    if kwargs:
        try:
            return val.format(**kwargs)
        except Exception:
            return val
    return val
