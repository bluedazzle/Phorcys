# coding: utf-8
from __future__ import unicode_literals
from django.db import models
from core.models import *


# Create your models here.

class Position(BaseModel):
    title = models.CharField(max_length=10, unique=True)

    def __unicode__(self):
        return self.title


class News(BaseNews):
    def __unicode__(self):
        return self.title


class Tournament(BaseTournament):
    def __unicode__(self):
        return self.name


class Topic(BaseTopic):
    author = models.ForeignKey('myuser.EUser', related_name='user_topics', on_delete=models.SET_NULL, null=True,
                               blank=True)

    def __unicode__(self):
        return '{0}-{1}'.format(self.title, self.author.nick)


class Team(BaseTeam):
    def __unicode__(self):
        return self.name


class Player(BasePlayer):
    position = models.ForeignKey(Position, related_name='position_players', on_delete=models.SET_NULL,
                                 null=True, blank=True)
    belong = models.ForeignKey(Team, related_name='team_players', on_delete=models.SET_NULL, null=True, blank=True)

    def __unicode__(self):
        return self.nick


class Weibo(BaseWeibo):
    type_choice = [(1, '选手微博'),
                   (2, '战队微博')]
    type = models.IntegerField(default=1, choices=type_choice)
    player_author = models.ForeignKey(Player, related_name='player_weibos', on_delete=models.SET_NULL, null=True,
                                      blank=True)
    team_author = models.ForeignKey(Team, related_name='team_weibos', on_delete=models.SET_NULL, null=True, blank=True)

    def __unicode__(self):
        if self.type == 1:
            return '{0}-{1}'.format(self.title, self.player_author.nick)
        else:
            return '{0}-{1}'.format(self.title, self.team_author.name)


class NewsComment(BaseComment):
    create_by = models.ForeignKey('myuser.EUser', related_name='user_news_comments', on_delete=models.SET_NULL,
                                  null=True, blank=True)
    belong = models.ForeignKey(News, related_name='news_comments', on_delete=models.SET_NULL, null=True, blank=True)

    def __unicode__(self):
        return self.create_by.nick


class TournamentComment(BaseComment):
    create_by = models.ForeignKey('myuser.EUser', related_name='user_tournament_comments', on_delete=models.SET_NULL,
                                  null=True, blank=True)
    belong = models.ForeignKey(Tournament, related_name='tournament_comments', on_delete=models.SET_NULL, null=True,
                               blank=True)

    def __unicode__(self):
        return self.create_by.nick


class WeiboComment(BaseComment):
    create_by = models.ForeignKey('myuser.EUser', related_name='user_weibo_comments', on_delete=models.SET_NULL,
                                  null=True, blank=True)
    belong = models.ForeignKey(Weibo, related_name='weibo_comments', on_delete=models.SET_NULL, null=True, blank=True)

    def __unicode__(self):
        return self.create_by.nick


class TopicComment(BaseComment):
    create_by = models.ForeignKey('myuser.EUser', related_name='user_topic_comments', on_delete=models.SET_NULL,
                                  null=True, blank=True)
    belong = models.ForeignKey(Topic, related_name='topic_comments', on_delete=models.SET_NULL, null=True, blank=True)

    def __unicode__(self):
        return self.create_by.nick


class SummonerSpells(BaseModel):
    name = models.CharField(max_length=20, unique=True)
    picture = models.ImageField(default='http://www.fibar.cn')

    def __unicode__(self):
        return self.name


class Equipment(BaseModel):
    name = models.CharField(max_length=30, unique=True)
    picture = models.ImageField(default='http://www.fibar.cn')

    def __unicode__(self):
        return self.name


class Hero(BaseModel):
    hero = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50, unique=True)
    picture = models.ImageField(default='http://www.fibar.cn')

    def __unicode__(self):
        return self.hero


class TournamentTeamInfo(BaseModel):
    team = models.ForeignKey(Team, related_name='team_ttinfos', on_delete=models.SET_NULL, null=True, blank=True)
    tournament = models.ForeignKey(Tournament, related_name='team_tournaments', on_delete=models.SET_NULL, null=True,
                                   blank=True)
    rank = models.IntegerField(default=0)
    kda = models.FloatField(default=0.0)
    average_kill = models.FloatField(default=0.0)
    average_dead = models.FloatField(default=0.0)
    average_assist = models.FloatField(default=0.0)
    average_time = models.FloatField(default=0.0)
    average_money_pm = models.FloatField(default=0.0)
    victory_times = models.IntegerField(default=0)
    tied_times = models.IntegerField(default=0)
    fail_times = models.IntegerField(default=0)

    def __unicode__(self):
        return '{0}-{1}'.format(self.team.short_name, self.tournament.name)


class PlayerInfo(BaseModel):
    player = models.ForeignKey(Player, related_name='player_ttinfos', on_delete=models.SET_NULL, null=True, blank=True)
    tournament = models.ForeignKey(Tournament, related_name='player_tournaments', on_delete=models.SET_NULL, null=True,
                                   blank=True)
    kda = models.FloatField(default=0.0)
    average_kill = models.FloatField(default=0.0)
    average_dead = models.FloatField(default=0.0)
    average_assist = models.FloatField(default=0.0)
    average_time = models.FloatField(default=0.0)
    average_money_pm = models.FloatField(default=0.0)
    victory_times = models.IntegerField(default=0)
    tied_times = models.IntegerField(default=0)
    fail_times = models.IntegerField(default=0)

    def __unicode__(self):
        return '{0}-{1}'.format(self.player.nick, self.tournament.name)


class LOLInfoExtend(BaseModel):
    focus_players = models.ManyToManyField(Player, related_name='player_followers', null=True, blank=True)
    focus_teams = models.ManyToManyField(Team, related_name='team_followers', null=True, blank=True)
    favourite_news = models.ManyToManyField(News, related_name='news_followers', null=True, blank=True)
    favourite_topic = models.ManyToManyField(Topic, related_name='topic_followers', null=True, blank=True)
    news_comment_thumb = models.ManyToManyField(News, related_name='news_thumbers', null=True, blank=True)
    topic_thumb = models.ManyToManyField(Topic, related_name='topic_thumbers', null=True, blank=True)
    topic_comment_thumb = models.ManyToManyField(TopicComment, related_name='topic_comment_thumbers', null=True,
                                                 blank=True)
    weibo_thumb = models.ManyToManyField(Weibo, related_name='weibo_thumbers', null=True, blank=True)
    tournament_thumb = models.ManyToManyField(Tournament, related_name='tournament_thumbers', null=True, blank=True)

    def __unicode__(self):
        return unicode(self.id)
