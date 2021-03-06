# Generated by Django 3.1.13 on 2021-07-07 10:05
from django.core.management import call_command
from django.db import migrations


def _create_flat_menu(apps, schema_editor):
    Site = apps.get_model('wagtailcore.Site')
    IogtFlatMenuItem = apps.get_model('home.IogtFlatMenuItem')
    FlatMenu = apps.get_model('wagtailmenus.FlatMenu')
    HomePage = apps.get_model('home.HomePage')

    site = Site.objects.get(hostname='localhost')
    flat_menu = FlatMenu.objects.create(title='Navbar', site_id=site.id, handle='nav_bar')
    homepage = HomePage.objects.get(slug='home')
    IogtFlatMenuItem.objects.create(link_page=homepage, menu=flat_menu, url_append='#home')
    IogtFlatMenuItem.objects.create(
        link_url='#', menu=flat_menu, link_text='Sections', url_append='top-level-sections')


def _delete_flat_menu(apps, schema_editor):
    IogtFlatMenuItem = apps.get_model('home.IogtFlatMenuItem')
    FlatMenu = apps.get_model('wagtailmenus.FlatMenu')

    IogtFlatMenuItem.objects.all().delete()
    FlatMenu.objects.all().delete()


def _create_index_pages(apps, schema_editor):
    call_command('create_index_pages')


def _delete_index_pages(apps, schema_editor):
    BannerIndexPage = apps.get_model('home.BannerIndexPage')
    FooterIndexPage = apps.get_model('home.FooterIndexPage')
    SectionIndexPage = apps.get_model('home.SectionIndexPage')

    BannerIndexPage.objects.all().delete()
    FooterIndexPage.objects.all().delete()
    SectionIndexPage.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20210707_0702'),
        ('wagtail_localize', '0012_localesynchronization'),
    ]

    operations = [
        migrations.RunPython(_create_flat_menu, _delete_flat_menu),
        migrations.RunPython(_create_index_pages, _delete_index_pages),
    ]
