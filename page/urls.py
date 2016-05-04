from django.conf.urls import patterns, include, url
from myuser.views import *
from page.views import NewsDetailView

urlpatterns = patterns('',
                       url(r'^news/(?P<nid>(\d)+)', NewsDetailView.as_view()),
                       )
