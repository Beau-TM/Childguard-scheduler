from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('directie',   'Directie'),
        ('leerkracht', 'Leerkracht'),
    ]

    WERKREGIME_CHOICES = [
        (100, 'Voltijds (100%)'),
        (80,  '4/5 (80%)'),
        (75,  '3/4 (75%)'),
        (50,  'Halftijds (50%)'),
    ]

    user                 = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role                 = models.CharField(max_length=20, choices=ROLE_CHOICES, default='leerkracht')
    must_change_password = models.BooleanField(default=True)
    werkregime           = models.IntegerField(choices=WERKREGIME_CHOICES, default=100,
                                               help_text='Werkpercentage van de leerkracht')

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"  # type: ignore

    @property
    def is_directie(self):
        return self.role == 'directie'

    @property
    def is_leerkracht(self):
        return self.role == 'leerkracht'

    @property
    def werkregime_factor(self):
        """Geeft het werkregime als decimale factor (bv. 0.8 voor 80%)"""
        return self.werkregime / 100
