# Generated by Django 2.2 on 2022-10-31 02:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20221030_1938'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='description',
            new_name='about_me',
        ),
    ]
