# Generated by Django 4.2.11 on 2024-05-22 18:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_remove_serviceprofile_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='services', to='services.category', verbose_name='Категория'),
            preserve_default=False,
        ),
    ]
