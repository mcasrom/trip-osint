// Recursos OSINT por destino - Enlaces oficiales
const RECURSOS_POR_PAIS = {
    // Asia
    "china": {
        prensa: [
            { nombre: "Xinhua Net", url: "http://www.xinhuanet.com/english/" },
            { nombre: "China Daily", url: "https://www.chinadaily.com.cn/" }
        ],
        maec: "https://www.exteriores.gob.es/Consulados/Pekin/Paginas/Recomendaciones-de-Viaje.aspx",
        embajada: "https://www.exteriores.gob.es/Consulados/Pekin",
        telefono_embajada: "+86 10 6532 3629"
    },
    "japon": {
        prensa: [
            { nombre: "The Japan Times", url: "https://www.japantimes.co.jp/" },
            { nombre: "NHK World", url: "https://www3.nhk.or.jp/nhkworld/" }
        ],
        maec: "https://www.exteriores.gob.es/Consulados/Tokio/Paginas/Recomendaciones-de-Viaje.aspx",
        embajada: "https://www.exteriores.gob.es/Consulados/Tokio",
        telefono_embajada: "+81 3 3583 0392"
    },
    "tailandia": {
        prensa: [
            { nombre: "Bangkok Post", url: "https://www.bangkokpost.com/" },
            { nombre: "The Nation Thailand", url: "https://www.nationthailand.com/" }
        ],
        maec: "https://www.exteriores.gob.es/Consulados/Bangkok/Paginas/Recomendaciones-de-Viaje.aspx",
        embajada: "https://www.exteriores.gob.es/Consulados/Bangkok",
        telefono_embajada: "+66 2 252 6111"
    },
    "vietnam": {
        prensa: [
            { nombre: "Viet Nam News", url: "https://vietnamnews.vn/" },
            { nombre: "Saigon Times", url: "https://english.thesaigontimes.vn/" }
        ],
        maec: "https://www.exteriores.gob.es/Consulados/Hanoi/Paginas/Recomendaciones-de-Viaje.aspx",
        embajada: "https://www.exteriores.gob.es/Consulados/Hanoi",
        telefono_embajada: "+84 24 3771 5200"
    },
    "india": {
        prensa: [
            { nombre: "The Times of India", url: "https://timesofindia.indiatimes.com/" },
            { nombre: "The Hindu", url: "https://www.thehindu.com/" }
        ],
        maec: "https://www.exteriores.gob.es/Consulados/NuevaDelhi/Paginas/Recomendaciones-de-Viaje.aspx",
        embajada: "https://www.exteriores.gob.es/Consulados/NuevaDelhi",
        telefono_embajada: "+91 11 4129 3000"
    },
    "indonesia": {
        prensa: [
            { nombre: "The Jakarta Post", url: "https://www.thejakartapost.com/" },
            { nombre: "Bali Sun", url: "https://www.thebalisun.com/" }
        ],
        maec: "https://www.exteriores.gob.es/Consulados/Yakarta/Paginas/Recomendaciones-de-Viaje.aspx",
        embajada: "https://www.exteriores.gob.es/Consulados/Yakarta",
        telefono_embajada: "+62 21 252 5115"
    },
    
    // Oriente Medio
    "emiratos arabes": {
        prensa: [
            { nombre: "Gulf News", url: "https://gulfnews.com/" },
            { nombre: "The National", url: "https://www.thenationalnews.com/" }
        ],
        maec: "https://www.exteriores.gob.es/Consulados/Dubai/Paginas/Recomendaciones-de-Viaje.aspx",
        embajada: "https://www.exteriores.gob.es/Consulados/Dubai",
        telefono_embajada: "+971 4 339 1600"
    },
    "qatar": {
        prensa: [
            { nombre: "The Peninsula", url: "https://thepeninsulaqatar.com/" },
            { nombre: "Qatar Tribune", url: "https://qatar-tribune.com/" }
        ],
        maec: "https://www.exteriores.gob.es/Consulados/Doha/Paginas/Recomendaciones-de-Viaje.aspx",
        embajada: "https://www.exteriores.gob.es/Consulados/Doha",
        telefono_embajada: "+974 4429 3300"
    },
    
    // Europa
    "rusia": {
        prensa: [
            { nombre: "Moscow Times", url: "https://www.themoscowtimes.com/" },
            { nombre: "Russia Today", url: "https://www.rt.com/" }
        ],
        maec: "https://www.exteriores.gob.es/Consulados/Moscu/Paginas/Recomendaciones-de-Viaje.aspx",
        embajada: "https://www.exteriores.gob.es/Consulados/Moscu",
        telefono_embajada: "+7 495 783 0850"
    },
    "españa": {
        prensa: [
            { nombre: "El País", url: "https://elpais.com/" },
            { nombre: "El Mundo", url: "https://www.elmundo.es/" }
        ],
        maec: "https://www.exteriores.gob.es/",
        embajada: "https://www.exteriores.gob.es/",
        telefono_embajada: "+34 91 379 9700"
    },
    
    // América
    "estados unidos": {
        prensa: [
            { nombre: "New York Times", url: "https://www.nytimes.com/" },
            { nombre: "USA Today", url: "https://www.usatoday.com/" }
        ],
        maec: "https://www.exteriores.gob.es/Consulados/Washington/Paginas/Recomendaciones-de-Viaje.aspx",
        embajada: "https://www.exteriores.gob.es/Consulados/Washington",
        telefono_embajada: "+1 202 452 0100"
    },
    "mexico": {
        prensa: [
            { nombre: "El Universal", url: "https://www.eluniversal.com.mx/" },
            { nombre: "Milenio", url: "https://www.milenio.com/" }
        ],
        maec: "https://www.exteriores.gob.es/Consulados/Mexico/Paginas/Recomendaciones-de-Viaje.aspx",
        embajada: "https://www.exteriores.gob.es/Consulados/Mexico",
        telefono_embajada: "+52 55 5281 3760"
    },
    
    // África
    "egipto": {
        prensa: [
            { nombre: "Egypt Today", url: "https://www.egypttoday.com/" },
            { nombre: "Al Ahram", url: "https://english.ahram.org.eg/" }
        ],
        maec: "https://www.exteriores.gob.es/Consulados/ElCairo/Paginas/Recomendaciones-de-Viaje.aspx",
        embajada: "https://www.exteriores.gob.es/Consulados/ElCairo",
        telefono_embajada: "+20 2 2795 6500"
    },
    "marruecos": {
        prensa: [
            { nombre: "Morocco World News", url: "https://www.moroccoworldnews.com/" },
            { nombre: "Hespress", url: "https://en.hespress.com/" }
        ],
        maec: "https://www.exteriores.gob.es/Consulados/Rabat/Paginas/Recomendaciones-de-Viaje.aspx",
        embajada: "https://www.exteriores.gob.es/Consulados/Rabat",
        telefono_embajada: "+212 537 63 36 00"
    }
};

