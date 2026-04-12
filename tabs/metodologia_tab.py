"""
tabs/metodologia_tab.py — Metodología, fuentes y transparencia
TripOSINT v2.0
"""
import streamlit as st
from datetime import datetime


def render():
    st.markdown("""
    <div style='background:#0d1a2a;border:1px solid #1e2d40;border-left:4px solid #00d4aa;
         border-radius:8px;padding:16px 20px;margin-bottom:20px'>
        <div style='font-family:JetBrains Mono;font-size:10px;color:#4a6080;
             letter-spacing:2px;text-transform:uppercase;margin-bottom:6px'>
            ▸ METODOLOGÍA · FUENTES · TRANSPARENCIA
        </div>
        <div style='font-size:1.1rem;font-weight:700;color:#00d4aa;font-family:JetBrains Mono'>
            Cómo funciona TripOSINT
        </div>
        <div style='font-size:12px;color:#4a6080;margin-top:4px'>
            Inteligencia abierta (OSINT) aplicada al viajero · sin algoritmos opacos · fuentes verificables
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Filosofía ─────────────────────────────────────────────────────────────
    with st.expander("🧭 Filosofía del proyecto", expanded=True):
        st.markdown("""
**TripOSINT** es un dashboard de inteligencia de viaje basado en **OSINT** (Open Source Intelligence):
toda la información proviene de **fuentes públicas, oficiales o verificadas**, sin trackers ni
datos comerciales de terceros.

El objetivo es darte una **fotografía real del destino** antes de viajar:
nivel de riesgo diplomático, situación sanitaria, tipo de cambio en tiempo real, prensa local
y todo lo que necesitas para tomar decisiones informadas — no solo reseñas de hoteles.

> *"Viaja con inteligencia, no con suerte."*
        """)

    # ── Fuentes por módulo ────────────────────────────────────────────────────
    st.markdown("""
    <div style='font-family:JetBrains Mono;font-size:11px;color:#00d4aa;
         letter-spacing:1px;text-transform:uppercase;margin:20px 0 10px'>
        ▸ FUENTES DE DATOS POR MÓDULO
    </div>
    """, unsafe_allow_html=True)

    fuentes = [
        {
            "tab": "🌐 Riesgo Global",
            "icon": "🌐",
            "fuente": "MAEC — Ministerio de Asuntos Exteriores de España",
            "url": "https://www.exteriores.gob.es/es/ServiciosAlCiudadano/Paginas/Recomendaciones-de-viaje.aspx",
            "tipo": "Base de datos curada (revisión trimestral)",
            "frecuencia": "Actualización manual cuando MAEC publica cambios",
            "notas": "Niveles 1–5 según clasificación oficial española. Se complementa con valoración de contexto geopolítico."
        },
        {
            "tab": "🚨 Alertas MAEC",
            "icon": "🚨",
            "fuente": "MAEC — Recomendaciones de viaje oficiales",
            "url": "https://www.exteriores.gob.es",
            "tipo": "Estática curada + scraping puntual",
            "frecuencia": "Revisión semanal / ante eventos relevantes",
            "notas": "Las alertas específicas se basan en los avisos publicados por el MAEC para cada país. Verifica siempre en la web oficial antes de viajar."
        },
        {
            "tab": "🌤️ Meteorología",
            "icon": "🌤️",
            "fuente": "Open-Meteo API (modelos NWP + ERA5) + Geocoding API Open-Meteo",
            "url": "https://open-meteo.com",
            "tipo": "API abierta · sin clave · tiempo real",
            "frecuencia": "Cada carga del dashboard (live, caché 1h)",
            "notas": "Pronóstico 7 días. Open-Meteo es gratuito para uso no comercial y no requiere registro. Precisión ±2°C típica en zonas bien cubiertas."
        },
        {
            "tab": "💱 Divisa & Cambio",
            "icon": "💱",
            "fuente": "ExchangeRate-API (free tier, base EUR) / Frankfurter BCE",
            "url": "https://www.frankfurter.app",
            "tipo": "API abierta · datos diarios BCE",
            "frecuencia": "Caché 1h · datos del cierre bancario europeo anterior",
            "notas": "Tipo de cambio de referencia BCE. No incluye comisiones bancarias ni de cambio en destino — añade un 2–5% al calcular tu presupuesto real."
        },
        {
            "tab": "📋 Requisitos entrada",
            "icon": "📋",
            "fuente": "IATA Travel Centre · embajadas · base curada MAEC",
            "url": "https://www.iata.org/en/services/travel-documents/",
            "tipo": "Base curada estática",
            "frecuencia": "Revisión mensual",
            "notas": "Requisitos de visado para ciudadanos españoles (pasaporte UE). Otras nacionalidades pueden diferir. Confirma siempre con la embajada del país destino."
        },
        {
            "tab": "🏥 Salud & OMS",
            "icon": "🏥",
            "fuente": "OMS (WHO) · Sanidad Exterior MSCBS · CDC Traveler's Health",
            "url": "https://www.who.int/travel-advice",
            "tipo": "Base curada con referencias vivas",
            "frecuencia": "Revisión mensual / ante alertas sanitarias activas",
            "notas": "Vacunas recomendadas según destino. Las recomendaciones son orientativas — consulta a tu médico o centro de vacunación internacional antes de viajar."
        },
        {
            "tab": "📰 Prensa local",
            "icon": "📰",
            "fuente": "RSS feeds de cabeceras locales y regionales (selección curada por región)",
            "url": "",
            "tipo": "RSS scraping · feedparser · live",
            "frecuencia": "Caché 15 minutos · últimas 48h de titulares",
            "notas": "Se muestran titulares de medios del país/región de destino para detectar situaciones de actualidad. La selección prioriza medios con RSS público estable. Fallback a feeds BBC/Reuters/Al Jazeera por región."
        },
        {
            "tab": "✅ Checklists",
            "icon": "✅",
            "fuente": "Elaboración propia · adaptada por motivo de viaje y características del país",
            "url": "",
            "tipo": "Lógica dinámica generada por perfil usuario",
            "frecuencia": "Estática — se actualiza con versiones del app",
            "notas": "Las listas varían según motivo (turismo, trabajo, salud...) y datos del país (enchufes, conducción, idioma, sanidad, nivel MAEC)."
        },
        {
            "tab": "ℹ️ Info & Contactos",
            "icon": "ℹ️",
            "fuente": "Embajadas · Policía local · Emergencias internacionales · base curada",
            "url": "",
            "tipo": "Base curada estática",
            "frecuencia": "Revisión mensual",
            "notas": "Teléfonos de emergencia, consulados y recursos de asistencia al viajero. Verifica que los números sigan activos antes de viajar."
        },
    ]

    for f in fuentes:
        with st.expander(f"{f['icon']} {f['tab']}"):
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown(f"**📡 Fuente:** {f['fuente']}")
                if f["url"]:
                    st.markdown(f"**🔗** [{f['url']}]({f['url']})")
                st.markdown(f"**🏷️ Tipo:** `{f['tipo']}`")
            with col2:
                st.markdown(f"**🔄 Frecuencia:** {f['frecuencia']}")
                st.markdown(f"**📝 Notas:** _{f['notas']}_")

    # ── Ciclo de actualización ────────────────────────────────────────────────
    st.markdown("""
    <div style='font-family:JetBrains Mono;font-size:11px;color:#00d4aa;
         letter-spacing:1px;text-transform:uppercase;margin:24px 0 10px'>
        ▸ CICLO DE ACTUALIZACIÓN
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    tarjetas = [
        ("⚡", "#00d4aa", "Live (caché 15–60 min)", "Meteorología · Tipo de cambio · RSS prensa", "Cada carga del dashboard"),
        ("📅", "#ffd600", "Semanal", "Alertas MAEC · Requisitos · Recomendaciones salud", "Revisión manual + cron semanal"),
        ("🗂️", "#ff9100", "Mensual / Por versión", "Base países · Checklists · Contactos · Vacunas", "Con cada nueva versión del app"),
    ]
    for col, (icon, color, titulo, items, sub) in zip([col1, col2, col3], tarjetas):
        with col:
            st.markdown(f"""
            <div style='background:#0d1a2a;border:1px solid #1e2d40;border-radius:8px;
                 padding:16px;text-align:center;height:140px'>
                <div style='font-size:1.5rem'>{icon}</div>
                <div style='font-family:JetBrains Mono;font-size:13px;color:{color};
                     font-weight:700;margin:6px 0 4px'>{titulo}</div>
                <div style='font-size:11px;color:#4a6080'>{items}</div>
                <div style='font-size:10px;color:#2a4060;margin-top:6px'>{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Stack técnico ─────────────────────────────────────────────────────────
    st.markdown("""
    <div style='font-family:JetBrains Mono;font-size:11px;color:#00d4aa;
         letter-spacing:1px;text-transform:uppercase;margin:24px 0 10px'>
        ▸ STACK TÉCNICO
    </div>
    """, unsafe_allow_html=True)

    with st.expander("🛠️ Stack técnico completo"):
        st.markdown("""
| Componente | Tecnología |
|---|---|
| Frontend | Streamlit 1.x |
| Backend | Python 3.11 |
| Meteorología | Open-Meteo API (open source, sin API key) |
| Tipo de cambio | ExchangeRate-API free / Frankfurter (BCE) |
| RSS parsing | feedparser |
| HTTP | requests |
| Despliegue local | Odroid C2 · DietPi · systemd / cron |
| Despliegue cloud | Streamlit Cloud (GitHub Actions) |
| Infraestructura | Auto-hospedado · sin cloud propietario |
        """)

    # ── Limitaciones ──────────────────────────────────────────────────────────
    st.markdown("""
    <div style='font-family:JetBrains Mono;font-size:11px;color:#00d4aa;
         letter-spacing:1px;text-transform:uppercase;margin:24px 0 10px'>
        ▸ LIMITACIONES Y AVISO LEGAL
    </div>
    """, unsafe_allow_html=True)

    st.warning("""
⚠️ **TripOSINT es una herramienta de referencia, no una fuente oficial.**

- Los datos se presentan con fines informativos. Antes de viajar, **verifica siempre en fuentes oficiales**: MAEC, embajada del país destino, OMS y compañía aérea.
- Los tipos de cambio son de referencia BCE — el cambio real en tu banco incluirá comisiones.
- Las recomendaciones sanitarias **no sustituyen la consulta médica**.
- El autor no se responsabiliza de decisiones tomadas exclusivamente en base a esta app.
    """)

    st.info("""
🔓 **Código abierto y auditable**

TripOSINT es software libre. Puedes revisar, modificar y contribuir en:
[github.com/mcasrom/trip-osint](https://github.com/mcasrom/trip-osint)

Sin trackers · Sin cookies · Sin publicidad · Sin datos de usuario almacenados.
    """)

    # ── Colaborar / Contribuir ────────────────────────────────────────────────
    st.markdown("""
    <div style='font-family:JetBrains Mono;font-size:11px;color:#00d4aa;
         letter-spacing:1px;text-transform:uppercase;margin:24px 0 10px'>
        ▸ COLABORAR
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
**🐛 Reportar errores o datos desactualizados**

Si detectas un nivel de riesgo incorrecto, un teléfono erróneo o cualquier dato
desactualizado, abre un issue en GitHub o escríbeme directamente.

[github.com/mcasrom/trip-osint/issues](https://github.com/mcasrom/trip-osint/issues)
        """)
    with col_b:
        st.markdown("""
**☕ Apoyar el proyecto**

TripOSINT es gratuito y sin publicidad. Si te resulta útil,
puedes invitarme a un café en Ko-fi:

[ko-fi.com/mcasrom](https://ko-fi.com/mcasrom)
        """)

    # ── Versión ───────────────────────────────────────────────────────────────
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M")
    st.markdown(f"""
    <div style='font-size:10px;color:#2a4060;font-family:JetBrains Mono;
         text-align:center;margin-top:28px;padding-top:12px;
         border-top:1px solid #1e2d40;line-height:2'>
        TripOSINT v2.0 · mcasrom · generado {ahora} ·
        <a href='https://github.com/mcasrom/trip-osint' target='_blank'
           style='color:#00d4aa;text-decoration:none'>github.com/mcasrom/trip-osint</a>
    </div>
    """, unsafe_allow_html=True)
