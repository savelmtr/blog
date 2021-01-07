from django import forms
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from taggit.models import Tag as TaggitTag
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import (FieldPanel, FieldRowPanel,
                                         InlinePanel, MultiFieldPanel,
                                         PageChooserPanel, StreamFieldPanel)
from wagtail.admin.staticfiles import versioned_static
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.blocks import RichTextBlock
from wagtail.core.fields import StreamField
from wagtail.core.models import Orderable, Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtailmetadata.models import MetadataPageMixin

from .streamblocks import Blockquote, SectionHeading, SingleImg


class BaseFieldsMixin(models.Model):
    image = models.ForeignKey(
        'wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+'
    )
    subtitle = models.CharField(_('Subtitle'), max_length=255, blank=True, null=True)
    content_panels = [
        FieldPanel('subtitle'),
        ImageChooserPanel('image'),
    ]
    class Meta:
        abstract = True


class BodyMixin(models.Model):

    body = StreamField([
        ('paragraph', RichTextBlock(icon='fa-paragraph', label=_('Text'))),
        ('section_heading', SectionHeading()),
        ('blockquote', Blockquote()),
        ('single_img', SingleImg()),
    ], blank=True, null=True)

    search_fields = [
        index.SearchField('body', partial_match=True),
    ]

    class Meta:
        abstract = True


class RootPage(BaseFieldsMixin, MetadataPageMixin, Page):
    subpage_types = ['BlogPage', 'FlatPage']

    content_panels = Page.content_panels + BaseFieldsMixin.content_panels

    def get_context(self, request):
        context = super().get_context(request)
        query = (BlogPage.objects.live()
            .descendant_of(self)[:settings.REST_FRAMEWORK['PAGE_SIZE']])
        count = BlogPage.objects.live().descendant_of(self).count()
        total_pages = (
            count // settings.REST_FRAMEWORK['PAGE_SIZE'] 
            + (1 if count % settings.REST_FRAMEWORK['PAGE_SIZE'] else 0)
        )
        context.update(
            {'posts': query, 'total_pages': total_pages})

        return context


class BlogPage(BodyMixin, BaseFieldsMixin, MetadataPageMixin, Page):
    parent_page_types = ['RootPage', ]

    tags = ClusterTaggableManager(through='PageTag', blank=True)
    date = models.DateTimeField(_('Date'), default=timezone.now)

    content_panels = Page.content_panels + [
        FieldRowPanel([
            MultiFieldPanel([StreamFieldPanel('body'), ], classname='col8'),
            MultiFieldPanel(
                [   
                    FieldPanel('subtitle'),
                    ImageChooserPanel('image'), 
                    FieldPanel('tags'),
                    FieldPanel('date'),
                ], classname='col4'),
        ]),
    ]

    search_fields = Page.search_fields + BodyMixin.search_fields

    class Meta:
        ordering = ['-date']


class FlatPage(BodyMixin, BaseFieldsMixin, MetadataPageMixin, Page):
    parent_page_types = ['RootPage', 'FlatPage']

    content_panels = Page.content_panels + [
        FieldRowPanel([
            MultiFieldPanel([StreamFieldPanel('body'), ], classname='col8'),
            MultiFieldPanel(
                [   
                    FieldPanel('subtitle'),
                    ImageChooserPanel('image')
                ], classname='col4'),
        ]),
    ]

    search_fields = Page.search_fields + BodyMixin.search_fields

class PageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage', on_delete=models.CASCADE, related_name='tagged_blog_pages'
    )


@register_snippet
class Tag(TaggitTag):
    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"
        proxy = True


@register_setting
class FooterSettings(BaseSetting):
    twitter_url = models.URLField(
        help_text=_('Your Twitter page URL'), blank=True, null=True)
    facebook_url = models.URLField(
        help_text=_('Your Facebook page URL'), blank=True, null=True)
    #linkedin_url = models.URLField(
    #    help_text='Your LinkedIn page URL', blank=True, null=True)
    github_url = models.URLField(
        help_text=_('Your GitHub page URL'), blank=True, null=True)
    #email = models.CharField(
    #    'Email', default='', max_length=255, help_text='Email', blank=True, null=True)
    #phone = models.CharField(
    #    'Phone number', max_length=255, help_text='Phone number', blank=True, null=True)
    #address = RichTextField('Address', blank=True, null=True)
    copyright = models.CharField(_('Copyright'), max_length=400, blank=True, null=True)

    class Meta:
        verbose_name = _('Footer Settings')


class MenuItem(Orderable):
    parent_page = ParentalKey(
        'blog.MainMenu',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='items'
    )

    page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    panels = [
        PageChooserPanel('page', ['blog.BlogPage', 'blog.FlatPage'])
    ]

    class Meta:
        verbose_name = _('Menu Item')
        verbose_name_plural = _('Menu Items')

@register_setting
class MainMenu(ClusterableModel, BaseSetting):
    home_link_text = models.CharField(_('Home Link Text'), max_length=255)

    panels = [
        FieldPanel('home_link_text'),
        InlinePanel('items', label=_('Menu Items')),
    ]
    class Meta:
        verbose_name = _('Main Menu')
