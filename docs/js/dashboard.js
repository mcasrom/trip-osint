// Trip-OSINT - Buscador UNIVERSAL (cualquier país)
console.log("Dashboard universal cargado - Versión 2.0");

// Base de datos de países (EXPANDIDA)
const PAISES_INFO = {
    // ASIA
    "china": { riesgo: 2, visado: "eVisa / exento 15 días según nacionalidad", moneda: "CNY", efectivo: "500 CNY", alertas: "Restricciones sanitarias variables, normativas locales estrictas" },
    "corea del norte": { riesgo: 4, visado: "PROHIBIDO para turistas occidentales", moneda: "KPW", efectivo: "No aplica", alertas: "RÉGIMEN DICTATORIAL - PELIGRO DE DETENCIÓN" },
    "corea del sur": { riesgo: 1, visado: "Exento 90 días (K-ETA)", moneda: "KRW", efectivo: "200,000 KRW", alertas: "" },
    "japon": { riesgo: 1, visado: "Exento 90 días", moneda: "JPY", efectivo: "20,000 JPY", alertas: "" },
    "tailandia": { riesgo: 2, visado: "Exento 30 días", moneda: "THB", efectivo: "6,000 THB", alertas: "Precaución zonas turísticas" },
    "vietnam": { riesgo: 2, visado: "eVisa 25 USD", moneda: "VND", efectivo: "5,000,000 VND", alertas: "Carteristas" },
    "india": { riesgo: 2, visado: "eVisa obligatorio", moneda: "INR", efectivo: "15,000 INR", alertas: "Precaución en grandes ciudades" },
    "indonesia": { riesgo: 2, visado: "eVOA 50 USD", moneda: "IDR", efectivo: "2,000,000 IDR", alertas: "Volcán Agung nivel 2" },
    "malasia": { riesgo: 1, visado: "Exento 90 días", moneda: "MYR", efectivo: "500 MYR", alertas: "" },
    "singapur": { riesgo: 1, visado: "Exento 30 días", moneda: "SGD", efectivo: "300 SGD", alertas: "" },
    "camboya": { riesgo: 2, visado: "eVisa 30 USD", moneda: "KHR", efectivo: "400,000 KHR", alertas: "Precaución en Phnom Penh" },
    "laos": { riesgo: 2, visado: "eVisa 30 USD", moneda: "LAK", efectivo: "2,000,000 LAK", alertas: "" },
    "birmania": { riesgo: 3, visado: "No recomendado", moneda: "MMK", efectivo: "200,000 MMK", alertas: "Golpe de estado en curso" },
    "nepal": { riesgo: 2, visado: "eVisa", moneda: "NPR", efectivo: "25,000 NPR", alertas: "" },
    "butan": { riesgo: 1, visado: "Visado obligatorio", moneda: "BTN", efectivo: "5,000 BTN", alertas: "" },
    "bangladesh": { riesgo: 3, visado: "eVisa", moneda: "BDT", efectivo: "15,000 BDT", alertas: "Inestabilidad política" },
    "pakistan": { riesgo: 3, visado: "eVisa", moneda: "PKR", efectivo: "30,000 PKR", alertas: "Alertas de seguridad" },
    "sri lanka": { riesgo: 2, visado: "eVisa", moneda: "LKR", efectivo: "40,000 LKR", alertas: "" },
    
    // ORIENTE MEDIO (con alertas reales)
    "iran": { riesgo: 4, visado: "NO RECOMENDADO", moneda: "IRR", efectivo: "No aplica", alertas: "GUERRA ACTIVA - NO VIAJAR" },
    "irak": { riesgo: 4, visado: "NO RECOMENDADO", moneda: "IQD", efectivo: "No aplica", alertas: "ESPACIO AÉREO CERRADO" },
    "israel": { riesgo: 4, visado: "NO RECOMENDADO", moneda: "ILS", efectivo: "No aplica", alertas: "CONFLICTO ACTIVO" },
    "emiratos arabes": { riesgo: 3, visado: "Exento", moneda: "AED", efectivo: "500 AED", alertas: "AEROPUERTO DXB CERRADO" },
    "qatar": { riesgo: 3, visado: "Exento", moneda: "QAR", efectivo: "500 QAR", alertas: "AEROPUERTO DOH CERRADO" },
    "arabia saudita": { riesgo: 3, visado: "eVisa", moneda: "SAR", efectivo: "500 SAR", alertas: "Alertas fronterizas" },
    "jordania": { riesgo: 3, visado: "eVisa", moneda: "JOD", efectivo: "200 JOD", alertas: "Zonas fronterizas inseguras" },
    "kuwait": { riesgo: 3, visado: "eVisa", moneda: "KWD", efectivo: "100 KWD", alertas: "Espacio aéreo afectado" },
    "bahrein": { riesgo: 3, visado: "eVisa", moneda: "BHD", efectivo: "100 BHD", alertas: "Espacio aéreo afectado" },
    "oman": { riesgo: 2, visado: "eVisa", moneda: "OMR", efectivo: "100 OMR", alertas: "Precaución zonas fronterizas" },
    "turquia": { riesgo: 2, visado: "eVisa", moneda: "TRY", efectivo: "4,000 TRY", alertas: "Evitar zonas específicas" },
    
    // EUROPA
    "rusia": { riesgo: 3, visado: "No recomendado", moneda: "RUB", efectivo: "15,000 RUB", alertas: "Conflicto en curso" },
    "ucrania": { riesgo: 4, visado: "NO VIAJAR", moneda: "UAH", efectivo: "No aplica", alertas: "GUERRA ACTIVA" },
    "españa": { riesgo: 1, visado: "Exento (UE)", moneda: "EUR", efectivo: "200 EUR", alertas: "" },
    "francia": { riesgo: 2, visado: "Schengen", moneda: "EUR", efectivo: "200 EUR", alertas: "Huelgas transporte" },
    "reino unido": { riesgo: 2, visado: "Exento 6 meses", moneda: "GBP", efectivo: "200 GBP", alertas: "" },
    "alemania": { riesgo: 1, visado: "Schengen", moneda: "EUR", efectivo: "200 EUR", alertas: "" },
    "italia": { riesgo: 2, visado: "Schengen", moneda: "EUR", efectivo: "200 EUR", alertas: "" },
    "portugal": { riesgo: 1, visado: "Schengen", moneda: "EUR", efectivo: "200 EUR", alertas: "" },
    
    // AMÉRICA
    "estados unidos": { riesgo: 1, visado: "ESTA obligatorio", moneda: "USD", efectivo: "200 USD", alertas: "" },
    "mexico": { riesgo: 2, visado: "Exento", moneda: "MXN", efectivo: "4,000 MXN", alertas: "Precaución zonas turísticas" },
    "canada": { riesgo: 1, visado: "eTA", moneda: "CAD", efectivo: "250 CAD", alertas: "" },
    "brasil": { riesgo: 2, visado: "Exento", moneda: "BRL", efectivo: "500 BRL", alertas: "Precaución ciudades grandes" },
    "argentina": { riesgo: 2, visado: "Exento", moneda: "ARS", efectivo: "100,000 ARS", alertas: "Crisis económica" },
    "colombia": { riesgo: 2, visado: "Exento", moneda: "COP", efectivo: "400,000 COP", alertas: "Precaución zonas rurales" },
    "peru": { riesgo: 2, visado: "Exento", moneda: "PEN", efectivo: "500 PEN", alertas: "" },
    "chile": { riesgo: 1, visado: "Exento", moneda: "CLP", efectivo: "150,000 CLP", alertas: "" },
    
    // ÁFRICA
    "egipto": { riesgo: 2, visado: "eVisa", moneda: "EGP", efectivo: "3,000 EGP", alertas: "Precaución península del Sinaí" },
    "marruecos": { riesgo: 2, visado: "Exento", moneda: "MAD", efectivo: "2,000 MAD", alertas: "" },
    "tunez": { riesgo: 2, visado: "Exento", moneda: "TND", efectivo: "400 TND", alertas: "" },
    "sudafrica": { riesgo: 2, visado: "Exento", moneda: "ZAR", efectivo: "3,000 ZAR", alertas: "Precaución en Johannesburgo" },
    "kenia": { riesgo: 2, visado: "eVisa", moneda: "KES", efectivo: "20,000 KES", alertas: "" },
    "tanzania": { riesgo: 2, visado: "eVisa", moneda: "TZS", efectivo: "500,000 TZS", alertas: "" }
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
    
    console.log("Buscando:", query);
    
    if (!query) {
        resultadoDiv.innerHTML = '<div style="background:#fef7e0;padding:15px;border-radius:12px;">✏️ Escribe un país (ej: china, corea del norte, rusia)</div>';
        resultadoDiv.style.display = 'block';
        return;
    }
    
    // Buscar coincidencia exacta o parcial
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
                    <p><strong>💵 Efectivo recomendado:</strong> ${encontrado.efectivo}</p>
                    <p><strong>📘 Pasaporte:</strong> 6 meses validez mínima</p>
                    <p><strong>💉 Vacunas:</strong> Consultar OMS según destino</p>
                    ${encontrado.alertas ? `<p><strong>⚠️ ALERTA OSINT:</strong> <span style="background:#c0392b;padding:2px 8px;border-radius:10px;">${encontrado.alertas}</span></p>` : ''}
                    <p><strong>📞 Emergencias:</strong> 112 / 911</p>
                </div>
                <button onclick="cerrarDestino()" style="margin-top:15px;background:#666;border:none;padding:10px 20px;border-radius:8px;color:white;cursor:pointer;">✖️ Cerrar</button>
            </div>
        `;
        resultadoDiv.style.display = 'block';
        resultadoDiv.scrollIntoView({ behavior: 'smooth' });
    } else {
        resultadoDiv.innerHTML = `<div style="background:#fef7e0;padding:15px;border-radius:12px;">❌ "${query}" no está en la base de datos. Prueba: china, corea del norte, rusia, iran, tailandia...</div>`;
        resultadoDiv.style.display = 'block';
    }
}

function cerrarDestino() {
    document.getElementById('destino-seleccionado').style.display = 'none';
    document.getElementById('buscador-destino').value = '';
}

// Configurar eventos cuando la página carga
document.addEventListener('DOMContentLoaded', function() {
    console.log("Página cargada, inicializando buscador universal...");
    
    const btn = document.getElementById('btn-buscar');
    if (btn) {
        btn.onclick = buscarPais;
        console.log("Botón conectado");
    }
    
    const input = document.getElementById('buscador-destino');
    if (input) {
        input.onkeypress = function(e) {
            if (e.key === 'Enter') buscarPais();
        };
        console.log("Input conectado");
    }
    
    // Mensaje de bienvenida
    const resultadoDiv = document.getElementById('destino-seleccionado');
    if (resultadoDiv && !resultadoDiv.innerHTML) {
        resultadoDiv.innerHTML = '<div style="background:#e8f0fe;padding:15px;border-radius:12px;">🌍 Escribe un país: china, corea del norte, rusia, iran, tailandia, japon...</div>';
        resultadoDiv.style.display = 'block';
    }
});
