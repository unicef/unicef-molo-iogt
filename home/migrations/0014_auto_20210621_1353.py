# Generated by Django 3.1.12 on 2021-06-21 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_merge_20210621_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cachesettings',
            name='cache',
            field=models.BooleanField(default=True, help_text='check to prompt first time users to download the website as an app', verbose_name='Prompt users to download?'),
        ),
    ]