# Generated by Django 4.2.11 on 2024-05-05 16:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceprofile',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_profiles', to=settings.AUTH_USER_MODEL, verbose_name='Собственник'),
        ),
        migrations.AddField(
            model_name='serviceprofile',
            name='service_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_profiles', to='services.servicetype', verbose_name='Тип сервиса'),
        ),
        migrations.AddField(
            model_name='serviceprofile',
            name='services',
            field=models.ManyToManyField(through='services.ServiceProfileService', to='services.service', verbose_name='Услуги'),
        ),
        migrations.AddField(
            model_name='service',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='services', to='services.category', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='service_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='services.serviceprofile', verbose_name='Профиль сервиса'),
        ),
        migrations.AddField(
            model_name='review',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='users.clientprofile', verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='review',
            name='service_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='services.serviceprofile', verbose_name='Сервис'),
        ),
        migrations.AddField(
            model_name='image',
            name='service_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_images', to='services.serviceprofile', verbose_name='Фото профиля сервиса'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='client_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_services', to='users.clientprofile'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='service_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_favorite_for_clients', to='services.serviceprofile'),
        ),
        migrations.AddField(
            model_name='employee',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='services.serviceprofile'),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='users.clientprofile', verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='comment',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='services.review', verbose_name='Отзыв'),
        ),
        migrations.AddField(
            model_name='category',
            name='parent_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='categories', to='services.category', verbose_name='Родительская категория'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='client_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='users.clientprofile', verbose_name='Клиент'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='schedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='services.schedule'),
        ),
        migrations.AddConstraint(
            model_name='serviceprofileservice',
            constraint=models.UniqueConstraint(fields=('service_profile', 'service'), name='unique_service_for_service_profile'),
        ),
        migrations.AddConstraint(
            model_name='serviceprofilecategory',
            constraint=models.UniqueConstraint(fields=('service_profile', 'category'), name='unique_category_for_service_profile'),
        ),
        migrations.AddConstraint(
            model_name='schedule',
            constraint=models.UniqueConstraint(fields=('service_profile', 'date', 'start', 'end'), name='unique_shedule'),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('service_profile', 'author'), name='unique_review'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('client_profile', 'service_profile'), name='unique_favorite'),
        ),
        migrations.AddConstraint(
            model_name='appointment',
            constraint=models.UniqueConstraint(fields=('client_profile', 'appointment_time'), name='unique_appointment'),
        ),
    ]
