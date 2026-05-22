from django import forms
from django.contrib.auth.forms import SetPasswordForm as DjangoSetPasswordForm


class SetPasswordForm(DjangoSetPasswordForm):
    new_password1 = forms.CharField(
        label='Nieuw wachtwoord',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'placeholder': 'Minimaal 8 tekens',
        }),
    )
    new_password2 = forms.CharField(
        label='Herhaal wachtwoord',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'placeholder': 'Herhaal uw wachtwoord',
        }),
    )

    error_messages = {
        'password_mismatch': 'De twee wachtwoorden komen niet overeen.',
    }
