# Generated by Django 4.1.2 on 2022-11-02 22:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0008_rename_age_preference_profile_age_preference_max_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="date_of_birth",
        ),
    ]
