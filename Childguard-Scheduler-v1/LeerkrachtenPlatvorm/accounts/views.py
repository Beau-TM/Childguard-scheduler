# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SetPasswordForm   # zie forms.py hieronder
from .models import UserProfile      # zie models.py hieronder


# ──────────────────────────────────────────────
#  LOGIN
# ──────────────────────────────────────────────
def login_view(request):
    """Iedereen wordt naar deze pagina gestuurd om in te loggen."""
    if request.user.is_authenticated:
        return redirect('dashboard')  # pas aan naar jouw dashboard-url-naam

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Controleer of dit de eerste login is
            profile, _ = UserProfile.objects.get_or_create(user=user)
            if profile.must_change_password:
                return redirect('set_password')

            return redirect('dashboard')
        else:
            messages.error(request, 'Ongeldige gebruikersnaam of wachtwoord.')

    from django.contrib.auth.forms import AuthenticationForm
    form = AuthenticationForm(request)
    return render(request, 'accounts/login.html', {'form': form})


# ──────────────────────────────────────────────
#  EERSTE LOGIN → WACHTWOORD INSTELLEN
# ──────────────────────────────────────────────
@login_required
def set_password_view(request):
    """
    Wordt getoond als profile.must_change_password == True.
    Na opslaan wordt de vlag uitgezet en wordt de gebruiker doorgestuurd.
    """
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    # Als wachtwoord al gewijzigd is: direct naar dashboard
    if not profile.must_change_password:
        return redirect('dashboard')

    if request.method == 'POST':
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()                          # slaat nieuw wachtwoord op in DB
            profile.must_change_password = False
            profile.save()
            messages.success(request, 'Uw wachtwoord is succesvol ingesteld. Welkom!')
            return redirect('dashboard')
    else:
        form = SetPasswordForm(request.user)

    return render(request, 'accounts/set_password.html', {'form': form})


# ──────────────────────────────────────────────
#  LOGOUT
# ──────────────────────────────────────────────
def logout_view(request):
    logout(request)
    return redirect('login')


# ──────────────────────────────────────────────
#  RESET DEMO  (optioneel, voor demo-omgeving)
# ──────────────────────────────────────────────
def reset_demo_view(request):
    """Reset alle demo-wachtwoorden naar de standaard waarden."""
    if request.method == 'POST':
        # Admin reset
        try:
            admin = User.objects.get(username='admin')
            admin.set_password('admin123')
            admin.save()
        except User.DoesNotExist:
            pass

        # Leerkrachten reset
        for username in ['teacher1', 'teacher2', 'teacher3']:
            try:
                teacher = User.objects.get(username=username)
                teacher.set_password('teacher123')
                teacher.save()
                profile, _ = UserProfile.objects.get_or_create(user=teacher)
                profile.must_change_password = True
                profile.save()
            except User.DoesNotExist:
                pass

        messages.success(request, 'Demo wachtwoorden zijn gereset.')

    return redirect('login')
