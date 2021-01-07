from rest_framework import generics
from .serializers import BlogPageSerializer, SearchPageSerializer
from blog.models import BlogPage
from wagtail.core.models import Site
from search.services import make_search_query


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
        self.queryset = make_search_query(search_query)
        return super().get(request)