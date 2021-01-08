from django.template import Library
from wagtail.core.models import Site

register = Library()


@register.simple_tag(takes_context=True)
def get_root(context):
    return Site.find_for_request(context['request']).root_page


@register.simple_tag(takes_context=True)
def webp_image(context, img, token):
	format = 'format-jpeg'
	if 'webp,image' in context['request'].META['HTTP_ACCEPT']:
		format = 'format-webp'
	token = token.split()
	token.append(format)
	return img.get_rendition('|'.join(token))