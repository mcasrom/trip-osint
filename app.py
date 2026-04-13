"""
TripOSINT — Dashboard de inteligencia para viajeros
Versión: 2.0
Autor: mcasrom
"""

import streamlit as st
from config.paises import PAISES

st.set_page_config(
    page_title="TripOSINT — Inteligencia para viajeros",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Estilos ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0a0f1a;
    color: #c8d8e8;
}
.stApp { background-color: #0a0f1a; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1520 0%, #0a1018 100%);
    border-right: 1px solid #1e2d40;
}
.stTabs [data-baseweb="tab-list"] {
    background: #0d1520;
    border-bottom: 1px solid #1e2d40;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    color: #4a6080;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    padding: 8px 14px;
}
.stTabs [aria-selected="true"] {
    color: #00d4aa !important;
    border-bottom: 2px solid #00d4aa !important;
    background: transparent !important;
}
[data-testid="stMetric"] {
    background: #0d1a2a;
    border: 1px solid #1e2d40;
    border-radius: 8px;
    padding: 12px 16px;
}
[data-testid="stMetricLabel"] { color: #4a6080 !important; font-size: 12px; }
[data-testid="stMetricValue"] { color: #c8d8e8 !important; font-size: 1.4rem; }
[data-testid="stExpander"] {
    background: #0d1a2a;
    border: 1px solid #1e2d40;
    border-radius: 8px;
}
.stAlert { border-radius: 8px; }
.trip-header {
    background: linear-gradient(135deg, #0d1a2a 0%, #0a1018 100%);
    border: 1px solid #1e2d40;
    border-left: 4px solid #00d4aa;
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 20px;
}
.trip-header h1 {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.4rem;
    color: #00d4aa;
    margin: 0 0 4px 0;
}
.trip-header p { color: #4a6080; font-size: 13px; margin: 0; }
[data-testid="stAppViewContainer"] > .main > div:first-child { padding-top: 0.5rem !important; }
div.block-container { padding-top: 1rem !important; }
.risk-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    font-weight: 600;
}
.risk-1 { background: #1a3a2a; color: #00e676; border: 1px solid #00e676; }
.risk-2 { background: #2a2a1a; color: #ffd600; border: 1px solid #ffd600; }
.risk-3 { background: #3a2a1a; color: #ff9100; border: 1px solid #ff9100; }
.risk-4 { background: #3a1a1a; color: #ff1744; border: 1px solid #ff1744; }
.risk-5 { background: #2a0a0a; color: #d50000; border: 1px solid #d50000; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:16px 0 8px'>
        <div style='font-size:2rem'>🌍</div>
        <div style='font-family:JetBrains Mono;font-size:14px;color:#00d4aa;font-weight:700'>
            TRIP<span style='color:#c8d8e8'>OSINT</span>
        </div>
        <div style='font-size:11px;color:#4a6080;margin-top:4px'>
            Inteligencia para viajeros v2.0
        </div>
    </div>
    <hr style='border-color:#1e2d40;margin:8px 0 16px'>
    """, unsafe_allow_html=True)

    # ── Share URL: leer ?pais= de la URL ────────────────────────────────
    _qp = st.query_params.get("pais", "")
    regiones = sorted(set(v["region"] for v in PAISES.values()))
    region_sel = st.selectbox("🌐 Región", ["Todas"] + regiones, key="region_sel")

    paises_filtrados = {
        k: v for k, v in sorted(PAISES.items())
        if region_sel == "Todas" or v["region"] == region_sel
    }

    _lista_paises = list(paises_filtrados.keys())
    _idx = _lista_paises.index(_qp) if _qp in _lista_paises else 0
    pais_nombre = st.selectbox("✈ País de destino", _lista_paises, index=_idx, key="pais_sel")
    pais = paises_filtrados[pais_nombre]

    st.markdown("<hr style='border-color:#1e2d40;margin:16px 0'>", unsafe_allow_html=True)

    motivo = st.selectbox(
        "🎯 Motivo del viaje",
        ["Turismo", "Trabajo / Negocios", "Familiar", "Estudios", "Sanitario"],
        key="motivo_sel"
    )

    # Mini-ficha en sidebar
    nivel_r = pais.get("nivel_riesgo_maec", 1)
    colores_r = {1:"#00e676", 2:"#ffd600", 3:"#ff9100", 4:"#ff1744", 5:"#d50000"}
    color_r = colores_r.get(nivel_r, "#c8d8e8")
    # ── Botón compartir ──────────────────────────────────────────────
    share_url = 'https://triposint.streamlit.app/?pais=' + pais_nombre
    st.markdown(
        '<div style="margin-bottom:12px;text-align:center">'
        '<a href="' + share_url + '" target="_blank" '
        'style="display:inline-block;background:#1e2d40;color:#00d4aa;'
        'font-family:JetBrains Mono;font-size:11px;font-weight:700;'
        'padding:7px 14px;border-radius:20px;text-decoration:none;'
        'border:1px solid #00d4aa;letter-spacing:0.5px">'
        '🔗 Compartir este destino</a></div>',
        unsafe_allow_html=True
    )
    st.markdown(f"""
    <hr style='border-color:#1e2d40;margin:16px 0'>
    <div style='background:#0d1a2a;border:1px solid #1e2d40;border-radius:8px;padding:12px'>
        <div style='font-size:11px;color:#4a6080;margin-bottom:8px;font-family:JetBrains Mono'>
            RESUMEN DESTINO
        </div>
        <div style='font-size:12px;color:#c8d8e8;line-height:1.8'>
            🏙️ {pais.get('capital','N/D')}<br>
            🗣️ {pais.get('idioma','N/D')}<br>
            🔌 {pais.get('enchufes','N/D')}<br>
            💱 {pais.get('moneda_codigo','N/D')} · {pais.get('voltaje','N/D')}<br>
            🚗 {pais.get('conduccion_lado','N/D')}<br>
            <span style='color:{color_r};font-weight:700'>⚠️ Riesgo MAEC: {nivel_r}/5</span>
        </div>
    </div>
    <div style='margin-top:16px;text-align:center'>
        <a href='https://ko-fi.com/mcasrom' target='_blank'
           style='display:inline-block;background:#FF5E5B;color:#fff;
           font-family:JetBrains Mono;font-size:12px;font-weight:700;
           padding:8px 16px;border-radius:20px;text-decoration:none;

           letter-spacing:0.5px'>
            ☕ Invítame a un café
        </a>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:10px;color:#4a6080;font-family:JetBrains Mono;
         text-align:center;margin-top:12px;line-height:1.8'>
        <a href='https://github.com/mcasrom/trip-osint' target='_blank'
           style='color:#00d4aa;text-decoration:none'>⌥ GitHub</a>
        &nbsp;·&nbsp;
        <a href='mailto:mybloggingnotes@gmail.com'
           style='color:#4a6080;text-decoration:none'>✉ Contacto</a><br>
        © 2026 M. Castillo (mcasrom)
    </div>
    """, unsafe_allow_html=True)

# ── Header principal ──────────────────────────────────────────────────────────
nivel_riesgo = pais.get("nivel_riesgo_maec", 1)
riesgo_labels = {
    1: ("🟢", "Sin riesgo especial"),
    2: ("🟡", "Precaución"),
    3: ("🟠", "Alta precaución"),
    4: ("🔴", "No recomendado"),
    5: ("⛔", "Desaconsejado totalmente"),
}
emoji_r, label_r = riesgo_labels.get(nivel_riesgo, ("⚪", "Sin datos"))

st.markdown(f"""
<div style='background:linear-gradient(135deg,#0d1a2a 0%,#0a1018 100%);
     border:1px solid #1e2d40;border-left:4px solid #00d4aa;
     border-radius:8px;padding:20px 24px;margin-bottom:20px'>

  <div style='font-family:JetBrains Mono;font-size:10px;color:#4a6080;
       letter-spacing:2px;text-transform:uppercase;margin-bottom:6px'>
    ▸ INTELIGENCIA DE VIAJE · OSINT · FUENTES OFICIALES
  </div>

  <div style='font-family:JetBrains Mono;font-size:1.4rem;font-weight:700;
       color:#00d4aa;line-height:1.2;margin-bottom:8px'>
    Viaja con inteligencia, no con suerte
    <span style='font-size:0.9rem;color:#c8d8e8;font-weight:400'>&nbsp;— {pais['emoji']} {pais_nombre}</span>
  </div>

  <div style='margin-bottom:10px'>
    <span class='risk-badge risk-{nivel_riesgo}'>{emoji_r} MAEC Nivel {nivel_riesgo}/5 · {label_r}</span>
  </div>

  <div style='font-size:12px;color:#4a6080;line-height:2'>
    🏙️ <span style='color:#c8d8e8'>{pais['capital']}</span>
    &nbsp;·&nbsp; 🌐 {pais['region']}
    &nbsp;·&nbsp; 💱 {pais['moneda_nombre']} ({pais['moneda_codigo']})
    &nbsp;·&nbsp; 🗣️ {pais.get('idioma','N/D')}
    &nbsp;·&nbsp; 🔌 {pais.get('enchufes','N/D')} · {pais.get('voltaje','N/D')}
    &nbsp;·&nbsp; 🚗 {pais.get('conduccion_lado','Derecha')}
    &nbsp;·&nbsp; 🎯 <span style='color:#00d4aa'>{motivo}</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "🌐 Riesgo Global",
    "🚨 Alertas MAEC",
    "🌤️ Meteorología",
    "💱 Divisa & Cambio",
    "📋 Requisitos entrada",
    "🏥 Salud & OMS",
    "📰 Prensa local",
    "✅ Checklists",
    "ℹ Info & Contactos",
    "🔬 Metodología & Fuentes",
    "📄 Export PDF",
])

tab_riesgo, tab_maec, tab_meteo, tab_divisa, tab_requisitos, tab_salud, tab_prensa, tab_checklist, tab_info, tab_metodologia, tab_export = tabs

with tab_riesgo:
    from tabs.riesgo_global_tab import render as render_riesgo
    render_riesgo()

with tab_maec:
    from tabs.maec_tab import render as render_maec
    render_maec(pais, pais_nombre, motivo)

with tab_meteo:
    from tabs.meteo_tab import render as render_meteo
    render_meteo(pais, pais_nombre)

with tab_divisa:
    from tabs.divisa_tab import render as render_divisa
    render_divisa(pais, pais_nombre)

with tab_requisitos:
    from tabs.requisitos_tab import render as render_requisitos
    render_requisitos(pais, pais_nombre, motivo)

with tab_salud:
    from tabs.salud_tab import render as render_salud
    render_salud(pais, pais_nombre)

with tab_prensa:
    from tabs.prensa_tab import render as render_prensa
    render_prensa(pais, pais_nombre)

with tab_checklist:
    from tabs.checklist_tab import render as render_checklist
    render_checklist(pais, pais_nombre, motivo)

with tab_info:
    from tabs.info_tab import render as render_info
    render_info(pais, pais_nombre)

with tab_metodologia:
    from tabs.metodologia_tab import render as render_metodologia
    render_metodologia()

with tab_export:
    from tabs.export_tab import render as render_export
    render_export(pais, pais_nombre, motivo)

# ── Footer global ─────────────────────────────────────────────────────────────
st.markdown("""
<hr style='border-color:#1e2d40;margin:32px 0 16px'>
<div style='display:flex;justify-content:space-between;align-items:center;
     flex-wrap:wrap;gap:12px;padding-bottom:16px'>
    <div style='font-size:11px;color:#4a6080;font-family:JetBrains Mono;line-height:1.8'>
        © 2026 <b style='color:#c8d8e8'>M. Castillo</b> (mcasrom) &nbsp;·&nbsp;
        <a href='mailto:mybloggingnotes@gmail.com'
           style='color:#4a6080;text-decoration:none'>mybloggingnotes@gmail.com</a><br>
        TripOSINT v2.0 · Datos de referencia ·
        <a href='https://github.com/mcasrom/trip-osint' target='_blank'
           style='color:#00d4aa;text-decoration:none'>github.com/mcasrom/trip-osint</a>
        · Verifica siempre en fuentes oficiales antes de viajar
    </div>
    <a href='https://ko-fi.com/mcasrom' target='_blank'
       style='display:inline-flex;align-items:center;gap:8px;
       background:#FF5E5B;color:#fff;font-family:JetBrains Mono;
       font-size:12px;font-weight:700;padding:8px 20px;border-radius:20px;
       text-decoration:none;letter-spacing:0.5px;white-space:nowrap'>
        ☕ Apoya el proyecto en Ko-fi
    </a>
</div>
""", unsafe_allow_html=True)
