# Generated by Django 3.2 on 2021-05-15 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20210515_2001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chats',
            name='datetime',
            field=models.DateTimeField(auto_now=True),
        ),
    ]