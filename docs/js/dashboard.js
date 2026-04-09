// Trip-OSINT Dashboard - Con buscador de destinos
const API_URL = 'data/';

let todosLosDestinos = [];
let datosCache = {};

// Base de datos de destinos disponibles
const DESTINOS_PREDEFINIDOS = {
    "gold_coast": { nombre: "Gold Coast", pais: "Australia", moneda: "AUD", riesgo: 2 },
    "bali": { nombre: "Bali", pais: "Indonesia", moneda: "IDR", riesgo: 2 },
    "saigon": { nombre: "Saigon", pais: "Vietnam", moneda: "VND", riesgo: 2 },
    "tokio": { nombre: "Tokio", pais: "Japón", moneda: "JPY", riesgo: 1 },
    "paris": { nombre: "París", pais: "Francia", moneda: "EUR", riesgo: 2 },
    "roma": { nombre: "Roma", pais: "Italia", moneda: "EUR", riesgo: 2 },
    "londres": { nombre: "Londres", pais: "Reino Unido", moneda: "GBP", riesgo: 2 },
    "nueva_york": { nombre: "Nueva York", pais: "EEUU", moneda: "USD", riesgo: 1 },
    "bangkok": { nombre: "Bangkok", pais: "Tailandia", moneda: "THB", riesgo: 2 },
    "cancun": { nombre: "Cancún", pais: "México", moneda: "MXN", riesgo: 3 },
    "dubai": { nombre: "Dubái", pais: "EAU", moneda: "AED", riesgo: 1 },
    "sydney": { nombre: "Sídney", pais: "Australia", moneda: "AUD", riesgo: 2 }
};

async function cargarJSON(destino) {
    if (datosCache[destino]) return datosCache[destino];
    try {
        const res = await fetch(API_URL + `${destino}_latest.json`);
        if (!res.ok) throw new Error('No encontrado');
        const data = await res.json();
        datosCache[destino] = data;
        return data;
    } catch(e) {
        return null;
    }
}

function generarDatosPorDefecto(destino) {
    const info = DESTINOS_PREDEFINIDOS[destino] || { nombre: destino, pais: "Desconocido", moneda: "USD", riesgo: 2 };
    return {
        destino: destino,
        timestamp: new Date().toISOString(),
        seguridad: info.riesgo,
        requisitos: {
            pasaporte: "6 meses validez",
            visado: DESTINOS_PREDEFINIDOS[destino]?.visado || "consultar requisitos locales",
            vacunas: "consultar OMS"
        },
        dinero: {
            efectivo_recomendado: `200 ${info.moneda}`,
            tarjetas_aceptadas: "Visa/Mastercard"
        },
        telefonos_interes: {
            policia_turistica: "112 o local",
            embajada: "consultar ministerio"
        },
        transporte: {
            aerolineas: ["locales", "internacionales"]
        },
        alertas: []
    };
}

function mostrarRiesgo(nivel) {
    if (nivel <= 1) return '<span class="riesgo-bajo">🟢 BAJO - Viaje seguro</span>';
    if (nivel <= 2) return '<span class="riesgo-medio">🟡 MEDIO - Precaución normal</span>';
    if (nivel <= 3) return '<span class="riesgo-alto">🟠 ALTO - Evitar no esencial</span>';
    return '<span class="riesgo-alto">🔴 CRÍTICO - No viajar</span>';
}

function renderTarjeta(destino, data, esDestacado = false) {
    const nombreShow = DESTINOS_PREDEFINIDOS[destino]?.nombre || destino.replace(/_/g, ' ').toUpperCase();
    const pais = DESTINOS_PREDEFINIDOS[destino]?.pais || "";
    const claseCard = esDestacado ? 'destino-card destacado' : 'destino-card';
    
    return `
        <div class="${claseCard}">
            <h2>${nombreShow} ${pais ? `🇦🇺 ${pais}` : ''}</h2>
            <p><strong>🛡️ Seguridad:</strong> ${mostrarRiesgo(data.seguridad)}</p>
            <p><strong>📘 Pasaporte:</strong> ${data.requisitos?.pasaporte || '6 meses'}</p>
            <p><strong>🎫 Visado:</strong> ${data.requisitos?.visado || 'Consultar'}</p>
            <p><strong>💉 Vacunas:</strong> ${data.requisitos?.vacunas || 'Ninguna obligatoria'}</p>
            <p><strong>💵 Efectivo recomendado:</strong> ${data.dinero?.efectivo_recomendado || '200 USD'}</p>
            <p><strong>💳 Tarjetas:</strong> ${data.dinero?.tarjetas_aceptadas || 'Visa/Mastercard'}</p>
            <p><strong>📞 Policía turística:</strong> ${data.telefonos_interes?.policia_turistica || '112'}</p>
            ${data.alertas?.length ? `<p><strong>⚠️ Alertas:</strong> ${data.alertas.join(', ')}</p>` : ''}
            <small>🕒 Datos: ${new Date(data.timestamp || Date.now()).toLocaleString()}</small>
        </div>
    `;
}