// Vacunas OMS - Listado actualizado por país
const VACUNAS_OMS = {
    "china": ["Hepatitis A", "Fiebre tifoidea", "Encefalitis japonesa", "Rabia"],
    "tailandia": ["Hepatitis A", "Fiebre tifoidea", "Dengue", "Rabia"],
    "india": ["Hepatitis A", "Fiebre tifoidea", "Fiebre amarilla", "Rabia", "Encefalitis japonesa"],
    "indonesia": ["Hepatitis A", "Fiebre tifoidea", "Fiebre amarilla", "Dengue"],
    "vietnam": ["Hepatitis A", "Fiebre tifoidea", "Encefalitis japonesa", "Rabia"],
    "egipto": ["Hepatitis A", "Fiebre tifoidea", "Fiebre amarilla"],
    "marruecos": ["Hepatitis A", "Fiebre tifoidea", "Rabia"]
};

function getRecursosPais(pais) {
    return RECURSOS_POR_PAIS[pais] || {
        prensa: [
            { nombre: "Google News", url: `https://news.google.com/search?q=${pais}` },
            { nombre: "BBC News", url: "https://www.bbc.com/" }
        ],
        maec: "https://www.exteriores.gob.es/ConsejeriaDeViajeros/Paginas/RecomendacionesDeViaje.aspx",
        embajada: "https://www.exteriores.gob.es/",
        telefono_embajada: "+34 91 379 9700"
    };
}

function getVacunasPais(pais) {
    return VACUNAS_OMS[pais] || ["Hepatitis A", "Fiebre tifoidea", "Tétanos"];
}

function mostrarRecursos(pais) {
    const recursos = getRecursosPais(pais);
    const vacunas = getVacunasPais(pais);
    
    let html = `
        <div style="margin-top: 20px; padding-top: 20px; border-top: 2px solid rgba(255,255,255,0.2);">
            <h4>📰 PRENSA LOCAL (${recursos.prensa.length} diarios)</h4>
            <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 15px;">
    `;
    
    for (const diario of recursos.prensa) {
        html += `<a href="${diario.url}" target="_blank" style="background:rgba(255,255,255,0.2);padding:5px 12px;border-radius:20px;text-decoration:none;color:white;">📰 ${diario.nombre}</a>`;
    }
    
    html += `
            </div>
            <h4>🏥 VACUNAS RECOMENDADAS (OMS)</h4>
            <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 15px;">
    `;
    
    for (const vacuna of vacunas) {
        html += `<span style="background:rgba(255,255,255,0.15);padding:4px 10px;border-radius:15px;">💉 ${vacuna}</span>`;
    }
    
    html += `
            </div>
            <h4>📋 ENLACES OFICIALES</h4>
            <div style="display: flex; gap: 15px; flex-wrap: wrap;">
                <a href="${recursos.maec}" target="_blank" style="color:white;">🇪🇸 MAEC - Recomendaciones</a>
                <a href="${recursos.embajada}" target="_blank" style="color:white;">🏛️ Embajada</a>
                <a href="https://www.who.int/travel-advice" target="_blank" style="color:white;">🌍 OMS - Viajes</a>
                <a href="https://www.sanidad.gob.es/" target="_blank" style="color:white;">🏥 Sanidad España</a>
            </div>
            <p style="margin-top: 15px;"><strong>📞 Teléfono Embajada:</strong> ${recursos.telefono_embajada}</p>
        </div>
    `;
    
    return html;
}
