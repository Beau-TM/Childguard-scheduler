from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from accounts.models import UserProfile
from django.contrib.auth.models import User
import calendar
from datetime import date


# ── FEESTDAGEN BELGIË tot 2030 ──
WETTELIJKE_FEESTDAGEN = [
    # 2025
    {'datum': date(2025,1,1),   'naam': 'Nieuwjaar'},
    {'datum': date(2025,4,21),  'naam': 'Paasmaandag'},
    {'datum': date(2025,5,1),   'naam': 'Dag van de Arbeid'},
    {'datum': date(2025,5,29),  'naam': 'O.H. Hemelvaart'},
    {'datum': date(2025,6,9),   'naam': 'Pinkstermaandag'},
    {'datum': date(2025,7,21),  'naam': 'Nationale Feestdag'},
    {'datum': date(2025,8,15),  'naam': 'O.L.V. Hemelvaart'},
    {'datum': date(2025,11,1),  'naam': 'Allerheiligen'},
    {'datum': date(2025,11,11), 'naam': 'Wapenstilstand'},
    {'datum': date(2025,12,25), 'naam': 'Kerstmis'},
    # 2026
    {'datum': date(2026,1,1),   'naam': 'Nieuwjaar'},
    {'datum': date(2026,4,6),   'naam': 'Paasmaandag'},
    {'datum': date(2026,5,1),   'naam': 'Dag van de Arbeid'},
    {'datum': date(2026,5,14),  'naam': 'O.H. Hemelvaart'},
    {'datum': date(2026,5,25),  'naam': 'Pinkstermaandag'},
    {'datum': date(2026,7,21),  'naam': 'Nationale Feestdag'},
    {'datum': date(2026,8,15),  'naam': 'O.L.V. Hemelvaart'},
    {'datum': date(2026,11,1),  'naam': 'Allerheiligen'},
    {'datum': date(2026,11,11), 'naam': 'Wapenstilstand'},
    {'datum': date(2026,12,25), 'naam': 'Kerstmis'},
    # 2027
    {'datum': date(2027,1,1),   'naam': 'Nieuwjaar'},
    {'datum': date(2027,3,29),  'naam': 'Paasmaandag'},
    {'datum': date(2027,5,1),   'naam': 'Dag van de Arbeid'},
    {'datum': date(2027,5,6),   'naam': 'O.H. Hemelvaart'},
    {'datum': date(2027,5,17),  'naam': 'Pinkstermaandag'},
    {'datum': date(2027,7,21),  'naam': 'Nationale Feestdag'},
    {'datum': date(2027,8,15),  'naam': 'O.L.V. Hemelvaart'},
    {'datum': date(2027,11,1),  'naam': 'Allerheiligen'},
    {'datum': date(2027,11,11), 'naam': 'Wapenstilstand'},
    {'datum': date(2027,12,25), 'naam': 'Kerstmis'},
    # 2028
    {'datum': date(2028,1,1),   'naam': 'Nieuwjaar'},
    {'datum': date(2028,4,17),  'naam': 'Paasmaandag'},
    {'datum': date(2028,5,1),   'naam': 'Dag van de Arbeid'},
    {'datum': date(2028,5,25),  'naam': 'O.H. Hemelvaart'},
    {'datum': date(2028,6,5),   'naam': 'Pinkstermaandag'},
    {'datum': date(2028,7,21),  'naam': 'Nationale Feestdag'},
    {'datum': date(2028,8,15),  'naam': 'O.L.V. Hemelvaart'},
    {'datum': date(2028,11,1),  'naam': 'Allerheiligen'},
    {'datum': date(2028,11,11), 'naam': 'Wapenstilstand'},
    {'datum': date(2028,12,25), 'naam': 'Kerstmis'},
    # 2029
    {'datum': date(2029,1,1),   'naam': 'Nieuwjaar'},
    {'datum': date(2029,4,2),   'naam': 'Paasmaandag'},
    {'datum': date(2029,5,1),   'naam': 'Dag van de Arbeid'},
    {'datum': date(2029,5,10),  'naam': 'O.H. Hemelvaart'},
    {'datum': date(2029,5,21),  'naam': 'Pinkstermaandag'},
    {'datum': date(2029,7,21),  'naam': 'Nationale Feestdag'},
    {'datum': date(2029,8,15),  'naam': 'O.L.V. Hemelvaart'},
    {'datum': date(2029,11,1),  'naam': 'Allerheiligen'},
    {'datum': date(2029,11,11), 'naam': 'Wapenstilstand'},
    {'datum': date(2029,12,25), 'naam': 'Kerstmis'},
    # 2030
    {'datum': date(2030,1,1),   'naam': 'Nieuwjaar'},
    {'datum': date(2030,4,22),  'naam': 'Paasmaandag'},
    {'datum': date(2030,5,1),   'naam': 'Dag van de Arbeid'},
    {'datum': date(2030,5,30),  'naam': 'O.H. Hemelvaart'},
    {'datum': date(2030,6,10),  'naam': 'Pinkstermaandag'},
    {'datum': date(2030,7,21),  'naam': 'Nationale Feestdag'},
    {'datum': date(2030,8,15),  'naam': 'O.L.V. Hemelvaart'},
    {'datum': date(2030,11,1),  'naam': 'Allerheiligen'},
    {'datum': date(2030,11,11), 'naam': 'Wapenstilstand'},
    {'datum': date(2030,12,25), 'naam': 'Kerstmis'},
]

