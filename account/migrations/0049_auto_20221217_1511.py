# Generated by Django 3.2.16 on 2022-12-17 15:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0048_chatroom_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatroom',
            name='body',
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_of_birth',
            field=models.DateField(blank=True, default=datetime.date(2022, 12, 17), null=True),
        ),
    ]
