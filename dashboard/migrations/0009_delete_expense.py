# Generated by Django 5.1.6 on 2025-04-18 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_alter_expense_date'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Expense',
        ),
    ]
