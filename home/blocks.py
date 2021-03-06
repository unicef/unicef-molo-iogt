from django.forms.utils import flatatt
from django.template.loader import render_to_string
from django.utils.html import format_html, format_html_join

from wagtail.core import blocks
from wagtail.core.blocks import PageChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtailmedia.blocks import AbstractMediaChooserBlock


class MediaBlock(AbstractMediaChooserBlock):
    def render_basic(self, value, context=None):
        if not value:
            return ''

        if value.type == 'video':
            player_code = '''
            <div>
                <video width="320" height="240" controls>
                    {0}
                    Your browser does not support the video tag.
                </video>
            </div>
            <p class='article__content--video'>If you cannot view the above video, perhaps you would you like to <a href={1} download> download it? </a></p>
            '''
        else:
            player_code = '''
            <div>
                <audio controls>
                    {0}
                    Your browser does not support the audio element.
                </audio>
            </div>
            <p class='article__content--audio'>If you cannot listen to the above audio, perhaps you would like to <a href={1} download> download it? </a></p>
            '''

        return format_html(player_code, format_html_join(
            '\n', "<source{0}>",
            [[flatatt(s)] for s in value.sources]
        ), value.url)


class SocialMediaLinkBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255)
    link = blocks.URLBlock()
    image = ImageChooserBlock()

    class Meta:
        icon = 'site'


class SocialMediaShareButtonBlock(blocks.StructBlock):
    platform = blocks.CharBlock(max_length=255)
    is_active = blocks.BooleanBlock(required=False)
    image = ImageChooserBlock(required=False)

    class Meta:
        icon = 'site'


class EmbeddedQuestionnaireChooserBlock(blocks.PageChooserBlock):

    def render_basic(self, value, context=None):
        context.update({
            'object': value,
            'type': value.__class__.__name__,
            'form': value.get_form(),
        })
        return render_to_string('blocks/embedded_questionnaire.html', context)

    class Meta:
        icon = 'form'


class PageButtonBlock(blocks.StructBlock):
    page = blocks.PageChooserBlock()
    text = blocks.CharBlock(required=False, max_length=255)

    class Meta:
        template = 'blocks/page_button.html'


class ArticleChooserBlock(PageChooserBlock):
    def __init__(self, *args, **kwargs):
        super().__init__(target_model='home.Article', *args, **kwargs)

    class Meta:
        template = 'blocks/article_page.html'