async function renderTodosDestinos() {
    const container = document.getElementById('destinos');
    if (!container) return;
    
    container.innerHTML = '<div class="loading">🔄 Cargando destinos...</div>';
    
    let html = '<div class="destinos-grid">';
    let alertasCount = 0;
    let destinosCargados = 0;
    
    for (const [destino, info] of Object.entries(DESTINOS_PREDEFINIDOS)) {
        let data = await cargarJSON(destino);
        if (!data) data = generarDatosPorDefecto(destino);
        html += renderTarjeta(destino, data, false);
        alertasCount += data.alertas?.length || 0;
        destinosCargados++;
    }
    
    html += '</div>';
    container.innerHTML = html;
    document.getElementById('total-destinos').innerText = destinosCargados;
    document.getElementById('alertas-activas').innerText = alertasCount;
}

async function buscarDestino() {
    const input = document.getElementById('buscador-destino');
    const query = input.value.trim().toLowerCase();
    const mensajeDiv = document.getElementById('selector-mensaje');
    const destinoDiv = document.getElementById('destino-seleccionado');
    
    if (!query) {
        mensajeDiv.innerHTML = '✏️ Escribe un país o ciudad';
        destinoDiv.style.display = 'none';
        return;
    }
    
    mensajeDiv.innerHTML = '🔍 Buscando...';
    
    // Buscar en destinos predefinidos
    let encontrado = null;
    let claveEncontrada = null;
    
    for (const [clave, info] of Object.entries(DESTINOS_PREDEFINIDOS)) {
        if (clave.includes(query) || info.nombre.toLowerCase().includes(query) || info.pais.toLowerCase().includes(query)) {
            encontrado = info;
            claveEncontrada = clave;
            break;
        }
    }
    
    if (encontrado) {
        let data = await cargarJSON(claveEncontrada);
        if (!data) data = generarDatosPorDefecto(claveEncontrada);
        
        destinoDiv.innerHTML = `
            <h2>🎯 Tu destino: ${encontrado.nombre} (${encontrado.pais})</h2>
            ${renderTarjeta(claveEncontrada, data, true)}
            <div style="margin-top: 15px;">
                <button onclick="document.getElementById('destino-seleccionado').scrollIntoView({behavior:'smooth'});" class="btn-primary">📌 Ver detalles</button>
                <button onclick="document.getElementById('buscador-destino').value=''; document.getElementById('destino-seleccionado').style.display='none';" class="btn" style="background:#666;">✖️ Cerrar</button>
            </div>
        `;
        destinoDiv.style.display = 'block';
        mensajeDiv.innerHTML = `✅ ${encontrado.nombre} encontrado. Datos OSINT actualizados.`;
        destinoDiv.scrollIntoView({ behavior: 'smooth' });
    } else {
        mensajeDiv.innerHTML = `⚠️ No encontramos "${query}". Puedes solicitarlo en el repositorio de GitHub.`;
        destinoDiv.style.display = 'none';
    }
}

async function cargarMeta() {
    try {
        const res = await fetch(API_URL + 'meta_last_update.txt');
        if (res.ok) {
            const meta = await res.json();
            const fecha = new Date(meta.ultima_actualizacion);
            document.getElementById('ultima-actualizacion').innerText = fecha.toLocaleDateString() + ' ' + fecha.toLocaleTimeString();
        } else {
            document.getElementById('ultima-actualizacion').innerText = new Date().toLocaleDateString();
        }
    } catch(e) {
        document.getElementById('ultima-actualizacion').innerText = new Date().toLocaleDateString();
    }
}

// Configurar evento del botón
document.addEventListener('DOMContentLoaded', () => {
    renderTodosDestinos();
    cargarMeta();
    
    const btn = document.getElementById('btn-buscar');
    if (btn) btn.addEventListener('click', buscarDestino);
    
    const input = document.getElementById('buscador-destino');
    if (input) input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') buscarDestino();
    });
});
