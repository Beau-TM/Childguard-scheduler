// Dashboard JS – Childguard Scheduler – Leerkracht

document.addEventListener('DOMContentLoaded', function () {

    // Automatisch alerts verbergen na 5 seconden
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.transition = 'opacity .4s ease';
            alert.style.opacity = '0';
            setTimeout(function () { alert.remove(); }, 400);
        }, 5000);
    });

    // Huidige datum instellen in de pagina header
    const datumEl = document.getElementById('huidige-datum');
    if (datumEl) {
        const nu = new Date();
        const opties = { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' };
        datumEl.textContent = nu.toLocaleDateString('nl-BE', opties);
    }

});