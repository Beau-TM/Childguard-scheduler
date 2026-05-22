import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from accounts.models import UserProfile
from datetime import date
import calendar as cal_mod


def leerkracht_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        try:
            if request.user.profile.is_directie:
                return redirect('directie:dashboard')
        except UserProfile.DoesNotExist:
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    return wrapper


def _maand_label(nu):
    maanden = ['januari','februari','maart','april','mei','juni',
               'juli','augustus','september','oktober','november','december']
    return f"{maanden[nu.month-1]} {nu.year}"


@leerkracht_required
def dashboard(request):
    from directie.models import Afmelding, Notificatie, Bewaking

    nu = date.today()
    eerste_dag = date(nu.year, nu.month, 1)
    _, laatste = cal_mod.monthrange(nu.year, nu.month)
    laatste_dag = date(nu.year, nu.month, laatste)

    # Notificaties ophalen en markeren als gelezen
    notificaties = list(Notificatie.objects.filter(
        ontvanger=request.user, gelezen=False
    ).order_by('-aangemaakt'))
    Notificatie.objects.filter(ontvanger=request.user, gelezen=False).update(gelezen=True)

    # Bewakingen deze maand
    bewakingen_maand = Bewaking.objects.filter(
        leerkracht=request.user,
        datum__gte=eerste_dag,
        datum__lte=laatste_dag,
    ).count()

    # Komende bewakingen vanaf vandaag
    TIJDEN = {'ochtend': '10:05–10:20', 'middag': '12:05–13:20', 'namiddag': '14:10–14:25'}
    komende = Bewaking.objects.filter(
        leerkracht=request.user, datum__gte=nu
    ).order_by('datum', 'moment')[:5]

    komende_data = [{
        'datum':      b.datum,
        'moment':     b.get_moment_display(),  # type: ignore
        'tijd':       TIJDEN.get(b.moment, ''),
        'speelplaats': b.speelplaats,
    } for b in komende]

    # Afmeldingen teller
    afmeldingen_nieuw = Afmelding.objects.filter(
        leerkracht=request.user, status='nieuw'
    ).count()

    try:
        werkregime = request.user.profile.werkregime
    except Exception:
        werkregime = 100

    context = {
        'notificaties':       notificaties,
        'bewakingen_maand':   bewakingen_maand,
        'komende_bewakingen': komende_data,
        'afmeldingen_nieuw':  afmeldingen_nieuw,
        'huidige_maand':      _maand_label(nu),
        'werkregime':         werkregime,
    }
    return render(request, 'leerkracht/dashboard.html', context)


