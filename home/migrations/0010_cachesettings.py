# Generated by Django 3.1.12 on 2021-06-16 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0059_apply_collection_ordering'),
        ('home', '0009_merge_20210609_0608'),
    ]

    operations = [
        migrations.CreateModel(
            name='CacheSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cache', models.BooleanField(default=False, help_text='Decide if the site cache should be switch on / off', verbose_name='Cache settings')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.site')),
            ],
            options={
                'verbose_name': 'Cache settings',
            },
        ),
    ]