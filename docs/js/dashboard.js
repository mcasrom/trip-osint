// Trip-OSINT - Buscador DINÁMICO (cualquier país, sin hardcode)
console.log("Dashboard dinámico cargado");

// Función genérica para obtener info de cualquier país
function obtenerInfoPais(pais) {
    // Intentar buscar en la base de datos
    if (window.PAISES_INFO && window.PAISES_INFO[pais]) {
        return window.PAISES_INFO[pais];
    }
    
    // Si no existe, generar información genérica
    return {
        riesgo: 2,
        visado: "Consultar embajada",
        moneda: "Local",
        efectivo: "200 USD equivalente",
        alertas: "Consultar fuentes oficiales antes de viajar"
    };
}

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
    const recursosDiv = document.getElementById('recursos-container');
    
    if (!query) {
        resultadoDiv.innerHTML = '<div style="background:#fef7e0;padding:15px;border-radius:12px;">✏️ Escribe un país</div>';
        resultadoDiv.style.display = 'block';
        return;
    }
    
    const info = obtenerInfoPais(query);
    const nombreMostrar = query.split(' ').map(p => p.charAt(0).toUpperCase() + p.slice(1)).join(' ');
    
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
    
    // Mostrar recursos si existen
    if (window.mostrarRecursos && window.RECURSOS_POR_PAIS) {
        if (window.RECURSOS_POR_PAIS[query]) {
            recursosDiv.innerHTML = window.mostrarRecursos(query);
        } else {
            recursosDiv.innerHTML = '<div style="margin-top:20px;padding:20px;background:rgba(0,0,0,0.05);border-radius:16px;"><p>📌 Para más información, consultar <a href="https://www.exteriores.gob.es/" target="_blank">Ministerio Asuntos Exteriores</a></p></div>';
        }
    }
}

function cerrarDestino() {
    document.getElementById('destino-seleccionado').style.display = 'none';
    document.getElementById('recursos-container').innerHTML = '';
    document.getElementById('buscador-destino').value = '';
}

// Cargar alertas reales
async function cargarAlertasReales() {
    try {
        const response = await fetch('data/alertas_globales.json');
        if (response.ok) {
            const alertas = await response.json();
            const alertasCriticasSpan = document.getElementById('alertas-criticas');
            const alertasAltasSpan = document.getElementById('alertas-altas');
            if (alertasCriticasSpan) alertasCriticasSpan.innerText = alertas.alertas_criticas || 0;
            if (alertasAltasSpan) alertasAltasSpan.innerText = alertas.alertas_altas || 0;
        }
    } catch(e) {
        console.log("Alertas no disponibles");
    }
}

// Inicializar
document.addEventListener('DOMContentLoaded', function() {
    console.log("Dashboard dinámico iniciado");
    cargarAlertasReales();
    
    const btn = document.getElementById('btn-buscar');
    if (btn) btn.onclick = buscarPais;
    
    const input = document.getElementById('buscador-destino');
    if (input) input.onkeypress = (e) => { if (e.key === 'Enter') buscarPais(); };
});
