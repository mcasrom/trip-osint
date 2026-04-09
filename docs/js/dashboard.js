// Dashboard dinámico - muestra cualquier destino que exista en data/
const API_URL = '../data/';

async function obtenerListaDestinos() {
    // Primero intentar desde meta_last_update.txt
    try {
        const res = await fetch(API_URL + 'meta_last_update.txt');
        const meta = await res.json();
        return meta.destinos || [];
    } catch(e) {
        // Si no, buscar archivos .json disponibles
        return [];
    }
}

async function cargarDestino(nombre) {
    try {
        const res = await fetch(API_URL + `${nombre}_latest.json`);
        if (!res.ok) return null;
        return await res.json();
    } catch(e) {
        return null;
    }
}

function mostrarRiesgo(nivel) {
    if (nivel <= 1) return '🟢 Bajo - Viaje seguro';
    if (nivel <= 2) return '🟡 Medio - Precaución normal';
    if (nivel <= 3) return '🟠 Alto - Evitar no esencial';
    return '🔴 Crítico - No viajar';
}

async function renderDashboard() {
    const container = document.getElementById('destinos');
    container.innerHTML = '<div class="loading">🔄 Cargando destinos...</div>';
    
    // Obtener lista de destinos
    let destinos = await obtenerListaDestinos();
    
    if (destinos.length === 0) {
        container.innerHTML = '<div class="error">⚠️ No hay datos disponibles. Esperando primera actualización del Odroid.</div>';
        return;
    }
    
    let html = '<div class="destinos-grid">';
    
    for (const destino of destinos) {
        const data = await cargarDestino(destino);
        if (!data) continue;
        
        const nombreMostrar = destino.replace(/_/g, ' ').toUpperCase();
        
        html += `
            <div class="destino-card">
                <h2>${nombreMostrar}</h2>
                <p><strong>🛡️ Seguridad:</strong> ${mostrarRiesgo(data.seguridad)}</p>
                <p><strong>📘 Pasaporte:</strong> ${data.requisitos.pasaporte}</p>
                <p><strong>🎫 Visado:</strong> ${data.requisitos.visado}</p>
                <p><strong>💉 Vacunas:</strong> ${data.requisitos.vacunas}</p>
                <p><strong>💵 Efectivo recomendado:</strong> ${data.dinero.efectivo_recomendado}</p>
                <p><strong>💳 Tarjetas:</strong> ${data.dinero.tarjetas_aceptadas}</p>
                <p><strong>📞 Policía turística:</strong> ${data.telefonos_interes.policia_turistica}</p>
                ${data.alertas.length ? `<p><strong>⚠️ Alertas:</strong> ${data.alertas.join(', ')}</p>` : ''}
                <small>🕒 Actualizado: ${new Date(data.timestamp).toLocaleString()}</small>
            </div>
        `;
    }
    
    html += '</div>';
    container.innerHTML = html;
}

// Cargar metadata de última actualización
async function cargarMeta() {
    try {
        const res = await fetch(API_URL + 'meta_last_update.txt');
        const meta = await res.json();
        const fecha = new Date(meta.ultima_actualizacion);
        const span = document.getElementById('last-update');
        if (span) span.innerText = fecha.toLocaleString();
    } catch(e) {
        console.log('Meta no disponible');
    }
}

// Ejecutar
renderDashboard();
cargarMeta();
