# Generated by Django 3.2 on 2021-05-25 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_profile_posts_liked'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='group_posts_liked',
            field=models.TextField(default=''),
        ),
    ]