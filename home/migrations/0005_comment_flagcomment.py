# Generated by Django 3.1.9 on 2021-05-06 08:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.search.index


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wagtailcore', '0059_apply_collection_ordering'),
        ('home', '0004_auto_20210409_1243'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('author_website', models.URLField(blank=True, verbose_name="author's Website")),
                ('comment', models.TextField(max_length=3000, verbose_name='comment')),
                ('submitted_at', models.DateTimeField(db_index=True, default=None, verbose_name='date/time submitted')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP address')),
                ('is_approved', models.BooleanField(default=True, verbose_name='is approved')),
                ('is_removed', models.BooleanField(db_index=True, default=False, verbose_name='is removed')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='wagtailcore.page')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='home.comment')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
        migrations.CreateModel(
            name='FlagComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flag', models.CharField(db_index=True, max_length=30, verbose_name='flag')),
                ('flagged_at', models.DateTimeField(default=None, verbose_name='flag date time')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_flags', to='home.comment', verbose_name='comment')),
                ('flagger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_flags', to=settings.AUTH_USER_MODEL, verbose_name='flagger')),
            ],
            options={
                'verbose_name': 'comment flag',
                'verbose_name_plural': 'comment flags',
                'unique_together': {('flagger', 'comment', 'flag')},
            },
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
    ]