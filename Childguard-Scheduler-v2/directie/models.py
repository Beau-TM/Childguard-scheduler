from django.db import models
from django.contrib.auth.models import User


class SpecialeDag(models.Model):
    TYPE_CHOICES = [
        ('feestdag',               'Feestdag'),
        ('vakantie',               'Schoolvakantie'),
        ('pedagogische_studiedag', 'Pedagogische studiedag'),
        ('facultatieve_vrije_dag', 'Facultatieve vrije dag'),
        ('extra',                  'Extra'),
    ]
    datum        = models.DateField()
    type         = models.CharField(max_length=30, choices=TYPE_CHOICES, default='pedagogische_studiedag')
    beschrijving = models.CharField(max_length=200, blank=True)
    is_wettelijk = models.BooleanField(default=False)

    class Meta:
        ordering = ['datum']
        verbose_name        = 'Speciale dag'
        verbose_name_plural = 'Speciale dagen'

    def __str__(self):
        return f"{self.datum} – {self.beschrijving} ({self.get_type_display()})"  # type: ignore


class Afmelding(models.Model):
    STATUS_CHOICES = [
        ('nieuw',    'Nieuw'),
        ('verwerkt', 'Verwerkt'),
        ('opgelost', 'Opgelost'),
    ]
    leerkracht  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='afmeldingen')
    datum       = models.DateField()
    reden       = models.TextField(blank=True)
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='nieuw')
    vervanger   = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='vervangingen')
    aangemaakt  = models.DateTimeField(auto_now_add=True)
    bijgewerkt  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-aangemaakt']
        verbose_name        = 'Afmelding'
        verbose_name_plural = 'Afmeldingen'

    def __str__(self):
        return f"{self.leerkracht.get_full_name()} – {self.datum} ({self.get_status_display()})"  # type: ignore


class Notificatie(models.Model):
    TYPE_CHOICES = [
        ('vervanger_aangesteld', 'Vervanger aangesteld'),
        ('afmelding_ontvangen',  'Afmelding ontvangen'),
    ]
    ontvanger   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaties')
    type        = models.CharField(max_length=30, choices=TYPE_CHOICES)
    bericht     = models.TextField()
    gelezen     = models.BooleanField(default=False)
    afmelding   = models.ForeignKey(Afmelding, on_delete=models.CASCADE, null=True, blank=True)
    aangemaakt  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-aangemaakt']

    def __str__(self):
        return f"Notificatie voor {self.ontvanger.username}: {self.bericht[:50]}"


class Planning(models.Model):
    jaar        = models.IntegerField()
    maand       = models.IntegerField()
    aangemaakt  = models.DateTimeField(auto_now_add=True)
    aangemaakt_door = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-jaar', '-maand']
        verbose_name        = 'Planning'
        verbose_name_plural = 'Planningen'

    def __str__(self):
        maanden = ['jan','feb','mrt','apr','mei','jun','jul','aug','sep','okt','nov','dec']
        return f"Planning {maanden[self.maand-1]} {self.jaar}"


class Bewaking(models.Model):
    MOMENT_CHOICES = [
        ('ochtend',  'Ochtend'),
        ('middag',   'Middag'),
        ('namiddag', 'Namiddag'),
    ]
    planning     = models.ForeignKey(Planning, on_delete=models.CASCADE, related_name='bewakingen')
    leerkracht   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bewakingen')
    datum        = models.DateField()
    moment       = models.CharField(max_length=10, choices=MOMENT_CHOICES)
    speelplaats  = models.CharField(max_length=50)

    class Meta:
        ordering = ['datum', 'moment']

    def __str__(self):
        return f"{self.leerkracht.get_full_name()} – {self.datum} {self.moment}"
