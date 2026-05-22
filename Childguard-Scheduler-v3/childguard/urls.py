from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password/', views.change_password_view, name='change_password'),

    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Teachers
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/<int:pk>/edit/', views.teacher_edit, name='teacher_edit'),
    path('teachers/<int:pk>/delete/', views.teacher_delete, name='teacher_delete'),

    # Calendar
    path('calendar/<int:teacher_id>/', views.teacher_calendar, name='teacher_calendar'),
    path('master-calendar/', views.master_calendar, name='master_calendar'),

    # Schedule
    path('generate/', views.schedule_generate, name='schedule_generate'),
    path('history/', views.schedule_history, name='schedule_history'),

    # Overview
    path('overview/', views.school_overview, name='school_overview'),

    # Absence / Problems
    path('problems/', views.absence_reporting, name='absence_reporting'),
    path('problems/<int:pk>/resolve/', views.resolve_problem, name='resolve_problem'),
    path('problems/mark-read/', views.mark_problems_read, name='mark_problems_read'),
    path('api/teacher-slots/', views.get_teacher_slots, name='get_teacher_slots'),

    # Special Days
    path('special-days/', views.special_days, name='special_days'),
    path('special-days/<int:pk>/delete/', views.special_day_delete, name='special_day_delete'),

    # Teaching Hours
    path('teaching-hours/', views.teaching_hours, name='teaching_hours'),
]
