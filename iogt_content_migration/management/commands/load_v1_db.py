from pathlib import Path
from django.core.management.base import BaseCommand
from wagtail.core.models import Page, Site
from django.core.files.images import ImageFile
from wagtail.images.models import Image
import home.models as models
import psycopg2
import psycopg2.extras
import json

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--host',
            default='0.0.0.0',
            help='IoGT V1 database host'
        )
        parser.add_argument(
            '--port',
            default='5432',
            help='IoGT V1 database port'
        )
        parser.add_argument(
            '--name',
            default='postgres',
            help='IoGT V1 database name'
        )
        parser.add_argument(
            '--user',
            default='postgres',
            help='IoGT V1 database user'
        )
        parser.add_argument(
            '--password',
            default='',
            help='IoGT V1 database password'
        )
        parser.add_argument(
            '--media-dir',
            required=True,
            help='Path to IoGT v1 media directory'
        )

    def handle(self, *args, **options):
        self.db_connect(options)
        self.media_dir = options.get('media_dir')

        self.clear()
        self.stdout.write('Existing site structure cleared')

        root = Page.get_first_root_node()
        self.migrate(root)

    def clear(self):
        models.FooterPage.objects.all().delete()
        models.FooterIndexPage.objects.all().delete()
        models.BannerPage.objects.all().delete()
        models.BannerIndexPage.objects.all().delete()
        models.Article.objects.all().delete()
        models.Section.objects.all().delete()
        models.SectionIndexPage.objects.all().delete()
        models.HomePage.objects.all().delete()
        Site.objects.all().delete()
        Image.objects.all().delete()

    def db_connect(self, options):
        connection_string = self.create_connection_string(options)
        self.stdout.write(f'DB connection string created, string={connection_string}')
        self.v1_conn = psycopg2.connect(connection_string)
        self.stdout.write('Connected to v1 DB')

    def __del__(self):
        try:
            self.v1_conn.close()
            self.stdout.write('Closed connection to v1 DB')
        except AttributeError:
            pass

    def create_connection_string(self, options):
        host = options.get('host', '0.0.0.0')
        port = options.get('port', '5432')
        name = options.get('name', 'postgres')
        user = options.get('user', 'postgres')
        password = options.get('password', '')
        return f"host={host} port={port} dbname={name} user={user} password={password}"

    def db_query(self, q):
        cur = self.v1_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(q)
        return cur

    def migrate(self, root):
        self.migrate_images()
        home = self.create_home_page(root)
        section_index_page, banner_index_page, footer_index_page = self.create_index_pages(home)
        self.migrate_sections(section_index_page)
        self.migrate_articles(section_index_page)
        self.migrate_banners(banner_index_page)
        self.migrate_footers(footer_index_page)
        Page.fix_tree()

    def create_home_page(self, root):
        cur = self.db_query('select * from core_main main join wagtailcore_page page on main.page_ptr_id = page.id')
        main = cur.fetchone()
        cur.close()
        home = None
        if main:
            home = models.HomePage(
                title=main['title'],
                draft_title=main['draft_title'],
                seo_title=main['seo_title'],
                slug=main['slug'],
                live=main['live'],
                latest_revision_created_at=main['latest_revision_created_at'],
                first_published_at=main['first_published_at'],
                last_published_at=main['last_published_at'],
            )
            root.add_child(instance=home)
        else:
            raise Exception('Could not find a main page in v1 DB')
        cur.close()

        cur = self.db_query('select * from wagtailcore_site')
        v1_site = cur.fetchone()
        cur.close()
        if v1_site:
            Site.objects.create(
                hostname=v1_site['hostname'],
                port=v1_site['port'],
                root_page=home,
                is_default_site=True,
                site_name=v1_site['site_name'] if v1_site['site_name'] else 'Internet of Good Things',
            )
        else:
            raise Exception('Could not find site in v1 DB')
        return home

    def create_index_pages(self, homepage):
        section_index_page = models.SectionIndexPage(title='Sections')
        homepage.add_child(instance=section_index_page)

        banner_index_page = models.BannerIndexPage(title='Banners')
        homepage.add_child(instance=banner_index_page)

        footer_footer_page = models.FooterIndexPage(title='Footers')
        homepage.add_child(instance=footer_footer_page)

        return section_index_page, banner_index_page, footer_footer_page

    def migrate_images(self):
        cur = self.db_query('select * from wagtailimages_image')
        content_type = self.find_content_type_id('wagtailimages', 'image')
        self.image_map = {}
        for row in cur:
            image_file = self.open_image_file(row['file'])
            if image_file:
                image = Image.objects.create(
                    title=row['title'],
                    file=ImageFile(image_file, name=row['file'].split('/')[-1]),
                    focal_point_x=row['focal_point_x'],
                    focal_point_y=row['focal_point_y'],
                    focal_point_width=row['focal_point_width'],
                    focal_point_height=row['focal_point_height'],
                    # uploaded_by_user='',
                )
                image.get_file_size()
                image.get_file_hash()
                tags = self.find_tags(content_type, row['id'])
                if tags:
                    image.tags.add(*tags)
                self.image_map.update({ row['id']: image })
        cur.close()
        self.stdout.write('Images migrated')

    def find_content_type_id(self, app_label, model):
        cur = self.db_query(f"select id from django_content_type where app_label = '{app_label}' and model = '{model}'")
        content_type = cur.fetchone()
        cur.close()
        return content_type.get('id')

    def open_image_file(self, file):
        file_path = Path(self.media_dir) / file
        try:
            return open(file_path, 'rb')
        except:
            self.stdout.write(f"Image file not found: {file_path}")

    def find_tags(self, content_type, object_id):
        tags_query = 'select t.name from taggit_tag t join taggit_taggeditem ti on t.id = ti.tag_id where ti.content_type_id = {} and ti.object_id = {}'
        cur = self.db_query(tags_query.format(content_type, object_id))
        tags = [tag['name'] for tag in cur]
        cur.close()
        return tags

    def migrate_sections(self, section_index_page):
        cur = self.db_query('select * from core_sectionpage csp join wagtailcore_page wcp on csp.page_ptr_id  = wcp.id order by wcp.path')
        for row in cur:
            self.create_section(section_index_page, row)
        cur.close()

    def create_section(self, section_index_page, row):
        section = models.Section(
            title=row['title'],
            draft_title=row['draft_title'],
            show_in_menus=True,
            font_color='1CABE2',
            slug=row['slug'],
            path=section_index_page.path + row['path'][12:],
            depth=row['depth'],
            numchild=row['numchild'],
            live=row['live'],
        )
        section.save()
        self.stdout.write(f"saved section, title={section.title}")

    def migrate_articles(self, section_index_page):
        cur = self.db_query("select * from core_articlepage cap join wagtailcore_page wcp on cap.page_ptr_id  = wcp.id where wcp.path like '000100010002%' order by wcp.path")
        for row in cur:
            self.create_article(section_index_page, row)
        cur.close()

    def create_article(self, section_index_page, row):
        article = models.Article(
            lead_image=self.image_map.get(row['image_id']),
            title=row['title'],
            draft_title=row['draft_title'],
            slug=row['slug'],
            path=section_index_page.path + row['path'][12:],
            depth=row['depth'],
            numchild=row['numchild'],
            live=row['live'],
            body=self.map_article_body(row['body']),
        )
        article.save()
        self.stdout.write(f"saved article, title={article.title}")

    def map_article_body(self, v1_body):
        v2_body = json.loads(v1_body)
        for block in v2_body:
            if block['type'] == 'paragraph':
                block['type'] = 'markdown'
        return json.dumps(v2_body)

    def migrate_banners(self, banner_index_page):
        cur = self.db_query("select * from core_bannerpage cbp join wagtailcore_page wcp on cbp.page_ptr_id  = wcp.id order by wcp.path")
        for row in cur:
            self.create_banner(banner_index_page, row)
        cur.close()

    def create_banner(self, banner_index_page, row):
        banner = models.BannerPage(
            banner_image=self.image_map.get(row['banner_id']),
            title=row['title'],
            draft_title=row['draft_title'],
            slug=row['slug'],
            path=banner_index_page.path + row['path'][12:],
            depth=row['depth'],
            numchild=row['numchild'],
            live=row['live']
        )
        banner.save()
        self.stdout.write(f"saved banner, title={banner.title}")

    def migrate_footers(self, footer_index_page):
        cur = self.db_query("select * from core_footerpage cfp join core_articlepage cap on cfp.articlepage_ptr_id = cap.page_ptr_id join wagtailcore_page wcp on cap.page_ptr_id = wcp.id order by wcp.path")
        for row in cur:
            self.create_footer(footer_index_page, row)
        cur.close()

    def create_footer(self, footer_index_page, row):
        footer = models.FooterPage(
            lead_image=self.image_map.get(row['image_id']),
            title=row['title'],
            draft_title=row['draft_title'],
            slug=row['slug'],
            path=footer_index_page.path + row['path'][12:],
            depth=row['depth'],
            numchild=row['numchild'],
            live=row['live'],
            body=self.map_article_body(row['body']),
        )
        footer.save()
        self.stdout.write(f"saved footer, title={footer.title}")
