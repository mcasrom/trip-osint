// Trip-OSINT - Con TABS funcionales
console.log("Dashboard cargado");

// Datos de destinos
const DESTINOS_DATA = {
    "gold_coast": { nombre: "Gold Coast", pais: "Australia", riesgo: 2, moneda: "AUD", visado: "eTA online", efectivo: "200 AUD", vacunas: "Ninguna", alertas: ["Temporada ciclones nov-abr"] },
    "bali": { nombre: "Bali", pais: "Indonesia", riesgo: 2, moneda: "IDR", visado: "eVOA 50 USD", efectivo: "2,000,000 IDR", vacunas: "Fiebre amarilla", alertas: ["Volcán Agung nivel 2"] },
    "saigon": { nombre: "Saigon", pais: "Vietnam", riesgo: 2, moneda: "VND", visado: "eVisa 25 USD", efectivo: "5,000,000 VND", vacunas: "Tifoidea", alertas: ["Carteristas"] },
    "tokio": { nombre: "Tokio", pais: "Japón", riesgo: 1, moneda: "JPY", visado: "Exento 90 días", efectivo: "20,000 JPY", vacunas: "Ninguna", alertas: [] },
    "paris": { nombre: "París", pais: "Francia", riesgo: 2, moneda: "EUR", visado: "Schengen", efectivo: "200 EUR", vacunas: "Ninguna", alertas: ["Huelgas transporte"] },
    "roma": { nombre: "Roma", pais: "Italia", riesgo: 2, moneda: "EUR", visado: "Schengen", efectivo: "200 EUR", vacunas: "Ninguna", alertas: [] },
    "londres": { nombre: "Londres", pais: "Reino Unido", riesgo: 2, moneda: "GBP", visado: "Exento 6 meses", efectivo: "200 GBP", vacunas: "Ninguna", alertas: [] },
    "nueva_york": { nombre: "Nueva York", pais: "EEUU", riesgo: 1, moneda: "USD", visado: "ESTA", efectivo: "200 USD", vacunas: "Ninguna", alertas: [] }
};

// DATOS PARA TABS
const MAEC_DATA = {
    "gold_coast": "🟡 Precaución normal. Seguridad general buena.",
    "bali": "🟡 Precaución por terrorismo. Zonas turísticas seguras.",
    "saigon": "🟡 Precaución por carteristas. Evitar manifestaciones.",
    "tokio": "🟢 Seguridad alta. Viaje seguro.",
    "paris": "🟡 Precaución en zonas turísticas y transporte público.",
    "nueva_york": "🟢 Seguridad alta. Precaución normal."
};

const PRENSA_DATA = {
    "gold_coast": "📰 Gold Coast Bulletin: Olas de calor esta semana. Transporte público normal.",
    "bali": "📰 Bali Sun: Temporada alta. Precios suben 20%. Volcán estable.",
    "saigon": "📰 Saigon Times: Lluvias intensas previstas. Precaución al conducir.",
    "tokio": "📰 Japan Times: Temporada de cerezos. Multitudes en zonas turísticas."
};

const VACUNAS_DATA = {
    "gold_coast": "💉 Ninguna obligatoria. Recomendadas: Tétanos, Hepatitis A y B.",
    "bali": "💉 OBLIGATORIA: Fiebre amarilla (si viene de zona endémica). Recomendadas: Tifoidea, Hepatitis A.",
    "saigon": "💉 Recomendadas: Tifoidea, Hepatitis A, Fiebre tifoidea. Malaria en zonas rurales.",
    "tokio": "💉 Ninguna obligatoria. Recomendadas: Encefalitis japonesa (si zonas rurales)."
};

