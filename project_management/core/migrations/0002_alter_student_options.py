# Generated by Django 5.0.2 on 2025-02-21 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['roll_number']},
        ),
    ]
