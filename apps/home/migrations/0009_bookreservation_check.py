# Generated by Django 3.2.6 on 2024-12-22 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_bookreservation_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookreservation',
            name='check',
            field=models.BooleanField(default=False),
        ),
    ]
