# coding: utf-8
from __future__ import unicode_literals
from django.db import models
from core.models import *


# Create your models here.

class Position(BaseModel):
    title = models.CharField(max_length=10, unique=True)
    code = models.IntegerField(default=1)

    def __unicode__(self):
        return self.title


class News(BaseNews):
    def __unicode__(self):
        return self.title


class TournamentTheme(BaseTournament):
    def __unicode__(self):
        return self.name


class Tournament(BaseTournament):
    uuid = models.CharField(max_length=30, unique=True)
    belong = models.ForeignKey(TournamentTheme, related_name='theme_tournaments', null=True, blank=True,
                               on_delete=models.SET_NULL)

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
    wid = models.CharField(max_length=64, unique=True)
    player_author = models.ForeignKey(Player, related_name='player_weibos', on_delete=models.SET_NULL, null=True,
                                      blank=True)
    team_author = models.ForeignKey(Team, related_name='team_weibos', on_delete=models.SET_NULL, null=True, blank=True)

    def __unicode__(self):
        # return unicode(self.id)
        if self.type == 1:
            return '{0}-{1}-{2}'.format(self.title, self.player_author.nick,
                                        self.create_time.strftime('%Y-%m-%d %H:%M:%S'))
        else:
            return '{0}-{1}-{2}'.format(self.title, self.team_author.name,
                                        self.create_time.strftime('%Y-%m-%d %H:%M:%S'))


class SpiderConfig(BaseModel):
    since_id = models.CharField(max_length=64, default=None)

    def __unicode__(self):
        return self.since_id


class NewsComment(BaseComment):
    create_by = models.ForeignKey('myuser.EUser', related_name='user_news_comments', on_delete=models.SET_NULL,
                                  null=True, blank=True)
    belong = models.ForeignKey(News, related_name='news_comments', on_delete=models.SET_NULL, null=True, blank=True)

    def __unicode__(self):
        if hasattr(self.create_by, 'nick'):
            return self.create_by.nick
        return unicode(self.id)


class NewsCommentReply(BaseComment):
    create_by = models.ForeignKey('myuser.EUser', related_name='user_news_replies', on_delete=models.SET_NULL,
                                  null=True, blank=True)
    reply = models.ForeignKey('myuser.EUser', related_name='user_news_replied')
    belong = models.ForeignKey(NewsComment, related_name='user_replies_belong')

    def __unicode__(self):
        if hasattr(self.create_by, 'nick') and hasattr(self.reply, 'nick'):
            return '{0}-{1}'.format(self.create_by.nick, self.reply.nick)
        else:
            return unicode(self.id)


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
        (4, 'BO5'),
        (5, 'BO5')
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
    tournament = models.ForeignKey(Tournament, related_name='tournament_matches', null=True, blank=True)
    status = models.IntegerField(default=1, choices=status_choice)
    team1_support = models.IntegerField(default=0)
    team2_support = models.IntegerField(default=0)

    def __unicode__(self):
        return '{0}-{1}'.format(self.name, self.match_time.strftime('%Y-%m-%d %H:%M:%S'))


class Game(BaseModel):
    game_id = models.CharField(max_length=20, unique=True)
    game_time = models.DateTimeField()
    win = models.ForeignKey(Team, related_name='team_wins', null=True, blank=True, on_delete=models.SET_NULL)
    duration = models.IntegerField(default=0)
    team1 = models.ForeignKey(Team, related_name='team_blue_games',
                              null=True, blank=True, on_delete=models.SET_NULL)
    team2 = models.ForeignKey(Team, related_name='team_red_games',
                              null=True, blank=True, on_delete=models.SET_NULL)
    match = models.ForeignKey(Match, related_name='match_games', null=True, blank=True)
    team1_ban = models.ManyToManyField(Hero, related_name='blue_ban_heros', null=True, blank=True)
    team2_ban = models.ManyToManyField(Hero, related_name='red_ban_heros', null=True, blank=True)
    team1_total_economic = models.FloatField(default=0.0)
    team2_total_economic = models.FloatField(default=0.0)
    team1_kill = models.IntegerField(default=0)
    team2_kill = models.IntegerField(default=0)
    team1_tower = models.IntegerField(default=0)
    team2_tower = models.IntegerField(default=0)
    team1_dragon = models.IntegerField(default=0)
    team2_dragon = models.IntegerField(default=0)
    team1_nahsor = models.IntegerField(default=0)
    team2_nahsor = models.IntegerField(default=0)
    video = models.URLField(null=True, blank=True)
    over = models.BooleanField(default=False)

    def __unicode__(self):
        return '{0}-{1}'.format(self.game_id, self.id)


