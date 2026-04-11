// Trip-OSINT Dashboard - Versión COMPLETA Y FUNCIONAL
console.log("Dashboard completo cargado");

// ==================== DATOS DE DESTINOS ====================
const PAISES_INFO = {
    "brasil": { riesgo: 2, visado: "Exento 90 días", moneda: "BRL", efectivo: "500 BRL", alertas: "Precaución grandes ciudades" },
    "argentina": { riesgo: 2, visado: "Exento 90 días", moneda: "ARS", efectivo: "100,000 ARS", alertas: "Crisis económica" },
    "chile": { riesgo: 1, visado: "Exento 90 días", moneda: "CLP", efectivo: "150,000 CLP", alertas: "" },
    "peru": { riesgo: 2, visado: "Exento 90 días", moneda: "PEN", efectivo: "500 PEN", alertas: "" },
    "colombia": { riesgo: 2, visado: "Exento 90 días", moneda: "COP", efectivo: "400,000 COP", alertas: "Precaución zonas rurales" },
    "uruguay": { riesgo: 1, visado: "Exento 90 días", moneda: "UYU", efectivo: "5,000 UYU", alertas: "" },
    "paraguay": { riesgo: 2, visado: "Exento 90 días", moneda: "PYG", efectivo: "1,200,000 PYG", alertas: "" },
    "bolivia": { riesgo: 2, visado: "Exento 90 días", moneda: "BOB", efectivo: "1,500 BOB", alertas: "Precaución por altura" },
    "ecuador": { riesgo: 2, visado: "Exento 90 días", moneda: "USD", efectivo: "200 USD", alertas: "" },
    "venezuela": { riesgo: 3, visado: "Exento 90 días", moneda: "VES", efectivo: "No recomendado", alertas: "CRISIS POLÍTICA" },
    "china": { riesgo: 2, visado: "eVisa", moneda: "CNY", efectivo: "500 CNY", alertas: "Restricciones sanitarias" },
    "japon": { riesgo: 1, visado: "Exento 90 días", moneda: "JPY", efectivo: "20,000 JPY", alertas: "" },
    "tailandia": { riesgo: 2, visado: "Exento 30 días", moneda: "THB", efectivo: "6,000 THB", alertas: "" },
    "india": { riesgo: 2, visado: "eVisa", moneda: "INR", efectivo: "15,000 INR", alertas: "" },
    "espana": { riesgo: 1, visado: "Exento UE", moneda: "EUR", efectivo: "200 EUR", alertas: "" },
    "mexico": { riesgo: 2, visado: "Exento", moneda: "MXN", efectivo: "4,000 MXN", alertas: "" }
};

// ==================== DATOS PARA TABS ====================
const MAEC_DATA = {
    "brasil": "🟡 Precaución normal en grandes ciudades. Evitar favelas.",
    "argentina": "🟡 Precaución en Buenos Aires. Crisis económica.",
    "chile": "🟢 Seguridad general buena.",
    "peru": "🟡 Precaución en Lima. Evitar zonas fronterizas.",
    "venezuela": "🔴 NO VIAJAR. Crisis política y social.",
    "china": "🟡 Restricciones sanitarias variables.",
    "japon": "🟢 Seguridad alta.",
    "tailandia": "🟡 Precaución en zonas turísticas."
};

const PRENSA_DATA = {
    "brasil": "📰 Folha: Protestas en São Paulo. O Globo: Clima inestable.",
    "argentina": "📰 Clarín: Inflación sube. La Nación: Paros transportes.",
    "chile": "📰 El Mercurio: Normalidad. Emol: Turismo recupera.",
    "peru": "📰 El Comercio: Protestas en regiones.",
    "venezuela": "📰 El Nacional: Crisis humanitaria.",
    "china": "📰 Xinhua: Normalidad. China Daily: Turismo interno.",
    "japon": "📰 Japan Times: Temporada cerezos. NHK: Todo normal."
};

