# Generated by Django 3.1.4 on 2021-05-21 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0007_auto_20210521_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worldborder',
            name='currency',
            field=models.CharField(default='still missing', max_length=30),
        ),
    ]