class GamePlayer(BaseModel):
    gid = models.CharField(max_length=64, unique=True)
    game = models.ForeignKey(Game, related_name='game_gameps', null=True, blank=True)
    player = models.ForeignKey(Player, related_name='player_game_players',
                               null=True, blank=True, on_delete=models.SET_NULL)
    hero = models.ForeignKey(Hero, related_name='hero_gps', null=True, blank=True, on_delete=models.SET_NULL)
    summoner1 = models.ForeignKey(SummonerSpells, related_name='summoner1_gps', null=True, blank=True,
                                  on_delete=models.SET_NULL)
    summoner2 = models.ForeignKey(SummonerSpells, related_name='summoner2_gps', null=True, blank=True,
                                  on_delete=models.SET_NULL)
    team = models.ForeignKey(Team, related_name='team_gplayers', null=True, blank=True, on_delete=models.SET_NULL)
    position = models.ForeignKey(Position, related_name='position_gplayers',
                                 null=True, blank=True, on_delete=models.SET_NULL)
    level = models.IntegerField(default=0)
    kill = models.IntegerField(default=0)
    dead = models.IntegerField(default=0)
    assist = models.IntegerField(default=0)
    kda = models.FloatField(default=0.0)
    war_rate = models.FloatField(default=0.0)
    farming = models.IntegerField(default=0)
    damage_rate = models.FloatField(default=0.0)
    economic = models.FloatField(default=0.0)
    equipments = models.ManyToManyField(Equipment, related_name='equipment_gps', null=True, blank=True)
    guard = models.ForeignKey(Equipment, null=True, related_name='guard_gps', blank=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.player.nick


class TournamentTeamInfo(BaseModel):
    uuid = models.CharField(max_length=64, unique=True)
    team = models.ForeignKey(Team, related_name='team_ttinfos', on_delete=models.SET_NULL, null=True, blank=True)
    tournament = models.ForeignKey(Tournament, related_name='team_tournaments', null=True, blank=True)
    rank = models.IntegerField(default=0)
    kda = models.FloatField(default=0.0)
    average_kill = models.FloatField(default=0.0)
    average_dead = models.FloatField(default=0.0)
    average_assist = models.FloatField(default=0.0)
    average_time = models.FloatField(default=0.0)
    average_money_pm = models.FloatField(default=0.0)
    victory_times = models.IntegerField(default=0)
    game_times = models.IntegerField(default=0)
    tied_times = models.IntegerField(default=0)
    fail_times = models.IntegerField(default=0)
    win_rate = models.FloatField(default=0.0)
    score = models.IntegerField(default=0)

    def __unicode__(self):
        return unicode(self.uuid)
        # return '{0}-{1}'.format(self.team.abbreviation, self.tournament.name)


class TotalTeamInfo(BaseModel):
    uuid = models.CharField(max_length=64, unique=True)
    team = models.ForeignKey(Team, related_name='team_totaltinfos', on_delete=models.SET_NULL, null=True, blank=True)
    tournament = models.ForeignKey(TournamentTheme, related_name='team_tournament_themes', null=True, blank=True)
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
    win_rate = models.FloatField(default=0.0)
    score = models.IntegerField(default=0)

    def __unicode__(self):
        return unicode(self.uuid)
        # return '{0}-{1}'.format(self.team.abbreviation, self.tournament.name)


class PlayerInfo(BaseModel):
    uuid = models.CharField(max_length=64, unique=True)
    player = models.ForeignKey(Player, related_name='player_ttinfos', null=True, blank=True)
    tournament = models.ForeignKey(Tournament, related_name='player_tournaments', null=True,
                                   blank=True)
    kda = models.FloatField(default=0.0)
    average_kill = models.FloatField(default=0.0)
    average_dead = models.FloatField(default=0.0)
    average_assist = models.FloatField(default=0.0)
    average_time = models.FloatField(default=0.0)
    average_money_pm = models.FloatField(default=0.0)
    average_hit_p10m = models.FloatField(default=0.0)
    average_melee_rate = models.FloatField(default=0.0)
    win_rate = models.FloatField(default=0.0)
    win_fail_rate = models.FloatField(default=0.0)
    victory_times = models.IntegerField(default=0)
    tied_times = models.IntegerField(default=0)
    fail_times = models.IntegerField(default=0)

    def __unicode__(self):
        return '{0}-{1}'.format(self.player.nick, self.tournament.name)


class TotalPlayerInfo(BaseModel):
    uuid = models.CharField(max_length=64, unique=True)
    player = models.ForeignKey(Player, related_name='player_totalinfos', null=True, blank=True)
    tournament = models.ForeignKey(TournamentTheme, related_name='player_tournament_themes', null=True,
                                   blank=True)
    kda = models.FloatField(default=0.0)
    average_kill = models.FloatField(default=0.0)
    average_dead = models.FloatField(default=0.0)
    average_assist = models.FloatField(default=0.0)
    average_time = models.FloatField(default=0.0)
    average_money_pm = models.FloatField(default=0.0)
    average_hit_p10m = models.FloatField(default=0.0)
    average_melee_rate = models.FloatField(default=0.0)
    win_rate = models.FloatField(default=0.0)
    win_fail_rate = models.FloatField(default=0.0)
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


class Tmp(BaseModel):
    pic_type = models.IntegerField(default=1)
    url = models.CharField(max_length=100, default='')
    team = models.ForeignKey(Team, related_name='tmp_teams', null=True, blank=True)
    player = models.ForeignKey(Player, related_name='tmp_players', null=True, blank=True)

    def __unicode__(self):
        return unicode(self.id)


class WeiboAdmin(BaseModel):
    token = models.CharField(max_length=128)
    uid = models.CharField(max_length=64, default='')

    def __unicode__(self):
        return self.token
