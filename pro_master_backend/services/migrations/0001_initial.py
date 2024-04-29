# Generated by Django 4.2.11 on 2024-04-29 09:06

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Наименование категории')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст')),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата публикации')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'ordering': ['service'],
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='services/profile_images', verbose_name='Фото')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст')),
                ('score', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Оценка')),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата публикации')),
            ],
            options={
                'verbose_name': 'Review',
                'verbose_name_plural': 'Reviews',
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='ServiceProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Имя профиля')),
                ('description', models.TextField(verbose_name='Описание сервиса')),
                ('profile_foto', models.ImageField(blank=True, null=True, upload_to='services/profile_foto/', verbose_name='Главное фото профиля')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Контактный номер телефона')),
                ('site_address', models.URLField(blank=True, null=True, verbose_name='Адрес сайта')),
                ('social_network_contacts', models.CharField(blank=True, max_length=100, null=True, verbose_name='Ссылка на аккаунт в социальных сетях')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата размещения информации')),
                ('first_name', models.CharField(blank=True, max_length=64, null=True, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=64, null=True, verbose_name='Фамилия')),
                ('is_organization', models.BooleanField(default=False, verbose_name='Статус Организации')),
            ],
            options={
                'verbose_name': 'Service Profile',
                'verbose_name_plural': 'Service Profiles',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='ServiceProfileCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_service_profiles', to='services.category')),
                ('service_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_categories', to='services.serviceprofile')),
            ],
            options={
                'verbose_name_plural': 'Профиль Сервиса - Категория',
            },
        ),
        migrations.AddField(
            model_name='serviceprofile',
            name='categories',
            field=models.ManyToManyField(through='services.ServiceProfileCategory', to='services.category', verbose_name='Категории услуг'),
        ),
    ]
