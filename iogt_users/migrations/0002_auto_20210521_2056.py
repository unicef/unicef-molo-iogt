# Generated by Django 3.1.11 on 2021-05-21 20:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iogt_users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('id',)},
        ),
        migrations.RenameField(
            model_name='user',
            old_name='has_accepted_terms_and_conditions',
            new_name='terms_accepted',
        ),
    ]
