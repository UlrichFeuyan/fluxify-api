# Generated by Django 4.1.7 on 2024-06-25 01:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taches', '0003_merge_0002_initial_0002_tache_quota'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tache',
            name='quota',
        ),
    ]