# ── VLAAMSE SCHOOLVAKANTIES tot 2030 ──
SCHOOLVAKANTIES = [

    # Zomervakantie 2025
    {'datum': date(2025,7,1),  'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,7,2),  'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,7,3),  'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,7,4),  'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,7,7),  'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,7,8),  'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,7,9),  'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,7,10), 'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,7,11), 'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,7,14), 'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,7,15), 'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,7,16), 'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,7,17), 'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,7,18), 'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,7,21), 'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,7,22), 'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,7,23), 'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,7,24), 'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,7,25), 'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,7,28), 'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,7,29), 'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,7,30), 'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,7,31), 'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,8,1),  'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,8,4),  'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,8,5),  'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,8,6),  'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,8,7),  'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,8,8),  'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,8,11), 'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,8,12), 'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,8,13), 'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,8,14), 'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,8,15), 'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,8,18), 'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,8,19), 'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,8,20), 'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,8,21), 'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,8,22), 'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,8,25), 'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,8,26), 'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,8,27), 'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,8,28), 'naam': 'Zomervakantie 2025'},
    {'datum': date(2025,8,29), 'naam': 'Zomervakantie 2025'},
    # Zomervakantie 2026
    {'datum': date(2026,7,1),  'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,7,2),  'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,7,3),  'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,7,6),  'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,7,7),  'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,7,8),  'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,7,9),  'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,7,10), 'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,7,13), 'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,7,14), 'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,7,15), 'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,7,16), 'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,7,17), 'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,7,20), 'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,7,22), 'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,7,23), 'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,7,24), 'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,7,27), 'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,7,28), 'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,7,29), 'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,7,30), 'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,7,31), 'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,8,3),  'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,8,4),  'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,8,5),  'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,8,6),  'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,8,7),  'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,8,10), 'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,8,11), 'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,8,12), 'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,8,13), 'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,8,17), 'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,8,18), 'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,8,19), 'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,8,20), 'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,8,21), 'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,8,24), 'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,8,25), 'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,8,26), 'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,8,27), 'naam': 'Zomervakantie 2026'},
    {'datum': date(2026,8,28), 'naam': 'Zomervakantie 2026'},
    # 2025-2026
    {'datum': date(2025,10,27), 'naam': 'Herfstvakantie 2025'},
    {'datum': date(2025,10,28), 'naam': 'Herfstvakantie 2025'},
    {'datum': date(2025,10,29), 'naam': 'Herfstvakantie 2025'},
    {'datum': date(2025,10,30), 'naam': 'Herfstvakantie 2025'},
    {'datum': date(2025,10,31), 'naam': 'Herfstvakantie 2025'},
    {'datum': date(2025,12,22), 'naam': 'Kerstvakantie 2025'},
    {'datum': date(2025,12,23), 'naam': 'Kerstvakantie 2025'},
    {'datum': date(2025,12,24), 'naam': 'Kerstvakantie 2025'},
    {'datum': date(2025,12,25), 'naam': 'Kerstvakantie 2025'},
    {'datum': date(2025,12,26), 'naam': 'Kerstvakantie 2025'},
    {'datum': date(2025,12,29), 'naam': 'Kerstvakantie 2025'},
    {'datum': date(2025,12,30), 'naam': 'Kerstvakantie 2025'},
    {'datum': date(2025,12,31), 'naam': 'Kerstvakantie 2025'},
    {'datum': date(2026,1,2),   'naam': 'Kerstvakantie 2026'},
    {'datum': date(2026,2,16),  'naam': 'Krokusvakantie 2026'},
    {'datum': date(2026,2,17),  'naam': 'Krokusvakantie 2026'},
    {'datum': date(2026,2,18),  'naam': 'Krokusvakantie 2026'},
    {'datum': date(2026,2,19),  'naam': 'Krokusvakantie 2026'},
    {'datum': date(2026,2,20),  'naam': 'Krokusvakantie 2026'},
    {'datum': date(2026,4,6),   'naam': 'Paasvakantie 2026'},
    {'datum': date(2026,4,7),   'naam': 'Paasvakantie 2026'},
    {'datum': date(2026,4,8),   'naam': 'Paasvakantie 2026'},
    {'datum': date(2026,4,9),   'naam': 'Paasvakantie 2026'},
    {'datum': date(2026,4,10),  'naam': 'Paasvakantie 2026'},
    {'datum': date(2026,4,13),  'naam': 'Paasvakantie 2026'},
    {'datum': date(2026,4,14),  'naam': 'Paasvakantie 2026'},
    {'datum': date(2026,4,15),  'naam': 'Paasvakantie 2026'},
    {'datum': date(2026,4,16),  'naam': 'Paasvakantie 2026'},
    {'datum': date(2026,4,17),  'naam': 'Paasvakantie 2026'},
    # 2026-2027
    {'datum': date(2026,11,2),  'naam': 'Herfstvakantie 2026'},
    {'datum': date(2026,11,3),  'naam': 'Herfstvakantie 2026'},
    {'datum': date(2026,11,4),  'naam': 'Herfstvakantie 2026'},
    {'datum': date(2026,11,5),  'naam': 'Herfstvakantie 2026'},
    {'datum': date(2026,11,6),  'naam': 'Herfstvakantie 2026'},
    {'datum': date(2026,12,21), 'naam': 'Kerstvakantie 2026'},
    {'datum': date(2026,12,22), 'naam': 'Kerstvakantie 2026'},
    {'datum': date(2026,12,23), 'naam': 'Kerstvakantie 2026'},
    {'datum': date(2026,12,24), 'naam': 'Kerstvakantie 2026'},
    {'datum': date(2026,12,25), 'naam': 'Kerstvakantie 2026'},
    {'datum': date(2026,12,28), 'naam': 'Kerstvakantie 2026'},
    {'datum': date(2026,12,29), 'naam': 'Kerstvakantie 2026'},
    {'datum': date(2026,12,30), 'naam': 'Kerstvakantie 2026'},
    {'datum': date(2026,12,31), 'naam': 'Kerstvakantie 2026'},
    {'datum': date(2027,1,4),   'naam': 'Kerstvakantie 2027'},
    {'datum': date(2027,3,1),   'naam': 'Krokusvakantie 2027'},
    {'datum': date(2027,3,2),   'naam': 'Krokusvakantie 2027'},
    {'datum': date(2027,3,3),   'naam': 'Krokusvakantie 2027'},
    {'datum': date(2027,3,4),   'naam': 'Krokusvakantie 2027'},
    {'datum': date(2027,3,5),   'naam': 'Krokusvakantie 2027'},
    {'datum': date(2027,3,29),  'naam': 'Paasvakantie 2027'},
    {'datum': date(2027,3,30),  'naam': 'Paasvakantie 2027'},
    {'datum': date(2027,3,31),  'naam': 'Paasvakantie 2027'},
    {'datum': date(2027,4,1),   'naam': 'Paasvakantie 2027'},
    {'datum': date(2027,4,2),   'naam': 'Paasvakantie 2027'},
    {'datum': date(2027,4,6),   'naam': 'Paasvakantie 2027'},
    {'datum': date(2027,4,7),   'naam': 'Paasvakantie 2027'},
    {'datum': date(2027,4,8),   'naam': 'Paasvakantie 2027'},
    {'datum': date(2027,4,9),   'naam': 'Paasvakantie 2027'},
]

