from django.db import models
from django.contrib.auth.models import User


class Lesuur(models.Model):
    DAG_CHOICES = [
        ('maandag',    'Maandag'),
        ('dinsdag',    'Dinsdag'),
        ('woensdag',   'Woensdag'),
        ('donderdag',  'Donderdag'),
        ('vrijdag',    'Vrijdag'),
    ]

    leerkracht  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesuren')
    dag         = models.CharField(max_length=20, choices=DAG_CHOICES)
    vak         = models.CharField(max_length=100)
    begin_tijd  = models.TimeField()
    eind_tijd   = models.TimeField()
    klas        = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['dag', 'begin_tijd']
        verbose_name        = 'Lesuur'
        verbose_name_plural = 'Lesuren'

    def __str__(self):
        return f"{self.leerkracht.get_full_name()} – {self.dag} {self.vak} ({self.begin_tijd}–{self.eind_tijd})"

    def tijd_display(self):
        return f"{self.begin_tijd.strftime('%H:%M')}–{self.eind_tijd.strftime('%H:%M')}"