# Generated by Django 3.0.3 on 2020-02-18 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openinghours', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openinghours',
            name='close',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='openinghours',
            name='open',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='openinghours',
            name='slots',
            field=models.IntegerField(null=True),
        ),
    ]
