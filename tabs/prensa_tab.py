"""
tabs/prensa_tab.py — Prensa local en tiempo real vía RSS
Usa feedparser para parsear feeds RSS de medios locales
"""
import streamlit as st
import requests
from datetime import datetime

try:
    import feedparser
    HAS_FEEDPARSER = True
except ImportError:
    HAS_FEEDPARSER = False

# Feeds RSS globales de respaldo por región
FEEDS_REGION = {
    "Europa": [
        {"nombre": "BBC Europe", "url": "http://feeds.bbci.co.uk/news/world/europe/rss.xml", "idioma": "EN"},
        {"nombre": "Euronews", "url": "https://feeds.feedburner.com/euronews/es/news", "idioma": "ES"},
        {"nombre": "El País Internacional", "url": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/internacional/portada", "idioma": "ES"},
    ],
    "América": [
        {"nombre": "BBC América", "url": "http://feeds.bbci.co.uk/news/world/latin_america/rss.xml", "idioma": "EN"},
        {"nombre": "El País América", "url": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/america/portada", "idioma": "ES"},
        {"nombre": "Reuters Americas", "url": "https://feeds.reuters.com/reuters/americasNews", "idioma": "EN"},
    ],
    "Asia": [
        {"nombre": "BBC Asia", "url": "http://feeds.bbci.co.uk/news/world/asia/rss.xml", "idioma": "EN"},
        {"nombre": "Al Jazeera Asia", "url": "https://www.aljazeera.com/xml/rss/all.xml", "idioma": "EN"},
        {"nombre": "Reuters Asia", "url": "https://feeds.reuters.com/reuters/asiaNews", "idioma": "EN"},
    ],
    "África": [
        {"nombre": "BBC Africa", "url": "http://feeds.bbci.co.uk/news/world/africa/rss.xml", "idioma": "EN"},
        {"nombre": "Al Jazeera", "url": "https://www.aljazeera.com/xml/rss/all.xml", "idioma": "EN"},
        {"nombre": "Reuters Africa", "url": "https://feeds.reuters.com/reuters/africaNews", "idioma": "EN"},
    ],
    "Oceanía": [
        {"nombre": "ABC News Australia", "url": "https://www.abc.net.au/news/feed/51120/rss.xml", "idioma": "EN"},
        {"nombre": "BBC World", "url": "http://feeds.bbci.co.uk/news/world/rss.xml", "idioma": "EN"},
    ],
}

# Feed de seguridad global como siempre útil
FEEDS_SEGURIDAD = [
    {"nombre": "MAEC Recomendaciones", "url": "https://www.exteriores.gob.es/rss/recomendaciones.aspx", "idioma": "ES"},
    {"nombre": "OSAC (US Dept State)", "url": "https://www.osac.gov/Content/RssView/7", "idioma": "EN"},
]


@st.cache_data(ttl=900)  # 15 minutos
def _fetch_feed(url: str, max_items: int = 6):
    """Parsea un feed RSS y devuelve lista de artículos."""
    if not HAS_FEEDPARSER:
        return [], "feedparser no instalado"
    try:
        headers = {"User-Agent": "TripOSINT/1.0 (travel intelligence dashboard)"}
        response = requests.get(url, timeout=8, headers=headers)
        feed = feedparser.parse(response.content)
        items = []
        for entry in feed.entries[:max_items]:
            titulo  = entry.get("title", "Sin título")
            link    = entry.get("link", "#")
            summary = entry.get("summary", entry.get("description", ""))
            # Limpiar HTML básico del summary
            import re
            summary = re.sub(r"<[^>]+>", "", summary)[:200]
            pub = ""
            if hasattr(entry, "published"):
                try:
                    from email.utils import parsedate_to_datetime
                    dt = parsedate_to_datetime(entry.published)
                    pub = dt.strftime("%d/%m %H:%M")
                except Exception:
                    pub = entry.published[:16] if entry.published else ""
            items.append({
                "titulo": titulo,
                "link": link,
                "summary": summary,
                "pub": pub,
            })
        return items, None
    except Exception as e:
        return [], str(e)


def _render_article(art: dict, idx: int):
    """Renderiza un artículo de feed."""
    pub_str = f"<span style='color:#4a6080;font-size:10px'>{art['pub']}</span>" if art["pub"] else ""
    st.markdown(f"""
    <div style='background:#0d1a2a;border:1px solid #1e2d40;border-radius:8px;
         padding:14px 16px;margin-bottom:8px;
         border-left:3px solid #1e3a50'>
        <div style='margin-bottom:6px'>
            {pub_str}
        </div>
        <a href='{art["link"]}' target='_blank'
           style='color:#c8d8e8;font-size:13px;font-weight:600;
           text-decoration:none;line-height:1.4;display:block;margin-bottom:6px'>
            {art["titulo"]}
        </a>
        <div style='color:#4a6080;font-size:12px;line-height:1.5'>
            {art["summary"][:180]}{"..." if len(art["summary"]) > 180 else ""}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render(pais: dict, pais_nombre: str):
    if not HAS_FEEDPARSER:
        st.error("❌ feedparser no instalado. Ejecuta: `pip install feedparser`")
        return

    st.markdown(f"#### 📰 Prensa local y regional — {pais_nombre}")

    region = pais.get("region", "Europa")
    fuentes_pais = pais.get("fuentes_prensa", [])

    # ── Selector de fuente ────────────────────────────────────────────────────
    todas_fuentes = fuentes_pais.copy()
    feeds_reg = FEEDS_REGION.get(region, FEEDS_REGION["Europa"])
    for f in feeds_reg:
        if f not in todas_fuentes:
            todas_fuentes.append(f)

    col_sel, col_refresh = st.columns([3, 1])
    with col_sel:
        opciones = [f["nombre"] for f in todas_fuentes]
        seleccion = st.multiselect(
            "📡 Fuentes activas",
            opciones,
            default=opciones[:3] if len(opciones) >= 3 else opciones,
            key="prensa_sel"
        )
    with col_refresh:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Actualizar", key="prensa_refresh"):
            st.cache_data.clear()

    # ── Cargar feeds seleccionados ────────────────────────────────────────────
    fuentes_activas = [f for f in todas_fuentes if f["nombre"] in seleccion]

    if not fuentes_activas:
        st.info("Selecciona al menos una fuente de noticias.")
        return

    # Tabs por fuente
    if len(fuentes_activas) == 1:
        fuente = fuentes_activas[0]
        with st.spinner(f"Cargando {fuente['nombre']}..."):
            items, err = _fetch_feed(fuente["url"])
        if err:
            st.warning(f"⚠️ No se pudo cargar {fuente['nombre']}: {err}")
        elif not items:
            st.info(f"Sin artículos recientes en {fuente['nombre']}")
        else:
            for i, art in enumerate(items):
                _render_article(art, i)
    else:
        tab_names = [f["nombre"] for f in fuentes_activas]
        tabs = st.tabs(tab_names)
        for tab, fuente in zip(tabs, fuentes_activas):
            with tab:
                idioma_badge = f"<span style='background:#1e2d40;color:#4a6080;font-size:10px;padding:2px 6px;border-radius:4px;font-family:JetBrains Mono'>{fuente.get('idioma','??')}</span>"
                st.markdown(f"🔗 [{fuente['url'][:60]}...]({fuente['url']}) {idioma_badge}", unsafe_allow_html=True)
                with st.spinner(f"Cargando {fuente['nombre']}..."):
                    items, err = _fetch_feed(fuente["url"])
                if err:
                    st.warning(f"⚠️ Feed no disponible: {err}")
                    st.markdown(f"[Abrir en navegador]({fuente['url']})")
                elif not items:
                    st.info("Sin artículos recientes.")
                else:
                    for i, art in enumerate(items):
                        _render_article(art, i)

    # ── Panel de seguridad ────────────────────────────────────────────────────
    with st.expander("🔐 Feeds de seguridad y alertas de viaje"):
        for f in FEEDS_SEGURIDAD:
            st.markdown(f"**{f['nombre']}** `{f.get('idioma','')}`")
            items, err = _fetch_feed(f["url"], max_items=4)
            if err or not items:
                st.caption(f"Feed no disponible · [Abrir web]({f['url']})")
            else:
                for art in items:
                    _render_article(art, 0)
            st.markdown("---")

    st.caption(f"⏱️ Feeds actualizados cada 15 min · {datetime.now().strftime('%H:%M:%S')}")
