// Trip-OSINT - Buscador UNIVERSAL (cualquier país)
console.log("Dashboard universal cargado");

// Base de datos de países con información actualizada (expandible)
const PAISES_INFO = {
    // Asia
    "china": { riesgo: 2, visado: "eVisa / exento 15 días según nacionalidad", moneda: "CNY", efectivo: "500 CNY", alertas: "Restricciones sanitarias variables" },
    "japon": { riesgo: 1, visado: "Exento 90 días", moneda: "JPY", efectivo: "20,000 JPY", alertas: "" },
    "corea del norte": { riesgo: 4, visado: "Prohibido para turistas occidentales", moneda: "KPW", efectivo: "No aplica", alertas: "Régimen dictatorial, peligro de detención" },
    "corea del sur": { riesgo: 1, visado: "Exento 90 días (K-ETA)", moneda: "KRW", efectivo: "200,000 KRW", alertas: "" },
    "tailandia": { riesgo: 2, visado: "Exento 30 días", moneda: "THB", efectivo: "6,000 THB", alertas: "Precaución zonas turísticas" },
    "vietnam": { riesgo: 2, visado: "eVisa 25 USD", moneda: "VND", efectivo: "5,000,000 VND", alertas: "Carteristas" },
    "india": { riesgo: 2, visado: "eVisa obligatorio", moneda: "INR", efectivo: "15,000 INR", alertas: "Precaución en grandes ciudades" },
    
    // Oriente Medio (con alertas reales)
    "iran": { riesgo: 4, visado: "No recomendado", moneda: "IRR", efectivo: "No aplica", alertas: "GUERRA ACTIVA - NO VIAJAR" },
    "irak": { riesgo: 4, visado: "No recomendado", moneda: "IQD", efectivo: "No aplica", alertas: "ESPACIO AÉREO CERRADO" },
    "israel": { riesgo: 4, visado: "No recomendado", moneda: "ILS", efectivo: "No aplica", alertas: "CONFLICTO ACTIVO" },
    "emiratos arabes": { riesgo: 3, visado: "Exento", moneda: "AED", efectivo: "500 AED", alertas: "AEROPUERTO DXB CERRADO" },
    "qatar": { riesgo: 3, visado: "Exento", moneda: "QAR", efectivo: "500 QAR", alertas: "AEROPUERTO DOH CERRADO" },
    "arabia saudita": { riesgo: 3, visado: "eVisa", moneda: "SAR", efectivo: "500 SAR", alertas: "Alertas fronterizas" },
    
    // Europa
    "rusia": { riesgo: 3, visado: "No recomendado", moneda: "RUB", efectivo: "15,000 RUB", alertas: "Conflicto en curso" },
    "ucrania": { riesgo: 4, visado: "No viajar", moneda: "UAH", efectivo: "No aplica", alertas: "GUERRA ACTIVA" },
    "españa": { riesgo: 1, visado: "Exento (UE)", moneda: "EUR", efectivo: "200 EUR", alertas: "" },
    "francia": { riesgo: 2, visado: "Schengen", moneda: "EUR", efectivo: "200 EUR", alertas: "Huelgas transporte" },
    "reino unido": { riesgo: 2, visado: "Exento 6 meses", moneda: "GBP", efectivo: "200 GBP", alertas: "" },
    
    // América
    "estados unidos": { riesgo: 1, visado: "ESTA obligatorio", moneda: "USD", efectivo: "200 USD", alertas: "" },
    "mexico": { riesgo: 2, visado: "Exento", moneda: "MXN", efectivo: "4,000 MXN", alertas: "Precaución en zonas turísticas" },
    "brasil": { riesgo: 2, visado: "Exento", moneda: "BRL", efectivo: "500 BRL", alertas: "Precaución ciudades grandes" },
    "colombia": { riesgo: 2, visado: "Exento", moneda: "COP", efectivo: "400,000 COP", alertas: "Precaución en zonas rurales" },
    
    // África
    "egipto": { riesgo: 2, visado: "eVisa", moneda: "EGP", efectivo: "3,000 EGP", alertas: "Precaución península del Sinaí" },
    "marruecos": { riesgo: 2, visado: "Exento", moneda: "MAD", efectivo: "2,000 MAD", alertas: "" },
    "sudafrica": { riesgo: 2, visado: "Exento", moneda: "ZAR", efectivo: "3,000 ZAR", alertas: "Precaución en Johannesburgo" },
};

