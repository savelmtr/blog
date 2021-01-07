from rest_framework import generics
from .serializers import BlogPageSerializer, SearchPageSerializer
from blog.models import BlogPage
from wagtail.core.models import Site
from search.services import make_search_query, get_pages_by_tags


class BlogPagesListView(generics.ListAPIView):
    serializer_class = BlogPageSerializer
    
    def get(self, request):
        self.queryset = (BlogPage.objects.live()
            .descendant_of(Site.find_for_request(request).root_page))
        return super().get(request)


class SearchView(generics.ListAPIView):
    serializer_class = SearchPageSerializer

    def get(self, request):
        search_query = request.GET.get('query', None)
        self.queryset = make_search_query(search_query, request)
        return super().get(request)


class TagsView(generics.ListAPIView):
    serializer_class = BlogPageSerializer

    def get(self, request):
        tags = request.GET.get('query', None)
        tags = tags.split(',') if tags else None
        self.queryset = get_pages_by_tags(tags, request)
        return super().get(request)