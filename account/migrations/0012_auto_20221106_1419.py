# Generated by Django 3.1 on 2022-11-06 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_auto_20221106_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender_identity',
            field=models.CharField(blank=True, choices=[('Woman', 'Woman'), ('Man', 'Man'), ('Transgender', 'Transgender'), ('Non-binary', 'Non-binaary')], default='N/A', max_length=15),
        ),
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default='users/default/user-default.png', upload_to='users/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='sexual_orientation',
            field=models.CharField(blank=True, choices=[('Lesbian', 'Lesbian'), ('Gay', 'Gay'), ('Bisexual', 'Bisexual'), ('Queer', 'Queer'), ('Asexual', 'Asexual'), ('Straight', 'Straight'), ('Other', 'Other')], default='N/A', max_length=15),
        ),
    ]
