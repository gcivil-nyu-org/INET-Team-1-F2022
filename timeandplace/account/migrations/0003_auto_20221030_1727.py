# Generated by Django 2.2 on 2022-10-31 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20221030_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='proposal_time',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]