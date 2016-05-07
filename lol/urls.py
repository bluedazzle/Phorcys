from django.conf.urls import patterns, include, url
from lol.views import *

urlpatterns = patterns('',
                       url(r'^news/(?P<nid>(\d)+)/comment', NewsCommentListView.as_view()),
                       url(r'^news/(?P<id>(\d)+)', NewsDetailView.as_view()),
                       url(r'^news', NewsListView.as_view()),
                       url(r'^bbs/(?P<id>(\d)+)', BBSDetalView.as_view()),
                       url(r'^bbs', BBSListView.as_view()),
                       url(r'^focus/player/(?P<pid>(\d)+)', FocusPlayerView.as_view()),
                       url(r'^focus/team/(?P<tid>(\d)+)', FocusTeamView.as_view()),
                       url(r'^focus/players', FocusPlayersListView.as_view()),
                       url(r'^focus/teams', FocusTeamsListView.as_view()),
                       url(r'^player/(?P<pid>(\d)+)/tournament/(?P<tid>(\d)+)', PlayerTournamentDetailView.as_view()),
                       url(r'^player/(?P<pid>(\d)+)/tournaments', PlayerTournamentsView.as_view()),
                       url(r'^player/(?P<id>(\d)+)', PlayerDetailView.as_view()),
                       url(r'^team/(?P<id>(\d)+)/tournament/(?P<tid>(\d)+)', TeamTournamentDetailView.as_view()),
                       url(r'^team/(?P<tid>(\d)+)/tournaments', TeamTournamentsView.as_view()),
                       url(r'^team/(?P<id>(\d)+)', TeamDetailView.as_view()),
                       url(r'^tournament/(?P<tid>(\d)+)/rank', TournamentRankView.as_view()),
                       url(r'^tournament/(?P<id>(\d)+)', TournamentDetailView.as_view()),
                       url(r'^match/(?P<id>(\d)+)', MatchDetailView.as_view()),
                       url(r'^matches', MatchListView.as_view()),
                       url(r'^players', PlayerListView.as_view()),
                       url(r'^heros', HeroListView.as_view()),
                       url(r'^summoners', SummonerListView.as_view()),
                       url(r'^equipments', EquipmentListView.as_view()),
                       url(r'^countries', CountryListView.as_view()),
                       url(r'^teams', TeamListView.as_view()),
                       url(r'^tournaments', TournamentListView.as_view()),
                       url(r'^comment', CommentCreateView.as_view()),
                       url(r'^thumb', ThumbView.as_view()),
                       url(r'^search', SearchView.as_view()),
                       url(r'^game/(?P<gid>(\d)+)', GameDetailView.as_view()),
                       url(r'^tmp', TmpListView.as_view()),
                       )
