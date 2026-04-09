// Trip-OSINT - Con alertas REALES desde el scraper OSINT
console.log("Dashboard con alertas reales cargado");

// Función para cargar alertas desde el JSON generado por el scraper
async function cargarAlertasReales() {
    try {
        const response = await fetch('data/alertas_globales.json');
        if (!response.ok) {
            console.log("No se encontró alertas_globales.json, usando datos por defecto");
            return null;
        }
        const alertas = await response.json();
        console.log("Alertas cargadas:", alertas);
        
        // Actualizar contadores del dashboard
        const alertasCriticasSpan = document.getElementById('alertas-criticas');
        const alertasAltasSpan = document.getElementById('alertas-altas');
        const totalDestinosSpan = document.getElementById('total-destinos');
        const alertasActivasSpan = document.getElementById('alertas-activas');
        
        if (alertasCriticasSpan) alertasCriticasSpan.innerText = alertas.alertas_criticas || 0;
        if (alertasAltasSpan) alertasAltasSpan.innerText = alertas.alertas_altas || 0;
        if (alertasActivasSpan) alertasActivasSpan.innerText = (alertas.alertas_criticas || 0) + (alertas.alertas_altas || 0);
        if (totalDestinosSpan) totalDestinosSpan.innerText = (alertas.paises_riesgo_4?.length || 0) + (alertas.paises_riesgo_3?.length || 0) + 10;
        
        // Actualizar fecha
        const fechaSpan = document.getElementById('ultima-actualizacion');
        if (fechaSpan && alertas.ultima_actualizacion) {
            const fecha = new Date(alertas.ultima_actualizacion);
            fechaSpan.innerText = fecha.toLocaleString();
        }
        
        // Mostrar lista de países en riesgo en el dashboard
        const paisesDiv = document.getElementById('paises-alerta-lista');
        if (paisesDiv) {
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
            
            if (alertas.aeropuertos_cerrados && alertas.aeropuertos_cerrados.length > 0) {
                html += '<h4>✈️ AEROPUERTOS CERRADOS</h4><ul>';
                for (const aeropuerto of alertas.aeropuertos_cerrados) {
                    html += `<li>${aeropuerto}</li>`;
                }
                html += '</ul>';
            }
            
            paisesDiv.innerHTML = html || '<p>No hay alertas activas en este momento</p>';
        }
        
        return alertas;
    } catch(e) {
        console.error("Error cargando alertas:", e);
        return null;
    }
}

// Base de datos de países para búsqueda (expandida)
const PAISES_INFO = {
    "china": { riesgo: 2, visado: "eVisa / exento 15 días según nacionalidad", moneda: "CNY", efectivo: "500 CNY", alertas: "Restricciones sanitarias variables" },
    "corea del norte": { riesgo: 4, visado: "PROHIBIDO", moneda: "KPW", efectivo: "No aplica", alertas: "PELIGRO DE DETENCIÓN" },
    "rusia": { riesgo: 3, visado: "No recomendado", moneda: "RUB", efectivo: "15,000 RUB", alertas: "Conflicto en curso" },
    "iran": { riesgo: 4, visado: "NO RECOMENDADO", moneda: "IRR", efectivo: "No aplica", alertas: "GUERRA ACTIVA" },
    "irak": { riesgo: 4, visado: "NO RECOMENDADO", moneda: "IQD", efectivo: "No aplica", alertas: "ESPACIO AÉREO CERRADO" },
    "israel": { riesgo: 4, visado: "NO RECOMENDADO", moneda: "ILS", efectivo: "No aplica", alertas: "CONFLICTO ACTIVO" },
    "emiratos arabes": { riesgo: 3, visado: "Exento", moneda: "AED", efectivo: "500 AED", alertas: "AEROPUERTO DXB CERRADO" },
    "qatar": { riesgo: 3, visado: "Exento", moneda: "QAR", efectivo: "500 QAR", alertas: "AEROPUERTO DOH CERRADO" },
    "tailandia": { riesgo: 2, visado: "Exento 30 días", moneda: "THB", efectivo: "6,000 THB", alertas: "" },
    "japon": { riesgo: 1, visado: "Exento 90 días", moneda: "JPY", efectivo: "20,000 JPY", alertas: "" },
    "españa": { riesgo: 1, visado: "Exento (UE)", moneda: "EUR", efectivo: "200 EUR", alertas: "" }
};

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
        resultadoDiv.innerHTML = '<div style="background:#fef7e0;padding:15px;border-radius:12px;">✏️ Escribe un país</div><div id="recursos-container"></div>';
        resultadoDiv.style.display = 'block';
        return;
    }
    
    let encontrado = null;
    let clave = null;
    
    for (const [k, v] of Object.entries(PAISES_INFO)) {
        if (k === query || k.includes(query) || query.includes(k)) {
            encontrado = v;
            clave = k;
            break;
        }
    }
    
    if (encontrado) {
        const nombreMostrar = clave.split(' ').map(p => p.charAt(0).toUpperCase() + p.slice(1)).join(' ');
        resultadoDiv.innerHTML = `
            <div style="background:linear-gradient(135deg,#667eea,#764ba2);border-radius:24px;padding:25px;color:white;margin-top:20px;">
                <h2>🎯 ${nombreMostrar}</h2>
                <div style="background:rgba(255,255,255,0.15);border-radius:16px;padding:20px;">
                    <p><strong>🛡️ Seguridad:</strong> ${riesgoTexto(encontrado.riesgo)}</p>
                    <p><strong>🎫 Visado:</strong> ${encontrado.visado}</p>
                    <p><strong>💰 Moneda:</strong> ${encontrado.moneda}</p>
                    <p><strong>💵 Efectivo:</strong> ${encontrado.efectivo}</p>
                    ${encontrado.alertas ? `<p><strong>⚠️ ALERTA:</strong> ${encontrado.alertas}</p>` : ''}
                </div><div id="recursos-container"></div>
                <button onclick="cerrarDestino()" style="margin-top:15px;background:#666;border:none;padding:10px 20px;border-radius:8px;color:white;cursor:pointer;">✖️ Cerrar</button>
            </div><div id="recursos-container"></div>
        `;
        resultadoDiv.style.display = 'block';
    } else {
        resultadoDiv.innerHTML = `<div style="background:#fef7e0;padding:15px;border-radius:12px;">❌ "${query}" no encontrado. Prueba: china, corea del norte, rusia, iran</div><div id="recursos-container"></div>`;
        resultadoDiv.style.display = 'block';
    }
}

function cerrarDestino() {
    document.getElementById('destino-seleccionado').style.display = 'none';
    document.getElementById('buscador-destino').value = '';
}

// Inicializar
document.addEventListener('DOMContentLoaded', function() {
    console.log("Inicializando dashboard...");
    cargarAlertasReales();
    
    const btn = document.getElementById('btn-buscar');
    if (btn) btn.onclick = buscarPais;
    
    const input = document.getElementById('buscador-destino');
    if (input) input.onkeypress = (e) => { if (e.key === 'Enter') buscarPais(); };
});
