from django.conf.urls import patterns, include, url
from myadmin.api_views import *

urlpatterns = patterns('',
                       url(r'^login', AdminLoginView.as_view()),
                       url(r'^logout', AdminLogoutView.as_view()),
                       url(r'^index', AdminIndexView.as_view()),
                       url(r'^admin', AdminUserView.as_view()),
                       url(r'^tournament/(?P<tid>(\d)+)/match/(?P<mid>(\d)+)/game', AdminGameView.as_view()),
                       url(r'^tournament/(?P<tid>(\d)+)/match', AdminMatchView.as_view()),
                       url(r'^tournaments', AdminTournamentListView.as_view()),
                       url(r'^tournament', AdminTournamentView.as_view()),
                       url(r'^game', AdminGameDetailView.as_view()),
                       )
