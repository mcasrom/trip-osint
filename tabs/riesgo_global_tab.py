"""
tabs/riesgo_global_tab.py — Mapa de riesgo global MAEC
Datos hardcoded basados en recomendaciones MAEC (actualizar trimestralmente)
Última revisión: Abril 2026
"""
import streamlit as st
from datetime import datetime

# ── Base de datos de riesgo global MAEC ──────────────────────────────────────
# Niveles: 1=Sin riesgo especial | 2=Precaución | 3=Alta precaución
#          4=No recomendado      | 5=Desaconsejado totalmente
# Fuente: exteriores.gob.es — revisar trimestralmente

ULTIMA_ACTUALIZACION = "Abril 2026"

RIESGO_GLOBAL = [
    # ── EUROPA ────────────────────────────────────────────────────────────────
    {"pais": "Alemania",          "region": "Europa",   "nivel": 1, "emoji": "🇩🇪", "alerta": ""},
    {"pais": "Austria",           "region": "Europa",   "nivel": 1, "emoji": "🇦🇹", "alerta": ""},
    {"pais": "Bélgica",           "region": "Europa",   "nivel": 1, "emoji": "🇧🇪", "alerta": "Amenaza terrorista activa"},
    {"pais": "Francia",           "region": "Europa",   "nivel": 1, "emoji": "🇫🇷", "alerta": "Plan Vigipirate — vigilancia elevada"},
    {"pais": "Italia",            "region": "Europa",   "nivel": 1, "emoji": "🇮🇹", "alerta": ""},
    {"pais": "Portugal",          "region": "Europa",   "nivel": 1, "emoji": "🇵🇹", "alerta": ""},
    {"pais": "Países Bajos",      "region": "Europa",   "nivel": 1, "emoji": "🇳🇱", "alerta": ""},
    {"pais": "Suiza",             "region": "Europa",   "nivel": 1, "emoji": "🇨🇭", "alerta": ""},
    {"pais": "Grecia",            "region": "Europa",   "nivel": 1, "emoji": "🇬🇷", "alerta": ""},
    {"pais": "Polonia",           "region": "Europa",   "nivel": 1, "emoji": "🇵🇱", "alerta": "Frontera con Bielorrusia — precaución zona norte"},
    {"pais": "República Checa",   "region": "Europa",   "nivel": 1, "emoji": "🇨🇿", "alerta": ""},
    {"pais": "Suecia",            "region": "Europa",   "nivel": 1, "emoji": "🇸🇪", "alerta": ""},
    {"pais": "Noruega",           "region": "Europa",   "nivel": 1, "emoji": "🇳🇴", "alerta": ""},
    {"pais": "Dinamarca",         "region": "Europa",   "nivel": 1, "emoji": "🇩🇰", "alerta": ""},
    {"pais": "Reino Unido",       "region": "Europa",   "nivel": 1, "emoji": "🇬🇧", "alerta": "Amenaza terrorista considerable (SUBSTANTIAL)"},
    {"pais": "Irlanda",           "region": "Europa",   "nivel": 1, "emoji": "🇮🇪", "alerta": ""},
    {"pais": "Croacia",           "region": "Europa",   "nivel": 1, "emoji": "🇭🇷", "alerta": ""},
    {"pais": "Hungría",           "region": "Europa",   "nivel": 1, "emoji": "🇭🇺", "alerta": ""},
    {"pais": "Rumanía",           "region": "Europa",   "nivel": 1, "emoji": "🇷🇴", "alerta": ""},
    {"pais": "Bulgaria",          "region": "Europa",   "nivel": 1, "emoji": "🇧🇬", "alerta": ""},
    {"pais": "Turquía",           "region": "Europa",   "nivel": 2, "emoji": "🇹🇷", "alerta": "Riesgo terrorista — frontera Siria/Irak no recomendada"},
    {"pais": "Serbia",            "region": "Europa",   "nivel": 2, "emoji": "🇷🇸", "alerta": "Tensión étnica en Kosovo"},
    {"pais": "Albania",           "region": "Europa",   "nivel": 2, "emoji": "🇦🇱", "alerta": "Crimen organizado"},
    {"pais": "Bosnia-Herz.",      "region": "Europa",   "nivel": 2, "emoji": "🇧🇦", "alerta": "Tensión política interna"},
    {"pais": "Georgia",           "region": "Europa",   "nivel": 2, "emoji": "🇬🇪", "alerta": "Zonas de Abjasia y Osetia del Sur — no acceder"},
    {"pais": "Armenia",           "region": "Europa",   "nivel": 2, "emoji": "🇦🇲", "alerta": "Tensión fronteriza con Azerbaiyán"},
    {"pais": "Moldavia",          "region": "Europa",   "nivel": 2, "emoji": "🇲🇩", "alerta": "Transnistria — no acceder"},
    {"pais": "Ucrania",           "region": "Europa",   "nivel": 5, "emoji": "🇺🇦", "alerta": "⛔ CONFLICTO ARMADO ACTIVO — No viajar"},
    {"pais": "Rusia",             "region": "Europa",   "nivel": 5, "emoji": "🇷🇺", "alerta": "⛔ Desaconsejado totalmente — Sanciones, detenciones arbitrarias, conflicto"},
    {"pais": "Bielorrusia",       "region": "Europa",   "nivel": 4, "emoji": "🇧🇾", "alerta": "🔴 Régimen autoritario — riesgo detención arbitraria"},

    # ── ORIENTE MEDIO ─────────────────────────────────────────────────────────
    {"pais": "Emiratos Árabes",   "region": "Oriente Medio", "nivel": 1, "emoji": "🇦🇪", "alerta": "Legislación muy estricta — respetar normas locales"},
    {"pais": "Qatar",             "region": "Oriente Medio", "nivel": 1, "emoji": "🇶🇦", "alerta": "Legislación estricta — alcohol y relaciones LGTBI+ ilegales"},
    {"pais": "Jordania",          "region": "Oriente Medio", "nivel": 2, "emoji": "🇯🇴", "alerta": "Frontera Siria/Irak — precaución zona norte"},
    {"pais": "Arabia Saudí",      "region": "Oriente Medio", "nivel": 2, "emoji": "🇸🇦", "alerta": "Legislación islámica muy estricta — LGTBI+ ilegal, alcohol prohibido"},
    {"pais": "Kuwait",            "region": "Oriente Medio", "nivel": 2, "emoji": "🇰🇼", "alerta": "Legislación estricta"},
    {"pais": "Omán",              "region": "Oriente Medio", "nivel": 2, "emoji": "🇴🇲", "alerta": ""},
    {"pais": "Líbano",            "region": "Oriente Medio", "nivel": 4, "emoji": "🇱🇧", "alerta": "🔴 Crisis económica grave, inestabilidad política, riesgo de conflicto"},
    {"pais": "Irak",              "region": "Oriente Medio", "nivel": 5, "emoji": "🇮🇶", "alerta": "⛔ Terrorismo, conflicto armado — No viajar"},
    {"pais": "Irán",              "region": "Oriente Medio", "nivel": 4, "emoji": "🇮🇷", "alerta": "🔴 Tensión regional extrema, detenciones arbitrarias, sanciones"},
    {"pais": "Siria",             "region": "Oriente Medio", "nivel": 5, "emoji": "🇸🇾", "alerta": "⛔ Conflicto armado activo — No viajar bajo ningún concepto"},
    {"pais": "Yemen",             "region": "Oriente Medio", "nivel": 5, "emoji": "🇾🇪", "alerta": "⛔ Guerra civil activa — No viajar"},
    {"pais": "Israel",            "region": "Oriente Medio", "nivel": 3, "emoji": "🇮🇱", "alerta": "🟠 Conflicto activo en Gaza — evitar sur y zonas fronterizas"},
    {"pais": "Palestina",         "region": "Oriente Medio", "nivel": 5, "emoji": "🇵🇸", "alerta": "⛔ Conflicto armado activo (Gaza) — No viajar"},

    # ── ASIA ──────────────────────────────────────────────────────────────────
    {"pais": "Japón",             "region": "Asia",     "nivel": 1, "emoji": "🇯🇵", "alerta": "País sísmico — conocer protocolos de emergencia"},
    {"pais": "Corea del Sur",     "region": "Asia",     "nivel": 1, "emoji": "🇰🇷", "alerta": ""},
    {"pais": "Singapur",          "region": "Asia",     "nivel": 1, "emoji": "🇸🇬", "alerta": "Penas muy severas por drogas (incluso tránsito)"},
    {"pais": "Tailandia",         "region": "Asia",     "nivel": 2, "emoji": "🇹🇭", "alerta": "Lèse-majesté — no criticar monarquía"},
    {"pais": "Vietnam",           "region": "Asia",     "nivel": 2, "emoji": "🇻🇳", "alerta": ""},
    {"pais": "Indonesia",         "region": "Asia",     "nivel": 2, "emoji": "🇮🇩", "alerta": "Riesgo terrorista y sísmica alta"},
    {"pais": "Malasia",           "region": "Asia",     "nivel": 2, "emoji": "🇲🇾", "alerta": ""},
    {"pais": "India",             "region": "Asia",     "nivel": 2, "emoji": "🇮🇳", "alerta": "Cachemira — no acceder; contaminación extrema Delhi"},
    {"pais": "China",             "region": "Asia",     "nivel": 2, "emoji": "🇨🇳", "alerta": "Internet restringida — VPN antes de viajar; Xinjiang/Tibet restricciones"},
    {"pais": "Nepal",             "region": "Asia",     "nivel": 2, "emoji": "🇳🇵", "alerta": "Zonas de montaña — riesgo de altitud"},
    {"pais": "Sri Lanka",         "region": "Asia",     "nivel": 2, "emoji": "🇱🇰", "alerta": "Recuperación post-crisis económica"},
    {"pais": "Filipinas",         "region": "Asia",     "nivel": 3, "emoji": "🇵🇭", "alerta": "🟠 Mindanao — no viajar; resto precaución alta"},
    {"pais": "Bangladesh",        "region": "Asia",     "nivel": 3, "emoji": "🇧🇩", "alerta": "🟠 Inestabilidad política, inundaciones"},
    {"pais": "Pakistán",          "region": "Asia",     "nivel": 4, "emoji": "🇵🇰", "alerta": "🔴 Terrorismo, inestabilidad — No recomendado"},
    {"pais": "Afganistán",        "region": "Asia",     "nivel": 5, "emoji": "🇦🇫", "alerta": "⛔ Talibán en el poder, terrorismo — No viajar"},
    {"pais": "Corea del Norte",   "region": "Asia",     "nivel": 5, "emoji": "🇰🇵", "alerta": "⛔ Régimen totalitario — No viajar"},
    {"pais": "Myanmar",           "region": "Asia",     "nivel": 4, "emoji": "🇲🇲", "alerta": "🔴 Golpe de Estado, conflicto armado interno"},

    # ── ÁFRICA ────────────────────────────────────────────────────────────────
    {"pais": "Marruecos",         "region": "África",   "nivel": 2, "emoji": "🇲🇦", "alerta": "Atención estafas turistas en medinas"},
    {"pais": "Túnez",             "region": "África",   "nivel": 2, "emoji": "🇹🇳", "alerta": "Riesgo terrorista en zonas fronterizas"},
    {"pais": "Egipto",            "region": "África",   "nivel": 3, "emoji": "🇪🇬", "alerta": "🟠 Sinaí norte y fronteras — No acceder"},
    {"pais": "Kenia",             "region": "África",   "nivel": 3, "emoji": "🇰🇪", "alerta": "🟠 Frontera Somalia, terrorismo Al-Shabaab"},
    {"pais": "Tanzania",          "region": "África",   "nivel": 2, "emoji": "🇹🇿", "alerta": ""},
    {"pais": "Sudáfrica",         "region": "África",   "nivel": 3, "emoji": "🇿🇦", "alerta": "🟠 Alta criminalidad urbana — precaución extrema"},
    {"pais": "Ghana",             "region": "África",   "nivel": 2, "emoji": "🇬🇭", "alerta": ""},
    {"pais": "Etiopía",           "region": "África",   "nivel": 3, "emoji": "🇪🇹", "alerta": "🟠 Conflicto interno activo en Tigray y Amhara"},
    {"pais": "Nigeria",           "region": "África",   "nivel": 4, "emoji": "🇳🇬", "alerta": "🔴 Boko Haram norte, criminalidad extrema Lagos"},
    {"pais": "Libia",             "region": "África",   "nivel": 5, "emoji": "🇱🇾", "alerta": "⛔ Conflicto armado, milicias — No viajar"},
    {"pais": "Sudán",             "region": "África",   "nivel": 5, "emoji": "🇸🇩", "alerta": "⛔ Guerra civil activa — No viajar"},
    {"pais": "Mali",              "region": "África",   "nivel": 5, "emoji": "🇲🇱", "alerta": "⛔ Terrorismo yihadista — No viajar"},
    {"pais": "Somalia",           "region": "África",   "nivel": 5, "emoji": "🇸🇴", "alerta": "⛔ Estado fallido, terrorismo — No viajar bajo ningún concepto"},

    # ── AMÉRICA ───────────────────────────────────────────────────────────────
    {"pais": "Estados Unidos",    "region": "América",  "nivel": 1, "emoji": "🇺🇸", "alerta": "ESTA obligatoria"},
    {"pais": "Canadá",            "region": "América",  "nivel": 1, "emoji": "🇨🇦", "alerta": ""},
    {"pais": "Argentina",         "region": "América",  "nivel": 2, "emoji": "🇦🇷", "alerta": "Inestabilidad económica"},
    {"pais": "Chile",             "region": "América",  "nivel": 1, "emoji": "🇨🇱", "alerta": ""},
    {"pais": "Perú",              "region": "América",  "nivel": 2, "emoji": "🇵🇪", "alerta": "Inestabilidad política, altitud"},
    {"pais": "Brasil",            "region": "América",  "nivel": 2, "emoji": "🇧🇷", "alerta": "Alta criminalidad en favelas y grandes ciudades"},
    {"pais": "Colombia",          "region": "América",  "nivel": 3, "emoji": "🇨🇴", "alerta": "🟠 FARC disidentes, ELN — zonas fronterizas evitar"},
    {"pais": "México",            "region": "América",  "nivel": 3, "emoji": "🇲🇽", "alerta": "🟠 Guerrero, Michoacán, Tamaulipas — No recomendado"},
    {"pais": "Cuba",              "region": "América",  "nivel": 2, "emoji": "🇨🇺", "alerta": "Escasez básicos, inestabilidad económica"},
    {"pais": "Rep. Dominicana",   "region": "América",  "nivel": 2, "emoji": "🇩🇴", "alerta": "Criminalidad en zonas no turísticas"},
    {"pais": "Venezuela",         "region": "América",  "nivel": 4, "emoji": "🇻🇪", "alerta": "🔴 Crisis humanitaria, criminalidad extrema — No recomendado"},
    {"pais": "Haití",             "region": "América",  "nivel": 5, "emoji": "🇭🇹", "alerta": "⛔ Estado fallido, bandas armadas — No viajar"},
    {"pais": "Ecuador",           "region": "América",  "nivel": 3, "emoji": "🇪🇨", "alerta": "🟠 Violencia narco en alza — precaución extrema"},

    # ── OCEANÍA ───────────────────────────────────────────────────────────────
    {"pais": "Australia",         "region": "Oceanía",  "nivel": 1, "emoji": "🇦🇺", "alerta": "UV extremo, fauna peligrosa"},
    {"pais": "Nueva Zelanda",     "region": "Oceanía",  "nivel": 1, "emoji": "🇳🇿", "alerta": ""},
]

