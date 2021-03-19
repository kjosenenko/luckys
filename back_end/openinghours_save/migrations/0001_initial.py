# Generated by Django 3.0.3 on 2020-02-18 03:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpeningHours',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.IntegerField(choices=[(1, 'Sunday'), (2, 'Monday'), (3, 'Tuesday'), (4, 'Wednesday'), (5, 'Thursday'), (6, 'Friday'), (7, 'Saturday')])),
                ('slots', models.IntegerField()),
                ('open', models.TimeField()),
                ('close', models.TimeField()),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.Location')),
            ],
        ),
    ]