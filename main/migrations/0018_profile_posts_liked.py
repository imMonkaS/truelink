# Generated by Django 3.2 on 2021-05-25 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20210525_0212'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='posts_liked',
            field=models.TextField(default=''),
        ),
    ]
