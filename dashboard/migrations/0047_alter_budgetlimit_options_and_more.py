# Generated by Django 5.1.6 on 2025-05-17 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0046_alter_budgetlimit_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='budgetlimit',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='budgetlimit',
            unique_together=set(),
        ),
    ]
