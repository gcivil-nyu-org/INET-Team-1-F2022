# Generated by Django 4.1.2 on 2022-11-16 17:01

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0020_remove_profile_proposal_location"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cusine",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cusine", models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name="profile",
            name="date_of_birth",
            field=models.DateField(
                blank=True, default=datetime.date(2022, 11, 16), null=True
            ),
        ),
        migrations.CreateModel(
            name="newLocation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("DBA", models.CharField(blank=True, max_length=255, null=True)),
                ("BORO", models.CharField(blank=True, max_length=255, null=True)),
                ("BUILDING", models.CharField(blank=True, max_length=255, null=True)),
                ("STREET", models.CharField(blank=True, max_length=255, null=True)),
                ("ZIPCODE", models.CharField(blank=True, max_length=255, null=True)),
                ("PHONE", models.CharField(blank=True, max_length=255, null=True)),
                ("LATITUDE", models.CharField(blank=True, max_length=255, null=True)),
                ("LONGITUDE", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "CUISINE",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="account.cusine",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="profile",
            name="cusine",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="account.cusine",
            ),
        ),
    ]
