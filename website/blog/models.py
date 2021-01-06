from django.db import models

from wagtail.core.models import Page
from wagtailmetadata.models import MetadataPageMixin
from wagtail.core.fields import StreamField
from wagtail.core.blocks import RichTextBlock
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from taggit.models import Tag as TaggitTag
from modelcluster.fields import ParentalKey
from wagtail.snippets.models import register_snippet
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, StreamFieldPanel, MultiFieldPanel

class BaseFieldsMixin(models.Model):
    image = models.ForeignKey(
        'wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+'
    )
    subtitle = models.CharField('Подзаголовок', max_length=255, blank=True, null=True)
    content_panels = [
        FieldPanel('subtitle'),
        ImageChooserPanel('image'),
    ]
    class Meta:
        abstract = True


class RootPage(BaseFieldsMixin, MetadataPageMixin, Page):
    subpage_types = ['BlogPage', ]

    content_panels = Page.content_panels + BaseFieldsMixin.content_panels


class BlogPage(BaseFieldsMixin, MetadataPageMixin, Page):
    parent_page_types = ['RootPage', ]

    body = StreamField([
        ('paragraph', RichTextBlock(icon='fa-paragraph', label='Текст')),
    ], blank=True, null=True)
    tags = ClusterTaggableManager(through='PageTag', blank=True)

    content_panels = Page.content_panels + [
        FieldRowPanel([
            MultiFieldPanel([StreamFieldPanel('body'), ], 
                heading='Основной материал', classname='col8'),
            MultiFieldPanel(
                [   
                    FieldPanel('subtitle'),
                    ImageChooserPanel('image'), 
                    FieldPanel('tags'), 
                ], classname='col4'),
        ]),
    ]


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