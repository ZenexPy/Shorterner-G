# Generated by Django 4.2.7 on 2023-12-17 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shorterner', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_email_verified',
            field=models.BooleanField(default=False),
        ),
    ]
