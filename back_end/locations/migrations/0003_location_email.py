# Generated by Django 2.2.5 on 2020-07-17 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_location_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='email',
            field=models.EmailField(blank=True, max_length=128, null=True),
        ),
    ]