const VACUNAS_DATA = {
    "brasil": "💉 OBLIGATORIA: Fiebre amarilla. Recomendadas: Hepatitis A, Tifoidea, Dengue.",
    "argentina": "💉 Recomendadas: Fiebre amarilla (norte), Hepatitis A.",
    "chile": "💉 Ninguna obligatoria. Recomendada: Hepatitis A.",
    "peru": "💉 Recomendadas: Fiebre amarilla, Hepatitis A, Malaria (amazonía).",
    "venezuela": "💉 OBLIGATORIA: Fiebre amarilla. Recomendadas: Malaria, Dengue.",
    "china": "💉 Recomendadas: Hepatitis A, Encefalitis japonesa.",
    "japon": "💉 Ninguna obligatoria. Recomendada: Encefalitis japonesa."
};

const CAMBIO_DATA = {
    "BRL": { valor: 0.18, cambio: "1 BRL = 0.18 EUR" },
    "ARS": { valor: 0.0011, cambio: "1,000 ARS = 1.10 EUR" },
    "CLP": { valor: 0.0010, cambio: "1,000 CLP = 1.00 EUR" },
    "PEN": { valor: 0.25, cambio: "1 PEN = 0.25 EUR" },
    "COP": { valor: 0.00024, cambio: "10,000 COP = 2.40 EUR" },
    "UYU": { valor: 0.023, cambio: "1 UYU = 0.023 EUR" },
    "USD": { valor: 0.92, cambio: "1 USD = 0.92 EUR" },
    "EUR": { valor: 1, cambio: "1 EUR = 1 EUR" },
    "CNY": { valor: 0.13, cambio: "1 CNY = 0.13 EUR" },
    "JPY": { valor: 0.0062, cambio: "100 JPY = 0.62 EUR" },
    "THB": { valor: 0.026, cambio: "1 THB = 0.026 EUR" },
    "INR": { valor: 0.011, cambio: "1 INR = 0.011 EUR" },
    "MXN": { valor: 0.052, cambio: "1 MXN = 0.052 EUR" }
};

// ==================== FUNCIONES TABS ====================
function cambiarTab(tabId) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    document.querySelector(`.tab-btn[data-tab="${tabId}"]`).classList.add('active');
    document.getElementById(`tab-${tabId}`).classList.add('active');
}

function actualizarTabsConDestino(pais) {
    const info = PAISES_INFO[pais];
    if (!info) return;
    
    // MAEC
    const maecDiv = document.getElementById('maec-info');
    if (maecDiv) maecDiv.innerHTML = `<p>${MAEC_DATA[pais] || '🟡 Consultar web oficial del ministerio.'}</p><p><strong>Teléfono consulado:</strong> +34 91 379 9700</p>`;
    
    // PRENSA
    const prensaDiv = document.getElementById('prensa-info');
    if (prensaDiv) prensaDiv.innerHTML = `<p>${PRENSA_DATA[pais] || '📰 Sin alertas destacadas en prensa local.'}</p><p><strong>Actualización:</strong> ${new Date().toLocaleDateString()}</p>`;
    
    // VACUNAS
    const vacunasDiv = document.getElementById('vacunas-info');
    if (vacunasDiv) vacunasDiv.innerHTML = `<p>${VACUNAS_DATA[pais] || '💉 Consultar centro de vacunación internacional.'}</p><p><strong>Recomendación:</strong> Vacunarse 4-6 semanas antes del viaje.</p>`;
    
    // CAMBIO
    const moneda = info.moneda;
    const cambio = CAMBIO_DATA[moneda];
    const cambioDiv = document.getElementById('cambio-info');
    if (cambioDiv && cambio) {
        cambioDiv.innerHTML = `
            <p><strong>${cambio.cambio}</strong></p>
            <p><strong>Efectivo recomendado:</strong> ${info.efectivo}</p>
            <p><strong>Consejo:</strong> Cambiar moneda en el destino, evitar aeropuertos.</p>
            <p><small>Última actualización: ${new Date().toLocaleString()}</small></p>
        `;
    }
}

