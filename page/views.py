from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView, ListView

from lol.models import News


class NewsDetailView(DetailView):
    model = News
    pk_url_kwarg = 'nid'
    template_name = 'lol/news.html'
    http_method_names = ['get']

    def get_object(self, queryset=None):
        object = super(NewsDetailView, self).get_object(queryset)
        object.views += 1
        object.save()
        return object


class NewsListView(ListView):
    model = News
    http_method_names = ['get']
    template_name = 'lol/news_list.html'
    paginate_by = 20

    def get_queryset(self):
        queryset = super(NewsListView, self).get_queryset()
        queryset = queryset.filter(publish=True)
        return queryset
