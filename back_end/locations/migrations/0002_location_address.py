# Generated by Django 3.0.3 on 2020-03-02 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='address',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