# Alle vrije dagen voor het planningsalgoritme
FEESTDAGEN = [f['datum'] for f in WETTELIJKE_FEESTDAGEN] + [v['datum'] for v in SCHOOLVAKANTIES]


def directie_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        try:
            if not request.user.profile.is_directie:
                return redirect('leerkracht:dashboard')
        except UserProfile.DoesNotExist:
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    return wrapper


def get_schooldagen(jaar, maand):
    _, aantal_dagen = calendar.monthrange(jaar, maand)
    return [
        date(jaar, maand, dag)
        for dag in range(1, aantal_dagen + 1)
        if date(jaar, maand, dag).weekday() < 5
        and date(jaar, maand, dag) not in FEESTDAGEN
    ]


def genereer_planning_algoritme(leerkrachten, schooldagen, bewakingen_per_dag):
    momenten      = ['ochtend', 'middag', 'namiddag'][:bewakingen_per_dag]
    speelplaatsen = ['Grote Speelplaats', 'Kleine Speelplaats']
    lk_per_sp     = 2

    totaal_gewicht    = sum(lk.werkregime for lk in leerkrachten)
    totaal_bewakingen = len(schooldagen) * len(momenten) * len(speelplaatsen) * lk_per_sp

    quota  = {lk.user.id: round((lk.werkregime / totaal_gewicht) * totaal_bewakingen) for lk in leerkrachten}
    teller = {lk.user.id: 0 for lk in leerkrachten}
    planning = {}

    for dag in schooldagen:
        planning[dag] = {}
        for moment in momenten:
            toegewezen_vandaag = []
            bewakingen_moment  = []
            for sp in speelplaatsen:
                for _ in range(lk_per_sp):
                    kandidaten = sorted(
                        [lk for lk in leerkrachten
                         if lk.user.id not in toegewezen_vandaag
                         and teller[lk.user.id] < quota[lk.user.id]],
                        key=lambda lk: teller[lk.user.id]
                    )
                    if not kandidaten:
                        kandidaten = sorted(
                            [lk for lk in leerkrachten if lk.user.id not in toegewezen_vandaag],
                            key=lambda lk: teller[lk.user.id]
                        )
                    if kandidaten:
                        gekozen = kandidaten[0]
                        teller[gekozen.user.id] += 1
                        toegewezen_vandaag.append(gekozen.user.id)
                        bewakingen_moment.append({
                            'naam':    gekozen.user.get_full_name() or gekozen.user.username,
                            'sp':      sp,
                            'user_id': gekozen.user.id,
                        })
            planning[dag][moment] = bewakingen_moment

    return planning, teller


