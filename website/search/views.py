from django.template.response import TemplateResponse
from django.views import View
from django.conf import settings

from .services import make_search_query, get_pages_by_tags, get_helper


class Search(View):

    template_name = 'search/search.html'

    def get(self, request, *args, **kwargs):

        search_query = request.GET.get('query', None)
        search_results, total_pages, count = get_helper(make_search_query, search_query, request)

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

        results, total_pages, count = get_helper(get_pages_by_tags, tags, request)

        return TemplateResponse(request, self.template_name, {
            'total_pages': total_pages,
            'tags': ', '.join(tags),
            'results': results,
            'count': count,
        })
