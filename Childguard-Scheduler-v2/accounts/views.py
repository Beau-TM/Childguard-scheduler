from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import SetPasswordForm
from .models import UserProfile
 
 
def login_view(request):
    if request.user.is_authenticated:
        return _redirect_by_role(request.user)
 
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
 
            profile, _ = UserProfile.objects.get_or_create(user=user)
            if profile.must_change_password:
                return redirect('accounts:set_password')
 
            return _redirect_by_role(user)
        else:
            messages.error(request, 'Ongeldige gebruikersnaam of wachtwoord.')
    else:
        form = AuthenticationForm(request)
 
    return render(request, 'accounts/login.html', {'form': form})
 
 
@login_required
def set_password_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
 
    if not profile.must_change_password:
        return _redirect_by_role(request.user)
 
    if request.method == 'POST':
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            profile.must_change_password = False
            profile.save()
            messages.success(request, 'Wachtwoord succesvol ingesteld. Welkom!')
            return _redirect_by_role(request.user)
    else:
        form = SetPasswordForm(request.user)
 
    return render(request, 'accounts/set_password.html', {'form': form})
 
 
def logout_view(request):
    logout(request)
    return redirect('accounts:login')
 
 
def _redirect_by_role(user):
    """Stuur gebruiker naar het juiste dashboard op basis van rol."""
    try:
        if user.profile.is_directie:
            return redirect('directie:dashboard')
    except UserProfile.DoesNotExist:
        pass
    return redirect('leerkracht:dashboard')
 