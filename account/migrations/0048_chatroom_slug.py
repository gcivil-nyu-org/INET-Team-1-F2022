# Generated by Django 3.2.16 on 2022-12-15 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0047_auto_20221215_1941'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='slug',
            field=models.SlugField(default='publicChat', max_length=250, unique_for_date='publish'),
        ),
    ]
