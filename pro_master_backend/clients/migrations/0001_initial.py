# Generated by Django 4.2.11 on 2024-05-15 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClientProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Логин')),
                ('first_name', models.CharField(blank=True, max_length=64, null=True, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=64, null=True, verbose_name='Фамилия')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='users/image/', verbose_name='Фото профиля')),
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Clients',
                'ordering': ['client'],
            },
        ),
    ]
