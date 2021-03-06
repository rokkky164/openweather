# Generated by Django 2.2.22 on 2021-05-15 05:38

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(verbose_name='Latitude')),
                ('longitude', models.FloatField(verbose_name='Longitude')),
                ('weather_data', jsonfield.fields.JSONField(default=list)),
                ('time_frequency', models.CharField(choices=[('Minutely', 'Minutely'), ('Hourly', 'Hourly'), ('Daily', 'Daily')], max_length=50, null=True)),
                ('city', models.CharField(max_length=255, verbose_name='City')),
            ],
        ),
    ]
