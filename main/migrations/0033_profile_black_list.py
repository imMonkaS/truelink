# Generated by Django 3.2 on 2021-05-29 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_auto_20210529_0100'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='black_list',
            field=models.TextField(default=''),
        ),
    ]