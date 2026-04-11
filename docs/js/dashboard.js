console.log("Dashboard cargado correctamente");

window.onload = () => {
    document.getElementById("actividad").innerHTML =
        "<h2>Actividad</h2><p>Dashboard operativo.</p>";

    document.getElementById("tension").innerHTML =
        "<h2>Tensión</h2><p>Datos cargados correctamente.</p>";

    let html = "<h2>Riesgo por país</h2>";
    for (const pais in PAISES_INFO) {
        const info = PAISES_INFO[pais];
        html += `<div class="pais"><strong>${pais}</strong> — Riesgo: ${info.riesgo}</div>`;
    }
    document.getElementById("riesgo").innerHTML = html;
};
