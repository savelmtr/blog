from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse

from .services import make_search_query


class Search(View):

    template_name = 'search/search.html'

    def get(self, request, *args, **kwargs):

        search_query = request.GET.get('query', None)
        search_results = make_search_query(search_query)[:settings.REST_FRAMEWORK['PAGE_SIZE']]
        count = make_search_query(search_query).count()
        total_pages = (
            count // settings.REST_FRAMEWORK['PAGE_SIZE'] 
            + (1 if count % settings.REST_FRAMEWORK['PAGE_SIZE'] else 0)
        )

        return TemplateResponse(request, self.template_name, {
            'total_pages': total_pages,
            'search_query': search_query,
            'search_results': search_results,
        })
