from wagtail.core.models import Page
from wagtail.search.models import Query


def make_search_query(search_query):
    # Search
    if search_query:
        search_results = Page.objects.live().search(search_query)
        query = Query.get(search_query)

        # Record hit
        query.add_hit()
    else:
        search_results = Page.objects.none()
    
    return search_results