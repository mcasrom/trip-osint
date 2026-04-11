"""
tabs/checklist_tab.py — Checklists interactivos de viaje
"""
import streamlit as st


CHECKLIST_VIAJE_BASE = [
    ("📄 Documentación", [
        "Pasaporte vigente (mínimo 6 meses tras regreso)",
        "DNI (copia)",
        "Visado (si requerido)",
        "Tarjeta sanitaria europea o seguro de viaje",
        "Billetes de avión (impresos o descargados offline)",
        "Reservas de hotel (confirmación impresa)",
        "Carnet de conducir internacional (si vas a conducir)",
        "Tarjetas bancarias (al menos 2 diferentes)",
        "Efectivo en moneda local (para llegada)",
        "Foto tamaño pasaporte (×2)",
    ]),
    ("🧳 Equipaje esencial", [
        "Adaptador de enchufes para el país de destino",
        "Cargador de móvil y banco de energía (powerbank)",
        "Candado para maleta o mochila",
        "Ropa adecuada al clima local",
        "Calzado cómodo para caminar",
        "Botiquín básico de viaje",
        "Medicación personal (+ extra por si acaso)",
        "Auriculares con cancelación de ruido (vuelos largos)",
        "Almohada de viaje cervical",
        "Bolsas de plástico reutilizables",
    ]),
    ("📱 Digital y conectividad", [
        "SIM local o eSIM contratada para destino",
        "VPN instalada y configurada (si el destino lo requiere)",
        "Mapas offline descargados (Google Maps / Maps.me)",
        "Apps de transporte local descargadas",
        "Traductor offline descargado (Google Translate)",
        "Seguro de viaje con teléfono de asistencia guardado",
        "Contactos de emergencia guardados en el móvil",
        "Fotos de documentos en la nube (Drive/iCloud cifrado)",
        "Notificación a banco de viaje al exterior",
        "Batería móvil cargada al 100%",
    ]),
    ("🔒 Seguridad personal", [
        "Riñonera o cinturón portadocumentos antirrobo",
        "Copia de documentos en lugar separado de los originales",
        "Registro de viaje en el MAEC completado",
        "Familiar o amigo con copia del itinerario",
        "Seguro de cancelación de viaje contratado",
        "Número de emergencias del destino guardado",
        "Número de la embajada española guardado",
        "Número de asistencia en viaje del seguro guardado",
    ]),
]

CHECKLIST_SALUD = [
    ("💉 Vacunas y profilaxis", [
        "Vacunas obligatorias del destino administradas (con antelación suficiente)",
        "Vacunas recomendadas valoradas con el médico",
        "Pauta antipalúdica iniciada si zona endémica",
        "Certificado internacional de vacunación (Carné amarillo) si requerido",
    ]),
    ("💊 Medicación", [
        "Medicación habitual con cantidad suficiente (+30% extra)",
        "Receta médica en inglés para medicación de viaje",
        "Informe médico resumido en inglés",
        "Autorización especial para medicamentos controlados (si aplica)",
        "Antihistamínico oral para alergias imprevistas",
        "Analgésico de rescate (ibuprofeno/paracetamol)",
        "Antidiarreico (loperamida) para urgencias",
        "Sales de rehidratación oral",
    ]),
    ("☀️ Prevención ambiental", [
        "Protector solar 50+ (y repuesto)",
        "Repelente de mosquitos con DEET 30% o Picaridina",
        "Gafas de sol con filtro UV",
        "Ropa de manga larga para zonas de mosquitos",
        "Pastillas potabilizadoras (si zonas remotas)",
        "Ropa térmica si destino con frío extremo",
    ]),
    ("🏥 Seguros y cobertura", [
        "Seguro médico de viaje con cobertura para el destino",
        "Teléfono de asistencia médica 24h guardado",
        "Cobertura para deportes de riesgo si los practicas",
        "Cobertura de evacuación y repatriación verificada",
        "Tarjeta sanitaria europea (si destino UE/EEE)",
    ]),
]


def _render_checklist_section(secciones: list, prefijo: str):
    """Renderiza una checklist con checkboxes interactivos."""
    completados = 0
    total = 0

    for titulo, items in secciones:
        st.markdown(f"**{titulo}**")
        for i, item in enumerate(items):
            key = f"{prefijo}_{titulo}_{i}"
            checked = st.checkbox(item, key=key)
            if checked:
                completados += 1
            total += 1
        st.markdown("")

    return completados, total


