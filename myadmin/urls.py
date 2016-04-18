from django.conf.urls import patterns, include, url
from myadmin.views import *

urlpatterns = patterns('',
                       url(r'^login$', AdminView.as_view()),
                       url(r'^index', AdminIndexView.as_view()),
                       url(r'^news', AdminNewsListView.as_view()),
                       url(r'^players', AdminPlayerListView.as_view()),
                       url(r'^teams', AdminTeamListView.as_view()),
                       url(r'^tournaments', AdminTournamentListView.as_view()),
                       url(r'^topics', AdminTopicListView.as_view()),
                       )
