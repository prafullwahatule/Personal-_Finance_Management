# Generated by Django 5.1.6 on 2025-05-11 13:28

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0034_remove_expense_date_remove_expense_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='date_time',
        ),
        migrations.AddField(
            model_name='expense',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='expense',
            name='time',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
    ]
