from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Teacher, SupervisionSlot, MonthSchedule, Absence, Problem, SpecialDay


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'get_full_name', 'role', 'first_login', 'is_active')
    list_filter = ('role', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Childguard', {'fields': ('role', 'first_login')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Childguard', {'fields': ('role', 'first_login')}),
    )


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'work_percentage', 'is_available', 'user')
    list_filter = ('is_available',)
    search_fields = ('name',)


class SupervisionSlotInline(admin.TabularInline):
    model = SupervisionSlot
    extra = 0
    raw_id_fields = ('teacher',)


@admin.register(MonthSchedule)
class MonthScheduleAdmin(admin.ModelAdmin):
    list_display = ('month', 'generated_at', 'slot_count')
    inlines = [SupervisionSlotInline]

    def slot_count(self, obj):
        return obj.slots.count()
    slot_count.short_description = '# Slots'


@admin.register(SupervisionSlot)
class SupervisionSlotAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'teacher', 'schedule')
    list_filter = ('schedule__month', 'teacher')
    date_hierarchy = 'date'
    raw_id_fields = ('teacher',)


@admin.register(Absence)
class AbsenceAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'date', 'reason', 'created_at')
    list_filter = ('teacher',)
    date_hierarchy = 'date'


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'date', 'status', 'is_new', 'submitted_at')
    list_filter = ('status', 'is_new')
    date_hierarchy = 'date'
    actions = ['mark_resolved']

    def mark_resolved(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='resolved', resolved_at=timezone.now(), is_new=False)
    mark_resolved.short_description = 'Markeer als opgelost'


@admin.register(SpecialDay)
class SpecialDayAdmin(admin.ModelAdmin):
    list_display = ('date', 'reason', 'type')
    list_filter = ('type',)
    date_hierarchy = 'date'
