# Generated by Django 4.2.4 on 2024-01-07 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coder', '0014_profile_completed_courses'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