# ── Config visual por nivel ───────────────────────────────────────────────────
NIVEL_CONFIG = {
    1: {"label": "Sin riesgo especial", "color": "#00e676", "bg": "#1a3a2a", "icon": "🟢", "short": "SEGURO"},
    2: {"label": "Precaución",          "color": "#ffd600", "bg": "#2a2a1a", "icon": "🟡", "short": "PRECAUCIÓN"},
    3: {"label": "Alta precaución",     "color": "#ff9100", "bg": "#2a1a0a", "icon": "🟠", "short": "ALTA PRECAUCIÓN"},
    4: {"label": "No recomendado",      "color": "#ff1744", "bg": "#3a1a1a", "icon": "🔴", "short": "NO RECOMENDADO"},
    5: {"label": "Desaconsejado",       "color": "#d50000", "bg": "#2a0a0a", "icon": "⛔", "short": "DESACONSEJADO"},
}


def render():
    st.markdown("#### 🌐 Mapa de Riesgo Global MAEC")

    # ── KPIs semáforo ─────────────────────────────────────────────────────────
    conteos = {n: 0 for n in range(1, 6)}
    for p in RIESGO_GLOBAL:
        conteos[p["nivel"]] += 1

    total = len(RIESGO_GLOBAL)
    cols = st.columns(5)
    for i, (nivel, cfg) in enumerate(NIVEL_CONFIG.items()):
        n = conteos[nivel]
        pct = round(n / total * 100)
        with cols[i]:
            st.markdown(f"""
            <div style='background:{cfg["bg"]};border:1px solid {cfg["color"]};
                 border-radius:10px;padding:14px 10px;text-align:center'>
                <div style='font-size:1.6rem'>{cfg["icon"]}</div>
                <div style='color:{cfg["color"]};font-family:JetBrains Mono;
                     font-size:1.6rem;font-weight:700;line-height:1'>{n}</div>
                <div style='color:{cfg["color"]};font-size:9px;font-weight:700;
                     letter-spacing:1px;margin:4px 0'>{cfg["short"]}</div>
                <div style='color:#4a6080;font-size:10px'>{pct}% del total</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Barra de distribución visual ──────────────────────────────────────────
    st.markdown("<div style='margin:16px 0 4px;display:flex;height:8px;border-radius:4px;overflow:hidden'>", unsafe_allow_html=True)
    colores = ["#00e676", "#ffd600", "#ff9100", "#ff1744", "#d50000"]
    segmentos = ""
    for nivel in range(1, 6):
        pct = conteos[nivel] / total * 100
        segmentos += f"<div style='flex:{pct};background:{colores[nivel-1]}'></div>"
    st.markdown(f"<div style='display:flex;height:8px;border-radius:4px;overflow:hidden;margin:12px 0'>{segmentos}</div>", unsafe_allow_html=True)

    # ── Alertas críticas destacadas (nivel 4-5) ───────────────────────────────
    criticos = [p for p in RIESGO_GLOBAL if p["nivel"] >= 4]
    with st.expander(f"🚨 Países con alerta máxima — {len(criticos)} destinos nivel 4-5", expanded=True):
        c1, c2 = st.columns(2)
        for i, p in enumerate(criticos):
            cfg = NIVEL_CONFIG[p["nivel"]]
            with (c1 if i % 2 == 0 else c2):
                st.markdown(f"""
                <div style='background:{cfg["bg"]};border:1px solid {cfg["color"]};
                     border-left:4px solid {cfg["color"]};border-radius:8px;
                     padding:10px 14px;margin-bottom:8px'>
                    <div style='display:flex;justify-content:space-between;align-items:center'>
                        <span style='font-size:14px'>{p["emoji"]} <b style='color:#c8d8e8'>{p["pais"]}</b></span>
                        <span style='color:{cfg["color"]};font-size:10px;font-family:JetBrains Mono;
                              font-weight:700'>{cfg["icon"]} {cfg["short"]}</span>
                    </div>
                    <div style='color:#4a6080;font-size:11px;margin-top:4px;line-height:1.4'>
                        {p["alerta"] if p["alerta"] else "Sin alertas específicas adicionales"}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Filtros ───────────────────────────────────────────────────────────────
    col_f1, col_f2, col_f3 = st.columns([2, 2, 1])
    with col_f1:
        regiones = ["Todas"] + sorted(set(p["region"] for p in RIESGO_GLOBAL))
        region_f = st.selectbox("🌐 Región", regiones, key="rg_region")
    with col_f2:
        niveles_opts = {
            "Todos los niveles": list(range(1, 6)),
            "🟢 Solo seguros (nivel 1)": [1],
            "🟡 Precaución o menos (1-2)": [1, 2],
            "🟠 Alta precaución o menos (1-3)": [1, 2, 3],
            "🔴 Solo no recomendados (4-5)": [4, 5],
        }
        nivel_sel_label = st.selectbox("⚠️ Nivel de riesgo", list(niveles_opts.keys()), key="rg_nivel")
        niveles_filtro = niveles_opts[nivel_sel_label]
    with col_f3:
        busqueda = st.text_input("🔍 Buscar", placeholder="país...", key="rg_buscar")

    # Aplicar filtros
    datos = RIESGO_GLOBAL
    if region_f != "Todas":
        datos = [p for p in datos if p["region"] == region_f]
    datos = [p for p in datos if p["nivel"] in niveles_filtro]
    if busqueda:
        datos = [p for p in datos if busqueda.lower() in p["pais"].lower()]

    st.markdown(f"<div style='color:#4a6080;font-size:12px;margin-bottom:12px'>"
                f"Mostrando <b style='color:#c8d8e8'>{len(datos)}</b> países de {total} · "
                f"Fuente: MAEC · Revisión: {ULTIMA_ACTUALIZACION}</div>",
                unsafe_allow_html=True)

    # ── Tabla de países ───────────────────────────────────────────────────────
    for p in sorted(datos, key=lambda x: (x["nivel"], x["pais"])):
        cfg = NIVEL_CONFIG[p["nivel"]]
        url_maec = f"https://www.exteriores.gob.es/es/ServiciosAlCiudadano/Paginas/Detalle-recomendaciones-de-viaje.aspx?IdP={p['pais'].replace(' ','+')}"
        alerta_html = (
            f"<span style='color:#4a6080;font-size:11px'>· {p['alerta']}</span>"
            if p["alerta"] else ""
        )
        st.markdown(f"""
        <div style='background:#0d1a2a;border:1px solid #1e2d40;
             border-left:4px solid {cfg["color"]};border-radius:8px;
             padding:10px 16px;margin-bottom:6px;
             display:flex;justify-content:space-between;align-items:center'>
            <div style='flex:1'>
                <span style='font-size:14px'>{p["emoji"]}</span>
                <b style='color:#c8d8e8;font-size:13px;margin-left:8px'>{p["pais"]}</b>
                <span style='color:#4a6080;font-size:11px;margin-left:6px'>{p["region"]}</span>
                <span style='margin-left:10px'>{alerta_html}</span>
            </div>
            <div style='display:flex;align-items:center;gap:12px;flex-shrink:0'>
                <span style='background:{cfg["bg"]};color:{cfg["color"]};
                      border:1px solid {cfg["color"]};border-radius:12px;
                      padding:3px 10px;font-size:10px;font-family:JetBrains Mono;
                      font-weight:700;white-space:nowrap'>
                    {cfg["icon"]} {p["nivel"]}/5 · {cfg["short"]}
                </span>
                <a href='https://www.exteriores.gob.es' target='_blank'
                   style='color:#00d4aa;font-size:11px;text-decoration:none;
                   font-family:JetBrains Mono;white-space:nowrap'>
                    MAEC →
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Nota legal ────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style='margin-top:20px;padding:12px 16px;background:#0d1520;
         border:1px solid #1e2d40;border-radius:8px;font-size:11px;
         color:#4a6080;font-family:JetBrains Mono;line-height:1.8'>
        ℹ️ Datos basados en recomendaciones oficiales del
        <a href='https://www.exteriores.gob.es' target='_blank'
           style='color:#00d4aa;text-decoration:none'>
           Ministerio de Asuntos Exteriores de España (MAEC)
        </a>
        · Revisión: <b style='color:#c8d8e8'>{ULTIMA_ACTUALIZACION}</b>
        · Actualizar trimestralmente o ante cambios geopolíticos relevantes<br>
        ⚠️ Esta información es orientativa. Verifica siempre en
        <b style='color:#c8d8e8'>exteriores.gob.es</b> antes de viajar.
        TripOSINT no se responsabiliza de decisiones tomadas en base a estos datos.
    </div>
    """, unsafe_allow_html=True)
