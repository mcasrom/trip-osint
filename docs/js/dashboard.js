// Trip-OSINT Dashboard - Versión FUNCIONAL
const API_URL = 'data/';

const DESTINOS = {
    "gold_coast": "Gold Coast (Australia)",
    "bali": "Bali (Indonesia)",
    "saigon": "Saigon (Vietnam)",
    "tokio": "Tokio (Japón)",
    "paris": "París (Francia)",
    "roma": "Roma (Italia)",
    "londres": "Londres (Reino Unido)",
    "nueva_york": "Nueva York (EEUU)",
    "bangkok": "Bangkok (Tailandia)",
    "cancun": "Cancún (México)",
    "dubai": "Dubái (EAU)",
    "sydney": "Sídney (Australia)"
};

function mostrarRiesgo(nivel) {
    if (nivel <= 1) return '🟢 BAJO - Viaje seguro';
    if (nivel <= 2) return '🟡 MEDIO - Precaución normal';
    if (nivel <= 3) return '🟠 ALTO - Evitar no esencial';
    return '🔴 CRÍTICO - No viajar';
}

async function cargarDestino(destino) {
    try {
        const res = await fetch(API_URL + destino + '_latest.json');
        if (res.ok) {
            return await res.json();
        }
    } catch(e) {}
    
    // Datos por defecto
    return {
        destino: destino,
        timestamp: new Date().toISOString(),
        seguridad: 2,
        requisitos: {
            pasaporte: "6 meses validez",
            visado: "Consultar requisitos locales",
            vacunas: "Consultar OMS"
        },
        dinero: {
            efectivo_recomendado: "200 USD",
            tarjetas_aceptadas: "Visa/Mastercard"
        },
        telefonos_interes: {
            policia_turistica: "112",
            embajada: "Consultar ministerio"
        },
        transporte: {
            aerolineas: ["Locales"]
        },
        alertas: []
    };
}

function renderTarjeta(destino, data) {
    const nombre = DESTINOS[destino] || destino.replace('_', ' ').toUpperCase();
    return `
        <div class="destino-card">
            <h2>✈️ ${nombre}</h2>
            <p><strong>🛡️ Seguridad:</strong> ${mostrarRiesgo(data.seguridad)}</p>
            <p><strong>📘 Pasaporte:</strong> ${data.requisitos?.pasaporte || '6 meses'}</p>
            <p><strong>🎫 Visado:</strong> ${data.requisitos?.visado || 'Consultar'}</p>
            <p><strong>💉 Vacunas:</strong> ${data.requisitos?.vacunas || 'Ninguna obligatoria'}</p>
            <p><strong>💵 Efectivo:</strong> ${data.dinero?.efectivo_recomendado || '200 USD'}</p>
            <p><strong>💳 Tarjetas:</strong> ${data.dinero?.tarjetas_aceptadas || 'Visa/Mastercard'}</p>
            <p><strong>📞 Emergencias:</strong> ${data.telefonos_interes?.policia_turistica || '112'}</p>
            ${data.alertas?.length ? `<p><strong>⚠️ Alertas:</strong> ${data.alertas.join(', ')}</p>` : ''}
            <small>🕒 Actualizado: ${new Date(data.timestamp).toLocaleString()}</small>
        </div>
    `;
}

async function mostrarTodosDestinos() {
    const container = document.getElementById('destinos');
    if (!container) return;
    
    container.innerHTML = '<div class="loading">🔄 Cargando destinos...</div>';
    let html = '<div class="destinos-grid">';
    
    for (const destino of Object.keys(DESTINOS)) {
        const data = await cargarDestino(destino);
        html += renderTarjeta(destino, data);
    }
    
    html += '</div>';
    container.innerHTML = html;
    document.getElementById('total-destinos').innerText = Object.keys(DESTINOS).length;
    document.getElementById('ultima-actualizacion').innerText = new Date().toLocaleString();
}

async function buscarDestino() {
    const input = document.getElementById('buscador-destino');
    const query = input.value.trim().toLowerCase();
    const resultadoDiv = document.getElementById('destino-seleccionado');
    
    if (!query) {
        alert('✏️ Escribe un destino (ej: Bali, Tokio, París)');
        return;
    }
    
    // Buscar coincidencia
    let encontrado = null;
    let claveEncontrada = null;
    
    for (const [clave, nombre] of Object.entries(DESTINOS)) {
        if (clave.includes(query) || nombre.toLowerCase().includes(query)) {
            encontrado = nombre;
            claveEncontrada = clave;
            break;
        }
    }
    
    if (encontrado) {
        const data = await cargarDestino(claveEncontrada);
        resultadoDiv.innerHTML = `
            <div class="destino-seleccionado-inner">
                <h2>🎯 DESTINO SELECCIONADO: ${encontrado}</h2>
                ${renderTarjeta(claveEncontrada, data)}
                <button onclick="cerrarSeleccion()" class="btn" style="margin-top:15px;background:#666;">✖️ Cerrar</button>
            </div>
        `;
        resultadoDiv.style.display = 'block';
        resultadoDiv.scrollIntoView({ behavior: 'smooth' });
    } else {
        alert(`❌ No encontramos "${query}". Destinos disponibles: ${Object.values(DESTINOS).join(', ')}`);
    }
}

function cerrarSeleccion() {
    document.getElementById('destino-seleccionado').style.display = 'none';
    document.getElementById('buscador-destino').value = '';
}

// Configurar eventos cuando la página carga
window.onload = function() {
    mostrarTodosDestinos();
    
    const btn = document.getElementById('btn-buscar');
    if (btn) {
        btn.onclick = buscarDestino;
    }
    
    const input = document.getElementById('buscador-destino');
    if (input) {
        input.onkeypress = function(e) {
            if (e.key === 'Enter') buscarDestino();
        };
    }
};
