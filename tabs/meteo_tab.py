"""
tabs/meteo_tab.py — Meteorología en tiempo real + previsión 7 días
API: Open-Meteo (gratuita, sin API key)
     Geocoding: Open-Meteo Geocoding API
"""
import streamlit as st
import requests
from datetime import datetime, timedelta

# Iconos WMO weather codes
WMO_ICONS = {
    0: ("☀️", "Despejado"),
    1: ("🌤️", "Mayormente despejado"),
    2: ("⛅", "Parcialmente nublado"),
    3: ("☁️", "Nublado"),
    45: ("🌫️", "Niebla"),
    48: ("🌫️", "Niebla helada"),
    51: ("🌦️", "Llovizna ligera"),
    53: ("🌦️", "Llovizna moderada"),
    55: ("🌧️", "Llovizna intensa"),
    61: ("🌧️", "Lluvia ligera"),
    63: ("🌧️", "Lluvia moderada"),
    65: ("🌧️", "Lluvia intensa"),
    71: ("🌨️", "Nieve ligera"),
    73: ("🌨️", "Nieve moderada"),
    75: ("❄️", "Nieve intensa"),
    80: ("🌦️", "Chubascos ligeros"),
    81: ("🌧️", "Chubascos moderados"),
    82: ("⛈️", "Chubascos fuertes"),
    85: ("🌨️", "Chubascos de nieve"),
    95: ("⛈️", "Tormenta"),
    96: ("⛈️", "Tormenta con granizo"),
    99: ("⛈️", "Tormenta fuerte con granizo"),
}


@st.cache_data(ttl=3600)
def _geocode(ciudad: str, pais_nombre: str):
    """Geocodifica ciudad usando Open-Meteo Geocoding API."""
    try:
        query = f"{ciudad}, {pais_nombre}"
        r = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": query, "count": 1, "language": "es", "format": "json"},
            timeout=8
        )
        if r.status_code == 200:
            results = r.json().get("results", [])
            if results:
                loc = results[0]
                return loc["latitude"], loc["longitude"], loc.get("timezone", "UTC")
    except Exception:
        pass
    return None, None, None


@st.cache_data(ttl=3600)
def _get_meteo(lat: float, lon: float, timezone: str = "auto"):
    """Obtiene forecast 7 días + datos actuales de Open-Meteo."""
    try:
        params = {
            "latitude": lat,
            "longitude": lon,
            "timezone": timezone,
            "current": [
                "temperature_2m", "relative_humidity_2m", "apparent_temperature",
                "precipitation", "weather_code", "wind_speed_10m",
                "wind_direction_10m", "surface_pressure", "uv_index",
            ],
            "daily": [
                "weather_code", "temperature_2m_max", "temperature_2m_min",
                "precipitation_sum", "precipitation_probability_max",
                "wind_speed_10m_max", "uv_index_max", "sunrise", "sunset",
            ],
            "wind_speed_unit": "kmh",
            "precipitation_unit": "mm",
        }
        r = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params=params,
            timeout=10
        )
        if r.status_code == 200:
            return r.json(), False
    except Exception:
        pass
    return None, True


def _wind_direction(deg: float) -> str:
    dirs = ["N", "NE", "E", "SE", "S", "SO", "O", "NO"]
    return dirs[round(deg / 45) % 8]


def _uv_level(uv: float) -> tuple:
    if uv < 3:
        return "Bajo", "#00e676"
    elif uv < 6:
        return "Moderado", "#ffd600"
    elif uv < 8:
        return "Alto", "#ff9100"
    elif uv < 11:
        return "Muy alto", "#ff1744"
    return "Extremo", "#d50000"


