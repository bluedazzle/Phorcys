from django.conf.urls import patterns, include, url
from myadmin.views import *

urlpatterns = patterns('',
                       url(r'^login$', AdminView.as_view()),
                       url(r'^index', AdminIndexView.as_view()),
                       url(r'^news/(?P<nid>(\d)+)', AdminModifyNewsView.as_view()),
                       url(r'^news', AdminNewsListView.as_view()),
                       url(r'^new_news', AdminNewNewsView.as_view()),
                       url(r'^players', AdminPlayerListView.as_view()),
                       url(r'^teams', AdminTeamListView.as_view()),
                       url(r'^tournaments', AdminTournamentListView.as_view()),
                       url(r'^tournament/(?P<tid>(\d)+)/match/(?P<mid>(\d)+)', AdminTournamentMatchView.as_view()),
                       url(r'^tournament/(?P<tid>(\d)+)', AdminTournamentDetailView.as_view()),
                       url(r'^tournament', AdminTournamentDetailView.as_view()),
                       url(r'^topics', AdminTopicListView.as_view()),
                       url(r'^setting', AdminSettingView.as_view()),
                       url(r'^logout', AdminLogoutView.as_view()),
                       url(r'^users', AdminUserListView.as_view()),
                       url(r'^invite', AdminInviteListView.as_view()),
                       url(r'^feedback', AdminFeedbackView.as_view()),
                       )
