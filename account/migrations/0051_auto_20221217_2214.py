# Generated by Django 3.2.16 on 2022-12-17 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0050_auto_20221217_1538'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='email',
        ),
        migrations.AlterField(
            model_name='comment',
            name='name',
            field=models.CharField(default='x', max_length=50),
        ),
    ]
