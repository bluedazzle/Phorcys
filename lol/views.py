# coding: utf-8

from __future__ import unicode_literals

from django.views.generic import ListView, DetailView, CreateView, UpdateView

from core.Mixin.CheckMixin import CheckSecurityMixin, CheckTokenMixin
from core.Mixin.StatusWrapMixin import *
from core.dss.Mixin import MultipleJsonResponseMixin, FormJsonResponseMixin, JsonResponseMixin

# Create your views here.
from lol.models import News, NewsComment, Topic, Player, Team, Tournament, Weibo
from lol.forms import *
from myuser.models import EUser


class NewsListView(CheckSecurityMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    """
    咨询列表
    """

    model = News
    datetime_type = 'timestamp'
    paginate_by = 10
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        self.message = 'success'
        self.status_code = INFO_SUCCESS
        return super(NewsListView, self).get(request, *args, **kwargs)


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


class PlayerListView(CheckSecurityMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    """
    选手列表
    """

    model = Player
    http_method_names = ['get']
    exclude_attr = ['modify_time', 'create_time', 'belong']
    foreign = True
    paginate_by = 20


class TeamListView(CheckSecurityMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    """
    战队列表
    """

    model = Team
    http_method_names = ['get']
    exclude_attr = ['modify_time', 'create_time']
    paginate_by = 20


class TournamentListView(CheckSecurityMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    """
    联赛列表
    """

    model = Tournament
    http_method_names = ['get']
    exclude_attr = ['modify_time', 'create_time']
    paginate_by = 20


class TournamentDetailView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    """
    联赛详情
    """

    model = Tournament
    http_method_names = ['get']
    exclude_attr = ['modify_time']
    pk_url_kwarg = 'id'


class CommentCreateView(CheckSecurityMixin, CheckTokenMixin, StatusWrapMixin, JsonResponseMixin, CreateView):
    """
    新评论
    """

    http_method_names = ['post']
    pk_url_kwarg = 'token'
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


