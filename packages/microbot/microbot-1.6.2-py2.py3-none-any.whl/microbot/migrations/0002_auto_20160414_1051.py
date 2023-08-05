# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-14 15:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('microbot', '0001_initial'),
    ]

    operations = [
	migrations.RenameModel(
            old_name='Recipient',
            new_name='TelegramRecipient',
        ),
        migrations.RenameModel(
            old_name='Bot',
            new_name='TelegramBot',
        ),
        migrations.RenameModel(
            old_name='ChatState',
            new_name='TelegramChatState',
        ),
        migrations.AlterModelOptions(
            name='telegrambot',
            options={'verbose_name': 'Telegram Bot', 'verbose_name_plural': 'Telegram Bots'},
        ),
        migrations.AlterModelOptions(
            name='telegramrecipient',
            options={'verbose_name': 'Telegram Recipient', 'verbose_name_plural': 'Telegram Recipients'},
        ),
        migrations.AlterModelOptions(
            name='telegramchatstate',
            options={'verbose_name': 'Telegram Chat State', 'verbose_name_plural': 'Telegram Chats States'},
        ),
    ]