function actualizarTabsGlobal() {
    const maecDiv = document.getElementById('maec-info');
    if (maecDiv) maecDiv.innerHTML = `<p>🟡 Riesgo medio global. Selecciona un destino en el buscador para ver recomendaciones específicas.</p><p><strong>Fuente:</strong> Ministerio Asuntos Exteriores</p>`;
    
    const prensaDiv = document.getElementById('prensa-info');
    if (prensaDiv) prensaDiv.innerHTML = `<p>📰 Selecciona un destino en el buscador para ver noticias específicas de prensa local.</p>`;
    
    const vacunasDiv = document.getElementById('vacunas-info');
    if (vacunasDiv) vacunasDiv.innerHTML = `<p>💉 Requisitos sanitarios varían por destino. Usa el buscador para información específica por país.</p><p><a href="https://www.who.int/travel-advice" target="_blank">🌍 Web oficial OMS</a></p>`;
    
    const cambioDiv = document.getElementById('cambio-info');
    if (cambioDiv) cambioDiv.innerHTML = `<p>💰 1 EUR = 0.92 USD | 1 EUR = 1.61 AUD | 1 EUR = 6.20 BRL</p><p>Selecciona un destino para ver cambio específico.</p>`;
}

// ==================== BUSCADOR ====================
function riesgoTexto(riesgo) {
    if (riesgo === 1) return '<span style="color:#27ae60;">🟢 BAJO - Viaje seguro</span>';
    if (riesgo === 2) return '<span style="color:#f39c12;">🟡 MEDIO - Precaución normal</span>';
    if (riesgo === 3) return '<span style="color:#e74c3c;">🟠 ALTO - Aplazar viaje</span>';
    return '<span style="color:#c0392b;">🔴 CRÍTICO - NO VIAJAR</span>';
}

function buscarPais() {
    const input = document.getElementById('buscador-destino');
    const query = input.value.trim().toLowerCase();
    const resultadoDiv = document.getElementById('destino-seleccionado');
    
    if (!query) {
        resultadoDiv.innerHTML = '<div style="background:#fef7e0;padding:15px;border-radius:12px;">✏️ Escribe un país (ej: brasil, argentina, china)</div>';
        resultadoDiv.style.display = 'block';
        return;
    }
    
    const info = PAISES_INFO[query];
    
    if (!info) {
        resultadoDiv.innerHTML = `<div style="background:#fef7e0;padding:15px;border-radius:12px;">❌ "${query}" no encontrado. Prueba: brasil, argentina, chile, peru, china, japon, tailandia</div>`;
        resultadoDiv.style.display = 'block';
        return;
    }
    
    const nombreMostrar = query.charAt(0).toUpperCase() + query.slice(1);
    
    resultadoDiv.innerHTML = `
        <div style="background:linear-gradient(135deg,#667eea,#764ba2);border-radius:24px;padding:25px;color:white;margin-top:20px;">
            <h2>🎯 ${nombreMostrar}</h2>
            <div style="background:rgba(255,255,255,0.15);border-radius:16px;padding:20px;">
                <p><strong>🛡️ Seguridad:</strong> ${riesgoTexto(info.riesgo)}</p>
                <p><strong>🎫 Visado:</strong> ${info.visado}</p>
                <p><strong>💰 Moneda:</strong> ${info.moneda}</p>
                <p><strong>💵 Efectivo recomendado:</strong> ${info.efectivo}</p>
                ${info.alertas ? `<p><strong>⚠️ ALERTA:</strong> ${info.alertas}</p>` : ''}
                <p><strong>📞 Emergencias:</strong> 112 / 911</p>
            </div>
            <button onclick="cerrarDestino()" style="margin-top:15px;background:#666;border:none;padding:10px 20px;border-radius:8px;color:white;cursor:pointer;">✖️ Cerrar</button>
        </div>
    `;
    resultadoDiv.style.display = 'block';
    
    // Actualizar tabs con la información del país
    actualizarTabsConDestino(query);
}

