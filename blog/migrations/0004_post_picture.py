# Generated by Django 3.1.4 on 2021-01-24 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='picture',
            field=models.ImageField(default='default.jpg', upload_to='post_pics'),
        ),
    ]