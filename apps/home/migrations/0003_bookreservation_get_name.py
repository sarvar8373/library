# Generated by Django 3.2.6 on 2024-12-17 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_bookreservation'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookreservation',
            name='get_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]