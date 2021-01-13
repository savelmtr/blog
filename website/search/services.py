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
        q = []
        for t in tags:
            q.append(
                BlogPage.objects.live()
                .descendant_of(Site.find_for_request(request).root_page)
                .filter(tags__slug=t)
            )
        results = q[0].intersection(*q[1:])
    else:
        results = BlogPage.objects.none()

    return results


def count_pages(count, per_page):
    return count // per_page + (1 if count % per_page else 0)


def get_helper(func, q, request):
    per_page = settings.REST_FRAMEWORK['PAGE_SIZE']
    que = func(q, request)
    rslt = que[:per_page]
    cnt = que.count()
    totlp = count_pages(cnt, per_page)
    return rslt, totlp, cnt
