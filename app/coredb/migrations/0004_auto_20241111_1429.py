# Generated by Django 3.2.25 on 2024-11-11 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coredb', '0003_auto_20241111_1422'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accounthistory',
            options={'verbose_name': 'accounthistory', 'verbose_name_plural': 'accounthistory'},
        ),
        migrations.AlterModelOptions(
            name='persongames',
            options={'verbose_name': 'person_game', 'verbose_name_plural': 'person_games'},
        ),
        migrations.AlterModelTable(
            name='accounthistory',
            table=None,
        ),
        migrations.AlterModelTable(
            name='persongames',
            table=None,
        ),
    ]
