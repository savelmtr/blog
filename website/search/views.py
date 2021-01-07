from django.template.response import TemplateResponse
from django.views import View
from django.conf import settings

from .services import make_search_query, get_pages_by_tags


class Search(View):

    template_name = 'search/search.html'

    def get(self, request, *args, **kwargs):

        search_query = request.GET.get('query', None)
        search_results = make_search_query(search_query, request)[:settings.REST_FRAMEWORK['PAGE_SIZE']]
        count = make_search_query(search_query, request).count()
        total_pages = (
            count // settings.REST_FRAMEWORK['PAGE_SIZE'] 
            + (1 if count % settings.REST_FRAMEWORK['PAGE_SIZE'] else 0)
        )

        return TemplateResponse(request, self.template_name, {
            'total_pages': total_pages,
            'search_query': search_query,
            'search_results': search_results,
            'count': count,
        })


class SearchByTag(View):

    template_name = 'search/tag.html'

    def get(self, request, *args, **kwargs):

        tags = request.GET.get('query', None)
        tags = tags.split(',') if tags else None

        results = get_pages_by_tags(tags, request)[:settings.REST_FRAMEWORK['PAGE_SIZE']]
        count = get_pages_by_tags(tags, request).count()
        total_pages = (
            count // settings.REST_FRAMEWORK['PAGE_SIZE'] 
            + (1 if count % settings.REST_FRAMEWORK['PAGE_SIZE'] else 0)
        )

        return TemplateResponse(request, self.template_name, {
            'total_pages': total_pages,
            'tags': ', '.join(tags),
            'results': results,
            'count': count,
        })