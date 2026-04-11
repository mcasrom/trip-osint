"""
tabs/maec_tab.py — Alertas y nivel de riesgo MAEC
"""
import streamlit as st
import requests
from datetime import datetime

RIESGO_INFO = {
    1: {
        "color": "#00e676", "bg": "#1a3a2a", "border": "#00e676",
        "label": "Sin riesgo especial",
        "desc": "El país no presenta riesgos especiales para los viajeros españoles. Se recomienda precaución general habitual.",
        "icon": "🟢",
    },
    2: {
        "color": "#ffd600", "bg": "#2a2a1a", "border": "#ffd600",
        "label": "Precaución",
        "desc": "Existen factores de riesgo que requieren precaución. Infórmate bien antes de viajar y toma medidas preventivas.",
        "icon": "🟡",
    },
    3: {
        "color": "#ff9100", "bg": "#2a1a0a", "border": "#ff9100",
        "label": "Alta precaución",
        "desc": "El país presenta riesgos significativos. Se recomienda valorar la necesidad del viaje y extremar la precaución.",
        "icon": "🟠",
    },
    4: {
        "color": "#ff1744", "bg": "#3a1a1a", "border": "#ff1744",
        "label": "Viaje no recomendado",
        "desc": "El MAEC desaconseja viajar a este país salvo causa de fuerza mayor. Riesgo elevado para la seguridad.",
        "icon": "🔴",
    },
    5: {
        "color": "#d50000", "bg": "#2a0a0a", "border": "#d50000",
        "label": "Viaje totalmente desaconsejado",
        "desc": "El MAEC desaconseja totalmente viajar. Situación de conflicto armado, crisis grave o riesgo extremo.",
        "icon": "⛔",
    },
}

CONSEJOS_POR_MOTIVO = {
    "Turismo": [
        "Registra tu viaje en el MAEC (registro de viajeros)",
        "Contrata seguro de viaje con asistencia en destino",
        "Guarda fotocopia del pasaporte separada del original",
        "Comparte tu itinerario con alguien de confianza",
    ],
    "Trabajo / Negocios": [
        "Verifica si necesitas visado de trabajo o de negocios",
        "Comprueba normativa fiscal local para trabajadores extranjeros",
        "Registra tu estancia en el consulado si supera 90 días",
        "Revisa tu seguro de salud cubre actividad profesional",
    ],
    "Familiar": [
        "Lleva documentación de menores si viajas con niños",
        "Verifica si necesitas autorización del otro progenitor",
        "Localiza hospitales y médicos de habla hispana en destino",
        "Registra tu viaje en el MAEC",
    ],
    "Estudios": [
        "Verifica visado de estudiante si estancia > 90 días",
        "Comprueba cobertura sanitaria para estudiantes",
        "Inscríbete en el consulado si estancia > 6 meses",
        "Revisa equivalencia de títulos universitarios",
    ],
    "Sanitario": [
        "Lleva informe médico traducido al idioma local",
        "Verifica cobertura de tu seguro para tratamiento en el exterior",
        "Localiza hospitales acreditados para tu tratamiento",
        "Lleva medicación suficiente + receta en inglés",
    ],
}


def render(pais: dict, pais_nombre: str, motivo: str):
    nivel = pais.get("nivel_riesgo_maec", 1)
    info = RIESGO_INFO.get(nivel, RIESGO_INFO[1])

    # ── Banner nivel de riesgo ────────────────────────────────────────────────
    st.markdown(f"""
    <div style='background:{info["bg"]};border:1px solid {info["border"]};
         border-left:5px solid {info["border"]};border-radius:10px;
         padding:20px 24px;margin-bottom:20px'>
        <div style='font-size:1.1rem;font-weight:700;color:{info["color"]};
             font-family:JetBrains Mono;margin-bottom:8px'>
            {info["icon"]} Nivel {nivel}/5 — {info["label"]}
        </div>
        <div style='color:#c8d8e8;font-size:14px;line-height:1.6'>
            {info["desc"]}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Columnas info + enlace MAEC ───────────────────────────────────────────
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("#### 📋 Recomendaciones generales MAEC")
        consejos = CONSEJOS_POR_MOTIVO.get(motivo, CONSEJOS_POR_MOTIVO["Turismo"])
        for c in consejos:
            st.markdown(f"- {c}")

        st.markdown("#### 🚨 Alertas activas")
        alertas = pais.get("alertas_maec", [])
        if alertas:
            for a in alertas:
                st.warning(a)
        else:
            st.success("No hay alertas específicas registradas para este destino.")

        requisitos_esp = pais.get("requisitos_especiales", [])
        if requisitos_esp:
            st.markdown("#### ⚠️ Requisitos especiales")
            for r in requisitos_esp:
                st.markdown(f"- ⚠️ {r}")

    with col2:
        st.markdown("#### 🔗 Recursos oficiales")
        url_maec = pais.get("url_maec", "https://www.exteriores.gob.es")
        st.markdown(f"""
        <div style='background:#0d1a2a;border:1px solid #1e2d40;
             border-radius:8px;padding:16px;margin-bottom:12px'>
            <div style='font-size:12px;color:#4a6080;margin-bottom:8px'>
                MINISTERIO DE ASUNTOS EXTERIORES
            </div>
            <a href='{url_maec}' target='_blank'
               style='color:#00d4aa;font-size:13px;text-decoration:none;
               font-family:JetBrains Mono'>
                🌐 Ficha país MAEC →
            </a>
        </div>
        <div style='background:#0d1a2a;border:1px solid #1e2d40;
             border-radius:8px;padding:16px;margin-bottom:12px'>
            <div style='font-size:12px;color:#4a6080;margin-bottom:8px'>
                REGISTRO DE VIAJEROS
            </div>
            <a href='https://registroviajeros.exteriores.gob.es' target='_blank'
               style='color:#00d4aa;font-size:13px;text-decoration:none;
               font-family:JetBrains Mono'>
                📝 Registrar mi viaje →
            </a>
        </div>
        <div style='background:#0d1a2a;border:1px solid #1e2d40;
             border-radius:8px;padding:16px'>
            <div style='font-size:12px;color:#4a6080;margin-bottom:8px'>
                EMERGENCIAS CONSULARES
            </div>
            <div style='color:#c8d8e8;font-size:13px;font-family:JetBrains Mono'>
                📞 +34 913 79 97 97
            </div>
            <div style='color:#4a6080;font-size:11px;margin-top:4px'>
                24h · Emergencias consulares
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Teléfonos de emergencia en destino ────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 📞 Teléfonos de emergencia en destino")
    c1, c2, c3 = st.columns(3)
    c1.metric("🚨 Emergencias", pais.get("telefono_emergencias", "112"))
    c2.metric("👮 Policía", pais.get("telefono_policia", "N/D"))
    c3.metric("🏛️ Embajada España", pais.get("telefono_embajada_es", "N/D"))

    # ── Nota de actualización ─────────────────────────────────────────────────
    st.markdown(f"""
    <div style='margin-top:16px;font-size:11px;color:#4a6080;
         font-family:JetBrains Mono;text-align:right'>
        ℹ️ Datos de referencia · Verifica siempre en <b style='color:#00d4aa'>exteriores.gob.es</b>
        antes de viajar · {datetime.now().strftime("%d/%m/%Y")}
    </div>
    """, unsafe_allow_html=True)
