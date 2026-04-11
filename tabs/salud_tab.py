"""
tabs/salud_tab.py — Salud y recomendaciones OMS
"""
import streamlit as st


def render(pais: dict, pais_nombre: str):
    vacunas_rec  = pais.get("vacunas_recomendadas", [])
    vacunas_obl  = pais.get("vacunas_obligatorias", [])
    notas_salud  = pais.get("notas_salud", "")
    url_oms      = pais.get("url_oms", "https://www.who.int")

    # ── Vacunas ───────────────────────────────────────────────────────────────
    st.markdown("#### 💉 Vacunas")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**🔴 Obligatorias**")
        if vacunas_obl:
            for v in vacunas_obl:
                st.error(f"💉 {v}")
        else:
            st.success("No se requieren vacunas obligatorias para ciudadanos españoles.")

    with c2:
        st.markdown("**🟡 Recomendadas**")
        if vacunas_rec:
            for v in vacunas_rec:
                st.warning(f"💉 {v}")
        else:
            st.success("No hay vacunas especialmente recomendadas para este destino.")

    # ── Notas sanitarias del país ─────────────────────────────────────────────
    if notas_salud:
        st.markdown("---")
        st.markdown("#### 🏥 Situación sanitaria")
        st.info(f"ℹ️ {notas_salud}")

    # ── Recursos OMS y Min. Sanidad ───────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 🌐 Recursos sanitarios oficiales")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown(f"""
        <div style='background:#0d1a2a;border:1px solid #1e2d40;border-radius:8px;padding:16px'>
            <div style='font-size:11px;color:#4a6080;margin-bottom:8px'>OMS / WHO</div>
            <a href='{url_oms}' target='_blank'
               style='color:#00d4aa;font-size:13px;font-family:JetBrains Mono;text-decoration:none'>
                🌍 Perfil país OMS →
            </a>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown("""
        <div style='background:#0d1a2a;border:1px solid #1e2d40;border-radius:8px;padding:16px'>
            <div style='font-size:11px;color:#4a6080;margin-bottom:8px'>MIN. SANIDAD ESPAÑA</div>
            <a href='https://www.sanidad.gob.es/profesionales/saludPublica/sanidadExterior/viajeros/home.htm'
               target='_blank'
               style='color:#00d4aa;font-size:13px;font-family:JetBrains Mono;text-decoration:none'>
                🏥 Sanidad para viajeros →
            </a>
        </div>
        """, unsafe_allow_html=True)
    with col_c:
        st.markdown("""
        <div style='background:#0d1a2a;border:1px solid #1e2d40;border-radius:8px;padding:16px'>
            <div style='font-size:11px;color:#4a6080;margin-bottom:8px'>CDC TRAVEL HEALTH</div>
            <a href='https://wwwnc.cdc.gov/travel' target='_blank'
               style='color:#00d4aa;font-size:13px;font-family:JetBrains Mono;text-decoration:none'>
                🔬 CDC Viajeros →
            </a>
        </div>
        """, unsafe_allow_html=True)

    # ── Botiquín recomendado ──────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 🧳 Botiquín de viaje recomendado")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        **🩹 Básico**
        - Analgésicos (ibuprofeno, paracetamol)
        - Antidiarreico (loperamida)
        - Antihistamínico oral
        - Apósitos y tiritas
        - Termómetro digital
        - Tijeras y pinzas
        """)
    with col2:
        st.markdown("""
        **☀️ Prevención**
        - Protector solar 50+
        - Repelente de mosquitos (DEET 30%+)
        - Sales de rehidratación oral
        - Pastillas potabilizadoras
        - Protección labial
        - Gafas de sol
        """)
    with col3:
        st.markdown("""
        **💊 Prescripción**
        - Tu medicación habitual (+ cantidad extra)
        - Receta médica en inglés
        - Informe médico traducido
        - Antipalúdicos (si zona de riesgo)
        - Antibiótico de amplio espectro (bajo prescripción)
        """)

    # ── Tarjeta sanitaria europea ─────────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 💳 Tarjeta Sanitaria Europea (TSE)")
    nivel_riesgo = pais.get("nivel_riesgo_maec", 1)
    region = pais.get("region", "")

    if region == "Europa" and pais.get("moneda_codigo") == "EUR" or region == "Europa":
        st.success("""
        ✅ La TSE es válida en este destino (país UE/EEE).
        Solicítala gratis en tu centro de salud o en [imss.gob.es](https://www.imss.es) antes de viajar.
        Cubre atención médica de urgencia en la misma condición que los ciudadanos locales.
        """)
    else:
        st.warning("""
        ⚠️ La TSE **no cubre** este destino. Contrata un seguro de viaje privado con
        cobertura médica mínima de 30.000€ y repatriación. Compara en:
        [IATI](https://www.iatiseguros.com) · [Intermundial](https://www.intermundial.es)
        · [Chapka](https://www.chapkadirect.es)
        """)

    # ── Notas cívicas ─────────────────────────────────────────────────────────
    notas_civicas = pais.get("notas_civicas", "")
    if notas_civicas:
        st.markdown("---")
        st.markdown("#### 🏛️ Normas cívicas y culturales")
        st.info(f"ℹ️ {notas_civicas}")
