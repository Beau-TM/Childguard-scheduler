// Gezamenlijke Kalender JS – Childguard Scheduler

document.addEventListener('DOMContentLoaded', function () {

    const overlay = document.getElementById('popup-overlay');
    const popupInhoud = document.getElementById('popup-inhoud');
    const popupDatum  = document.getElementById('popup-datum');
    const popupDag    = document.getElementById('popup-dag');

    // Klik op een dag cel
    document.querySelectorAll('.dag-cel[data-datum]').forEach(function (cel) {
        cel.addEventListener('click', function () {
            const datum    = cel.dataset.datum;
            const dagNaam  = cel.dataset.dagnaam;
            const datumObj = new Date(datum + 'T00:00:00');
            const opties   = { day: 'numeric', month: 'long', year: 'numeric' };

            popupDatum.textContent = datumObj.toLocaleDateString('nl-BE', opties);
            popupDag.textContent   = dagNaam;

            // Bouw inhoud op basis van data-attributen
            const bewakingData = cel.dataset.bewakingen;
            let html = '';

            if (bewakingData && bewakingData !== '[]') {
                const bewakingen = JSON.parse(bewakingData);

                // Groepeer per moment
                const momenten = {};
                bewakingen.forEach(function (b) {
                    if (!momenten[b.moment]) momenten[b.moment] = {};
                    if (!momenten[b.moment][b.speelplaats]) momenten[b.moment][b.speelplaats] = [];
                    momenten[b.moment][b.speelplaats].push(b);
                });

                const momentVolgorde = ['ochtend', 'middag', 'namiddag'];
                const momentTijden  = {
                    'ochtend':  '10:05 – 10:20',
                    'middag':   '12:05 – 13:20',
                    'namiddag': '14:10 – 14:25'
                };
                const momentIcoon = {
                    'ochtend':  '<path d="M6.76 4.84l-1.8-1.79-1.41 1.41 1.79 1.79 1.42-1.41zM4 10.5H1v2h3v-2zm9-9.95h-2V3.5h2V.55zm7.45 3.91l-1.41-1.41-1.79 1.79 1.41 1.41 1.79-1.79zm-3.21 13.7l1.79 1.8 1.41-1.41-1.8-1.79-1.4 1.4zM20 10.5v2h3v-2h-3zm-8-5c-3.31 0-6 2.69-6 6s2.69 6 6 6 6-2.69 6-6-2.69-6-6-6zm-1 16.95h2V19.5h-2v2.95zm-7.45-3.91l1.41 1.41 1.79-1.8-1.41-1.41-1.79 1.8z"/>',
                    'middag':   '<path d="M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5zM2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1zm18 0h2c.55 0 1-.45 1-1s-.45-1-1-1h-2c-.55 0-1 .45-1 1s.45 1 1 1zM11 2v2c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1zm0 18v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1z"/>',
                    'namiddag': '<path d="M12 3a9 9 0 1 0 0 18A9 9 0 0 0 12 3zm0 16c-3.87 0-7-3.13-7-7s3.13-7 7-7 7 3.13 7 7-3.13 7-7 7zm1-11h-2v5l4 2.5.75-1.23L13 12V8z"/>',
                };

                momentVolgorde.forEach(function (moment) {
                    if (!momenten[moment]) return;

                    html += `<div class="popup-moment">
                        <div class="popup-moment-titel">
                            <svg viewBox="0 0 24 24" fill="currentColor">${momentIcoon[moment]}</svg>
                            ${moment.charAt(0).toUpperCase() + moment.slice(1)}
                            <span class="popup-moment-tijd">${momentTijden[moment]}</span>
                        </div>`;

                    Object.entries(momenten[moment]).forEach(function ([sp, leerkrachten]) {
                        html += `<div class="popup-speelplaats">
                            <div class="popup-sp-naam">${sp}</div>
                            <div class="popup-lk-lijst">`;

                        leerkrachten.forEach(function (lk) {
                            const isMij = lk.is_mij ? ' is-mij' : '';
                            html += `<div class="popup-lk${isMij}">
                                <span class="popup-lk-dot"></span>
                                ${lk.naam}${lk.is_mij ? ' (u)' : ''}
                            </div>`;
                        });

                        html += `</div></div>`;
                    });

                    html += `</div>`;
                });
            } else {
                html = `<div class="popup-leeg">
                    <svg viewBox="0 0 24 24"><path d="M20 3h-1V1h-2v2H7V1H5v2H4c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 18H4V8h16v13z"/></svg>
                    Geen bewakingen gepland
                </div>`;
            }

            popupInhoud.innerHTML = html;
            overlay.classList.add('actief');
        });
    });

    // Popup sluiten
    document.getElementById('popup-sluit').addEventListener('click', sluitPopup);
    overlay.addEventListener('click', function (e) {
        if (e.target === overlay) sluitPopup();
    });
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') sluitPopup();
    });

    function sluitPopup() {
        overlay.classList.remove('actief');
    }

    // Maand dropdown navigatie
    const maandSelect = document.getElementById('maand-select');
    if (maandSelect) {
        maandSelect.addEventListener('change', function () {
            const [jaar, maand] = this.value.split('-');
            window.location.href = `?jaar=${jaar}&maand=${maand}`;
        });
    }

});