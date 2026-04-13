import os
"""
tabs/export_tab.py — Export PDF informe por país
"""
import io
import streamlit as st
from fpdf import FPDF
from datetime import datetime

COLORES_RIESGO = {1: "BAJO", 2: "MODERADO", 3: "ALTO", 4: "MUY ALTO", 5: "EXTREMO"}

FONT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "fonts")

class InformePDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("DejaVu", "", os.path.join(FONT_DIR, "DejaVuSans.ttf"))
        self.add_font("DejaVu", "B", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"))

    def header(self):
        self.set_font("DejaVu", "B", 14)
        self.set_text_color(0, 212, 170)
        self.cell(0, 10, "TRIPOSINT — Informe de Inteligencia para Viajeros", ln=True)
        self.set_draw_color(30, 45, 64)
        self.line(10, 20, 200, 20)
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "", 8)
        self.set_text_color(74, 96, 128)
        self.cell(0, 10, f"TripOSINT v2.0 · mcasrom · triposint.streamlit.app · Pág. {self.page_no()}", align="C")

def seccion(pdf, titulo):
    pdf.set_font("DejaVu", "B", 10)
    pdf.set_fill_color(13, 26, 42)
    pdf.set_text_color(0, 212, 170)
    pdf.cell(0, 7, titulo, ln=True, fill=True)
    pdf.set_text_color(50, 50, 50)
    pdf.ln(1)

def fila(pdf, label, valor):
    pdf.set_font("DejaVu", "B", 9)
    pdf.set_text_color(74, 96, 128)
    pdf.cell(45, 6, label + ":", ln=False)
    pdf.set_font("DejaVu", "", 9)
    pdf.set_text_color(30, 30, 30)
    pdf.multi_cell(pdf.w - pdf.r_margin - pdf.l_margin - 45, 6, str(valor) if valor else "N/D")

