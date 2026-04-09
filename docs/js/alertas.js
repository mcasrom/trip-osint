// Cargar alertas OSINT en el dashboard
async function cargarAlertas() {
    try {
        const response = await fetch('data/alertas_globales.json');
        if (!response.ok) throw new Error('No se pudieron cargar alertas');
        const alertas = await response.json();
        
        // Actualizar contadores
        const alertasCriticasSpan = document.getElementById('alertas-criticas');
        const alertasAltasSpan = document.getElementById('alertas-altas');
        
        if (alertasCriticasSpan) alertasCriticasSpan.innerText = alertas.alertas_criticas;
        if (alertasAltasSpan) alertasAltasSpan.innerText = alertas.alertas_altas;
        
        // Mostrar lista de países con riesgo
        const paisesDiv = document.getElementById('paises-alerta');
        if (paisesDiv && alertas.paises_riesgo_4) {
            let html = '<div class="alertas-lista">';
            html += '<h4>🔴 NO VIAJAR (Nivel 4)</h4><ul>';
            for (const pais of alertas.paises_riesgo_4) {
                html += `<li><strong>${pais.nombre}</strong> - ${pais.motivo}</li>`;
            }
            html += '</ul>';
            
            if (alertas.paises_riesgo_3 && alertas.paises_riesgo_3.length > 0) {
                html += '<h4>🟠 APLAZAR VIAJE (Nivel 3)</h4><ul>';
                for (const pais of alertas.paises_riesgo_3) {
                    html += `<li><strong>${pais.nombre}</strong> - ${pais.motivo}</li>`;
                }
                html += '</ul>';
            }
            
            if (alertas.aeropuertos_cerrados) {
                html += `<h4>✈️ Aeropuertos cerrados</h4><ul>`;
                for (const aeropuerto of alertas.aeropuertos_cerrados) {
                    html += `<li>${aeropuerto}</li>`;
                }
                html += '</ul>';
            }
            
            html += `<p><small>Última actualización: ${new Date(alertas.ultima_actualizacion).toLocaleString()}</small></p>`;
            html += '</div>';
            paisesDiv.innerHTML = html;
        }
        
        return alertas;
    } catch(e) {
        console.error('Error cargando alertas:', e);
        return null;
    }
}

// Llamar al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    cargarAlertas();
});
