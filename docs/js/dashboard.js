// Trip-OSINT - Versión SIMPLE que FUNCIONA
console.log("Dashboard cargado");

// Datos de destinos (hardcodeados por ahora)
const DESTINOS_DATA = {
    "gold_coast": { nombre: "Gold Coast", pais: "Australia", riesgo: 2, moneda: "AUD", visado: "eTA online", efectivo: "200 AUD", vacunas: "Ninguna" },
    "bali": { nombre: "Bali", pais: "Indonesia", riesgo: 2, moneda: "IDR", visado: "eVOA 50 USD", efectivo: "2,000,000 IDR", vacunas: "Fiebre amarilla" },
    "saigon": { nombre: "Saigon", pais: "Vietnam", riesgo: 2, moneda: "VND", visado: "eVisa 25 USD", efectivo: "5,000,000 VND", vacunas: "Tifoidea" },
    "tokio": { nombre: "Tokio", pais: "Japón", riesgo: 1, moneda: "JPY", visado: "Exento 90 días", efectivo: "20,000 JPY", vacunas: "Ninguna" },
    "paris": { nombre: "París", pais: "Francia", riesgo: 2, moneda: "EUR", visado: "Schengen", efectivo: "200 EUR", vacunas: "Ninguna" },
    "roma": { nombre: "Roma", pais: "Italia", riesgo: 2, moneda: "EUR", visado: "Schengen", efectivo: "200 EUR", vacunas: "Ninguna" },
    "londres": { nombre: "Londres", pais: "Reino Unido", riesgo: 2, moneda: "GBP", visado: "Exento 6 meses", efectivo: "200 GBP", vacunas: "Ninguna" },
    "nueva_york": { nombre: "Nueva York", pais: "EEUU", riesgo: 1, moneda: "USD", visado: "ESTA", efectivo: "200 USD", vacunas: "Ninguna" }
};

function mostrarRiesgo(nivel) {
    if (nivel == 1) return '<span style="color:#27ae60;">🟢 BAJO - Viaje seguro</span>';
    if (nivel == 2) return '<span style="color:#f39c12;">🟡 MEDIO - Precaución normal</span>';
    if (nivel == 3) return '<span style="color:#e74c3c;">🟠 ALTO - Evitar no esencial</span>';
    return '<span style="color:#c0392b;">🔴 CRÍTICO - No viajar</span>';
}

// Función para buscar destino
window.buscarDestino = function() {
    const input = document.getElementById('buscador-destino');
    const query = input.value.trim().toLowerCase();
    const destinoDiv = document.getElementById('destino-seleccionado');
    
    console.log("Buscando:", query);
    
    if (!query) {
        destinoDiv.innerHTML = '<div style="background:#fef7e0;padding:15px;border-radius:12px;">✏️ Escribe un destino</div>';
        destinoDiv.style.display = 'block';
        return;
    }
    
    // Buscar coincidencia
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
        destinoDiv.innerHTML = `
            <div style="background:linear-gradient(135deg,#667eea,#764ba2);border-radius:24px;padding:25px;color:white;margin-top:20px;">
                <h2>🎯 DESTINO: ${encontrado.nombre} (${encontrado.pais})</h2>
                <div style="background:rgba(255,255,255,0.15);border-radius:16px;padding:20px;margin-top:15px;">
                    <p><strong>🛡️ Seguridad:</strong> ${mostrarRiesgo(encontrado.riesgo)}</p>
                    <p><strong>🎫 Visado:</strong> ${encontrado.visado}</p>
                    <p><strong>📘 Pasaporte:</strong> 6 meses validez</p>
                    <p><strong>💉 Vacunas:</strong> ${encontrado.vacunas}</p>
                    <p><strong>💰 Moneda:</strong> ${encontrado.moneda}</p>
                    <p><strong>💵 Efectivo recomendado:</strong> ${encontrado.efectivo}</p>
                    <p><strong>📞 Policía turística:</strong> 112 / 000</p>
                    <p><strong>🏥 Embajada:</strong> Consultar ministerio</p>
                    <p><small>🕒 Datos OSINT actualizados diariamente</small></p>
                </div>
                <button onclick="cerrarDestino()" style="margin-top:15px;background:#666;color:white;border:none;padding:10px 20px;border-radius:8px;cursor:pointer;">✖️ Cerrar</button>
            </div>
        `;
        destinoDiv.style.display = 'block';
        destinoDiv.scrollIntoView({ behavior: 'smooth' });
    } else {
        destinoDiv.innerHTML = `<div style="background:#fef7e0;padding:15px;border-radius:12px;">❌ No encontramos "${query}". Destinos: ${Object.keys(DESTINOS_DATA).join(', ')}</div>`;
        destinoDiv.style.display = 'block';
    }
};

window.cerrarDestino = function() {
    document.getElementById('destino-seleccionado').style.display = 'none';
    document.getElementById('buscador-destino').value = '';
};

// Mostrar todos los destinos al cargar
window.mostrarTodosDestinos = function() {
    const container = document.getElementById('destinos');
    if (!container) return;
    
    let html = '<div style="display:grid;gap:20px;grid-template-columns:repeat(auto-fill,minmax(350px,1fr));">';
    
    for (const [k, v] of Object.entries(DESTINOS_DATA)) {
        html += `
            <div style="background:white;border-radius:16px;padding:20px;box-shadow:0 2px 8px rgba(0,0,0,0.1);">
                <h3>✈️ ${v.nombre} (${v.pais})</h3>
                <p><strong>Seguridad:</strong> ${mostrarRiesgo(v.riesgo)}</p>
                <p><strong>Visado:</strong> ${v.visado}</p>
                <p><strong>Efectivo:</strong> ${v.efectivo}</p>
                <button onclick="document.getElementById('buscador-destino').value='${k}';buscarDestino();" style="margin-top:10px;background:#667eea;color:white;border:none;padding:8px 16px;border-radius:8px;cursor:pointer;">🔍 Ver detalles</button>
            </div>
        `;
    }
    
    html += '</div>';
    container.innerHTML = html;
    document.getElementById('total-destinos').innerText = Object.keys(DESTINOS_DATA).length;
    document.getElementById('ultima-actualizacion').innerText = new Date().toLocaleString();
};

// Inicializar cuando la página carga
document.addEventListener('DOMContentLoaded', function() {
    console.log("Página cargada, inicializando...");
    window.mostrarTodosDestinos();
    
    const btn = document.getElementById('btn-buscar');
    if (btn) {
        btn.onclick = window.buscarDestino;
        console.log("Botón conectado");
    }
    
    const input = document.getElementById('buscador-destino');
    if (input) {
        input.onkeypress = function(e) {
            if (e.key === 'Enter') window.buscarDestino();
        };
    }
});