def render(pais: dict, pais_nombre: str, motivo: str):
    tab_viaje, tab_salud, tab_urls = st.tabs([
        "🧳 Checklist de viaje",
        "🏥 Checklist de salud",
        "🔗 URLs y teléfonos clave",
    ])

    # ── CHECKLIST VIAJE ───────────────────────────────────────────────────────
    with tab_viaje:
        st.markdown(f"#### ✅ Checklist de viaje — {pais_nombre} · {motivo}")
        st.markdown("""
        <div style='font-size:13px;color:#4a6080;margin-bottom:16px'>
        Marca cada punto conforme lo vayas completando. El progreso se guarda durante la sesión.
        </div>
        """, unsafe_allow_html=True)

        completados, total = _render_checklist_section(CHECKLIST_VIAJE_BASE, f"viaje_{pais_nombre}")

        # Barra de progreso
        pct = int(completados / total * 100) if total else 0
        color = "#00e676" if pct == 100 else ("#ffd600" if pct >= 50 else "#ff6b35")
        st.markdown(f"""
        <div style='margin-top:16px;background:#0d1a2a;border:1px solid #1e2d40;
             border-radius:8px;padding:16px'>
            <div style='display:flex;justify-content:space-between;margin-bottom:8px'>
                <span style='color:#4a6080;font-size:13px'>Progreso total</span>
                <span style='color:{color};font-family:JetBrains Mono;font-weight:700'>
                    {completados}/{total} — {pct}%
                </span>
            </div>
            <div style='background:#1e2d40;border-radius:4px;height:8px'>
                <div style='background:{color};width:{pct}%;height:8px;border-radius:4px;
                     transition:width 0.3s'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if pct == 100:
            st.balloons()
            st.success("🎉 ¡Checklist completa! Estás listo para volar.")

    # ── CHECKLIST SALUD ───────────────────────────────────────────────────────
    with tab_salud:
        st.markdown(f"#### 🏥 Checklist de salud — {pais_nombre}")

        # Mostrar vacunas específicas del país al inicio
        vacunas_obl = pais.get("vacunas_obligatorias", [])
        vacunas_rec = pais.get("vacunas_recomendadas", [])
        if vacunas_obl:
            st.error(f"🔴 **Vacunas OBLIGATORIAS para {pais_nombre}:** " + ", ".join(vacunas_obl))
        if vacunas_rec:
            st.warning(f"🟡 **Vacunas recomendadas para {pais_nombre}:** " + ", ".join(vacunas_rec))

        completados_s, total_s = _render_checklist_section(CHECKLIST_SALUD, f"salud_{pais_nombre}")
        pct_s = int(completados_s / total_s * 100) if total_s else 0
        color_s = "#00e676" if pct_s == 100 else ("#ffd600" if pct_s >= 50 else "#ff6b35")

        st.markdown(f"""
        <div style='margin-top:16px;background:#0d1a2a;border:1px solid #1e2d40;
             border-radius:8px;padding:16px'>
            <div style='display:flex;justify-content:space-between;margin-bottom:8px'>
                <span style='color:#4a6080;font-size:13px'>Salud — Progreso</span>
                <span style='color:{color_s};font-family:JetBrains Mono;font-weight:700'>
                    {completados_s}/{total_s} — {pct_s}%
                </span>
            </div>
            <div style='background:#1e2d40;border-radius:4px;height:8px'>
                <div style='background:{color_s};width:{pct_s}%;height:8px;border-radius:4px'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── URLs Y TELÉFONOS ──────────────────────────────────────────────────────
    with tab_urls:
        st.markdown(f"#### 🔗 URLs y teléfonos clave — {pais_nombre}")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**📞 Teléfonos de emergencia**")
            telefonos = [
                ("🚨 Emergencias en destino", pais.get("telefono_emergencias", "112")),
                ("👮 Policía en destino",     pais.get("telefono_policia", "N/D")),
                ("🏛️ Embajada España",        pais.get("telefono_embajada_es", "N/D")),
                ("🆘 Emergencias consulares ES", "+34 913 79 97 97"),
                ("🏥 Asistencia médica SOS Int.", "+34 91 590 9929"),
            ]
            for nombre, tel in telefonos:
                st.markdown(f"""
                <div style='background:#0d1a2a;border:1px solid #1e2d40;border-radius:6px;
                     padding:10px 14px;margin-bottom:6px;display:flex;justify-content:space-between'>
                    <span style='color:#c8d8e8;font-size:13px'>{nombre}</span>
                    <span style='color:#00d4aa;font-family:JetBrains Mono;font-size:13px;
                          font-weight:600'>{tel}</span>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            st.markdown("**🌐 URLs esenciales**")
            url_maec = pais.get("url_maec", "https://www.exteriores.gob.es")
            url_oms  = pais.get("url_oms", "https://www.who.int")
            urls = [
                ("🏛️ MAEC — Ficha país",          url_maec),
                ("📝 Registro viajeros MAEC",       "https://registroviajeros.exteriores.gob.es"),
                ("🌍 OMS — Perfil sanitario",       url_oms),
                ("🏥 Min. Sanidad viajeros",        "https://www.sanidad.gob.es/profesionales/saludPublica/sanidadExterior/viajeros/home.htm"),
                ("✈️ IATA Travel Centre",           "https://www.iatatravelcentre.com"),
                ("💱 XE.com — Divisas",             "https://www.xe.com"),
                ("🗺️ Google Maps offline",          "https://support.google.com/maps/answer/6291838"),
                ("📡 CDC Travel Health",            "https://wwwnc.cdc.gov/travel"),
            ]
            for nombre, url in urls:
                st.markdown(f"""
                <div style='background:#0d1a2a;border:1px solid #1e2d40;border-radius:6px;
                     padding:10px 14px;margin-bottom:6px'>
                    <a href='{url}' target='_blank'
                       style='color:#00d4aa;font-size:12px;text-decoration:none;
                       font-family:JetBrains Mono'>
                        {nombre} →
                    </a>
                </div>
                """, unsafe_allow_html=True)
