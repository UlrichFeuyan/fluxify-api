# Generated by Django 4.1.7 on 2024-06-12 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demande', '0003_commentaire'),
    ]

    operations = [
        migrations.AddField(
            model_name='demande',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
