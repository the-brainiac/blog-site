# Generated by Django 3.0.5 on 2020-11-22 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20201121_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='profile_pic',
            field=models.ImageField(default='images/default.jpg', upload_to='profile_pics'),
        ),
    ]