function riesgoTexto(riesgo) {
    if (riesgo === 1) return '<span style="color:#27ae60;">🟢 BAJO - Viaje seguro</span>';
    if (riesgo === 2) return '<span style="color:#f39c12;">🟡 MEDIO - Precaución normal</span>';
    if (riesgo === 3) return '<span style="color:#e74c3c;">🟠 ALTO - Aplazar viaje</span>';
    return '<span style="color:#c0392b;">🔴 CRÍTICO - NO VIAJAR</span>';
}

window.buscarPais = function() {
    const input = document.getElementById('buscador-destino');
    const query = input.value.trim().toLowerCase();
    const resultadoDiv = document.getElementById('destino-seleccionado');
    
    if (!query) {
        resultadoDiv.innerHTML = '<div class="error-msg">✏️ Escribe un país (ej: china, corea del norte, emiratos arabes)</div>';
        resultadoDiv.style.display = 'block';
        return;
    }
    
    // Buscar en la base de datos
    let encontrado = null;
    let clave = null;
    
    for (const [k, v] of Object.entries(PAISES_INFO)) {
        if (k.includes(query) || query.includes(k)) {
            encontrado = v;
            clave = k;
            break;
        }
    }
    
    // Si no está en la base, generar información genérica
    if (!encontrado) {
        encontrado = {
            riesgo: 2,
            visado: "Consultar embajada",
            moneda: "Local",
            efectivo: "200 USD equivalente",
            alertas: "Consultar fuentes oficiales antes de viajar"
        };
        clave = query;
    }
    
    const nombreMostrar = clave.split(' ').map(p => p.charAt(0).toUpperCase() + p.slice(1)).join(' ');
    
    resultadoDiv.innerHTML = `
        <div style="background:linear-gradient(135deg,#667eea,#764ba2);border-radius:24px;padding:25px;color:white;">
            <h2>🎯 ${nombreMostrar}</h2>
            <div style="background:rgba(255,255,255,0.15);border-radius:16px;padding:20px;">
                <p><strong>🛡️ Seguridad:</strong> ${riesgoTexto(encontrado.riesgo)}</p>
                <p><strong>🎫 Visado:</strong> ${encontrado.visado}</p>
                <p><strong>💰 Moneda:</strong> ${encontrado.moneda}</p>
                <p><strong>💵 Efectivo recomendado:</strong> ${encontrado.efectivo}</p>
                <p><strong>📘 Pasaporte:</strong> 6 meses validez mínima</p>
                <p><strong>💉 Vacunas:</strong> Consultar OMS según destino</p>
                ${encontrado.alertas ? `<p><strong>⚠️ Alertas:</strong> ${encontrado.alertas}</p>` : ''}
                <p><strong>📞 Emergencias:</strong> 112 / 911</p>
            </div>
            <button onclick="cerrarDestino()" style="margin-top:15px;background:#666;border:none;padding:10px 20px;border-radius:8px;color:white;cursor:pointer;">✖️ Cerrar</button>
        </div>
    `;
    resultadoDiv.style.display = 'block';
    resultadoDiv.scrollIntoView({ behavior: 'smooth' });
};

window.cerrarDestino = function() {
    document.getElementById('destino-seleccionado').style.display = 'none';
    document.getElementById('buscador-destino').value = '';
};

// Sugerencias para el datalist (países más buscados)
const paisesSugeridos = [
    "china", "corea del norte", "corea del sur", "japon", "tailandia", "vietnam", "india",
    "iran", "irak", "israel", "emiratos arabes", "qatar", "arabia saudita",
    "rusia", "ucrania", "españa", "francia", "reino unido",
    "estados unidos", "mexico", "brasil", "colombia",
    "egipto", "marruecos", "sudafrica"
];

// Actualizar datalist
document.addEventListener('DOMContentLoaded', function() {
    const datalist = document.getElementById('lista-destinos');
    if (datalist) {
        datalist.innerHTML = '';
        paisesSugeridos.forEach(pais => {
            const option = document.createElement('option');
            option.value = pais;
            datalist.appendChild(option);
        });
    }
    
    // Configurar buscador
    const btn = document.getElementById('btn-buscar');
    if (btn) btn.onclick = window.buscarPais;
    
    const input = document.getElementById('buscador-destino');
    if (input) input.onkeypress = (e) => { if (e.key === 'Enter') window.buscarPais(); };
});
