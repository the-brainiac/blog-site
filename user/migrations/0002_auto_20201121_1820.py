# Generated by Django 3.0.5 on 2020-11-21 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='profile_pic',
            field=models.ImageField(upload_to='profile_pics'),
        ),
    ]
