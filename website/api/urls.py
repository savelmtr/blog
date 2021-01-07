from django.urls import path

from .views import BlogPagesListView, SearchView

app_name = 'api'

urlpatterns = [
    path('posts/', BlogPagesListView.as_view(), name='blog_pages_list'),
    path('search/', SearchView.as_view(), name='search'),
]
