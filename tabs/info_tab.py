"""
tabs/info_tab.py — Información general y contactos útiles
"""
import streamlit as st
from datetime import datetime


def render(pais: dict, pais_nombre: str):
    st.markdown(f"#### ℹ️ Información general — {pais_nombre}")

    # ── Ficha del país ────────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🏙️ Capital",       pais.get("capital", "N/D"))
    col2.metric("🗣️ Idioma",        pais.get("idioma_oficial", "N/D"))
    col3.metric("💱 Moneda",        f"{pais.get('moneda_nombre','N/D')} ({pais.get('moneda_codigo','N/D')})")
    col4.metric("🔌 Enchufe",       pais.get("enchufes", "N/D"))

    st.markdown("---")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### 📞 Contactos de emergencia")
        contactos = [
            ("🚨 Emergencias",         pais.get("telefono_emergencias", "112")),
            ("👮 Policía",             pais.get("telefono_policia", "N/D")),
            ("🏛️ Embajada España",     pais.get("telefono_embajada_es", "N/D")),
            ("🆘 Consulados ES (24h)", "+34 913 79 97 97"),
        ]
        for label, val in contactos:
            st.markdown(f"""
            <div style='background:#0d1a2a;border:1px solid #1e2d40;border-radius:6px;
                 padding:12px 16px;margin-bottom:8px;display:flex;justify-content:space-between;
                 align-items:center'>
                <span style='color:#c8d8e8;font-size:13px'>{label}</span>
                <span style='color:#00d4aa;font-family:JetBrains Mono;font-size:14px;
                      font-weight:700'>{val}</span>
            </div>
            """, unsafe_allow_html=True)

    with col_b:
        st.markdown("#### 🌐 Recursos online")
        url_maec = pais.get("url_maec", "https://www.exteriores.gob.es")
        url_oms  = pais.get("url_oms",  "https://www.who.int")

        recursos = [
            ("🏛️ Ficha MAEC",              url_maec),
            ("📝 Registro viajeros",        "https://registroviajeros.exteriores.gob.es"),
            ("🌍 OMS Perfil sanitario",     url_oms),
            ("✈️ IATA Travel Centre",       "https://www.iatatravelcentre.com"),
            ("💱 XE.com Divisas",           "https://www.xe.com"),
            ("📡 CDC Travel Health",        "https://wwwnc.cdc.gov/travel"),
        ]
        for nombre, url in recursos:
            st.markdown(f"- [{nombre}]({url})")

    # ── Notas del país ────────────────────────────────────────────────────────
    st.markdown("---")
    col_s, col_c = st.columns(2)
    with col_s:
        notas_salud = pais.get("notas_salud", "")
        if notas_salud:
            st.markdown("#### 🏥 Notas sanitarias")
            st.info(notas_salud)
    with col_c:
        notas_civicas = pais.get("notas_civicas", "")
        if notas_civicas:
            st.markdown("#### 🏛️ Notas cívicas")
            st.info(notas_civicas)

    # ── Prensa del país ───────────────────────────────────────────────────────
    diarios = pais.get("diarios", [])
    if diarios:
        st.markdown("---")
        st.markdown("#### 📰 Prensa local")
        for d in diarios:
            st.markdown(f"- [{d['nombre']}]({d['url']})")

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align:center;font-size:11px;color:#4a6080;font-family:JetBrains Mono'>
        TripOSINT v1.0 · mcasrom ·
        <a href='https://github.com/mcasrom/trip-osint'
           style='color:#00d4aa;text-decoration:none'>GitHub</a>
        · Datos de referencia · Verifica siempre en fuentes oficiales antes de viajar
        · {datetime.now().strftime("%d/%m/%Y %H:%M")}
    </div>
    """, unsafe_allow_html=True)
