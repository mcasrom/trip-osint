// Trip-OSINT Dashboard - Versión Profesional
const API_URL = '../data/';

// Información real de destinos (cuando no hay datos del scraper)
const DEFAULT_DATA = {
    "gold_coast": {
        seguridad: 2,
        requisitos: { pasaporte: "6 meses", visado: "eTA (online)", vacunas: "Ninguna" },
        dinero: { efectivo_recomendado: "200 AUD", tarjetas_aceptadas: "Visa/Mastercard" },
        telefonos_interes: { policia_turistica: "000", embajada: "+61 2 6270 6666" },
        transporte: { aerolineas: ["Qantas", "Virgin", "Jetstar"] },
        alertas: ["Temporada de ciclones: nov-abr"]
    },
    "bali": {
        seguridad: 2,
        requisitos: { pasaporte: "6 meses", visado: "eVOA (50 USD)", vacunas: "Fiebre amarilla" },
        dinero: { efectivo_recomendado: "2,000,000 IDR", tarjetas_aceptadas: "Visa/Mastercard" },
        telefonos_interes: { policia_turistica: "110", embajada: "+62 21 2555 5200" },
        transporte: { aerolineas: ["Garuda", "AirAsia", "Lion Air"] },
        alertas: ["Volcán Agung: nivel 2"]
    },
    "saigon": {
        seguridad: 2,
        requisitos: { pasaporte: "6 meses", visado: "eVisa (25 USD)", vacunas: "Fiebre tifoidea" },
        dinero: { efectivo_recomendado: "5,000,000 VND", tarjetas_aceptadas: "Visa/Mastercard" },
        telefonos_interes: { policia_turistica: "113", embajada: "+84 28 3822 5807" },
        transporte: { aerolineas: ["Vietnam Airlines", "VietJet"] },
        alertas: ["Precaución con carteristas"]
    }
};

async function cargarDestino(nombre) {
    try {
        const res = await fetch(API_URL + `${nombre}_latest.json`);
        if (!res.ok) throw new Error('No encontrado');
        const data = await res.json();
        return { ...DEFAULT_DATA[nombre], ...data };
    } catch(e) {
        return DEFAULT_DATA[nombre] || null;
    }
}

function mostrarRiesgo(nivel) {
    if (nivel <= 1) return '<span class="riesgo-bajo">🟢 BAJO - Viaje seguro</span>';
    if (nivel <= 2) return '<span class="riesgo-medio">🟡 MEDIO - Precaución normal</span>';
    if (nivel <= 3) return '<span class="riesgo-alto">🟠 ALTO - Evitar no esencial</span>';
    return '<span class="riesgo-alto">🔴 CRÍTICO - No viajar</span>';
}

function getIconoMoneda(destino) {
    const map = { gold_coast: "AUD", bali: "IDR", saigon: "VND", paris: "EUR", roma: "EUR", berlin: "EUR", lisboa: "EUR" };
    return map[destino] || "USD";
}

async function cargarDestinos() {
    const destinosFromMeta = await obtenerDestinosDesdeMeta();
    return destinosFromMeta.length ? destinosFromMeta : Object.keys(DEFAULT_DATA);
}

async function obtenerDestinosDesdeMeta() {
    try {
        const res = await fetch(API_URL + 'meta_last_update.txt');
        const meta = await res.json();
        return meta.destinos || [];
    } catch(e) {
        return [];
    }
}

async function renderDashboard() {
    const container = document.getElementById('destinos');
    container.innerHTML = '<div class="loading">🔄 Cargando inteligencia de viajes...</div>';
    
    const destinos = await cargarDestinos();
    document.getElementById('total-destinos').innerText = destinos.length;
    
    let html = '';
    let alertasCount = 0;
    
    for (const destino of destinos) {
        const data = await cargarDestino(destino);
        if (!data) continue;
        
        alertasCount += data.alertas?.length || 0;
        const nombreShow = destino.replace(/_/g, ' ').toUpperCase();
        const moneda = getIconoMoneda(destino);
        
        html += `
            <div class="destino-card">
                <h2>${nombreShow}</h2>
                <p><strong>🛡️ Seguridad:</strong> ${mostrarRiesgo(data.seguridad)}</p>
                <p><strong>📘 Pasaporte:</strong> ${data.requisitos?.pasaporte || '6 meses'}</p>
                <p><strong>🎫 Visado:</strong> ${data.requisitos?.visado || 'Consultar'}</p>
                <p><strong>💉 Vacunas:</strong> ${data.requisitos?.vacunas || 'Ninguna obligatoria'}</p>
                <p><strong>💵 Efectivo recomendado:</strong> ${data.dinero?.efectivo_recomendado || '200 USD'} ${moneda}</p>
                <p><strong>💳 Tarjetas:</strong> ${data.dinero?.tarjetas_aceptadas || 'Visa/Mastercard'}</p>
                <p><strong>📞 Policía turística:</strong> ${data.telefonos_interes?.policia_turistica || '112'}</p>
                <p><strong>✈️ Aerolíneas locales:</strong> ${data.transporte?.aerolineas?.join(', ') || 'Consultar'}</p>
                ${data.alertas?.length ? `<p><strong>⚠️ Alertas activas:</strong> ${data.alertas.join(', ')}</p>` : ''}
                <small>🕒 Datos OSINT actualizados: ${new Date(data.timestamp || Date.now()).toLocaleString()}</small>
            </div>
        `;
    }
    
    document.getElementById('alertas-activas').innerText = alertasCount;
    container.innerHTML = html;
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

// Ejecutar
renderDashboard();
cargarMeta();