def generar_pdf(pais_nombre, pais, motivo):
    pdf = InformePDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Cabecera destino
    pdf.set_font("DejaVu", "B", 18)
    pdf.set_text_color(30, 30, 30)
    emoji = pais.get("emoji", "")
    pdf.cell(0, 12, f"{pais_nombre}", ln=True)
    pdf.set_font("DejaVu", "", 10)
    pdf.set_text_color(74, 96, 128)
    nivel = pais.get("nivel_riesgo_maec", 1)
    pdf.cell(0, 6, f"Región: {pais.get('region','N/D')}  ·  Motivo: {motivo}  ·  Riesgo MAEC: {nivel}/5 — {COLORES_RIESGO.get(nivel,'')}", ln=True)
    pdf.cell(0, 6, f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}  ·  triposint.streamlit.app", ln=True)
    pdf.ln(4)

    # Información general
    seccion(pdf, "INFORMACIÓN GENERAL")
    fila(pdf, "Capital", pais.get("capital"))
    fila(pdf, "Idioma", pais.get("idioma"))
    fila(pdf, "Moneda", f"{pais.get('moneda_nombre')} ({pais.get('moneda_codigo')})")
    fila(pdf, "Enchufes", pais.get("enchufes"))
    fila(pdf, "Voltaje", f"{pais.get('voltaje')} / {pais.get('frecuencia')}")
    fila(pdf, "Conducción", pais.get("conduccion_lado"))
    fila(pdf, "Internet", pais.get("internet_calidad"))
    pdf.ln(3)

    # Entrada
    seccion(pdf, "REQUISITOS DE ENTRADA")
    fila(pdf, "Visa (españoles)", pais.get("visa_espana"))
    fila(pdf, "Documentación", pais.get("pasaporte_o_dni"))
    requisitos = pais.get("requisitos_especiales", [])
    fila(pdf, "Requisitos esp.", ", ".join(requisitos) if requisitos else "Ninguno")
    pdf.ln(3)

    # Salud
    seccion(pdf, "SALUD Y SANIDAD")
    fila(pdf, "Riesgo sanitario", pais.get("riesgo_salud"))
    fila(pdf, "Malaria", pais.get("riesgo_malaria"))
    vacunas_rec = pais.get("vacunas_recomendadas", [])
    vacunas_obl = pais.get("vacunas_obligatorias", [])
    fila(pdf, "Vacunas recomend.", ", ".join(vacunas_rec) if vacunas_rec else "Ninguna")
    fila(pdf, "Vacunas obligat.", ", ".join(vacunas_obl) if vacunas_obl else "Ninguna")
    notas_salud = pais.get("notas_salud", "")
    if notas_salud:
        fila(pdf, "Notas salud", notas_salud)
    pdf.ln(3)

    # Seguridad
    seccion(pdf, "SEGURIDAD Y ALERTAS MAEC")
    alertas = pais.get("alertas_maec", [])
    if alertas:
        for a in alertas:
            pdf.set_font("DejaVu", "", 9)
            pdf.set_text_color(30, 30, 30)
            pdf.multi_cell(0, 6, f"• {a}")
    else:
        fila(pdf, "Alertas", "Sin alertas activas")
    notas_civicas = pais.get("notas_civicas", "")
    if notas_civicas:
        pdf.ln(2)
        fila(pdf, "Notas cívicas", notas_civicas)
    pdf.ln(3)

    # Contactos de emergencia
    seccion(pdf, "CONTACTOS DE EMERGENCIA")
    fila(pdf, "Emergencias", pais.get("telefono_emergencias"))
    fila(pdf, "Policía", pais.get("telefono_policia"))
    fila(pdf, "Embajada España", pais.get("telefono_embajada_es"))
    fila(pdf, "Web MAEC", pais.get("url_maec"))
    pdf.ln(3)

    # Disclaimer
    pdf.set_font("DejaVu", "", 8)
    pdf.set_text_color(74, 96, 128)
    pdf.multi_cell(0, 5, "AVISO: Este informe es orientativo. Verifica siempre la información en fuentes oficiales (MAEC, OMS, embajadas) antes de viajar. TripOSINT no se responsabiliza de decisiones tomadas basándose en este documento.")

    buf = io.BytesIO()
    pdf.output(buf)
    buf.seek(0)
    return buf.getvalue()

def render(pais, pais_nombre, motivo):
    st.markdown("### 📄 Export — Informe PDF del destino")
    st.markdown(f"Genera un informe de inteligencia completo para **{pais_nombre}** en formato PDF.")

    col1, col2 = st.columns([2, 1])
    with col1:
        incluir_salud     = st.checkbox("Incluir sección Salud", value=True)
        incluir_seguridad = st.checkbox("Incluir sección Seguridad / MAEC", value=True)
        incluir_contactos = st.checkbox("Incluir Contactos de emergencia", value=True)
    with col2:
        st.markdown(f"""
        <div style='background:#0d1a2a;border:1px solid #1e2d40;border-radius:8px;padding:12px;font-family:JetBrains Mono;font-size:11px;color:#4a6080'>
            🌍 <b style='color:#c8d8e8'>{pais_nombre}</b><br>
            🎯 {motivo}<br>
            ⚠ Riesgo: {pais.get('nivel_riesgo_maec',1)}/5
        </div>
        """, unsafe_allow_html=True)

    if st.button("📥 Generar y descargar PDF", type="primary"):
        with st.spinner("Generando informe..."):
            try:
                pdf_bytes = generar_pdf(pais_nombre, pais, motivo)
                fname = f"triposint_{pais_nombre.lower().replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
                st.download_button(
                    label="⬇ Descargar informe PDF",
                    data=pdf_bytes,
                    file_name=fname,
                    mime="application/pdf",
                    type="primary"
                )
                st.success(f"Informe generado: {fname}")
            except Exception as e:
                st.error(f"Error generando PDF: {e}")
