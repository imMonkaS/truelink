# Generated by Django 3.2 on 2021-05-15 23:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_chats_datetime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chats',
            old_name='user1',
            new_name='receiver_id',
        ),
        migrations.RenameField(
            model_name='chats',
            old_name='user2',
            new_name='sender_id',
        ),
    ]