def initialiseer_wettelijke_dagen():
    from directie.models import SpecialeDag
    for f in WETTELIJKE_FEESTDAGEN:
        SpecialeDag.objects.get_or_create(
            datum=f['datum'], type='feestdag',
            defaults={'beschrijving': f['naam'], 'is_wettelijk': True}
        )
    for v in SCHOOLVAKANTIES:
        SpecialeDag.objects.get_or_create(
            datum=v['datum'], type='vakantie',
            defaults={'beschrijving': v['naam'], 'is_wettelijk': True}
        )


def get_academiejaar():
    """Geeft het huidige academiejaar terug als (start_jaar, eind_jaar)."""
    nu = date.today()
    if nu.month >= 9:
        return nu.year, nu.year + 1
    else:
        return nu.year - 1, nu.year


@directie_required
def speciale_dagen(request):
    from directie.models import SpecialeDag

    initialiseer_wettelijke_dagen()

    if request.method == 'POST':
        actie = request.POST.get('actie')
        if actie == 'toevoegen':
            datum        = request.POST.get('datum')
            type_dag     = request.POST.get('type', 'feestdag')
            beschrijving = request.POST.get('beschrijving', '')
            if datum:
                SpecialeDag.objects.get_or_create(
                    datum=datum,
                    defaults={'type': type_dag, 'beschrijving': beschrijving, 'is_wettelijk': False}
                )
                messages.success(request, f'Speciale dag toegevoegd!')
            else:
                messages.error(request, 'Datum is verplicht.')
        elif actie == 'verwijderen':
            dag_id = request.POST.get('dag_id')
            try:
                dag = SpecialeDag.objects.get(id=dag_id, is_wettelijk=False)
                dag.delete()
                messages.success(request, 'Speciale dag verwijderd.')
            except SpecialeDag.DoesNotExist:
                messages.error(request, 'Kan deze dag niet verwijderen.')
        return redirect('directie:speciale_dagen')

    start_jaar, eind_jaar = get_academiejaar()
    start_datum = date(start_jaar, 9, 1)
    eind_datum  = date(eind_jaar, 8, 31)
    huidig_jaar = date.today().year

    eigen_dagen = SpecialeDag.objects.filter(
        datum__gte=start_datum, datum__lte=eind_datum, is_wettelijk=False
    )

    telling = {
        'pedagogische_studiedag': eigen_dagen.filter(type='pedagogische_studiedag').count(),
        'facultatieve_vrije_dag': eigen_dagen.filter(type='facultatieve_vrije_dag').count(),
        'extra':                  eigen_dagen.filter(type='extra').count(),
        'totaal':                 eigen_dagen.count(),
        'feestdagen_jaar': len([f for f in WETTELIJKE_FEESTDAGEN if f['datum'].year == huidig_jaar]),
        'vakanties_jaar':  len([v for v in SCHOOLVAKANTIES
                                if date(start_jaar, 9, 1) <= v['datum'] <= date(eind_jaar, 8, 31)]),
    }

    context = {
        'eigen_dagen':  eigen_dagen,
        'telling':      telling,
        'huidig_jaar':  huidig_jaar,
        'academiejaar': f'{start_jaar}-{eind_jaar}',
    }
    return render(request, 'directie/speciale_dagen.html', context)


