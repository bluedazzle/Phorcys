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
    tournaments = models.ManyToManyField(Tournament, related_name='tournament_teams')

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
    picture = models.CharField(default='http://www.fibar.cn', max_length=100)

    def __unicode__(self):
        return self.name


class Equipment(BaseModel):
    name = models.CharField(max_length=30, unique=True)
    picture = models.CharField(default='http://www.fibar.cn', max_length=100)

    def __unicode__(self):
        return self.name


class Hero(BaseModel):
    hero = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50, unique=True)
    picture = models.CharField(default='http://www.fibar.cn', max_length=100)

    def __unicode__(self):
        return self.hero


class Match(BaseModel):
    match_choice = [
        (1, 'BO1'),
        (2, 'BO2'),
        (3, 'BO3'),
        (4, 'BO5')
    ]
    status_choice = [
        (1, '未进行'),
        (2, '进行中'),
        (3, '已结束')
    ]
    name = models.CharField(max_length=100, default='默认比赛')
    match_type = models.IntegerField(default=1, choices=match_choice)
    match_time = models.DateTimeField()
    team1_score = models.IntegerField(default=0)
    team2_score = models.IntegerField(default=0)
    team1 = models.ForeignKey(Team, related_name='team1_matches', null=True, blank=True, on_delete=models.SET_NULL)
    team2 = models.ForeignKey(Team, related_name='team2_matches', null=True, blank=True, on_delete=models.SET_NULL)
    tournament = models.ForeignKey(Tournament, related_name='tournament_matches', null=True, blank=True,
                                   on_delete=models.SET_NULL)
    status = models.IntegerField(default=1, choices=status_choice)

    def __unicode__(self):
        return self.name


class Game(BaseModel):
    game_id = models.CharField(max_length=20, unique=True)
    game_time = models.DateTimeField()
    win = models.ForeignKey(Team, related_name='team_wins', null=True, blank=True, on_delete=models.SET_NULL)
    duration = models.IntegerField(default=0)
    team1 = models.ForeignKey(Team, related_name='team_blue_games',
                              null=True, blank=True, on_delete=models.SET_NULL)
    team2 = models.ForeignKey(Team, related_name='team_red_games',
                              null=True, blank=True, on_delete=models.SET_NULL)
    match = models.ForeignKey(Match, related_name='match_games', null=True, blank=True, on_delete=models.SET_NULL)
    team1_ban = models.ManyToManyField(Hero, related_name='blue_ban_heros', null=True, blank=True)
    team2_ban = models.ManyToManyField(Hero, related_name='red_ban_heros', null=True, blank=True)

    def __unicode__(self):
        return self.game_id


class GamePlayer(BaseModel):
    site_choice = [
        (1, '蓝方'),
        (2, '红方')
    ]
    game = models.ForeignKey(Game, related_name='game_gameps', null=True, blank=True, on_delete=models.SET_NULL)
    player = models.ForeignKey(Player, related_name='player_game_players',
                               null=True, blank=True, on_delete=models.SET_NULL)
    hero = models.ForeignKey(Hero, related_name='hero_gps', null=True, blank=True, on_delete=models.SET_NULL)
    summoner1 = models.ForeignKey(SummonerSpells, related_name='summoner1_gps', null=True, blank=True,
                                  on_delete=models.SET_NULL)
    summoner2 = models.ForeignKey(SummonerSpells, related_name='summoner2_gps', null=True, blank=True,
                                  on_delete=models.SET_NULL)
    site = models.IntegerField(default=1, choices=site_choice)
    level = models.IntegerField(default=0)
    kill = models.IntegerField(default=0)
    dead = models.IntegerField(default=0)
    assist = models.IntegerField(default=0)
    kda = models.FloatField(default=0.0)
    war_rate = models.FloatField(default=0.0)
    farming = models.IntegerField(default=0)
    damage_rage = models.FloatField(default=0.0)
    economic = models.FloatField(default=0.0)
    equipments = models.ManyToManyField(Equipment, related_name='equipment_gps', null=True, blank=True)
    guard = models.ForeignKey(Equipment, null=True, related_name='guard_gps', blank=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.player.nick


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
        return unicode(self.id)
        # return '{0}-{1}'.format(self.team.abbreviation, self.tournament.name)


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