const CAMBIO_DATA = {
    "AUD": { valor: 0.61, cambio: "1 AUD = 0.61 EUR" },
    "IDR": { valor: 0.000058, cambio: "10,000 IDR = 0.58 EUR" },
    "VND": { valor: 0.000038, cambio: "10,000 VND = 0.38 EUR" },
    "JPY": { valor: 0.0062, cambio: "100 JPY = 0.62 EUR" },
    "EUR": { valor: 1, cambio: "1 EUR = 1 EUR" },
    "USD": { valor: 0.92, cambio: "1 USD = 0.92 EUR" },
    "GBP": { valor: 1.17, cambio: "1 GBP = 1.17 EUR" }
};

// FUNCIONES TABS
window.cambiarTab = function(tabId) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    document.querySelector(`.tab-btn[data-tab="${tabId}"]`).classList.add('active');
    document.getElementById(`tab-${tabId}`).classList.add('active');
};

function actualizarTabsConDestino(destino) {
    const info = DESTINOS_DATA[destino];
    if (!info) return;
    
    // MAEC
    const maecDiv = document.getElementById('maec-info');
    if (maecDiv) maecDiv.innerHTML = `<p>${MAEC_DATA[destino] || '🟡 Consultar web oficial del ministerio.'}</p><p><strong>Teléfono consulado:</strong> +${info.pais === 'Australia' ? '61 2 6270 6666' : '34 91 123 4567'}</p>`;
    
    // PRENSA
    const prensaDiv = document.getElementById('prensa-info');
    if (prensaDiv) prensaDiv.innerHTML = `<p>${PRENSA_DATA[destino] || '📰 Sin alertas destacadas en prensa local.'}</p><p><strong>Actualización:</strong> ${new Date().toLocaleDateString()}</p>`;
    
    // VACUNAS
    const vacunasDiv = document.getElementById('vacunas-info');
    if (vacunasDiv) vacunasDiv.innerHTML = `<p>${VACUNAS_DATA[destino] || '💉 Consultar centro de vacunación internacional.'}</p><p><strong>Recomendación:</strong> Vacunarse 4-6 semanas antes del viaje.</p>`;
    
    // CAMBIO
    const moneda = info.moneda;
    const cambio = CAMBIO_DATA[moneda];
    if (cambio && document.getElementById('cambio-info')) {
        document.getElementById('cambio-info').innerHTML = `
            <p><strong>${cambio.cambio}</strong></p>
            <p><strong>Efectivo recomendado:</strong> ${info.efectivo}</p>
            <p><strong>Consejo:</strong> Cambiar moneda en el destino, evitar aeropuertos.</p>
            <p><small>Última actualización: ${new Date().toLocaleString()}</small></p>
        `;
    }
}

function actualizarTabsGlobal() {
    const maecDiv = document.getElementById('maec-info');
    if (maecDiv) maecDiv.innerHTML = `<p>🟡 Riesgo medio global. Consultar destino específico para recomendaciones detalladas.</p><p><strong>Fuente:</strong> Ministerio Asuntos Exteriores</p>`;
    
    const prensaDiv = document.getElementById('prensa-info');
    if (prensaDiv) prensaDiv.innerHTML = `<p>📰 Selecciona un destino en el buscador para ver noticias específicas.</p>`;
    
    const vacunasDiv = document.getElementById('vacunas-info');
    if (vacunasDiv) vacunasDiv.innerHTML = `<p>💉 Requisitos sanitarios varían por destino. Usa el buscador para información específica.</p>`;
    
    const cambioDiv = document.getElementById('cambio-info');
    if (cambioDiv) cambioDiv.innerHTML = `<p>💰 1 EUR = 0.92 USD | 1 EUR = 1.61 AUD | 1 EUR = 17,241 IDR | 1 EUR = 26,315 VND</p><p>Selecciona un destino para ver cambio específico.</p>`;
}

function mostrarRiesgo(nivel) {
    if (nivel == 1) return '<span style="color:#27ae60;">🟢 BAJO</span>';
    if (nivel == 2) return '<span style="color:#f39c12;">🟡 MEDIO</span>';
    return '<span style="color:#e74c3c;">🔴 ALTO</span>';
}

