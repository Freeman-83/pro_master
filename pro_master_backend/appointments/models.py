from django.db import models

from clients.models import ClientProfile

from services.models import ServiceProfile


class Schedule(models.Model):
    """Модель Расписания работы Сервиса."""

    service_profile = models.ForeignKey(
        ServiceProfile,
        on_delete=models.CASCADE,
        verbose_name='Профиль сервиса',
        related_name='schedules'
    )
    date = models.DateField(
        'Дата рабочего дня',
        unique=True
    )
    start = models.TimeField(
        'Начало рабочего интервала',
        unique=True
    )
    end = models.TimeField(
        'Конец рабочего интервала',
        unique=True
    )

    class Meta:
        ordering = ['service_profile']
        verbose_name = 'Schedule'
        verbose_name_plural = 'Schedules'
        constraints = [
            models.UniqueConstraint(
                fields=['service_profile', 'date', 'start', 'end'],
                name='unique_shedule')
        ]

    def __str__(self):
        return f'{self.start} {self.end}'


class Appointment(models.Model):
    """Модель Записи на услугу."""

    schedule = models.ForeignKey(
        Schedule,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    client_profile = models.ForeignKey(
        ClientProfile,
        on_delete=models.CASCADE,
        verbose_name='Клиент',
        related_name='appointments'
    )
    appointment_time = models.TimeField('Время записи')

    class Meta:
        ordering = ['client_profile']
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
        constraints = [
            models.UniqueConstraint(
                fields=['client_profile', 'appointment_time'],
                name='unique_appointment')
        ]

    def __str__(self):
        return f'{self.service_profile} {self.client_profile}'
