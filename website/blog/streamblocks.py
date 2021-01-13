from wagtail.core.blocks import CharBlock, StructBlock, TextBlock, URLBlock
from wagtail.images.blocks import ImageChooserBlock
from django.utils.translation import gettext_lazy as _


class SectionHeading(CharBlock):

    class Meta:
        label = _('Section Heading')
        template = 'blog/streamblocks/section_heading.html'


class Blockquote(TextBlock):

    class Meta:
        label = _('Blockquote')
        template = 'blog/streamblocks/blockquote.html'


class SingleImg(StructBlock):
    image = ImageChooserBlock(_('Image'))
    url = URLBlock(label=_('URL'), required=False)
    caption = CharBlock(label=_('Caption'), required=False)

    class Meta:
        label = _('Single Image')
        template = 'blog/streamblocks/single_image.html'
