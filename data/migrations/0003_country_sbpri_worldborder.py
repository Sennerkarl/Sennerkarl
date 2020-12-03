# Generated by Django 3.1.4 on 2020-12-03 18:50

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('data', '0002_auto_20201103_1724'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('countries', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='SBPRI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('Bolivia', models.DecimalField(decimal_places=5, max_digits=8)),
                ('Uruguay', models.DecimalField(decimal_places=5, max_digits=8)),
                ('Paraguay', models.DecimalField(decimal_places=5, max_digits=8)),
                ('Venezuela', models.DecimalField(decimal_places=5, max_digits=8)),
                ('Colombia', models.DecimalField(decimal_places=5, max_digits=8)),
                ('Ecuador', models.DecimalField(decimal_places=5, max_digits=8)),
                ('Peru', models.DecimalField(decimal_places=5, max_digits=8)),
                ('Chile', models.DecimalField(decimal_places=5, max_digits=8)),
                ('Argentina', models.DecimalField(decimal_places=5, max_digits=8)),
                ('Mexico', models.DecimalField(decimal_places=5, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='WorldBorder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('area', models.IntegerField()),
                ('pop2005', models.IntegerField(verbose_name='Population 2005')),
                ('fips', models.CharField(max_length=2, null=True, verbose_name='FIPS Code')),
                ('iso2', models.CharField(max_length=2, verbose_name='2 Digit ISO')),
                ('iso3', models.CharField(max_length=3, verbose_name='3 Digit ISO')),
                ('un', models.IntegerField(verbose_name='United Nations Code')),
                ('region', models.IntegerField(verbose_name='Region Code')),
                ('subregion', models.IntegerField(verbose_name='Sub-Region Code')),
                ('lon', models.FloatField()),
                ('lat', models.FloatField()),
                ('mpoly', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
        ),
    ]
