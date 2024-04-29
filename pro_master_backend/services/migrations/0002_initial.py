# Generated by Django 4.2.11 on 2024-04-29 09:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('services', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceprofile',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_profiles', to=settings.AUTH_USER_MODEL, verbose_name='Собственник'),
        ),
        migrations.AddField(
            model_name='review',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='review',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='services.serviceprofile', verbose_name='Сервис'),
        ),
        migrations.AddField(
            model_name='image',
            name='service_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='services.serviceprofile', verbose_name='Фото профиля сервиса'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_services', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='favorite',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_favorite_for_clients', to='services.serviceprofile'),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
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
        migrations.AddConstraint(
            model_name='serviceprofilecategory',
            constraint=models.UniqueConstraint(fields=('service_profile', 'category'), name='unique_category_for_service'),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('service', 'author'), name='unique_review'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('client', 'service'), name='unique_favorite'),
        ),
    ]
