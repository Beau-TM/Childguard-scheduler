from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Systeembeheerder'),
        ('director', 'Directie'),
        ('teacher', 'Leerkracht'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='teacher')
    first_login = models.BooleanField(default=True)

    def is_admin_or_director(self):
        return self.role in ('admin', 'director')

    def __str__(self):
        return self.get_full_name() or self.username


class Teacher(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='teacher_profile'
    )
    name = models.CharField(max_length=200)
    work_percentage = models.IntegerField(default=100, help_text="100 = voltijds, 50 = halftijds")
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class SpecialDay(models.Model):
    TYPE_CHOICES = [
        ('holiday', 'Verlofdag'),
        ('trip', 'Uitstap'),
        ('studyday', 'Studiedag'),
        ('other', 'Andere'),
    ]
    date = models.DateField(unique=True)
    reason = models.CharField(max_length=300)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='other')

    def __str__(self):
        return f"{self.date} – {self.reason}"


class MonthSchedule(models.Model):
    month = models.CharField(max_length=7, unique=True, help_text="YYYY-MM")
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Planning {self.month}"


class SupervisionSlot(models.Model):
    schedule = models.ForeignKey(MonthSchedule, on_delete=models.CASCADE, related_name='slots')
    date = models.DateField()
    time = models.CharField(max_length=20)
    teacher = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='slots'
    )

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return f"{self.date} {self.time} – {self.teacher}"


class Absence(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='absences')
    date = models.DateField()
    reason = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.teacher} afwezig op {self.date}"


class Problem(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('resolved', 'Opgelost'),
    ]
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='problems')
    # Het specifieke slot waarvoor de leerkracht zich afmeldt (optioneel)
    slot = models.ForeignKey(
        SupervisionSlot, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='problems', verbose_name='Bewakingsslot'
    )
    date = models.DateField()
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    is_new = models.BooleanField(default=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    suggested_replacement = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='suggested_for'
    )
    replacement_teacher = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='replacements'
    )

    def __str__(self):
        return f"Afmelding van {self.teacher} op {self.date} ({self.status})"
