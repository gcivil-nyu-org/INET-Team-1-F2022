# Generated by Django 3.2.16 on 2022-12-18 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0055_auto_20221218_1346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='profile',
        ),
        migrations.AddField(
            model_name='comment',
            name='profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='account.profile'),
            preserve_default=False,
        ),
    ]