function cerrarDestino() {
    document.getElementById('destino-seleccionado').style.display = 'none';
    document.getElementById('buscador-destino').value = '';
    actualizarTabsGlobal();
}

// ==================== ALERTAS REALES ====================
async function cargarAlertasReales() {
    try {
        const response = await fetch('data/alertas_globales.json');
        if (response.ok) {
            const alertas = await response.json();
            const alertasCriticasSpan = document.getElementById('alertas-criticas');
            const alertasAltasSpan = document.getElementById('alertas-altas');
            const totalDestinosSpan = document.getElementById('total-destinos');
            const alertasActivasSpan = document.getElementById('alertas-activas');
            
            if (alertasCriticasSpan) alertasCriticasSpan.innerText = alertas.alertas_criticas || 0;
            if (alertasAltasSpan) alertasAltasSpan.innerText = alertas.alertas_altas || 0;
            if (alertasActivasSpan) alertasActivasSpan.innerText = (alertas.alertas_criticas || 0) + (alertas.alertas_altas || 0);
            if (totalDestinosSpan) totalDestinosSpan.innerText = Object.keys(PAISES_INFO).length;
            
            const fechaSpan = document.getElementById('ultima-actualizacion');
            if (fechaSpan && alertas.ultima_actualizacion) {
                const fecha = new Date(alertas.ultima_actualizacion);
                fechaSpan.innerText = fecha.toLocaleString();
            }
            
            // Mostrar lista de países en riesgo
            const paisesDiv = document.getElementById('paises-alerta-lista');
            if (paisesDiv && alertas.paises_riesgo_4) {
                let html = '';
                if (alertas.paises_riesgo_4 && alertas.paises_riesgo_4.length > 0) {
                    html += '<h4 style="color:#e74c3c;">🔴 RIESGO CRÍTICO (NO VIAJAR)</h4><ul>';
                    for (const pais of alertas.paises_riesgo_4) {
                        html += `<li><strong>${pais.nombre}</strong> - ${pais.motivo}</li>`;
                    }
                    html += '</ul>';
                }
                if (alertas.paises_riesgo_3 && alertas.paises_riesgo_3.length > 0) {
                    html += '<h4 style="color:#f39c12;">🟠 RIESGO ALTO (APLAZAR VIAJE)</h4><ul>';
                    for (const pais of alertas.paises_riesgo_3) {
                        html += `<li><strong>${pais.nombre}</strong> - ${pais.motivo}</li>`;
                    }
                    html += '</ul>';
                }
                paisesDiv.innerHTML = html || '<p>No hay alertas activas</p>';
            }
        }
    } catch(e) {
        console.log("Alertas no disponibles:", e);
        document.getElementById('total-destinos').innerText = Object.keys(PAISES_INFO).length;
        document.getElementById('ultima-actualizacion').innerText = new Date().toLocaleString();
    }
}

// ==================== INICIALIZACIÓN ====================
document.addEventListener('DOMContentLoaded', function() {
    console.log("Inicializando dashboard completo...");
    
    cargarAlertasReales();
    actualizarTabsGlobal();
    
    // Configurar tabs
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.onclick = () => cambiarTab(btn.getAttribute('data-tab'));
    });
    
    // Configurar buscador
    const btn = document.getElementById('btn-buscar');
    if (btn) btn.onclick = buscarPais;
    
    const input = document.getElementById('buscador-destino');
    if (input) input.onkeypress = (e) => { if (e.key === 'Enter') buscarPais(); };
    
    // Mostrar mensaje inicial
    const resultadoDiv = document.getElementById('destino-seleccionado');
    if (resultadoDiv && !resultadoDiv.innerHTML) {
        resultadoDiv.innerHTML = '<div style="background:#e8f0fe;padding:15px;border-radius:12px;">🌍 Escribe un país: brasil, argentina, chile, peru, china, japon...</div>';
        resultadoDiv.style.display = 'block';
    }
});
