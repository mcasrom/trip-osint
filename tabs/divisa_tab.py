"""
tabs/divisa_tab.py — Tipo de cambio en tiempo real
Usa exchangerate-api.com (free tier, sin API key para EUR base)
"""
import streamlit as st
import requests
from datetime import datetime

@st.cache_data(ttl=3600)
def _get_rates():
    """Obtiene tasas de cambio desde EUR. Fallback a datos fijos si falla."""
    try:
        r = requests.get("https://api.exchangerate-api.com/v4/latest/EUR", timeout=8)
        if r.status_code == 200:
            data = r.json()
            return data.get("rates", {}), data.get("date", "N/D"), False
    except Exception:
        pass
    # Fallback tasas aproximadas (se actualizan al reiniciar)
    fallback = {
        "USD": 1.08, "GBP": 0.86, "JPY": 162.0, "CNY": 7.8, "INR": 90.0,
        "MXN": 18.5, "ARS": 950.0, "COP": 4300.0, "THB": 38.0, "AUD": 1.65,
        "MAD": 10.8, "EGP": 52.0, "AED": 3.97, "ILS": 4.0, "BRL": 5.5,
        "CHF": 0.95, "SEK": 11.2, "NOK": 11.8, "DKK": 7.46, "PLN": 4.25,
        "CZK": 25.0, "HUF": 390.0, "RON": 4.97, "BGN": 1.96, "HRK": 7.53,
        "TRY": 35.0, "RUB": 99.0, "KRW": 1450.0, "SGD": 1.45, "HKD": 8.45,
        "NZD": 1.78, "ZAR": 20.0, "NGN": 1650.0, "KES": 140.0, "GHS": 16.5,
        "EUR": 1.0,
    }
    return fallback, "datos locales (sin conexión)", True


def _formato_cantidad(cantidad: float, codigo: str, rate: float) -> str:
    resultado = cantidad * rate
    if resultado >= 1000:
        return f"{resultado:,.2f} {codigo}"
    elif resultado >= 1:
        return f"{resultado:.4f} {codigo}"
    else:
        return f"{resultado:.6f} {codigo}"


def render(pais: dict, pais_nombre: str):
    codigo = pais.get("moneda_codigo", "EUR")
    nombre_moneda = pais.get("moneda_nombre", "Euro")

    rates, fecha, es_fallback = _get_rates()

    st.markdown(f"#### 💱 {nombre_moneda} ({codigo})")

    if es_fallback:
        st.warning("⚠️ Sin conexión a API de cambio. Mostrando tasas de referencia aproximadas.")
    else:
        st.success(f"✅ Tasas actualizadas: {fecha}")

    # ── Tasa EUR → moneda destino ─────────────────────────────────────────────
    rate = rates.get(codigo, None)

    if rate:
        col1, col2, col3 = st.columns(3)
        col1.metric(f"1 EUR →", f"{rate:.4f} {codigo}")
        col2.metric(f"1 {codigo} →", f"{1/rate:.4f} EUR")
        col3.metric("Actualizado", fecha)

        st.markdown("---")

        # ── Conversor interactivo ─────────────────────────────────────────────
        st.markdown("#### 🔄 Conversor")
        cc1, cc2 = st.columns(2)

        with cc1:
            st.markdown(f"**EUR → {codigo}**")
            eur_input = st.number_input(
                "Euros (€)", min_value=0.0, value=100.0, step=10.0,
                key="eur_input"
            )
            resultado_ida = eur_input * rate
            st.markdown(f"""
            <div style='background:#0d1a2a;border:1px solid #00d4aa;border-radius:8px;
                 padding:16px;text-align:center;margin-top:8px'>
                <div style='font-size:1.8rem;font-weight:700;color:#00d4aa;
                     font-family:JetBrains Mono'>
                    {resultado_ida:,.2f} {codigo}
                </div>
                <div style='font-size:12px;color:#4a6080;margin-top:4px'>
                    {eur_input:.2f} EUR × {rate:.4f}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with cc2:
            st.markdown(f"**{codigo} → EUR**")
            dest_input = st.number_input(
                f"{codigo}", min_value=0.0, value=100.0, step=10.0,
                key="dest_input"
            )
            resultado_vuelta = dest_input / rate
            st.markdown(f"""
            <div style='background:#0d1a2a;border:1px solid #1e2d40;border-radius:8px;
                 padding:16px;text-align:center;margin-top:8px'>
                <div style='font-size:1.8rem;font-weight:700;color:#c8d8e8;
                     font-family:JetBrains Mono'>
                    {resultado_vuelta:,.2f} EUR
                </div>
                <div style='font-size:12px;color:#4a6080;margin-top:4px'>
                    {dest_input:.2f} {codigo} ÷ {rate:.4f}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # ── Tabla de equivalencias rápidas ────────────────────────────────────
        st.markdown("#### 📊 Equivalencias rápidas")
        cantidades = [5, 10, 20, 50, 100, 200, 500, 1000]
        cols = st.columns(4)
        for i, c in enumerate(cantidades):
            with cols[i % 4]:
                st.markdown(f"""
                <div style='background:#0d1a2a;border:1px solid #1e2d40;
                     border-radius:6px;padding:10px;text-align:center;margin-bottom:8px'>
                    <div style='color:#4a6080;font-size:11px'>{c} EUR</div>
                    <div style='color:#00d4aa;font-size:14px;font-weight:600;
                         font-family:JetBrains Mono'>{c * rate:,.2f}</div>
                    <div style='color:#4a6080;font-size:10px'>{codigo}</div>
                </div>
                """, unsafe_allow_html=True)

    else:
        st.error(f"No se dispone de tasa de cambio para {codigo}. Consulta un banco o XE.com.")

    # ── Consejos con el dinero ────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 💡 Consejos para el dinero en destino")

    moneda_euro = codigo == "EUR"
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        **💳 Tarjetas**
        - Avisa a tu banco antes de viajar
        - Elige siempre cobrar en moneda local (evita DCC)
        - Lleva al menos 2 tarjetas de distinto banco
        - Visa/Mastercard más aceptadas que Amex
        """)
    with col_b:
        if moneda_euro:
            st.markdown("""
            **💶 Efectivo (zona Euro)**
            - No necesitas cambiar divisas
            - Lleva algo de efectivo para mercados y pequeños comercios
            - Los cajeros suelen ser gratuitos en la zona euro
            """)
        else:
            st.markdown(f"""
            **💵 Efectivo ({codigo})**
            - Cambia en banco o casa de cambio oficial, nunca en calle
            - Compara tasas en [XE.com](https://www.xe.com)
            - Reserva algo de EUR para emergencias
            - Los aeropuertos tienen peores tasas — cambia solo lo mínimo
            """)

    st.markdown(f"""
    <div style='margin-top:12px;font-size:11px;color:#4a6080;font-family:JetBrains Mono'>
        Fuente: exchangerate-api.com · Solo referencia · No es asesoramiento financiero
    </div>
    """, unsafe_allow_html=True)
