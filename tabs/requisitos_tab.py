"""
tabs/requisitos_tab.py — Requisitos de entrada al país
"""
import streamlit as st
from datetime import datetime


def render(pais: dict, pais_nombre: str, motivo: str):
    visado      = pais.get("visado_es", False)
    pasaporte   = pais.get("pasaporte_requerido", True)
    dni_valido  = pais.get("dni_valido", False)
    requisitos  = pais.get("requisitos_especiales", [])

    # ── Semáforo de documentación ─────────────────────────────────────────────
    st.markdown("#### 📄 Documentación necesaria")
    c1, c2, c3 = st.columns(3)

    with c1:
        color_vis = "#ff1744" if visado else "#00e676"
        label_vis = "REQUERIDO" if visado else "NO requerido"
        st.markdown(f"""
        <div style='background:#0d1a2a;border:1px solid {color_vis};border-radius:10px;
             padding:20px;text-align:center'>
            <div style='font-size:2rem'>{"🔴" if visado else "🟢"}</div>
            <div style='color:{color_vis};font-weight:700;font-family:JetBrains Mono;
                 margin:8px 0 4px;font-size:14px'>VISADO</div>
            <div style='color:#c8d8e8;font-size:13px'>{label_vis}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        color_pas = "#00e676" if pasaporte else "#ffd600"
        label_pas = "Obligatorio" if pasaporte else "No necesario"
        st.markdown(f"""
        <div style='background:#0d1a2a;border:1px solid {color_pas};border-radius:10px;
             padding:20px;text-align:center'>
            <div style='font-size:2rem'>{"🛂" if pasaporte else "✅"}</div>
            <div style='color:{color_pas};font-weight:700;font-family:JetBrains Mono;
                 margin:8px 0 4px;font-size:14px'>PASAPORTE</div>
            <div style='color:#c8d8e8;font-size:13px'>{label_pas}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        color_dni = "#00e676" if dni_valido else "#ff1744"
        label_dni = "Válido como viajero" if dni_valido else "NO válido"
        st.markdown(f"""
        <div style='background:#0d1a2a;border:1px solid {color_dni};border-radius:10px;
             padding:20px;text-align:center'>
            <div style='font-size:2rem'>{"🪪" if dni_valido else "❌"}</div>
            <div style='color:{color_dni};font-weight:700;font-family:JetBrains Mono;
                 margin:8px 0 4px;font-size:14px'>DNI ESPAÑOL</div>
            <div style='color:#c8d8e8;font-size:13px'>{label_dni}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Requisitos especiales ─────────────────────────────────────────────────
    if requisitos:
        st.markdown("---")
        st.markdown("#### ⚠️ Requisitos especiales")
        for r in requisitos:
            st.warning(f"⚠️ {r}")

    # ── Info por motivo de viaje ──────────────────────────────────────────────
    st.markdown("---")
    st.markdown(f"#### 🎯 Requisitos específicos — {motivo}")

    info_motivo = {
        "Turismo": {
            "items": [
                "Pasaporte o DNI con validez mínima de 6 meses tras la fecha de regreso",
                "Billete de regreso o itinerario de vuelo",
                "Seguro de viaje con cobertura médica mínima 30.000€ (recomendado)",
                "Reserva de alojamiento (algunos países la exigen en frontera)",
                "Medios económicos suficientes (varía por país)",
            ],
            "links": [
                ("IATA Travel Centre", "https://www.iatatravelcentre.com"),
                ("Timatic (requisitos entrada)", "https://www.timaticweb2.com"),
            ]
        },
        "Trabajo / Negocios": {
            "items": [
                "Visado de negocios puede ser necesario aunque el turístico no lo sea",
                "Carta de invitación de empresa local (muchos países la exigen)",
                "Documentación mercantil y contratos en algunos destinos",
                "Permiso de trabajo si la actividad genera ingresos locales",
                "Seguro de responsabilidad civil profesional recomendado",
            ],
            "links": [
                ("ICEX — Exportar", "https://www.icex.es"),
                ("Cámara de Comercio", "https://www.camara.es"),
            ]
        },
        "Familiar": {
            "items": [
                "Autorización del otro progenitor si menor viaja con uno solo",
                "Partida de nacimiento del menor (apostillada)",
                "Documentación de menores debe coincidir exactamente con tutores",
                "Algunos países exigen que menores tengan pasaporte propio",
                "Certificado de matrimonio si apellidos difieren (algunos países)",
            ],
            "links": [
                ("Min. Asuntos Exteriores — menores", "https://www.exteriores.gob.es"),
                ("Apostilla — Min. Justicia", "https://www.mjusticia.gob.es"),
            ]
        },
        "Estudios": {
            "items": [
                "Visado de estudiante si estancia supera 90 días (en la mayoría de países)",
                "Carta de aceptación del centro educativo",
                "Prueba de medios económicos suficientes",
                "Seguro médico con cobertura en destino",
                "Inscripción consular si estancia > 6 meses",
            ],
            "links": [
                ("Erasmus+ (UE)", "https://erasmus-plus.ec.europa.eu"),
                ("Becas MAEC-AECID", "https://www.aecid.es"),
            ]
        },
        "Sanitario": {
            "items": [
                "Visado médico en algunos países (China, India, etc.)",
                "Informe médico oficial con diagnóstico y tratamiento",
                "Receta médica en inglés y/o idioma local para medicamentos",
                "Autorización para transportar medicamentos especiales (opiáceos, etc.)",
                "Seguro médico internacional con cobertura específica del tratamiento",
            ],
            "links": [
                ("SEMFYC — Viajeros", "https://www.semfyc.es"),
                ("Min. Sanidad — Viajes", "https://www.sanidad.gob.es"),
            ]
        },
    }

    info = info_motivo.get(motivo, info_motivo["Turismo"])
    col_req, col_links = st.columns([3, 1])

    with col_req:
        for item in info["items"]:
            st.markdown(f"- {item}")

    with col_links:
        st.markdown("**🔗 Recursos**")
        for nombre, url in info["links"]:
            st.markdown(f"[{nombre}]({url})")

    # ── Documentos recomendados a llevar ─────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 📁 Documentos a llevar siempre")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        **Originales:**
        - Pasaporte / DNI vigente
        - Tarjeta sanitaria europea (si aplica)
        - Seguro de viaje (póliza + teléfono asistencia)
        - Tarjetas bancarias
        - Reservas de vuelo y hotel (impreso o descargado offline)
        """)
    with col_b:
        st.markdown("""
        **Copias (separadas de los originales):**
        - Fotocopia de pasaporte/DNI
        - Foto tamaño pasaporte (×2)
        - Copia del seguro de viaje
        - Contactos de emergencia escritos en papel
        - Dirección del alojamiento en idioma local
        """)

    # ── Enchufes y voltaje ────────────────────────────────────────────────────
    st.markdown("---")
    c_enc, c_vol, c_idm = st.columns(3)
    c_enc.metric("🔌 Enchufe", pais.get("enchufes", "N/D"))
    c_vol.metric("⚡ Voltaje", pais.get("voltaje", "N/D"))
    c_idm.metric("🗣️ Idioma oficial", pais.get("idioma_oficial", "N/D"))
