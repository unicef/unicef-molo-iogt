# Generated by Django 3.1.12 on 2021-06-04 11:44

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0022_uploadedimage'),
        ('wagtailcore', '0059_apply_collection_ordering'),
        ('home', '0004_auto_20210409_1243'),
    ]

    operations = [
        migrations.CreateModel(
            name='BannerIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='BannerPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('external_link', models.URLField(blank=True, help_text='Optional external link which a banner will link to e.g., https://www.google.com', null=True)),
                ('banner_image', models.ForeignKey(help_text='Image to display as the banner', on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtailimages.image')),
                ('banner_link_page', models.ForeignKey(blank=True, help_text='Optional page to which the banner will link to', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='banners', to='wagtailcore.page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='HomePageBanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('banner_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.bannerpage')),
                ('source', modelcluster.fields.ParentalKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='home_page_banners', to='wagtailcore.page')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FeaturedContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.page')),
                ('source', modelcluster.fields.ParentalKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='featured_content', to='wagtailcore.page')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]