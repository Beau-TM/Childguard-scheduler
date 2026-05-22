from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Teacher, Problem, Absence, SpecialDay, User, SupervisionSlot


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Gebruikersnaam',
        widget=forms.TextInput(attrs={'placeholder': 'Voer gebruikersnaam in', 'class': 'form-input'}),
    )
    password = forms.CharField(
        label='Wachtwoord',
        widget=forms.PasswordInput(attrs={'placeholder': 'Voer wachtwoord in', 'class': 'form-input'}),
    )


class ChangePasswordForm(forms.Form):
    new_password = forms.CharField(
        label='Nieuw wachtwoord',
        min_length=6,
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Minimaal 6 tekens'}),
    )
    confirm_password = forms.CharField(
        label='Bevestig wachtwoord',
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Herhaal wachtwoord'}),
    )

    def clean(self):
        cleaned = super().clean()
        pw1 = cleaned.get('new_password')
        pw2 = cleaned.get('confirm_password')
        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError('Wachtwoorden komen niet overeen.')
        return cleaned


class TeacherForm(forms.ModelForm):
    WORK_CHOICES = [
        (100, 'Voltijds (100%)'),
        (80, '4/5 (80%)'),
        (75, 'Driekwart (75%)'),
        (60, '3/5 (60%)'),
        (50, 'Halftijds (50%)'),
    ]
    work_percentage = forms.ChoiceField(
        choices=WORK_CHOICES,
        label='Werkregime',
        widget=forms.Select(attrs={'class': 'form-input'}),
    )
    # Optional: create a login account at the same time
    username = forms.CharField(
        label='Gebruikersnaam (login)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Laat leeg als al bestaat'}),
    )
    temp_password = forms.CharField(
        label='Tijdelijk wachtwoord',
        required=False,
        min_length=6,
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Minimaal 6 tekens'}),
    )

    class Meta:
        model = Teacher
        fields = ['name', 'work_percentage', 'is_available']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Volledige naam'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
        labels = {
            'name': 'Naam',
            'is_available': 'Beschikbaar',
        }

    def clean(self):
        cleaned = super().clean()
        username = cleaned.get('username')
        temp_password = cleaned.get('temp_password')
        if username and not temp_password:
            raise forms.ValidationError('Vul ook een tijdelijk wachtwoord in als je een loginaccount aanmaakt.')
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Gebruikersnaam "{username}" is al in gebruik.')
        return cleaned

    def save(self, commit=True):
        teacher = super().save(commit=False)
        username = self.cleaned_data.get('username')
        temp_password = self.cleaned_data.get('temp_password')
        if commit:
            teacher.save()
            if username and temp_password:
                user = User.objects.create_user(
                    username=username,
                    password=temp_password,
                    role='teacher',
                    first_login=True,
                )
                teacher.user = user
                teacher.save()
        return teacher


class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['teacher', 'date', 'slot', 'description']
        widgets = {
            'teacher': forms.Select(attrs={'class': 'form-input', 'id': 'id_teacher'}),
            'date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date', 'id': 'id_date'}),
            'slot': forms.Select(attrs={'class': 'form-input', 'id': 'id_slot'}),
            'description': forms.Textarea(attrs={
                'class': 'form-input', 'rows': 3,
                'placeholder': 'Beschrijf de reden van afmelding...'
            }),
        }
        labels = {
            'teacher': 'Leerkracht',
            'date': 'Datum',
            'slot': 'Bewakingsslot (optioneel)',
            'description': 'Reden / beschrijving',
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slot'].required = False
        self.fields['slot'].empty_label = '— Geen specifiek slot —'
        self.fields['slot'].queryset = SupervisionSlot.objects.none()

        if user and user.role == 'teacher':
            try:
                teacher = user.teacher_profile
                self.fields['teacher'].initial = teacher
                self.fields['teacher'].widget = forms.HiddenInput()
                from datetime import date as _date
                self.fields['slot'].queryset = SupervisionSlot.objects.filter(
                    teacher=teacher, date__gte=_date.today()
                ).order_by('date', 'time').select_related('schedule')
            except Exception:
                pass

        if args and args[0]:
            post = args[0]
            teacher_id = post.get('teacher')
            if teacher_id:
                try:
                    from datetime import date as _date
                    self.fields['slot'].queryset = SupervisionSlot.objects.filter(
                        teacher_id=teacher_id, date__gte=_date.today()
                    ).order_by('date', 'time')
                except Exception:
                    pass


class AbsenceForm(forms.ModelForm):
    class Meta:
        model = Absence
        fields = ['teacher', 'date', 'reason']
        widgets = {
            'teacher': forms.Select(attrs={'class': 'form-input'}),
            'date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'reason': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Reden van afwezigheid'}),
        }
        labels = {
            'teacher': 'Leerkracht',
            'date': 'Datum',
            'reason': 'Reden',
        }


class SpecialDayForm(forms.ModelForm):
    class Meta:
        model = SpecialDay
        fields = ['date', 'reason', 'type']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'reason': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Beschrijving'}),
            'type': forms.Select(attrs={'class': 'form-input'}),
        }
        labels = {
            'date': 'Datum',
            'reason': 'Reden',
            'type': 'Type',
        }


class ScheduleConfigForm(forms.Form):
    month = forms.CharField(
        label='Maand',
        widget=forms.TextInput(attrs={'class': 'form-input', 'type': 'month'}),
        help_text='Selecteer de maand waarvoor de planning gegenereerd moet worden.',
    )
    slots_per_day = forms.IntegerField(
        label='Bewakingen per dag',
        min_value=1,
        max_value=5,
        initial=3,
        widget=forms.NumberInput(attrs={'class': 'form-input'}),
    )

    def clean_month(self):
        import re
        value = self.cleaned_data.get('month', '')
        if not re.match(r'^\d{4}-(0[1-9]|1[0-2])$', value):
            raise forms.ValidationError('Gebruik het formaat YYYY-MM, bijv. 2026-05.')
        return value
