from rest_framework import serializers
from blog.models import BlogPage
from wagtail.core.models import Page
from django.utils import formats
from datetime import datetime
from django.utils.translation import gettext_lazy as _


class BlogPageSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['meta'] = '{0} {1}'.format(
            _('Posted on'),
            formats.date_format(datetime.fromisoformat(rep['date']), "DATE_FORMAT")
        )
        return rep

    class Meta:
        model = BlogPage
        fields = ('title', 'subtitle', 'date', 'url')


class SearchPageSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['subtitle'] = getattr(instance.specific, 'subtitle', None)
        rep['date'] = getattr(instance.specific, 'date', None)
        if rep['date']:
            rep['meta'] = '{0} {1}'.format(
                _('Posted on'),
                formats.date_format(datetime.fromisoformat(str(rep['date'])), "DATE_FORMAT")
            )
        return rep

    class Meta:
        model = Page
        fields = ('title', 'url')
