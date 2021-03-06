# Generated by Django 3.1.4 on 2021-02-20 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_auto_20201204_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='sbpri',
            name='Australia',
            field=models.DecimalField(blank=True, decimal_places=5, default='nan', max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='sbpri',
            name='Austria',
            field=models.DecimalField(blank=True, decimal_places=5, default='nan', max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='sbpri',
            name='Canada',
            field=models.DecimalField(blank=True, decimal_places=5, default='nan', max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='sbpri',
            name='Germany',
            field=models.DecimalField(blank=True, decimal_places=5, default='nan', max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='sbpri',
            name='India',
            field=models.DecimalField(blank=True, decimal_places=5, default='nan', max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='sbpri',
            name='Ireland',
            field=models.DecimalField(blank=True, decimal_places=5, default='nan', max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='sbpri',
            name='New_Zealand',
            field=models.DecimalField(blank=True, decimal_places=5, default='nan', max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='sbpri',
            name='Pakistan',
            field=models.DecimalField(blank=True, decimal_places=5, default='nan', max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='sbpri',
            name='Singapore',
            field=models.DecimalField(blank=True, decimal_places=5, default='nan', max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='sbpri',
            name='South_Africa',
            field=models.DecimalField(blank=True, decimal_places=5, default='nan', max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='sbpri',
            name='Switzerland',
            field=models.DecimalField(blank=True, decimal_places=5, default='nan', max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='sbpri',
            name='United_States',
            field=models.DecimalField(blank=True, decimal_places=5, default='nan', max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='sbpri',
            name='Argentina',
            field=models.DecimalField(blank=True, decimal_places=5, default='nan', max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='sbpri',
            name='Bolivia',
            field=models.DecimalField(blank=True, decimal_places=5, default='nan', max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='sbpri',
            name='Chile',
            field=models.DecimalField(blank=True, decimal_places=5, default='nan', max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='sbpri',
            name='Colombia',
            field=models.DecimalField(blank=True, decimal_places=5, default='nan', max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='sbpri',
            name='Ecuador',
            field=models.DecimalField(blank=True, decimal_places=5, default='nan', max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='sbpri',
            name='Mexico',
            field=models.DecimalField(blank=True, decimal_places=5, default='nan', max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='sbpri',
            name='Paraguay',
            field=models.DecimalField(blank=True, decimal_places=5, default='nan', max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='sbpri',
            name='Peru',
            field=models.DecimalField(blank=True, decimal_places=5, default='nan', max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='sbpri',
            name='Uruguay',
            field=models.DecimalField(blank=True, decimal_places=5, default='nan', max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='sbpri',
            name='Venezuela',
            field=models.DecimalField(blank=True, decimal_places=5, default='nan', max_digits=8, null=True),
        ),
    ]
