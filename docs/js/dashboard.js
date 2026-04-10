cat << 'EOF' > docs/js/dashboard.js
async function cargarJSON(ruta) {
    try {
        const r = await fetch(ruta);
        return await r.json();
    } catch (e) {
        return { error: "No se pudo cargar " + ruta };
    }
}

async function main() {
    document.getElementById("actividad").textContent =
        JSON.stringify(await cargarJSON("data/alertas_globales.json"), null, 2);

    document.getElementById("tension").textContent =
        JSON.stringify(await cargarJSON("data/roma_latest.json"), null, 2);

    document.getElementById("riesgo").textContent =
        JSON.stringify(await cargarJSON("data/paris_latest.json"), null, 2);
}

main();
EOF
