# Generated by Django 3.2.25 on 2024-12-04 13:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coredb', '0005_friends'),
    ]

    operations = [
        migrations.RenameField(
            model_name='friends',
            old_name='recipent',
            new_name='recipient',
        ),
    ]
