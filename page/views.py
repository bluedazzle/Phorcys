from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView

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
