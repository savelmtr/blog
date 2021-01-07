from wagtail.core.models import Page
from wagtail.search.models import Query
from wagtail.core.models import Site
from blog.models import BlogPage

def make_search_query(search_query, request):
    # Search
    if search_query:
        search_results = (
            Page.objects.live()
            .descendant_of(Site.find_for_request(request).root_page)
            .search(search_query)
        )
        query = Query.get(search_query)

        # Record hit
        query.add_hit()
    else:
        search_results = Page.objects.none()
    
    return search_results


def get_pages_by_tags(tags, request):
    if tags:
        results = (
            BlogPage.objects.live()
            .descendant_of(Site.find_for_request(request).root_page)
            .filter(tags__slug__in=tags)
        )
    else:
        results = BlogPage.objects.none()

    return results