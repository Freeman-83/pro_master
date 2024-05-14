from django.contrib import admin

from .models import Appointment, Schedule

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'service_profile',
                    'date',
                    'start',
                    'end')
    list_display_links = ('service_profile',)
    search_fields = ('service_profile',)
    list_filter = ('service_profile', 'date', 'start', 'end')
    empty_value_display = '-пусто-'


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'client_profile',
                    'schedule',
                    'appointment_time')
    list_display_links = ('client_profile',)
    search_fields = ('client_profile',)
    list_filter = ('client_profile', 'schedule', 'appointment_time')
    empty_value_display = '-пусто-'
