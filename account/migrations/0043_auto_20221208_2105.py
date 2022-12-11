# Generated by Django 2.2 on 2022-12-08 21:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0042_auto_20221208_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='location_dropdown',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.newLocation'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='proposal_datetime_local',
            field=models.DateTimeField(null=True),
        ),
    ]