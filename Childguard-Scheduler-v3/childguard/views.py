from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from datetime import date, timedelta
import json
import calendar as cal_module

from .models import Teacher, SupervisionSlot, MonthSchedule, Absence, Problem, SpecialDay, User
from .forms import (
    LoginForm, ChangePasswordForm, TeacherForm,
    AbsenceForm, ProblemForm, SpecialDayForm, ScheduleConfigForm
)

def require_admin(view_func):
    """Decorator: only allow admin/director users."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_admin_or_director():
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper

# Auth

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        if user.first_login and user.role == 'teacher':
            return redirect('change_password')
        return redirect('dashboard')
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['new_password'])
            request.user.first_login = False
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Wachtwoord succesvol gewijzigd.')
            return redirect('dashboard')
    else:
        form = ChangePasswordForm()
    return render(request, 'childguard/change_password.html', {'form': form})


# Dashboard 

@login_required
def dashboard(request):
    if request.user.role == 'teacher':
        return teacher_dashboard(request)

    today = date.today()
    current_month = today.strftime('%Y-%m')
    teachers = Teacher.objects.all()
    active_teachers = teachers.filter(is_available=True).count()
    open_problems = Problem.objects.filter(status='open').count()

    try:
        schedule = MonthSchedule.objects.get(month=current_month)
        slots = schedule.slots.all()
        total_slots = slots.count()
        assigned_slots = slots.filter(teacher__isnull=False).count()
        coverage_pct = round(assigned_slots / total_slots * 100) if total_slots else 0
    except MonthSchedule.DoesNotExist:
        total_slots = assigned_slots = coverage_pct = 0

    context = {
        'active_teachers': active_teachers,
        'total_teachers': teachers.count(),
        'open_problems': open_problems,
        'total_slots': total_slots,
        'assigned_slots': assigned_slots,
        'coverage_pct': coverage_pct,
        'current_month': current_month,
        'current_month_display': _format_month(current_month),
        'unread_count': Problem.objects.filter(is_new=True).count(),
    }
    return render(request, 'childguard/dashboard.html', context)


def teacher_dashboard(request):
    try:
        teacher = request.user.teacher_profile
    except Teacher.DoesNotExist:
        messages.error(request, 'Geen leerkracht-profiel gevonden.')
        return render(request, 'childguard/teacher_dashboard.html', {})

    today = date.today()
    current_month = today.strftime('%Y-%m')

    try:
        schedule = MonthSchedule.objects.get(month=current_month)
        my_slots = schedule.slots.filter(teacher=teacher).order_by('date', 'time')
        upcoming_slots = [s for s in my_slots if s.date >= today][:5]
    except MonthSchedule.DoesNotExist:
        my_slots = []
        upcoming_slots = []

    my_problems = Problem.objects.filter(teacher=teacher).order_by('-submitted_at')[:5]
    my_absences = Absence.objects.filter(teacher=teacher).order_by('-date')[:5]

    context = {
        'teacher': teacher,
        'upcoming_slots': upcoming_slots,
        'my_slots_count': len(list(my_slots)),
        'my_problems': my_problems,
        'my_absences': my_absences,
        'current_month_display': _format_month(current_month),
    }
    return render(request, 'childguard/teacher_dashboard.html', context)


# Teachers

@require_admin
@login_required
def teacher_list(request):
    teachers = Teacher.objects.all().order_by('name')
    form = TeacherForm()
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Leerkracht toegevoegd.')
            return redirect('teacher_list')
    return render(request, 'childguard/teacher_list.html', {'teachers': teachers, 'form': form})


@require_admin
@login_required
def teacher_edit(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    form = TeacherForm(request.POST or None, instance=teacher)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Leerkracht bijgewerkt.')
        return redirect('teacher_list')
    return render(request, 'childguard/teacher_edit.html', {'form': form, 'teacher': teacher})


@require_admin
@login_required
@require_POST
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    name = teacher.name
    teacher.delete()
    messages.success(request, f'Leerkracht {name} verwijderd.')
    return redirect('teacher_list')


# Schedule 

@require_admin
@login_required
def schedule_generate(request):
    today = date.today()
    form = ScheduleConfigForm(request.POST or None, initial={
        'month': today.strftime('%Y-%m'),
        'slots_per_day': 3,
    })

    if request.method == 'POST' and form.is_valid():
        month = form.cleaned_data['month']
        slots_per_day = form.cleaned_data['slots_per_day']
        _generate_schedule(month, slots_per_day)
        messages.success(request, f'Planning voor {_format_month(month)} gegenereerd.')
        return redirect('master_calendar')

    return render(request, 'childguard/schedule_generate.html', {'form': form})


def _generate_schedule(month_str, slots_per_day):
    year, month = map(int, month_str.split('-'))
    teachers = list(Teacher.objects.filter(is_available=True))
    if not teachers:
        return

    special_dates = set(
        SpecialDay.objects.filter(date__year=year, date__month=month).values_list('date', flat=True)
    )
    absence_map = {}
    for a in Absence.objects.filter(date__year=year, date__month=month):
        absence_map.setdefault(str(a.date), []).append(a.teacher_id)

    # Delete existing schedule for this month
    MonthSchedule.objects.filter(month=month_str).delete()
    schedule = MonthSchedule.objects.create(month=month_str)

    time_slots = ['10:05-10:20', '12:05-13:20', '14:10-14:25']
    total_work = sum(t.work_percentage for t in teachers)
    teacher_counts = {t.id: 0 for t in teachers}

    for day in range(1, cal_module.monthrange(year, month)[1] + 1):
        current_date = date(year, month, day)
        if current_date.weekday() >= 5:  # skip weekends
            continue
        if current_date in special_dates:
            continue

        date_str = str(current_date)
        absent_ids = absence_map.get(date_str, [])
        available = [t for t in teachers if t.id not in absent_ids]
        if not available:
            available = teachers

        for i in range(slots_per_day):
            time = time_slots[i] if i < len(time_slots) else f"{10+i}:00-{10+i}:30"
            # Pick teacher with lowest relative slot count
            best = min(
                available,
                key=lambda t: teacher_counts[t.id] / (t.work_percentage / 100)
            )
            SupervisionSlot.objects.create(
                schedule=schedule,
                date=current_date,
                time=time,
                teacher=best,
            )
            teacher_counts[best.id] += 1


@require_admin
@login_required
def schedule_history(request):
    schedules = MonthSchedule.objects.all().order_by('-month')
    return render(request, 'childguard/schedule_history.html', {'schedules': schedules})


# Master Calendar 

@login_required
def master_calendar(request):
    today = date.today()
    month_str = request.GET.get('month', today.strftime('%Y-%m'))
    year, month = map(int, month_str.split('-'))

    try:
        schedule = MonthSchedule.objects.get(month=month_str)
        slots = schedule.slots.select_related('teacher').order_by('date', 'time')
    except MonthSchedule.DoesNotExist:
        slots = []

    special_days = {
        str(sd.date): sd for sd in SpecialDay.objects.filter(date__year=year, date__month=month)
    }

    # Build calendar grid
    cal_grid = _build_calendar_grid(year, month, slots, special_days)

    # Month navigation
    prev_month = _offset_month(month_str, -1)
    next_month = _offset_month(month_str, 1)

    context = {
        'month_str': month_str,
        'month_display': _format_month(month_str),
        'cal_grid': cal_grid,
        'prev_month': prev_month,
        'next_month': next_month,
        'teachers': Teacher.objects.all(),
    }
    return render(request, 'childguard/master_calendar.html', context)


# Teacher Calendar 

@login_required
def teacher_calendar(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    today = date.today()
    month_str = request.GET.get('month', today.strftime('%Y-%m'))
    year, month = map(int, month_str.split('-'))

    try:
        schedule = MonthSchedule.objects.get(month=month_str)
        slots = schedule.slots.filter(teacher=teacher).order_by('date', 'time')
    except MonthSchedule.DoesNotExist:
        slots = []

    special_days = {
        str(sd.date): sd for sd in SpecialDay.objects.filter(date__year=year, date__month=month)
    }
    cal_grid = _build_calendar_grid(year, month, slots, special_days, teacher=teacher)

    context = {
        'teacher': teacher,
        'month_str': month_str,
        'month_display': _format_month(month_str),
        'cal_grid': cal_grid,
        'prev_month': _offset_month(month_str, -1),
        'next_month': _offset_month(month_str, 1),
        'slot_count': len(list(slots)),
    }
    return render(request, 'childguard/teacher_calendar.html', context)


# School Overview 

@require_admin
@login_required
def school_overview(request):
    teachers = Teacher.objects.all()
    today = date.today()
    month_str = today.strftime('%Y-%m')

    stats = []
    for t in teachers:
        slot_count = SupervisionSlot.objects.filter(teacher=t).count()
        problem_count = Problem.objects.filter(teacher=t).count()
        stats.append({
            'teacher': t,
            'slot_count': slot_count,
            'problem_count': problem_count,
        })

    context = {
        'stats': stats,
        'total_teachers': teachers.count(),
        'open_problems': Problem.objects.filter(status='open').count(),
    }
    return render(request, 'childguard/school_overview.html', context)


# Absence / Problem Reporting 

@login_required
def absence_reporting(request):
    user = request.user
    is_admin = user.is_admin_or_director()

    if is_admin:
        problems = Problem.objects.select_related(
            'teacher', 'slot', 'suggested_replacement', 'replacement_teacher'
        ).order_by('-submitted_at')
    else:
        try:
            teacher = user.teacher_profile
            problems = Problem.objects.filter(teacher=teacher).select_related(
                'slot', 'suggested_replacement', 'replacement_teacher'
            ).order_by('-submitted_at')
        except Teacher.DoesNotExist:
            problems = Problem.objects.none()
            teacher = None

    form = ProblemForm(request.POST or None, user=user)
    if request.method == 'POST' and form.is_valid():
        problem = form.save(commit=False)
        # Auto-suggest replacement: best available teacher for this date/slot
        suggested = _get_suggested_replacement(problem.teacher, problem.date)
        problem.suggested_replacement = suggested
        problem.is_new = True
        problem.save()
        messages.success(request, 'Afmelding ingediend. De directie wordt op de hoogte gesteld.')
        return redirect('absence_reporting')

    context = {
        'problems': problems,
        'form': form,
        'is_admin': is_admin,
        'unread_count': Problem.objects.filter(is_new=True).count() if is_admin else 0,
        'all_teachers': Teacher.objects.filter(is_available=True).order_by('name'),
    }
    return render(request, 'childguard/absence_reporting.html', context)


@require_admin
@login_required
def resolve_problem(request, pk):
    """Directie kiest hoe een afmelding opgelost wordt:
    - Automatisch: bevestig de voorgestelde vervanger
    - Manueel: kies zelf een vervanger uit de lijst
    - Gewoon sluiten: geen specifieke vervanger nodig
    """
    problem = get_object_or_404(Problem, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'auto':
            # Bevestig de automatisch voorgestelde vervanger
            replacement = problem.suggested_replacement
            problem.replacement_teacher = replacement
            if replacement and problem.slot:
                problem.slot.teacher = replacement
                problem.slot.save()
        elif action == 'manual':
            # Directie heeft zelf een vervanger gekozen
            replacement_id = request.POST.get('replacement_id')
            if replacement_id:
                try:
                    replacement = Teacher.objects.get(pk=replacement_id)
                    problem.replacement_teacher = replacement
                    if problem.slot:
                        problem.slot.teacher = replacement
                        problem.slot.save()
                except Teacher.DoesNotExist:
                    pass
        # action == 'close': gewoon sluiten zonder vervanger

        problem.status = 'resolved'
        problem.is_new = False
        problem.resolved_at = timezone.now()
        problem.save()
        messages.success(request, 'Afmelding verwerkt.')
        return redirect('absence_reporting')

    # GET: toon het resolve-modal (fallback, normaal via POST vanuit modal)
    return redirect('absence_reporting')


@require_admin
@login_required
@require_POST
def mark_problems_read(request):
    Problem.objects.filter(is_new=True).update(is_new=False)
    return redirect('absence_reporting')


@login_required
def get_teacher_slots(request):
    """AJAX endpoint: geeft slots terug voor een leerkracht (voor het afmeldformulier)."""
    teacher_id = request.GET.get('teacher_id')
    if not teacher_id:
        return JsonResponse({'slots': []})
    try:
        from datetime import date as _date
        slots = SupervisionSlot.objects.filter(
            teacher_id=teacher_id, date__gte=_date.today()
        ).order_by('date', 'time').values('id', 'date', 'time')
        return JsonResponse({'slots': [
            {'id': s['id'], 'label': f"{s['date']} – {s['time']}"} for s in slots
        ]})
    except Exception:
        return JsonResponse({'slots': []})


# Special Days

@require_admin
@login_required
def special_days(request):
    days = SpecialDay.objects.order_by('date')
    form = SpecialDayForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Speciale dag toegevoegd.')
        return redirect('special_days')
    return render(request, 'childguard/special_days.html', {'days': days, 'form': form})


@require_admin
@login_required
@require_POST
def special_day_delete(request, pk):
    day = get_object_or_404(SpecialDay, pk=pk)
    day.delete()
    messages.success(request, 'Speciale dag verwijderd.')
    return redirect('special_days')


# Teaching Hours

@login_required
def teaching_hours(request):
    try:
        teacher = request.user.teacher_profile
    except Teacher.DoesNotExist:
        return redirect('dashboard')

    slots = SupervisionSlot.objects.filter(teacher=teacher).order_by('date')
    by_month = {}
    for slot in slots:
        key = slot.date.strftime('%Y-%m')
        by_month.setdefault(key, []).append(slot)

    month_data = [
        {'month': k, 'display': _format_month(k), 'slots': v, 'count': len(v)}
        for k, v in sorted(by_month.items())
    ]

    context = {
        'teacher': teacher,
        'month_data': month_data,
        'total_slots': slots.count(),
    }
    return render(request, 'childguard/teaching_hours.html', context)


# Helpers

DUTCH_MONTHS = [
    '', 'januari', 'februari', 'maart', 'april', 'mei', 'juni',
    'juli', 'augustus', 'september', 'oktober', 'november', 'december'
]


def _format_month(month_str):
    year, month = month_str.split('-')
    return f"{DUTCH_MONTHS[int(month)]} {year}"


def _offset_month(month_str, delta):
    year, month = map(int, month_str.split('-'))
    month += delta
    if month > 12:
        month = 1
        year += 1
    elif month < 1:
        month = 12
        year -= 1
    return f"{year}-{month:02d}"

def _get_suggested_replacement(teacher, absence_date):
    """Pick the available teacher with fewest slots on that date."""
    absent_ids = list(
        Absence.objects.filter(date=absence_date).values_list('teacher_id', flat=True)
    )
    absent_ids.append(teacher.id)
    candidates = Teacher.objects.filter(is_available=True).exclude(id__in=absent_ids)
    if not candidates.exists():
        return None
    # Prefer the one with fewest total slots
    return min(candidates, key=lambda t: SupervisionSlot.objects.filter(teacher=t).count())


def _build_calendar_grid(year, month, slots, special_days, teacher=None):
    """Return a list of week-lists with day dicts for the calendar template."""
    first_day = date(year, month, 1)
    days_in_month = cal_module.monthrange(year, month)[1]

    # Group slots by date
    slots_by_date = {}
    for slot in slots:
        slots_by_date.setdefault(str(slot.date), []).append(slot)

    # Monday-based week grid
    grid = []
    # Leading empty cells
    week = [None] * first_day.weekday()

    for day in range(1, days_in_month + 1):
        current = date(year, month, day)
        date_str = str(current)
        week.append({
            'date': current,
            'date_str': date_str,
            'slots': slots_by_date.get(date_str, []),
            'special': special_days.get(date_str),
            'is_today': current == date.today(),
            'is_weekend': current.weekday() >= 5,
        })
        if len(week) == 7:
            grid.append(week)
            week = []

    if week:
        week += [None] * (7 - len(week))
        grid.append(week)

    return grid


# Error handlers

def custom_403(request, exception=None):
    return render(request, 'childguard/403.html', status=403)


def custom_404(request, exception=None):
    return render(request, 'childguard/404.html', status=404)
