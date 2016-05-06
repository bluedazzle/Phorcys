# coding: utf-8

from __future__ import unicode_literals

import time

from django.db.models import Q, Count
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View

from core.Mixin.CheckMixin import CheckSecurityMixin, CheckTokenMixin
from core.Mixin.StatusWrapMixin import *
from core.dss.Mixin import MultipleJsonResponseMixin, FormJsonResponseMixin, JsonResponseMixin

# Create your views here.
from core.dss.Serializer import serializer
from core.models import Country
from lol.models import News, NewsComment, Topic, Player, Team, Tournament, Weibo, Match, TournamentTeamInfo, Game, Hero, \
    SummonerSpells, Equipment, GamePlayer, TournamentTheme, PlayerInfo, TotalPlayerInfo, TotalTeamInfo
from lol.forms import *
from myuser.models import EUser


class NewsListView(CheckSecurityMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    """
    咨讯列表
    """

    model = News
    datetime_type = 'timestamp'
    paginate_by = 10
    exclude_attr = ['content', 'modify_time']
    http_method_names = ['get']

    def get_queryset(self):
        datetime_format = self.request.GET.get('datetime')
        all = self.request.GET.get('all')
        if datetime_format:
            self.datetime_type = datetime_format
        queryset = super(NewsListView, self).get_queryset().order_by('-create_time')
        if not all:
            queryset = queryset.filter(publish=True)
        queryset = queryset.annotate(comment_number=Count('news_comments'))
        queryset = queryset.annotate(follow_number=Count('news_followers'))
        return queryset


class NewsDetailView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    """
    资讯详情列表
    """

    model = News
    http_method_names = ['get']
    datetime_type = 'timestamp'
    pk_url_kwarg = 'id'


class NewsCommentListView(CheckSecurityMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    """
    资讯评论列表
    """

    model = NewsComment
    http_method_names = ['get']
    datetime_type = 'timestamp'
    include_attr = ['create_time', 'content', 'thumb', 'id']
    paginate_by = 20
    belong = None

    def get_queryset(self):
        news_list = News.objects.filter(id=self.kwargs.get('nid'))
        if news_list.exists():
            self.belong = news_list[0]
        else:
            self.message = '资讯不存在'
            self.status_code = INFO_NO_EXIST
        self.queryset = NewsComment.objects.filter(belong=self.belong)
        return self.queryset


class BBSListView(CheckSecurityMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    """
    社区列表
    """

    model = Topic
    datetime_type = 'timestamp'
    paginate_by = 10
    foreign = True
    http_method_names = ['get']
    exclude_attr = ['password', 'token', 'modify_time', 'last_login', 'content']


class BBSDetalView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    """
    获取帖子详情
    """

    model = Topic
    http_method_names = ['get']
    datetime_type = 'timestamp'
    pk_url_kwarg = 'id'
    foreign = True
    exclude_attr = ['password', 'token', 'modify_time', 'last_login']


class BBSCreateView(CheckSecurityMixin, StatusWrapMixin, FormJsonResponseMixin, CreateView):
    """
    发帖
    """

    model = Topic
    http_method_names = ['post']
    datetime_type = 'timestamp'


class FocusPlayersListView(CheckSecurityMixin, CheckTokenMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    """
    关注选手列表
    """

    model = Player
    http_method_names = ['get']
    exclude_attr = ['modify_time']
    datetime_type = 'timestamp'
    paginate_by = 40

    def get_queryset(self):
        self.queryset = self.user.lol.focus_players.all()
        return self.queryset

    def get(self, request, *args, **kwargs):
        if not self.wrap_check_token_result():
            return self.render_to_response(dict())
        return super(FocusPlayersListView, self).get(request, *args, **kwargs)


class FocusTeamsListView(CheckSecurityMixin, CheckTokenMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    """
    关注战队列表
    """

    model = Player
    http_method_names = ['get']
    exclude_attr = ['modify_time']
    datetime_type = 'timestamp'
    paginate_by = 40

    def get(self, request, *args, **kwargs):
        if not self.wrap_check_token_result():
            return self.render_to_response(dict())
        return super(FocusTeamsListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        self.queryset = self.user.lol.focus_teams.all()
        return self.queryset


class FocusTeamView(CheckSecurityMixin, CheckTokenMixin, StatusWrapMixin, JsonResponseMixin, UpdateView):
    """
    关注/取关战队
    """

    model = Team
    http_method_names = ['patch']
    datetime_type = 'timestamp'
    pk_url_kwarg = 'tid'

    def patch(self, request, *args, **kwargs):
        if not self.wrap_check_sign_result():
            return self.render_to_response(dict())
        if not self.wrap_check_token_result():
            return self.render_to_response(dict())
        tid = kwargs.get('tid', None)
        teams = Team.objects.filter(id=tid)
        if teams.exists():
            team = teams[0]
            focus_teams = self.user.lol.focus_teams
            if team in focus_teams.all():
                focus_teams.remove(team)
                return self.render_to_response({'focus': False})
            focus_teams.add(team)
            return self.render_to_response({'focus': True})
        self.message = '战队不存在'
        self.status_code = INFO_NO_EXIST
        return self.render_to_response(dict())


class FocusPlayerView(CheckSecurityMixin, CheckTokenMixin, StatusWrapMixin, JsonResponseMixin, UpdateView):
    """
    关注/取关选手
    """

    model = Player
    http_method_names = ['patch']
    datetime_type = 'timestamp'
    pk_url_kwarg = 'pid'

    def patch(self, request, *args, **kwargs):
        if not self.wrap_check_sign_result():
            return self.render_to_response(dict())
        if not self.wrap_check_token_result():
            return self.render_to_response(dict())
        pid = kwargs.get('pid', None)
        players = Player.objects.filter(id=pid)
        if players.exists():
            player = players[0]
            focus_players = self.user.lol.focus_players
            if player in focus_players.all():
                focus_players.remove(player)
                return self.render_to_response({'focus': False})
            focus_players.add(player)
            return self.render_to_response({'focus': True})
        self.message = '选手不存在'
        self.status_code = INFO_NO_EXIST
        return self.render_to_response(dict())


class PlayerDetailView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    """
    选手详情
    """

    model = Player
    http_method_names = ['get']
    exclude_attr = ['modify_time', 'create_time']
    foreign = True
    pk_url_kwarg = 'id'


class TeamDetailView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    """
    战队详情
    """

    model = Team
    http_method_names = ['get']
    exclude_attr = ['modify_time', 'create_time']
    foreign = True
    pk_url_kwarg = 'id'

    def get_object(self, queryset=None):
        obj = super(TeamDetailView, self).get_object()
        if self.request.GET.get('add_player'):
            player_list = Player.objects.filter(belong=obj)
            if player_list.exists():
                setattr(obj, 'player_list', player_list)
        return obj


class PlayerListView(CheckSecurityMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    """
    选手列表
    """

    model = Player
    http_method_names = ['get']
    exclude_attr = ['modify_time', 'create_time']
    foreign = True
    paginate_by = 60
    ordering = '-nick, -create_time'

    def get_queryset(self):
        queryset = super(PlayerListView, self).get_queryset()
        query_str = self.request.GET.get('query')
        if query_str:
            queryset = queryset.filter(Q(nick__icontains=query_str) | Q(name__icontains=query_str))
        return queryset


class TeamListView(CheckSecurityMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    """
    战队列表
    """

    model = Team
    http_method_names = ['get']
    exclude_attr = ['modify_time', 'create_time']
    foreign = True
    paginate_by = 20

    def get_queryset(self):
        queryset = super(TeamListView, self).get_queryset()
        if self.request.GET.get('add_player'):
            map(self.add_player, queryset)
        query_str = self.request.GET.get('query')
        if query_str:
            queryset = queryset.filter(Q(name__icontains=query_str) | Q(abbreviation__icontains=query_str))
        return queryset

    def get(self, request, *args, **kwargs):
        all = request.GET.get('all')
        if all:
            self.paginate_by = 0
        return super(TeamListView, self).get(request, *args, **kwargs)

    def add_player(self, team):
        player_list = team.team_players.all()
        if player_list.exists():
            setattr(team, 'players', player_list)
        else:
            setattr(team, 'players', None)


class TournamentListView(CheckSecurityMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    """
    联赛列表
    """

    model = TournamentTheme
    http_method_names = ['get']
    exclude_attr = ['modify_time', 'create_time']
    paginate_by = 20


class TournamentDetailView(CheckSecurityMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    """
    联赛详情
    """

    model = Tournament
    http_method_names = ['get']
    exclude_attr = ['modify_time']
    foreign = True
    pk_url_kwarg = 'id'
    object = None
    is_tournament = None

    def get_object(self):
        queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        queryset = queryset.filter(pk=pk)
        try:
            obj = queryset.get()
        except Exception, e:
            self.message = 'no data'
            self.status_code = INFO_NO_EXIST
        return obj

    def get(self, request, *args, **kwargs):
        self.is_tournament = request.GET.get('ist')
        if self.is_tournament:
            self.object_list = self.get_queryset()
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        else:
            return super(TournamentDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TournamentDetailView, self).get_context_data(**kwargs)
        if self.is_tournament:
            match_list = Match.objects.filter(tournament=self.object).order_by('-match_time')
            team_list = self.object.tournament_teams.all()
            context['tournament'] = self.object
            del context['tournament_list']
            context['match_list'] = match_list
            context['team_list'] = team_list
            return context
        else:
            tournament_list = context['tournament_list']
            pk = self.kwargs.get(self.pk_url_kwarg, None)
            tt = TournamentTheme.objects.filter(id=pk)
            if tt.exists():
                tournament_list = tournament_list.filter(belong=tt)
                map(self.get_match_and_team, tournament_list)
                context['tournament_list'] = tournament_list
                return context
            self.message = 'no data'
            self.status_code = INFO_NO_EXIST
            return dict()

    def get_match_and_team(self, tournament):
        match_list = Match.objects.filter(tournament=tournament)
        team_list = tournament.tournament_teams.all()
        setattr(tournament, 'match_list', match_list)
        setattr(tournament, 'team_list', team_list)


class MatchListView(CheckSecurityMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    """
    比赛列表
    """

    model = Match
    http_method_names = ['get']
    datetime_type = 'string'
    foreign = True
    paginate_by = 20

    def get_queryset(self):
        feature = self.request.GET.get('feature')
        date = datetime.date.today() + datetime.timedelta(days=1)
        queryset = super(MatchListView, self).get_queryset()
        if feature:
            queryset = queryset.filter(match_time__gte=date).order_by('match_time')
        else:
            queryset = queryset.filter(match_time__lt=date).order_by('-match_time')
        map(self.add_date, queryset)
        return queryset

    def add_date(self, match):
        match_date = match.match_time.strftime('%Y%m%d')
        match_weekday = match.match_time.weekday() + 1
        setattr(match, 'match_date', match_date)
        setattr(match, 'match_weekday', match_weekday)


class MatchDetailView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    """
    联赛比赛详情
    """

    model = Match
    http_method_names = ['get']
    foreign = True
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        game_list = Game.objects.filter(match=self.object).order_by('-create_time')
        context = super(MatchDetailView, self).get_context_data(**kwargs)
        map(self.get_ban_list, game_list)
        # map(self.get_game_detail, game_list)
        context['game_list'] = game_list
        return context

    # def get_game_detail(self, game):
    #     detail_list = game.game_gameps.all().order_by('team_id')
    #     if detail_list:
    #         for itm in detail_list:
    #             equipments = itm.equipments.all()
    #             position = itm.position
    #             itm.position = position
    #             summoner1 = itm.summoner1
    #             summoner2 = itm.summoner2
    #             setattr(itm, 'equipments', equipments)
    #             setattr(itm, 'summoner1', summoner1)
    #             setattr(itm, 'summoner2', summoner2)
    #         setattr(game, 'detail_list', detail_list)
    #     else:
    #         setattr(game, 'detail_list', None)

    def get_ban_list(self, game):
        team1_ban = game.team1_ban.all()
        team2_ban = game.team2_ban.all()
        if team1_ban.exists():
            setattr(game, 'team1_bans', team1_ban)
        else:
            setattr(game, 'team1_bans', None)
        if team2_ban.exists():
            setattr(game, 'team2_bans', team2_ban)
        else:
            setattr(game, 'team2_bans', None)


class GameDetailView(CheckSecurityMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    """
    对局详情
    """

    model = GamePlayer
    http_method_names = ['get']
    foreign = True

    def get_queryset(self):
        queryset = super(GameDetailView, self).get_queryset()
        game_id = self.kwargs.get('gid', '')
        game = Game.objects.get(game_id=game_id)
        queryset = queryset.filter(game=game).order_by('team_id', '-create_time')
        map(self.get_equipments, queryset)
        return queryset

    def get_equipments(self, detail):
        equipments = detail.equipments.all()
        if equipments.exists():
            setattr(detail, 'equipment_list', equipments)
        else:
            setattr(detail, 'equipment_list', None)


class CommentCreateView(CheckSecurityMixin, CheckTokenMixin, StatusWrapMixin, JsonResponseMixin, CreateView):
    """
    新评论
    """

    http_method_names = ['post']
    pk_url_kwarg = 'token'
    exclude_attr = ['modify_time', 'country', 'flag']
    success_url = 'localhost'
    obj = None
    type = 0

    def get_obj(self):
        obj_list = [None, News, Topic, Weibo, Tournament]
        cid = self.request.POST.get('id', '')
        self.type = int(self.request.POST.get('type'))
        if self.type not in range(1, 5):
            self.status_code = INFO_NO_EXIST
            self.message = '评论类型不存在'
            return None
        objs = obj_list[self.type].objects.filter(id=cid)
        if not objs.exists():
            self.message = '评论主题不存在'
            self.status_code = INFO_NO_EXIST
            return None
        self.obj = objs[0]
        return self.obj

    def get_form_class(self):
        form_list = (None, NewsCommentForm, TopicCommentForm, WeiboCommentForm, TournamentCommentForm)
        if self.type not in range(1, 5):
            self.status_code = INFO_NO_EXIST
            self.message = '评论类型不存在'
            self.type = 0
        self.form_class = form_list[self.type]
        return self.form_class

    def form_valid(self, form):
        super(CommentCreateView, self).form_valid(form)
        self.object.create_by = self.user
        self.object.belong = self.obj
        self.object.save()
        return self.render_to_response(dict())

    def post(self, request, *args, **kwargs):
        if not self.wrap_check_sign_result():
            return self.render_to_response(dict())
        if not self.wrap_check_token_result():
            return self.render_to_response(dict())
        if not self.get_obj():
            return self.render_to_response(dict())
        return super(CommentCreateView, self).post(request, *args, **kwargs)


class ThumbView(CheckSecurityMixin, CheckTokenMixin, StatusWrapMixin, JsonResponseMixin, UpdateView):
    """
    点赞/取赞
    """

    http_method_names = ['post']
    pk_url_kwarg = 'token'
    success_url = 'localhost'
    obj = None
    type = 0

    def get_obj(self):
        obj_list = [None, NewsComment, Topic, TopicComment, Weibo, Tournament]
        tid = self.request.POST.get('id', '')
        self.type = int(self.request.POST.get('type'))
        if self.type not in range(1, 6):
            self.status_code = INFO_NO_EXIST
            self.message = '点赞类型不存在'
            return None
        objs = obj_list[self.type].objects.filter(id=tid)
        if not objs.exists():
            self.message = '点赞主题不存在'
            self.status_code = INFO_NO_EXIST
            return None
        self.obj = objs[0]
        return self.obj

    def post(self, request, *args, **kwargs):
        if not self.wrap_check_sign_result():
            return self.render_to_response(dict())
        if not self.wrap_check_token_result():
            return self.render_to_response(dict())
        if not self.get_obj():
            return self.render_to_response(dict())
        lol_ext = self.user.lol
        thumb_list = [None, lol_ext.news_comment_thumb,
                      lol_ext.topic_thumb,
                      lol_ext.topic_comment_thumb,
                      lol_ext.weibo_thumb,
                      lol_ext.tournament_thumb]
        thumb_obj = thumb_list[self.type]
        if self.obj not in thumb_obj.all():
            thumb_obj.add(self.obj)
            self.obj.thumb += 1
            self.obj.save()
            return self.render_to_response({'thumb': True})
        return self.render_to_response({'thumb': False})


class SearchView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, ListView):
    """
    搜索视图
    """

    http_method_names = ['get']
    model = Team
    type = 1
    content = ''
    include_attr = ['name', 'nick', 'logo', 'avatar', 'id', 'abbreviation']

    def get_queryset(self):
        result_dict = {}
        self.type = int(self.request.GET.get('type', 1))
        self.content = self.request.GET.get('content', '')
        if self.content == '':
            return result_dict
        player_list = Player.objects.filter(nick__icontains=self.content)
        team_list = Team.objects.filter(Q(name__icontains=self.content) | Q(abbreviation__icontains=self.content))
        result_dict['players'] = player_list
        result_dict['teams'] = team_list
        if self.type == 2:
            return result_dict
        tournament_list = Tournament.objects.filter(name__icontains=self.content)
        result_dict['tournaments'] = tournament_list
        return result_dict


class HeroListView(CheckSecurityMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    """
    英雄列表
    """

    model = Hero
    paginate_by = 20
    include_attr = ['picture', 'hero', 'name', 'id']

    def get(self, request, *args, **kwargs):
        all = request.GET.get('all')
        if all:
            self.paginate_by = 0
        return super(HeroListView, self).get(request, *args, **kwargs)


class SummonerListView(CheckSecurityMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    """
    召唤师技能列表
    """

    model = SummonerSpells
    include_attr = ['picture', 'id', 'name']


class EquipmentListView(CheckSecurityMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    """
    装备列表
    """

    include_attr = ['picture', 'id', 'name']
    model = Equipment
    paginate_by = 20

    def get(self, request, *args, **kwargs):
        all = request.GET.get('all')
        if all:
            self.paginate_by = 0
        return super(EquipmentListView, self).get(request, *args, **kwargs)


class CountryListView(CheckSecurityMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    """
    国家列表
    """

    include_attr = ['name', 'flag']
    model = Country


class PlayerTournamentDetailView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    """
    选手赛事信息
    """

    model = PlayerInfo
    datetime_type = 'timestamp'
    exclude_attr = ['tournament', 'player', 'game', 'country', 'team']
    foreign = True

    def get(self, request, *args, **kwargs):
        tid = self.kwargs.get('tid')
        pid = self.kwargs.get('pid')
        if tid and pid:
            piid = '{0}p{1}'.format(tid, pid)
            player_info_list = TotalPlayerInfo.objects.filter(uuid=piid)
            if player_info_list.exists():
                player_info = player_info_list[0]
                context = self.get_game_detail_list(pid, tid)
                context['player_info'] = player_info
                return self.render_to_response(context)
            self.message = '选手赛事信息不存在'
            self.status_code = INFO_NO_EXIST
            return self.render_to_response(dict())
        self.message = '参数缺失'
        self.status_code = ERROR_DATA
        return self.render_to_response(dict())

    def get_game_detail_list(self, pid, tid):
        player = Player.objects.get(id=pid)
        tournament_theme = TournamentTheme.objects.get(id=tid)
        tournament_list = tournament_theme.theme_tournaments.all()
        player_detail_list = []
        for tournament in tournament_list:
            match_list = Match.objects.filter(tournament=tournament)
            for match in match_list:
                game_list = match.match_games.all()
                for game in game_list:
                    gps = game.game_gameps.filter(player=player)
                    if gps.exists():
                        gps = gps[0]
                        setattr(gps, 'game_id', game.game_id)
                        setattr(gps, 'game_time', int(time.mktime(game.game_time.timetuple())))
                        player_detail_list.append(gps)
        player_detail_list.sort(key=lambda player_info: player_info.game_time, reverse=True)
        context = {'history': player_detail_list}
        return context


class PlayerTournamentsView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    """
    选手参赛列表
    """

    model = TournamentTheme

    def get(self, request, *args, **kwargs):
        pid = self.kwargs.get('pid')
        if pid:
            player = Player.objects.filter(id=pid)
            if player.exists():
                player = player[0]
                team = player.belong
                tournament_list = team.tournaments.all()
                tournaments = []
                for tournament in tournament_list:
                    tt = tournament.belong
                    tournament_dict = {'title': tt.name, 'id': tt.id}
                    if tournament_dict not in tournaments:
                        tournaments.append(tournament_dict)
                return self.render_to_response({'tournaments': tournaments})
            else:
                self.message = '选手不存在'
                self.status_code = INFO_NO_EXIST
                return self.render_to_response(dict())
        self.message = '参数错误'
        self.status_code = ERROR_DATA


class TeamTournamentsView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    """
    战队参赛列表
    """

    model = TournamentTheme

    def get(self, request, *args, **kwargs):
        tid = self.kwargs.get('tid')
        if tid:
            team = Team.objects.filter(id=tid)
            if team.exists():
                team = team[0]
                tournament_list = team.tournaments.all()
                tournaments = []
                for tournament in tournament_list:
                    tt = tournament.belong
                    tournament_dict = {'title': tt.name, 'id': tt.id}
                    if tournament_dict not in tournaments:
                        tournaments.append(tournament_dict)
                return self.render_to_response({'tournaments': tournaments})
            else:
                self.message = '战队不存在'
                self.status_code = INFO_NO_EXIST
                return self.render_to_response(dict())
        self.message = '参数错误'
        self.status_code = ERROR_DATA


class TeamTournamentDetailView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, View):
    """
    战队联赛信息
    """
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        tid = self.kwargs.get('tid')
        id = self.kwargs.get('id')
        if id and tid:
            tiid = '{0}t{1}'.format(tid, id)
            team_info_list = TotalTeamInfo.objects.filter(uuid=tiid)
            if team_info_list.exists():
                team_info = team_info_list[0]
                context = {'team_info': team_info}
                return self.render_to_response(context)
            self.message = '战队赛事信息不存在'
            self.status_code = INFO_NO_EXIST
            return self.render_to_response(dict())
        self.message = '参数缺失'
        self.status_code = ERROR_DATA
        return self.render_to_response(dict())


class TournamentRankView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, View):
    """
    联赛排名列表
    """

    http_method_names = ['get']
    foreign = True
    include_attr = ['rank', 'score', 'victory_times', 'start_time', 'end_time',
                    'fail_times', 'team', 'name', 'abbreviation', 'cover', 'id', 'logo']

    def get(self, request, *args, **kwargs):
        tid = self.kwargs.get('tid')
        if tid:
            tournament_theme = TournamentTheme.objects.filter(id=tid)
            if tournament_theme.exists():
                tournament_theme = tournament_theme[0]
                tournament_list = tournament_theme.theme_tournaments.all()
                t_list = []
                for tournament in tournament_list:
                    team_info_list = TournamentTeamInfo.objects.filter(tournament=tournament).order_by('rank')
                    info = {'group': team_info_list, 'name': tournament.name}
                    t_list.append(info)
                return self.render_to_response({'group_list': t_list, 'tournament': tournament_theme})
            self.message = '联赛不存在'
            self.status_code = INFO_NO_EXIST
            return self.render_to_response(dict())
        self.message = '数据缺失'
        self.status_code = ERROR_DATA
        return self.render_to_response(dict())


