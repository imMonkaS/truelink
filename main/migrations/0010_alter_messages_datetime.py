# Generated by Django 3.2 on 2021-05-15 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_rename_chats_messages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='datetime',
            field=models.DateTimeField(auto_now=True),
        ),
    ]