@directie_required
def planning_genereren(request):
    nu = timezone.now()
    maanden_nl = ['januari','februari','maart','april','mei','juni',
                  'juli','augustus','september','oktober','november','december']

    beschikbare_maanden = []
    for i in range(7):
        m = (nu.month - 1 + i) % 12
        j = nu.year + ((nu.month - 1 + i) // 12)
        beschikbare_maanden.append({
            'value': f'{j}-{str(m+1).zfill(2)}',
            'label': f'{maanden_nl[m]} {j}',
        })

    leerkrachten         = UserProfile.objects.filter(role='leerkracht').select_related('user')
    planning_gegenereerd = request.session.pop('planning_gegenereerd', False)

    if request.method == 'POST':
        maand_str          = request.POST.get('maand', f'{nu.year}-{str(nu.month).zfill(2)}')
        bewakingen_per_dag = int(request.POST.get('bewakingen_per_dag', 3))
        try:
            jaar, maand = map(int, maand_str.split('-'))
        except ValueError:
            jaar, maand = nu.year, nu.month

        if not leerkrachten.exists():
            messages.error(request, 'Voeg eerst leerkrachten toe.')
            return redirect('directie:planning_genereren')

        schooldagen = get_schooldagen(jaar, maand)
        if not schooldagen:
            messages.error(request, 'Geen schooldagen gevonden voor deze maand.')
            return redirect('directie:planning_genereren')

        planning, teller = genereer_planning_algoritme(list(leerkrachten), schooldagen, bewakingen_per_dag)

        # Opslaan in DB — bewaar alle vorige planningen
        from directie.models import Planning, Bewaking
        from django.contrib.auth.models import User as AuthUser
        planning_obj = Planning.objects.create(
            jaar=jaar, maand=maand, aangemaakt_door=request.user
        )
        bewakingen_bulk = []
        for dag, momenten in planning.items():
            for moment, toewijzingen in momenten.items():
                for t in toewijzingen:
                    bewakingen_bulk.append(Bewaking(
                        planning=planning_obj,
                        leerkracht_id=t['user_id'],
                        datum=dag,
                        moment=moment,
                        speelplaats=t['sp'],
                    ))
        Bewaking.objects.bulk_create(bewakingen_bulk)

        request.session['planning_gegenereerd'] = True
        request.session['planning_maand']       = maand_str
        messages.success(request, f'Planning voor {maanden_nl[maand-1]} {jaar} succesvol gegenereerd en opgeslagen!')
        return redirect('directie:planning_genereren')

    context = {
        'beschikbare_maanden':  beschikbare_maanden,
        'geselecteerde_maand':  f'{nu.year}-{str(nu.month).zfill(2)}',
        'bewakingen_per_dag':   3,
        'leerkrachten':         leerkrachten,
        'actieve_leerkrachten': leerkrachten.count(),
        'totaal_leerkrachten':  leerkrachten.count(),
        'planning_gegenereerd': planning_gegenereerd,
    }
    return render(request, 'directie/planning_genereren.html', context)


@directie_required
def kalender(request):
    return render(request, 'directie/kalender.html')


@directie_required
def dashboard(request):
    from directie.models import Afmelding
    leerkracht_profielen = UserProfile.objects.filter(role='leerkracht')
    actieve_leerkrachten = leerkracht_profielen.count()
    maanden = ['januari','februari','maart','april','mei','juni',
               'juli','augustus','september','oktober','november','december']
    dagen   = ['maandag','dinsdag','woensdag','donderdag','vrijdag','zaterdag','zondag']
    nu = timezone.now()

    nieuwe_afmeldingen = Afmelding.objects.filter(status='nieuw').count()
    te_verwerken       = Afmelding.objects.filter(status__in=['nieuw','verwerkt']).count()
    recente_afmeldingen = Afmelding.objects.filter(
        status='nieuw'
    ).select_related('leerkracht').order_by('-aangemaakt')[:5]

    context = {
        'actieve_leerkrachten': actieve_leerkrachten,
        'totaal_leerkrachten':  actieve_leerkrachten,
        'planning_percentage':  0,
        'planning_toegewezen':  0,
        'planning_totaal':      0,
        'open_problemen':       nieuwe_afmeldingen,
        'nieuwe_afmeldingen':   nieuwe_afmeldingen,
        'te_verwerken':         te_verwerken,
        'recente_afmeldingen':  recente_afmeldingen,
        'huidige_maand':        f"{maanden[nu.month-1]} {nu.year}",
        'vandaag':              f"{dagen[nu.weekday()]} {nu.day} {maanden[nu.month-1]} {nu.year}",
        'bewakingen_vandaag': {
            'ochtend_groot': None, 'ochtend_klein': None,
            'middag_groot':  None, 'middag_klein':  None,
            'namiddag_groot':None, 'namiddag_klein':None,
        },
    }
    return render(request, 'directie/dashboard.html', context)


def zoek_vervanger(afmelding):
    """
    Zoek automatisch een geschikte vervanger voor een afmelding.
    Kiest de leerkracht met de minste bewakingen die die dag niet al een bewaking heeft.
    """
    from directie.models import Afmelding
    datum = afmelding.datum
    # Alle leerkrachten behalve de zieke
    kandidaten = UserProfile.objects.filter(role='leerkracht').exclude(user=afmelding.leerkracht)
    # Filter weg wie die dag ook afwezig is
    afwezigen_ids = Afmelding.objects.filter(
        datum=datum, status__in=['nieuw', 'verwerkt']
    ).values_list('leerkracht_id', flat=True)
    kandidaten = kandidaten.exclude(user__id__in=afwezigen_ids)
    if not kandidaten.exists():
        return None
    # Kies degene met minste vervangingen deze maand
    from django.db.models import Count
    kandidaat = (
        kandidaten
        .annotate(aantal=Count('user__vervangingen'))
        .order_by('aantal')
        .first()
    )
    return kandidaat.user if kandidaat else None


@directie_required
def afmeldingen(request):
    from directie.models import Afmelding
    from accounts.models import UserProfile

    if request.method == 'POST':
        actie = request.POST.get('actie')

        if actie == 'toevoegen':
            leerkracht_id = request.POST.get('leerkracht_id')
            datum         = request.POST.get('datum')
            reden         = request.POST.get('reden', '')
            auto_vervang  = request.POST.get('auto_vervanger') == 'on'
            try:
                leerkracht = User.objects.get(id=leerkracht_id)
                afmelding  = Afmelding.objects.create(
                    leerkracht=leerkracht,
                    datum=datum,
                    reden=reden,
                    status='nieuw',
                )
                if auto_vervang:
                    vervanger = zoek_vervanger(afmelding)
                    if vervanger:
                        afmelding.vervanger = vervanger
                        afmelding.status    = 'verwerkt'
                        afmelding.save()
                        messages.success(request,
                            f'Afmelding aangemaakt. Vervanger: {vervanger.get_full_name() or vervanger.username}')
                    else:
                        messages.warning(request,
                            'Afmelding aangemaakt maar geen geschikte vervanger gevonden. Wijs manueel aan.')
                else:
                    messages.success(request, 'Afmelding aangemaakt.')
            except User.DoesNotExist:
                messages.error(request, 'Leerkracht niet gevonden.')

        elif actie == 'vervanger_instellen':
            afmelding_id  = request.POST.get('afmelding_id')
            vervanger_id  = request.POST.get('vervanger_id')
            try:
                afmelding = Afmelding.objects.get(id=afmelding_id)
                vervanger = User.objects.get(id=vervanger_id)
                afmelding.vervanger = vervanger
                afmelding.status    = 'verwerkt'
                afmelding.save()
                from directie.models import Notificatie
                zieke = afmelding.leerkracht.get_full_name() or afmelding.leerkracht.username
                datum_str = afmelding.datum.strftime('%d/%m/%Y')
                Notificatie.objects.create(
                    ontvanger=vervanger,
                    type='vervanger_aangesteld',
                    bericht=f'Je bent aangesteld als vervanger voor {zieke} op {datum_str}. Je hebt die dag bewaking.',
                    afmelding=afmelding,
                )
                messages.success(request,
                    f'{vervanger.get_full_name() or vervanger.username} ingesteld als vervanger.')
            except (Afmelding.DoesNotExist, User.DoesNotExist):
                messages.error(request, 'Fout bij instellen vervanger.')

        elif actie == 'auto_vervangen':
            afmelding_id = request.POST.get('afmelding_id')
            try:
                afmelding = Afmelding.objects.get(id=afmelding_id)
                vervanger = zoek_vervanger(afmelding)
                if vervanger:
                    afmelding.vervanger = vervanger
                    afmelding.status    = 'verwerkt'
                    afmelding.save()
                    from directie.models import Notificatie
                    zieke = afmelding.leerkracht.get_full_name() or afmelding.leerkracht.username
                    datum_str = afmelding.datum.strftime('%d/%m/%Y')
                    Notificatie.objects.create(
                        ontvanger=vervanger,
                        type='vervanger_aangesteld',
                        bericht=f'Je bent aangesteld als vervanger voor {zieke} op {datum_str}. Je hebt die dag bewaking.',
                        afmelding=afmelding,
                    )
                    messages.success(request,
                        f'Vervanger automatisch ingesteld: {vervanger.get_full_name() or vervanger.username}')
                else:
                    messages.warning(request, 'Geen geschikte vervanger gevonden.')
            except Afmelding.DoesNotExist:
                messages.error(request, 'Afmelding niet gevonden.')

        elif actie == 'oplossen':
            afmelding_id = request.POST.get('afmelding_id')
            try:
                afmelding        = Afmelding.objects.get(id=afmelding_id)
                afmelding.status = 'opgelost'
                afmelding.save()
                messages.success(request, 'Afmelding gemarkeerd als opgelost.')
            except Afmelding.DoesNotExist:
                messages.error(request, 'Afmelding niet gevonden.')

        elif actie == 'verwijderen':
            afmelding_id = request.POST.get('afmelding_id')
            try:
                Afmelding.objects.get(id=afmelding_id).delete()
                messages.success(request, 'Afmelding verwijderd.')
            except Afmelding.DoesNotExist:
                messages.error(request, 'Afmelding niet gevonden.')

        return redirect('directie:afmeldingen')

    alle_afmeldingen = Afmelding.objects.select_related('leerkracht', 'vervanger').all()
    leerkrachten_lijst = UserProfile.objects.filter(role='leerkracht').select_related('user')

    telling = {
        'nieuw':    alle_afmeldingen.filter(status='nieuw').count(),
        'verwerkt': alle_afmeldingen.filter(status='verwerkt').count(),
        'opgelost': alle_afmeldingen.filter(status='opgelost').count(),
    }

    context = {
        'afmeldingen':      alle_afmeldingen,
        'leerkrachten':     leerkrachten_lijst,
        'telling':          telling,
        'vandaag':          date.today(),
    }
    return render(request, 'directie/afmeldingen.html', context)


@directie_required
def verwerk_afmelding(request, afmelding_id):
    return redirect('directie:afmeldingen')


@directie_required
def leerkrachten(request):
    from accounts.models import UserProfile
    from directie.models import Afmelding
    from django.db.models import Count
    from datetime import date
    import calendar

    nu = date.today()
    eerste_dag = date(nu.year, nu.month, 1)
    _, laatste = calendar.monthrange(nu.year, nu.month)
    laatste_dag = date(nu.year, nu.month, laatste)

    leerkrachten_lijst = UserProfile.objects.filter(role='leerkracht').select_related('user')

    leerkrachten_data = []
    for lk in leerkrachten_lijst:
        # Bewakingen deze maand (als vervanger aangesteld)
        deze_maand = Afmelding.objects.filter(
            vervanger=lk.user,
            datum__gte=eerste_dag,
            datum__lte=laatste_dag,
        ).count()

        # Afmeldingen dit jaar
        dit_jaar = Afmelding.objects.filter(
            leerkracht=lk.user,
            datum__year=nu.year,
        ).count()

        # Is vandaag afgemeld?
        afgemeld_vandaag = Afmelding.objects.filter(
            leerkracht=lk.user,
            datum=nu,
            status__in=['nieuw', 'verwerkt']
        ).exists()

        leerkrachten_data.append({
            'profiel':        lk,
            'naam':           lk.user.get_full_name() or lk.user.username,
            'werkregime':     lk.get_werkregime_display(), #type:ignore
            'werkregime_pct': lk.werkregime,
            'deze_maand':     deze_maand,
            'dit_jaar':       dit_jaar,
            'afgemeld':       afgemeld_vandaag,
        })

    context = {
        'leerkrachten':      leerkrachten_data,
        'totaal':            leerkrachten_lijst.count(),
        'huidige_maand':     nu.strftime('%B %Y'),
    }
    return render(request, 'directie/leerkrachten.html', context)


@directie_required
def school_overzicht(request):
    from directie.models import Planning, Bewaking
    from accounts.models import UserProfile
    from django.utils import timezone
    import calendar

    nu = timezone.now()
    maanden_nl = ['januari','februari','maart','april','mei','juni',
                  'juli','augustus','september','oktober','november','december']

    # Haal de meest recente planning op, of die van deze maand
    try:
        planning_obj = Planning.objects.filter(
            jaar=nu.year, maand=nu.month
        ).latest('aangemaakt')
    except Planning.DoesNotExist:
        planning_obj = Planning.objects.order_by('-jaar', '-maand').first()

    leerkrachten = UserProfile.objects.filter(role='leerkracht').select_related('user')
    totaal_leerkrachten = leerkrachten.count()

    if planning_obj:
        alle_bewakingen = Bewaking.objects.filter(planning=planning_obj).select_related('leerkracht')
        totaal_bewakingen = alle_bewakingen.count()

        # Per leerkracht stats
        leerkracht_stats = []
        totaal_gewicht = sum(lk.werkregime for lk in leerkrachten)
        for lk in leerkrachten:
            aantal = alle_bewakingen.filter(leerkracht=lk.user).count()
            verwacht = round((lk.werkregime / totaal_gewicht) * totaal_bewakingen) if totaal_gewicht else 0
            aandeel = round((aantal / totaal_bewakingen) * 100, 1) if totaal_bewakingen else 0
            leerkracht_stats.append({
                'naam':     lk.user.get_full_name() or lk.user.username,
                'regime':   lk.werkregime,
                'aantal':   aantal,
                'verwacht': verwacht,
                'aandeel':  aandeel,
            })

        # Eerlijkheidsscore: hoe dicht zit iedereen bij verwacht?
        if leerkracht_stats and totaal_bewakingen:
            afwijkingen = [abs(s['aantal'] - s['verwacht']) for s in leerkracht_stats]
            gem_afwijking = sum(afwijkingen) / len(afwijkingen) if afwijkingen else 0
            max_afwijking = totaal_bewakingen / totaal_leerkrachten if totaal_leerkrachten else 1
            eerlijkheid = max(0, round(100 - (gem_afwijking / max_afwijking) * 100)) if max_afwijking else 100
        else:
            eerlijkheid = 100

        # Aankomende bewakingen (volgende 10 vanaf vandaag)
        from datetime import date as date_type
        aankomend = alle_bewakingen.filter(
            datum__gte=date_type.today()
        ).order_by('datum', 'moment').select_related('leerkracht')[:10]

        TIJDEN = {'ochtend': '10:05–10:20', 'middag': '12:05–13:20', 'namiddag': '14:10–14:25'}
        aankomend_data = [{
            'datum':       b.datum,
            'moment':      b.get_moment_display(),  # type: ignore
            'tijd':        TIJDEN.get(b.moment, ''),
            'speelplaats': b.speelplaats,
            'leerkracht':  b.leerkracht.get_full_name() or b.leerkracht.username,
        } for b in aankomend]

        planning_label = f"{maanden_nl[planning_obj.maand-1]} {planning_obj.jaar}"
    else:
        leerkracht_stats = []
        totaal_bewakingen = 0
        eerlijkheid = 100
        aankomend_data = []
        planning_label = 'Geen planning beschikbaar'

    # Alle beschikbare planningen voor dropdown
    alle_planningen = Planning.objects.all().order_by('-jaar', '-maand')

    context = {
        'planning':          planning_obj,
        'planning_label':    planning_label,
        'alle_planningen':   alle_planningen,
        'leerkracht_stats':  leerkracht_stats,
        'totaal_bewakingen': totaal_bewakingen,
        'totaal_leerkrachten': totaal_leerkrachten,
        'eerlijkheid':       eerlijkheid,
        'aankomend':         aankomend_data,
    }
    return render(request, 'directie/school_overzicht.html', context)


@directie_required
def planning_geschiedenis(request):
    from directie.models import Planning, Bewaking

    alle_planningen = Planning.objects.all().order_by('-jaar', '-maand', '-aangemaakt')

    planningen_data = []
    for p in alle_planningen:
        totaal = Bewaking.objects.filter(planning=p).count()
        planningen_data.append({
            'planning': p,
            'totaal':   totaal,
            'label':    str(p),
        })

    context = {
        'planningen': planningen_data,
    }
    return render(request, 'directie/planning_geschiedenis.html', context)


@directie_required
def planning_detail(request, planning_id):
    from directie.models import Planning, Bewaking

    try:
        planning_obj = Planning.objects.get(id=planning_id)
    except Planning.DoesNotExist:
        from django.http import Http404
        raise Http404

    bewakingen = Bewaking.objects.filter(
        planning=planning_obj
    ).select_related('leerkracht').order_by('datum', 'moment')

    # Groepeer per datum
    from collections import defaultdict
    per_dag = defaultdict(lambda: defaultdict(list))
    for b in bewakingen:
        per_dag[b.datum][b.moment].append({
            'naam':       b.leerkracht.get_full_name() or b.leerkracht.username,
            'speelplaats': b.speelplaats,
        })

    per_dag_lijst = []
    for datum in sorted(per_dag.keys()):
        per_dag_lijst.append({
            'datum':   datum,
            'momenten': dict(per_dag[datum]),
        })

    # Stats per leerkracht
    from accounts.models import UserProfile
    from django.db.models import Count
    leerkrachten = UserProfile.objects.filter(role='leerkracht').select_related('user')
    totaal_bewakingen = bewakingen.count()
    lk_stats = []
    for lk in leerkrachten:
        aantal = bewakingen.filter(leerkracht=lk.user).count()
        if aantal > 0:
            lk_stats.append({
                'naam':   lk.user.get_full_name() or lk.user.username,
                'aantal': aantal,
                'aandeel': round((aantal / totaal_bewakingen) * 100, 1) if totaal_bewakingen else 0,
            })
    lk_stats.sort(key=lambda x: x['aantal'], reverse=True)

    context = {
        'planning':          planning_obj,
        'per_dag':           per_dag_lijst,
        'lk_stats':          lk_stats,
        'totaal_bewakingen': totaal_bewakingen,
        'label':             str(planning_obj),
    }
    return render(request, 'directie/planning_detail.html', context)
