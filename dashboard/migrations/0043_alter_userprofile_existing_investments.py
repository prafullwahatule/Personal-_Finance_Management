# Generated by Django 5.1.6 on 2025-05-15 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0042_remove_userprofile_annual_income_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='existing_investments',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]
