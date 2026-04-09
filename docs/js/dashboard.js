// Trip-OSINT - Versión que LEE alertas del JSON (sin hardcode)
console.log("Dashboard cargado - leyendo alertas reales");

// ==================== DATOS DE DESTINOS ====================
const PAISES_INFO = {
    "brasil": { riesgo: 2, visado: "Exento 90 días", moneda: "BRL", efectivo: "500 BRL", alertas: "Precaución grandes ciudades" },
    "argentina": { riesgo: 2, visado: "Exento 90 días", moneda: "ARS", efectivo: "100,000 ARS", alertas: "Crisis económica" },
    "chile": { riesgo: 1, visado: "Exento 90 días", moneda: "CLP", efectivo: "150,000 CLP", alertas: "" },
    "peru": { riesgo: 2, visado: "Exento 90 días", moneda: "PEN", efectivo: "500 PEN", alertas: "" },
    "colombia": { riesgo: 2, visado: "Exento 90 días", moneda: "COP", efectivo: "400,000 COP", alertas: "" },
    "venezuela": { riesgo: 3, visado: "Exento", moneda: "VES", efectivo: "No recomendado", alertas: "CRISIS POLÍTICA" },
    "china": { riesgo: 2, visado: "eVisa", moneda: "CNY", efectivo: "500 CNY", alertas: "Restricciones sanitarias" },
    "japon": { riesgo: 1, visado: "Exento", moneda: "JPY", efectivo: "20,000 JPY", alertas: "" },
    "tailandia": { riesgo: 2, visado: "Exento", moneda: "THB", efectivo: "6,000 THB", alertas: "" },
    "espana": { riesgo: 1, visado: "Exento UE", moneda: "EUR", efectivo: "200 EUR", alertas: "" }
};

// ==================== DATOS PARA TABS ====================
const MAEC_DATA = {
    "brasil": "🟡 Precaución normal en grandes ciudades. Evitar favelas.",
    "argentina": "🟡 Precaución en Buenos Aires. Crisis económica.",
    "venezuela": "🔴 NO VIAJAR. Crisis política y social.",
    "china": "🟡 Restricciones sanitarias variables."
};

const PRENSA_DATA = {
    "brasil": "📰 Folha: Protestas en São Paulo. O Globo: Clima inestable.",
    "argentina": "📰 Clarín: Inflación sube. La Nación: Paros transportes.",
    "venezuela": "📰 El Nacional: Crisis humanitaria."
};

const VACUNAS_DATA = {
    "brasil": "💉 OBLIGATORIA: Fiebre amarilla. Recomendadas: Hepatitis A, Tifoidea.",
    "argentina": "💉 Recomendadas: Fiebre amarilla (norte), Hepatitis A.",
    "venezuela": "💉 OBLIGATORIA: Fiebre amarilla. Recomendadas: Malaria, Dengue."
};

const CAMBIO_DATA = {
    "BRL": { valor: 0.18, cambio: "1 BRL = 0.18 EUR" },
    "ARS": { valor: 0.0011, cambio: "1,000 ARS = 1.10 EUR" },
    "CLP": { valor: 0.0010, cambio: "1,000 CLP = 1.00 EUR" },
    "PEN": { valor: 0.25, cambio: "1 PEN = 0.25 EUR" },
    "COP": { valor: 0.00024, cambio: "10,000 COP = 2.40 EUR" },
    "USD": { valor: 0.92, cambio: "1 USD = 0.92 EUR" },
    "EUR": { valor: 1, cambio: "1 EUR = 1 EUR" },
    "CNY": { valor: 0.13, cambio: "1 CNY = 0.13 EUR" },
    "JPY": { valor: 0.0062, cambio: "100 JPY = 0.62 EUR" },
    "THB": { valor: 0.026, cambio: "1 THB = 0.026 EUR" }
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
    
    const maecDiv = document.getElementById('maec-info');
    if (maecDiv) maecDiv.innerHTML = `<p>${MAEC_DATA[pais] || '🟡 Consultar web oficial del ministerio.'}</p>`;
    
    const prensaDiv = document.getElementById('prensa-info');
    if (prensaDiv) prensaDiv.innerHTML = `<p>${PRENSA_DATA[pais] || '📰 Sin alertas destacadas.'}</p>`;
    
    const vacunasDiv = document.getElementById('vacunas-info');
    if (vacunasDiv) vacunasDiv.innerHTML = `<p>${VACUNAS_DATA[pais] || '💉 Consultar centro de vacunación.'}</p>`;
    
    const moneda = info.moneda;
    const cambio = CAMBIO_DATA[moneda];
    const cambioDiv = document.getElementById('cambio-info');
    if (cambioDiv && cambio) {
        cambioDiv.innerHTML = `<p><strong>${cambio.cambio}</strong></p><p><strong>Efectivo:</strong> ${info.efectivo}</p>`;
    }
}