def render(pais: dict, pais_nombre: str):
    capital = pais.get("capital", pais_nombre)
    lat_cfg = pais.get("lat", None)
    lon_cfg = pais.get("lon", None)

    st.markdown(f"#### 🌤️ Meteorología — {capital}")

    # Geocoding si no hay coords en config
    if lat_cfg and lon_cfg:
        lat, lon, tz = lat_cfg, lon_cfg, pais.get("timezone", "auto")
        st.caption(f"📍 {capital} ({lat:.2f}°, {lon:.2f}°)")
    else:
        with st.spinner(f"Localizando {capital}..."):
            lat, lon, tz = _geocode(capital, pais_nombre)

    if not lat:
        st.error(f"No se pudo geocodificar '{capital}'. Añade lat/lon en config/paises.py")
        return

    # Obtener datos meteo
    with st.spinner("Obteniendo datos meteorológicos..."):
        data, error = _get_meteo(lat, lon, tz or "auto")

    if error or not data:
        st.error("No se pudieron obtener datos meteorológicos. Comprueba conexión.")
        return

    curr = data.get("current", {})
    daily = data.get("daily", {})

    # ── Condición actual ──────────────────────────────────────────────────────
    wcode = curr.get("weather_code", 0)
    emoji_w, desc_w = WMO_ICONS.get(wcode, ("🌡️", "Desconocido"))
    temp   = curr.get("temperature_2m", "--")
    sensac = curr.get("apparent_temperature", "--")
    hum    = curr.get("relative_humidity_2m", "--")
    viento = curr.get("wind_speed_10m", "--")
    v_dir  = curr.get("wind_direction_10m", 0)
    presion= curr.get("surface_pressure", "--")
    uv     = curr.get("uv_index", 0)
    precip = curr.get("precipitation", 0)
    uv_label, uv_color = _uv_level(uv or 0)

    st.markdown(f"""
    <div style='background:#0d1a2a;border:1px solid #1e2d40;border-radius:12px;
         padding:24px;margin-bottom:20px'>
        <div style='display:flex;align-items:center;gap:16px;margin-bottom:16px'>
            <div style='font-size:3.5rem'>{emoji_w}</div>
            <div>
                <div style='font-size:2.5rem;font-weight:700;color:#c8d8e8;
                     font-family:JetBrains Mono;line-height:1'>{temp}°C</div>
                <div style='color:#4a6080;font-size:14px;margin-top:4px'>{desc_w}</div>
                <div style='color:#4a6080;font-size:12px'>
                    Sensación térmica: <span style='color:#c8d8e8'>{sensac}°C</span>
                </div>
            </div>
        </div>
        <div style='display:grid;grid-template-columns:repeat(4,1fr);gap:12px'>
            <div style='background:#0a1018;border-radius:8px;padding:12px;text-align:center'>
                <div style='color:#4a6080;font-size:11px'>💧 Humedad</div>
                <div style='color:#00d4aa;font-size:1.2rem;font-weight:700;
                     font-family:JetBrains Mono'>{hum}%</div>
            </div>
            <div style='background:#0a1018;border-radius:8px;padding:12px;text-align:center'>
                <div style='color:#4a6080;font-size:11px'>💨 Viento</div>
                <div style='color:#00d4aa;font-size:1.2rem;font-weight:700;
                     font-family:JetBrains Mono'>{viento} km/h</div>
                <div style='color:#4a6080;font-size:10px'>{_wind_direction(v_dir or 0)}</div>
            </div>
            <div style='background:#0a1018;border-radius:8px;padding:12px;text-align:center'>
                <div style='color:#4a6080;font-size:11px'>🌡️ Presión</div>
                <div style='color:#00d4aa;font-size:1.2rem;font-weight:700;
                     font-family:JetBrains Mono'>{presion} hPa</div>
            </div>
            <div style='background:#0a1018;border-radius:8px;padding:12px;text-align:center'>
                <div style='color:#4a6080;font-size:11px'>☀️ UV</div>
                <div style='color:{uv_color};font-size:1.2rem;font-weight:700;
                     font-family:JetBrains Mono'>{uv or 0:.1f}</div>
                <div style='color:{uv_color};font-size:10px'>{uv_label}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Forecast 7 días ───────────────────────────────────────────────────────
    st.markdown("#### 📅 Previsión 7 días")

    fechas  = daily.get("time", [])
    tmax    = daily.get("temperature_2m_max", [])
    tmin    = daily.get("temperature_2m_min", [])
    wcodes  = daily.get("weather_code", [])
    precips = daily.get("precipitation_sum", [])
    prob_ll = daily.get("precipitation_probability_max", [])
    uv_max  = daily.get("uv_index_max", [])
    sunr    = daily.get("sunrise", [])
    suns    = daily.get("sunset", [])
    vmax    = daily.get("wind_speed_10m_max", [])

    dias_es = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]

    cols = st.columns(min(len(fechas), 7))
    for i, col in enumerate(cols):
        if i >= len(fechas):
            break
        try:
            fecha_dt = datetime.strptime(fechas[i], "%Y-%m-%d")
            dia_semana = dias_es[fecha_dt.weekday()]
            dia_num    = fecha_dt.strftime("%d/%m")
            es_hoy     = i == 0
        except Exception:
            dia_semana, dia_num, es_hoy = "---", "", False

        wc = wcodes[i] if i < len(wcodes) else 0
        em, dsc = WMO_ICONS.get(wc, ("🌡️", ""))
        tx = f"{tmax[i]:.0f}°" if i < len(tmax) else "--"
        tn = f"{tmin[i]:.0f}°" if i < len(tmin) else "--"
        pp = f"{precips[i]:.1f}mm" if i < len(precips) else "--"
        pr = f"{prob_ll[i]}%" if i < len(prob_ll) else "--"
        uv_d = f"{uv_max[i]:.0f}" if i < len(uv_max) else "--"

        border = "border:2px solid #00d4aa" if es_hoy else "border:1px solid #1e2d40"
        with col:
            st.markdown(f"""
            <div style='background:#0d1a2a;{border};border-radius:10px;
                 padding:12px 8px;text-align:center;margin-bottom:4px'>
                <div style='color:{"#00d4aa" if es_hoy else "#4a6080"};
                     font-size:11px;font-weight:700;font-family:JetBrains Mono'>
                    {"HOY" if es_hoy else dia_semana}
                </div>
                <div style='color:#4a6080;font-size:10px'>{dia_num}</div>
                <div style='font-size:1.8rem;margin:6px 0'>{em}</div>
                <div style='color:#ff6b6b;font-size:13px;font-weight:700'>{tx}</div>
                <div style='color:#4a9eff;font-size:12px'>{tn}</div>
                <div style='color:#4a6080;font-size:10px;margin-top:6px'>
                    🌧 {pr}<br>💧 {pp}<br>☀️ UV {uv_d}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Sunrise/Sunset ────────────────────────────────────────────────────────
    if sunr and suns:
        try:
            sr = sunr[0].split("T")[1][:5] if "T" in sunr[0] else sunr[0][-5:]
            ss = suns[0].split("T")[1][:5] if "T" in suns[0] else suns[0][-5:]
            st.markdown(f"""
            <div style='display:flex;gap:16px;margin-top:12px'>
                <div style='background:#0d1a2a;border:1px solid #1e2d40;border-radius:8px;
                     padding:12px 20px;flex:1;text-align:center'>
                    <span style='font-size:1.2rem'>🌅</span>
                    <span style='color:#ffd600;font-family:JetBrains Mono;
                          font-size:1.1rem;margin-left:8px'>{sr}</span>
                    <span style='color:#4a6080;font-size:11px;margin-left:8px'>Amanecer</span>
                </div>
                <div style='background:#0d1a2a;border:1px solid #1e2d40;border-radius:8px;
                     padding:12px 20px;flex:1;text-align:center'>
                    <span style='font-size:1.2rem'>🌇</span>
                    <span style='color:#ff9100;font-family:JetBrains Mono;
                          font-size:1.1rem;margin-left:8px'>{ss}</span>
                    <span style='color:#4a6080;font-size:11px;margin-left:8px'>Atardecer</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        except Exception:
            pass

    # ── Recomendaciones según clima ───────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 🎒 Recomendaciones para el viaje")

    recos = []
    if isinstance(temp, (int, float)):
        if temp < 5:
            recos.append("🧥 Temperatura muy baja — ropa de abrigo gruesa imprescindible")
        elif temp < 15:
            recos.append("🧣 Temperatura fresca — lleva capas y chaqueta")
        elif temp > 35:
            recos.append("🌡️ Calor intenso — hidratación frecuente, evita exposición al mediodía")

    if isinstance(uv, (int, float)) and uv >= 6:
        recos.append(f"☀️ UV {uv_label} ({uv:.0f}) — protector solar SPF 50+ obligatorio")

    if prob_ll and len(prob_ll) > 0 and prob_ll[0] is not None and prob_ll[0] > 50:
        recos.append(f"☂️ Alta probabilidad de lluvia ({prob_ll[0]}%) — lleva paraguas o chubasquero")

    if isinstance(viento, (int, float)) and viento > 40:
        recos.append(f"💨 Viento fuerte ({viento} km/h) — precaución en actividades al aire libre")

    if not recos:
        recos.append("✅ Condiciones meteorológicas favorables para el viaje")

    for r in recos:
        st.info(r)

    st.caption(f"🔄 Datos: Open-Meteo API · Actualizado: {datetime.now().strftime('%H:%M')} · Forecast hasta 7 días")
