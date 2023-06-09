# Generated by Django 3.2 on 2021-05-28 12:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0025_auto_20210528_1533'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servermessage',
            name='chat_id',
        ),
        migrations.RemoveField(
            model_name='servermessage',
            name='sender_id',
        ),
        migrations.RemoveField(
            model_name='servermessage',
            name='server_id',
        ),
        migrations.AddField(
            model_name='servermessage',
            name='chat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.serverchat'),
        ),
        migrations.AddField(
            model_name='servermessage',
            name='sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='servermessage',
            name='server',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.server'),
        ),
        migrations.AlterField(
            model_name='serverchat',
            name='server',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.server'),
        ),
    ]