function actualizarTabsGlobal() {
    const maecDiv = document.getElementById('maec-info');
    if (maecDiv) maecDiv.innerHTML = `<p>Selecciona un destino en el buscador</p>`;
    
    const prensaDiv = document.getElementById('prensa-info');
    if (prensaDiv) prensaDiv.innerHTML = `<p>Selecciona un destino</p>`;
    
    const vacunasDiv = document.getElementById('vacunas-info');
    if (vacunasDiv) vacunasDiv.innerHTML = `<p>Selecciona un destino</p><p><a href="https://www.who.int/travel-advice" target="_blank">🌍 OMS</a></p>`;
    
    const cambioDiv = document.getElementById('cambio-info');
    if (cambioDiv) cambioDiv.innerHTML = `<p>1 EUR = 0.92 USD | 1 EUR = 6.20 BRL</p>`;
}

// ==================== ALERTAS REALES (LEYENDO JSON) ====================
let ALERTAS_GLOBALES = null;

async function cargarAlertasReales() {
    try {
        console.log("Cargando alertas desde JSON...");
        const response = await fetch('data/alertas_globales.json');
        
        if (response.ok) {
            ALERTAS_GLOBALES = await response.json();
            console.log("Alertas cargadas:", ALERTAS_GLOBALES);
            
            // Actualizar contadores con datos REALES del JSON
            const alertasCriticasSpan = document.getElementById('alertas-criticas');
            const alertasAltasSpan = document.getElementById('alertas-altas');
            const alertasActivasSpan = document.getElementById('alertas-activas');
            const totalDestinosSpan = document.getElementById('total-destinos');
            const fechaSpan = document.getElementById('ultima-actualizacion');
            
            if (alertasCriticasSpan) {
                const criticas = ALERTAS_GLOBALES.alertas_criticas || 0;
                alertasCriticasSpan.innerText = criticas;
                console.log("Críticas:", criticas);
            }
            
            if (alertasAltasSpan) {
                const altas = ALERTAS_GLOBALES.alertas_altas || 0;
                alertasAltasSpan.innerText = altas;
                console.log("Altas:", altas);
            }
            
            if (alertasActivasSpan) {
                const total = (ALERTAS_GLOBALES.alertas_criticas || 0) + (ALERTAS_GLOBALES.alertas_altas || 0);
                alertasActivasSpan.innerText = total;
            }
            
            if (totalDestinosSpan) {
                totalDestinosSpan.innerText = Object.keys(PAISES_INFO).length;
            }
            
            if (fechaSpan && ALERTAS_GLOBALES.ultima_actualizacion) {
                const fecha = new Date(ALERTAS_GLOBALES.ultima_actualizacion);
                fechaSpan.innerText = fecha.toLocaleString();
            }
            
            // Mostrar lista de países en riesgo
            const paisesDiv = document.getElementById('paises-alerta-lista');
            if (paisesDiv) {
                let html = '';
                
                if (ALERTAS_GLOBALES.paises_riesgo_4 && ALERTAS_GLOBALES.paises_riesgo_4.length > 0) {
                    html += '<h4 style="color:#e74c3c;">🔴 RIESGO CRÍTICO (NO VIAJAR)</h4><ul>';
                    for (const pais of ALERTAS_GLOBALES.paises_riesgo_4) {
                        html += `<li><strong>${pais.nombre}</strong> - ${pais.motivo}</li>`;
                    }
                    html += '</ul>';
                }
                
                if (ALERTAS_GLOBALES.paises_riesgo_3 && ALERTAS_GLOBALES.paises_riesgo_3.length > 0) {
                    html += '<h4 style="color:#f39c12;">🟠 RIESGO ALTO (APLAZAR VIAJE)</h4><ul>';
                    for (const pais of ALERTAS_GLOBALES.paises_riesgo_3) {
                        html += `<li><strong>${pais.nombre}</strong> - ${pais.motivo}</li>`;
                    }
                    html += '</ul>';
                }
                
                if (ALERTAS_GLOBALES.aeropuertos_cerrados && ALERTAS_GLOBALES.aeropuertos_cerrados.length > 0) {
                    html += '<h4>✈️ AEROPUERTOS CERRADOS</h4><ul>';
                    for (const aeropuerto of ALERTAS_GLOBALES.aeropuertos_cerrados) {
                        html += `<li>${aeropuerto}</li>`;
                    }
                    html += '</ul>';
                }
                
                paisesDiv.innerHTML = html || '<p>No hay alertas activas</p>';
            }
        } else {
            console.log("No se encontró alertas_globales.json");
            document.getElementById('total-destinos').innerText = Object.keys(PAISES_INFO).length;
            document.getElementById('ultima-actualizacion').innerText = new Date().toLocaleString();
        }
    } catch(e) {
        console.error("Error cargando alertas:", e);
        document.getElementById('total-destinos').innerText = Object.keys(PAISES_INFO).length;
        document.getElementById('ultima-actualizacion').innerText = new Date().toLocaleString();
    }
}