window.buscarDestino = function() {
    const input = document.getElementById('buscador-destino');
    const query = input.value.trim().toLowerCase();
    const destinoDiv = document.getElementById('destino-seleccionado');
    
    let encontrado = null;
    let clave = null;
    
    for (const [k, v] of Object.entries(DESTINOS_DATA)) {
        if (k.includes(query) || v.nombre.toLowerCase().includes(query) || v.pais.toLowerCase().includes(query)) {
            encontrado = v;
            clave = k;
            break;
        }
    }
    
    if (encontrado) {
        actualizarTabsConDestino(clave);
        destinoDiv.innerHTML = `
            <div style="background:linear-gradient(135deg,#667eea,#764ba2);border-radius:24px;padding:25px;color:white;">
                <h2>🎯 ${encontrado.nombre} (${encontrado.pais})</h2>
                <div style="background:rgba(255,255,255,0.15);border-radius:16px;padding:20px;">
                    <p><strong>🛡️ Seguridad:</strong> ${mostrarRiesgo(encontrado.riesgo)}</p>
                    <p><strong>🎫 Visado:</strong> ${encontrado.visado}</p>
                    <p><strong>💉 Vacunas:</strong> ${encontrado.vacunas}</p>
                    <p><strong>💵 Efectivo:</strong> ${encontrado.efectivo}</p>
                    <p><strong>📞 Emergencias:</strong> 112</p>
                    ${encontrado.alertas.length ? `<p><strong>⚠️ Alertas:</strong> ${encontrado.alertas.join(', ')}</p>` : ''}
                </div>
                <button onclick="cerrarDestino()" style="margin-top:15px;background:#666;border:none;padding:10px 20px;border-radius:8px;color:white;cursor:pointer;">✖️ Cerrar</button>
            </div>
        `;
        destinoDiv.style.display = 'block';
        destinoDiv.scrollIntoView({ behavior: 'smooth' });
    } else {
        destinoDiv.innerHTML = `<div style="background:#fef7e0;padding:15px;border-radius:12px;">❌ No encontrado. Destinos: ${Object.keys(DESTINOS_DATA).join(', ')}</div>`;
        destinoDiv.style.display = 'block';
    }
};

window.cerrarDestino = function() {
    document.getElementById('destino-seleccionado').style.display = 'none';
    document.getElementById('buscador-destino').value = '';
    actualizarTabsGlobal();
};

function mostrarTodosDestinos() {
    const container = document.getElementById('destinos');
    if (!container) return;
    
    let html = '<div style="display:grid;gap:20px;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));">';
    for (const [k, v] of Object.entries(DESTINOS_DATA)) {
        html += `
            <div style="background:white;border-radius:16px;padding:20px;box-shadow:0 2px 8px rgba(0,0,0,0.1);">
                <h3>✈️ ${v.nombre}</h3>
                <p>${mostrarRiesgo(v.riesgo)}</p>
                <button onclick="document.getElementById('buscador-destino').value='${k}';buscarDestino();" style="background:#667eea;color:white;border:none;padding:8px 16px;border-radius:8px;cursor:pointer;">Ver detalles</button>
            </div>
        `;
    }
    html += '</div>';
    container.innerHTML = html;
    document.getElementById('total-destinos').innerText = Object.keys(DESTINOS_DATA).length;
    document.getElementById('ultima-actualizacion').innerText = new Date().toLocaleString();
}

// Configurar tabs
document.addEventListener('DOMContentLoaded', function() {
    mostrarTodosDestinos();
    actualizarTabsGlobal();
    
    // Configurar botones de tabs
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.onclick = () => cambiarTab(btn.getAttribute('data-tab'));
    });
    
    // Configurar buscador
    const btn = document.getElementById('btn-buscar');
    if (btn) btn.onclick = window.buscarDestino;
    
    const input = document.getElementById('buscador-destino');
    if (input) input.onkeypress = (e) => { if (e.key === 'Enter') window.buscarDestino(); };
});
