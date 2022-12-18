# Generated by Django 3.2.16 on 2022-12-18 01:24

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0051_auto_20221217_2214'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.OneToOneField(default=3, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_of_birth',
            field=models.DateField(blank=True, default=datetime.date(2022, 12, 18), null=True),
        ),
    ]
