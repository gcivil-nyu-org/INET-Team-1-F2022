# Generated by Django 4.1.2 on 2022-11-08 22:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0013_remove_profile_users_like_profile_hides_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="matches",
            field=models.ManyToManyField(
                blank=True, related_name="matched_with", to="account.profile"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="date_of_birth",
            field=models.DateField(
                blank=True, default=datetime.date(2022, 11, 8), null=True
            ),
        ),
    ]
