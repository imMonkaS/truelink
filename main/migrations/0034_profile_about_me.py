# Generated by Django 3.2 on 2021-05-30 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_profile_black_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='about_me',
            field=models.TextField(default=''),
        ),
    ]
