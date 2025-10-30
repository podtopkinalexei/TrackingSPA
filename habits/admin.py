from django.contrib import admin
from .models import Habit

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'place', 'time', 'is_pleasant',
                   'periodicity', 'is_public', 'created_at')
    list_filter = ('is_pleasant', 'is_public', 'periodicity', 'created_at')
    search_fields = ('action', 'place', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'action', 'place', 'time')
        }),
        ('Тип и периодичность', {
            'fields': ('is_pleasant', 'periodicity', 'time_to_complete')
        }),
        ('Вознаграждение', {
            'fields': ('related_habit', 'reward'),
            'description': 'Можно указать либо связанную привычку, либо вознаграждение'
        }),
        ('Видимость', {
            'fields': ('is_public',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