// ==================== BUSCADOR ====================
function riesgoTexto(riesgo) {
    if (riesgo === 1) return '<span style="color:#27ae60;">🟢 BAJO</span>';
    if (riesgo === 2) return '<span style="color:#f39c12;">🟡 MEDIO</span>';
    if (riesgo === 3) return '<span style="color:#e74c3c;">🟠 ALTO</span>';
    return '<span style="color:#c0392b;">🔴 CRÍTICO</span>';
}

function buscarPais() {
    const input = document.getElementById('buscador-destino');
    const query = input.value.trim().toLowerCase();
    const resultadoDiv = document.getElementById('destino-seleccionado');
    
    if (!query) {
        resultadoDiv.innerHTML = '<div style="background:#fef7e0;padding:15px;border-radius:12px;">✏️ Escribe un país</div>';
        resultadoDiv.style.display = 'block';
        return;
    }
    
    const info = PAISES_INFO[query];
    
    if (!info) {
        resultadoDiv.innerHTML = `<div style="background:#fef7e0;padding:15px;border-radius:12px;">❌ "${query}" no encontrado</div>`;
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
                <p><strong>💵 Efectivo:</strong> ${info.efectivo}</p>
                ${info.alertas ? `<p><strong>⚠️ ALERTA:</strong> ${info.alertas}</p>` : ''}
            </div>
            <button onclick="cerrarDestino()" style="margin-top:15px;background:#666;border:none;padding:10px 20px;border-radius:8px;color:white;cursor:pointer;">✖️ Cerrar</button>
        </div>
    `;
    resultadoDiv.style.display = 'block';
    actualizarTabsConDestino(query);
}

function cerrarDestino() {
    document.getElementById('destino-seleccionado').style.display = 'none';
    document.getElementById('buscador-destino').value = '';
    actualizarTabsGlobal();
}

// ==================== INICIALIZACIÓN ====================
document.addEventListener('DOMContentLoaded', function() {
    console.log("Inicializando dashboard...");
    cargarAlertasReales();
    actualizarTabsGlobal();
    
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.onclick = () => cambiarTab(btn.getAttribute('data-tab'));
    });
    
    const btn = document.getElementById('btn-buscar');
    if (btn) btn.onclick = buscarPais;
    
    const input = document.getElementById('buscador-destino');
    if (input) input.onkeypress = (e) => { if (e.key === 'Enter') buscarPais(); };
});

// AÑADIR AUSTRALIA (sin tocar el resto)
PAISES_INFO["australia"] = { 
    riesgo: 1, 
    visado: "eTA obligatorio", 
    moneda: "AUD", 
    efectivo: "200 AUD", 
    alertas: "" 
};

MAEC_DATA["australia"] = "🟢 Seguridad alta. Seguir normas de playa y fauna silvestre.";

PRENSA_DATA["australia"] = "📰 Gold Coast Bulletin: Temporada de turistas. The Sydney Morning Herald: Normalidad.";

VACUNAS_DATA["australia"] = "💉 Ninguna obligatoria. Recomendada: Hepatitis A, Tétanos.";

CAMBIO_DATA["AUD"] = { valor: 0.61, cambio: "1 AUD = 0.61 EUR" };
