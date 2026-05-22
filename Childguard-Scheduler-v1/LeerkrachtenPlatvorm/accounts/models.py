# models.py
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Uitbreiding op het standaard Django User-model.
    Houdt bij of een gebruiker bij de eerste login
    verplicht is zijn wachtwoord te wijzigen.
    """
    ROLE_CHOICES = [
        ('directie',    'Directie'),
        ('leerkracht',  'Leerkracht'),
    ]

    user                 = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role                 = models.CharField(max_length=20, choices=ROLE_CHOICES, default='leerkracht')
    must_change_password = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"  # type: ignore

    @property
    def is_directie(self):
        return self.role == 'directie'

    @property
    def is_leerkracht(self):
        return self.role == 'leerkracht'