@leerkracht_required
def gezamenlijke_kalender(request):
    from directie.models import Bewaking

    nu = date.today()
    jaar  = int(request.GET.get('jaar',  nu.year))
    maand = int(request.GET.get('maand', nu.month))

    vorige_maand   = maand - 1 if maand > 1 else 12
    vorige_jaar    = jaar if maand > 1 else jaar - 1
    volgende_maand = maand + 1 if maand < 12 else 1
    volgende_jaar  = jaar if maand < 12 else jaar + 1

    eerste_dag = date(jaar, maand, 1)
    _, laatste = cal_mod.monthrange(jaar, maand)
    laatste_dag = date(jaar, maand, laatste)

    bewakingen = Bewaking.objects.filter(
        datum__gte=eerste_dag, datum__lte=laatste_dag
    ).select_related('leerkracht').order_by('datum', 'moment')

    # Groepeer per datum - bewaking data voor JS popup
    bewaking_dict = {}
    for b in bewakingen:
        key = str(b.datum)
        if key not in bewaking_dict:
            bewaking_dict[key] = []
        bewaking_dict[key].append({
            'naam':       b.leerkracht.get_full_name() or b.leerkracht.username,
            'is_mij':     b.leerkracht == request.user,
            'moment':     b.moment,
            'speelplaats': b.speelplaats,
        })

    # Kalender grid bouwen
    DAGEN_NL = ['Maandag','Dinsdag','Woensdag','Donderdag','Vrijdag','Zaterdag','Zondag']
    eerste_weekdag = eerste_dag.weekday()
    kalender_dagen = []

    # Lege cellen vorige maand
    for i in range(eerste_weekdag):
        _, prev_laatste = cal_mod.monthrange(vorige_jaar, vorige_maand)
        dag_nr = prev_laatste - eerste_weekdag + i + 1
        kalender_dagen.append({
            'nummer': dag_nr, 'huidige_maand': False,
            'is_vandaag': False, 'datum_str': '', 'dagnaam': '',
            'bewakingen_json': '[]', 'heeft_bewaking': False,
        })

    # Huidige maand
    for dag in range(1, laatste + 1):
        d = date(jaar, maand, dag)
        datum_str = str(d)
        bew = bewaking_dict.get(datum_str, [])
        has_own = any(b['is_mij'] for b in bew)
        kalender_dagen.append({
            'nummer':         dag,
            'huidige_maand':  True,
            'is_vandaag':     d == nu,
            'datum_str':      datum_str,
            'dagnaam':        DAGEN_NL[d.weekday()],
            'bewakingen_json': json.dumps(bew, ensure_ascii=False),
            'heeft_bewaking': len(bew) > 0,
            'eigen_bewaking': has_own,
            'preview_namen':  [b['naam'] for b in bew[:2]],
            'meer_dan_2':     max(0, len(bew) - 2),
        })

    # Aanvullen tot meervoud van 7
    while len(kalender_dagen) % 7 != 0:
        kalender_dagen.append({
            'nummer': '', 'huidige_maand': False,
            'is_vandaag': False, 'datum_str': '', 'dagnaam': '',
            'bewakingen_json': '[]', 'heeft_bewaking': False,
        })

    # Legende
    from accounts.models import UserProfile
    leerkrachten = UserProfile.objects.filter(role='leerkracht').select_related('user')
    KLEUREN = [
        ('#bbf7d0', '#166534'), ('#dbeafe', '#1e40af'),
        ('#fde68a', '#92400e'), ('#fce7f3', '#9d174d'),
        ('#e0e7ff', '#3730a3'), ('#fee2e2', '#b91c1c'),
    ]
    legende = []
    for i, lk in enumerate(leerkrachten):
        bg, fg = KLEUREN[i % len(KLEUREN)]
        legende.append({
            'naam':   lk.user.get_full_name() or lk.user.username,
            'bg':     bg,
            'fg':     fg,
            'is_mij': lk.user == request.user,
        })

    maanden_nl = ['januari','februari','maart','april','mei','juni',
                  'juli','augustus','september','oktober','november','december']

    # Dropdown opties (huidige maand +/- 6)
    dropdown_opties = []
    for delta in range(-3, 7):
        m = ((nu.month - 1 + delta) % 12)
        j = nu.year + ((nu.month - 1 + delta) // 12)
        dropdown_opties.append({
            'value': f'{j}-{m+1}',
            'label': f'{maanden_nl[m]} {j}',
            'actief': j == jaar and (m+1) == maand,
        })

    context = {
        'kalender_dagen':  kalender_dagen,
        'maand_label':     f'{maanden_nl[maand-1]} {jaar}',
        'jaar': jaar, 'maand': maand,
        'vorige_jaar': vorige_jaar, 'vorige_maand': vorige_maand,
        'volgende_jaar': volgende_jaar, 'volgende_maand': volgende_maand,
        'legende':        legende,
        'dropdown_opties': dropdown_opties,
        'huidige_maand':  _maand_label(nu),
    }
    return render(request, 'leerkracht/gezamenlijke_kalender.html', context)
@leerkracht_required
def mijn_lesuren(request):
    nu = timezone.now()
    context = {
        'huidige_maand': _maand_label(nu),
        'heeft_lesuren': False,
        'totaal_uren':   '0.0',
        'totaal_lessen': 0,
    }
    return render(request, 'leerkracht/mijn_lesuren.html', context)


@leerkracht_required
def afmeldingen(request):
    from directie.models import Afmelding
    mijn_afmeldingen = Afmelding.objects.filter(
        leerkracht=request.user
    ).select_related('vervanger').order_by('-aangemaakt')

    context = {
        'huidige_maand':        _maand_label(timezone.now()),
        'mijn_afmeldingen':     mijn_afmeldingen,
        'afmeldingen_nieuw':    mijn_afmeldingen.filter(status='nieuw').count(),
        'afmeldingen_verwerkt': mijn_afmeldingen.filter(status='opgelost').count(),
    }
    return render(request, 'leerkracht/afmeldingen.html', context)


@leerkracht_required
def afmelding_indienen(request):
    from directie.models import Afmelding, Notificatie
    from django.contrib.auth.models import User

    if request.method == 'POST':
        datum = request.POST.get('datum')
        reden = request.POST.get('reden', '')

        if not datum:
            messages.error(request, 'Datum is verplicht.')
            return redirect('leerkracht:afmeldingen')

        if Afmelding.objects.filter(leerkracht=request.user, datum=datum).exists():
            messages.warning(request, 'Je hebt al een afmelding voor die datum.')
            return redirect('leerkracht:afmeldingen')

        afmelding = Afmelding.objects.create(
            leerkracht=request.user, datum=datum, reden=reden, status='nieuw',
        )

        naam = request.user.get_full_name() or request.user.username
        for directeur in User.objects.filter(profile__role='directie'):
            Notificatie.objects.create(
                ontvanger=directeur,
                type='afmelding_ontvangen',
                bericht=f"{naam} heeft zich afgemeld voor {afmelding.datum.strftime('%d/%m/%Y')}. Reden: {reden or '–'}",
                afmelding=afmelding,
            )

        messages.success(request, f'Afmelding voor {afmelding.datum.strftime("%d/%m/%Y")} ingediend.')
    return redirect('leerkracht:afmeldingen')


@leerkracht_required
def afmelding_annuleren(request):
    from directie.models import Afmelding

    if request.method == 'POST':
        afmelding_id = request.POST.get('afmelding_id')
        try:
            Afmelding.objects.get(id=afmelding_id, leerkracht=request.user, status='nieuw').delete()
            messages.success(request, 'Afmelding geannuleerd.')
        except Afmelding.DoesNotExist:
            messages.error(request, 'Afmelding kan niet meer geannuleerd worden.')
    return redirect('leerkracht:afmeldingen')