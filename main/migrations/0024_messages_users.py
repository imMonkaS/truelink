# Generated by Django 3.2 on 2021-05-28 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_auto_20210528_1236'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='users',
            field=models.TextField(default='asd'),
            preserve_default=False,
        ),
    ]
