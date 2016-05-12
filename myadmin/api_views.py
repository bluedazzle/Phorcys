# coding: utf-8
from __future__ import unicode_literals

import random
import string

import datetime

from django.db.models import Count, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response

# Create your views here.
from django.utils.timezone import get_current_timezone
from django.views.generic import UpdateView, DetailView, TemplateView, ListView, RedirectView, View, CreateView, \
    DeleteView
from django.views.generic.base import TemplateResponseMixin

from core.models import Country
from core.utils import upload_picture, create_game_id, create_tournament_id, create_token
from lol.models import News, Tournament, Team, Player, Topic, TournamentTeamInfo, Match, Game, Hero, GamePlayer, \
    SummonerSpells, Equipment, Position, TournamentTheme, PlayerInfo, TotalTeamInfo, TotalPlayerInfo
from myadmin.forms import AdminLoginForm
from myadmin.models import EAdmin
from myadmin.utils import calculate_game_data
from myuser.models import EUser, Invite
from core.Mixin.CheckMixin import CheckSecurityMixin, CheckAdminPermissionMixin
from core.Mixin.StatusWrapMixin import *
from core.Mixin.JsonRequestMixin import JsonRequestMixin
from core.dss.Mixin import *


class AdminLoginView(CheckSecurityMixin, AdminStatusWrapMixin, JsonRequestMixin, JsonResponseMixin, UpdateView):
    model = EAdmin
    pk_url_kwarg = 'username'
    form_class = AdminLoginForm
    http_method_names = ['post', 'options']
    include_attr = ['token', 'nick', 'phone']
    success_url = 'localhost'
    token = ''
    count = 64

    def create_token(self):
        return string.join(
            random.sample('ZYXWVUTSRQPONMLKJIHGFEDCBA1234567890zyxwvutsrqponmlkjihgfedcbazyxwvutsrqponmlkjihgfedcba',
                          self.count)).replace(" ", "")

    def form_invalid(self, form):
        if not self.object:
            return self.render_to_response(dict())
        super(AdminLoginView, self).form_invalid(form)
        self.status_code = ERROR_DATA
        self.message = json.loads(form.errors.as_json())
        return self.render_to_response(dict())

    def form_valid(self, form):
        if not self.object:
            return self.render_to_response(dict())
        super(AdminLoginView, self).form_valid(form)
        if not self.object.check_password(form.cleaned_data.get('password')):
            self.message = [('password', '密码不正确')]
            self.status_code = ERROR_PASSWORD
            return self.render_to_response(dict())
        self.token = self.create_token()
        self.object.token = self.token
        self.object.save()
        self.request.session['token'] = self.token
        return self.render_to_response(self.object)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.request.POST.get(self.pk_url_kwarg, None)
        queryset = queryset.filter(phone=pk)
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            self.message = [('username', '帐号不存在')]
            self.status_code = INFO_NO_EXIST
            return None
        return obj


class AdminLogoutView(CheckSecurityMixin, CheckAdminPermissionMixin, StatusWrapMixin, JsonResponseMixin,
                      TemplateResponseMixin, View):
    http_method_names = ['get']
    template_name = 'admin/admin_login.html'

    def get(self, request, *args, **kwargs):
        if not self.wrap_check_sign_result():
            return self.render_to_response(dict())
        request.session['token'] = ''
        return self.render_to_response(dict())


class AdminIndexView(CheckSecurityMixin, CheckAdminPermissionMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    pk_url_kwarg = ''
    http_method_names = ['get']

    def get_queryset(self):
        message_dict = {}
        message_dict['users'] = EUser.objects.all().count()
        message_dict['news'] = News.objects.all().count()
        message_dict['topics'] = TournamentTheme.objects.all().count()
        return message_dict

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_queryset())


class AdminUserView(CheckSecurityMixin, CheckAdminPermissionMixin, StatusWrapMixin, JsonRequestMixin, JsonResponseMixin,
                    DetailView):
    pk_url_kwarg = 'token'
    http_method_names = ['get', 'post']
    include_attr = ['nick', 'last_login', 'phone']

    def get(self, request, *args, **kwargs):
        if not self.wrap_check_token_result():
            return self.render_to_response(dict())
        return self.render_to_response(self.admin)

    def post(self, request, *args, **kwargs):
        if not self.wrap_check_token_result():
            return self.render_to_response(dict())
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        if old_password and new_password:
            if self.admin.check_password(old_password):
                self.admin.set_password(new_password)
                self.admin.save()
                return self.render_to_response(dict())
            else:
                self.message = '原密码不正确'
                self.status_code = ERROR_PASSWORD
                return self.render_to_response(dict())
        self.message = '参数缺失'
        self.status_code = ERROR_DATA
        return self.render_to_response(dict())


class AdminTournamentListView(CheckSecurityMixin, CheckAdminPermissionMixin,
                              StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    model = Tournament
    http_method_names = ['get']
    foreign = True
    context_object_name = 'tournaments'
    include_attr = ['name', 'start_time', 'end_time', 'cover', 'match_numbers', 'team_numbers', 'id', 'percent',
                    'belong']

    def get_queryset(self):
        today = datetime.date.today()
        activity_tournaments = Tournament.objects.filter(end_time__gte=today)
        # .annotate(team_numbers=Count('team_tournaments')).annotate(match_numbers=Count('tournament_matches'))
        finished_tournaments = Tournament.objects.filter(end_time__lt=today)
        # .annotate(team_numbers=Count('team_tournaments')).annotate(match_numbers=Count('tournament_matches'))
        map(self.get_percent, activity_tournaments)
        map(self.get_extra_number, activity_tournaments)
        map(self.get_extra_number, finished_tournaments)
        tournaments = {'activity_tournaments': activity_tournaments,
                       'finished_tournaments': finished_tournaments}
        return tournaments

    def get_percent(self, tournament):
        today = datetime.date.today()
        start_day = tournament.start_time
        end_day = tournament.end_time
        total = end_day - start_day
        current = end_day - today
        use = total - current
        if use.days > 0:
            percent = round(float(use.days) / total.days * 100)
        else:
            percent = 0
        setattr(tournament, 'percent', percent)

    def get_extra_number(self, tournament):
        tn = tournament.team_tournaments.all().count()
        setattr(tournament, 'team_numbers', tn)
        mn = tournament.tournament_matches.all().count()
        setattr(tournament, 'match_numbers', mn)


class AdminTournamentThemeView(CheckSecurityMixin, CheckAdminPermissionMixin,
                               StatusWrapMixin, MultipleJsonResponseMixin, JsonRequestMixin, ListView):
    model = TournamentTheme
    http_method_names = ['post', 'get']

    def post(self, request, *args, **kwargs):
        img = request.FILES.get('img')
        if img:
            re_path, save_path = upload_picture(img)
            name = request.POST.get('name')
            start_time = datetime.datetime.strptime(unicode(request.POST.get('start_time')), "%Y-%m-%d")
            end_time = datetime.datetime.strptime(unicode(request.POST.get('end_time')), "%Y-%m-%d")
            # teams = request.POST.get('teams').split(',')
            TournamentTheme(
                name=name,
                start_time=start_time,
                end_time=end_time,
                cover=re_path
            ).save()
            # tournament = TournamentTheme.objects.get(name=name)
            # for tid in teams:
            #     team = Team.objects.filter(id=tid)
            #     if team.exists():
            #         team = team[0]
            #         TournamentTeamInfo(team=team,
            #                            tournament=tournament).save()
            #         team.tournaments.add(tournament)
            return self.render_to_response(dict())


class AdminTournamentView(CheckSecurityMixin, CheckAdminPermissionMixin,
                          StatusWrapMixin, JsonResponseMixin, JsonRequestMixin, DetailView):
    model = Tournament
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        ttid = request.POST.get('ttid')
        tt = TournamentTheme.objects.get(id=ttid)
        name = '{0}-{1}'.format(tt.name, request.POST.get('name'))
        teams = request.POST.get('teams')
        uuid = create_tournament_id()
        Tournament(name=name,
                   uuid=uuid,
                   start_time=tt.start_time,
                   end_time=tt.end_time,
                   cover=tt.cover,
                   belong=tt).save()
        tournament = Tournament.objects.get(name=name)

        for tid in teams:
            team = Team.objects.filter(id=tid)
            if team.exists():
                team = team[0]
                TournamentTeamInfo(team=team,
                                   uuid='{0}t{1}'.format(uuid, team.id),
                                   tournament=tournament).save()
                uuid = '{0}t{1}'.format(tt.id, team.id)
                if not TotalTeamInfo.objects.filter(uuid=uuid).exists():
                    TotalTeamInfo(team=team,
                                  uuid=uuid,
                                  tournament=tt
                                  ).save()
                team.tournaments.add(tournament)
            players = team.team_players.all()
            for player in players:
                PlayerInfo(uuid='{0}p{1}'.format(uuid, player.id),
                           player=player,
                           tournament=tournament
                           ).save()
                uuid = '{0}p{1}'.format(tt.id, player.id)
                if not TotalPlayerInfo.objects.filter(uuid=uuid):
                    TotalPlayerInfo(uuid=uuid,
                                    player=player,
                                    tournament=tt).save()
        return self.render_to_response(dict())


class AdminMatchView(CheckSecurityMixin, CheckAdminPermissionMixin,
                     StatusWrapMixin, JsonResponseMixin, JsonRequestMixin, DetailView):
    model = Match
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        tid = unicode(kwargs.get('tid'))
        if tid:
            tournament = Tournament.objects.filter(id=tid)
            if tournament.exists():
                tournament = tournament[0]
                name = request.POST.get('name', '')
                match_time = datetime.datetime.strptime(unicode(request.POST.get('start_time')), '%Y-%m-%d %H:%M:%S')
                match_type = int(request.POST.get('match_type'))
                tid1 = request.POST.get('teams')[0]
                tid2 = request.POST.get('teams')[1]
                team1 = Team.objects.filter(id=tid1)[0]
                team2 = Team.objects.filter(id=tid2)[0]
                Match(name=name,
                      match_type=match_type,
                      team1=team1,
                      team2=team2,
                      tournament=tournament,
                      match_time=match_time).save()
                return self.render_to_response(dict())
        self.message = 'error'
        self.status_code = ERROR_DATA
        return self.render_to_response(dict())


class AdminGameDeleteView(CheckSecurityMixin, CheckAdminPermissionMixin,
                          StatusWrapMixin, JsonResponseMixin, DeleteView):
    model = Game
    http_method_names = ['delete']
    pk_url_kwarg = 'gid'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return self.render_to_response(dict())


class AdminGamePlayerDeleteView(CheckSecurityMixin, CheckAdminPermissionMixin,
                                StatusWrapMixin, JsonResponseMixin, DeleteView):
    model = GamePlayer
    http_method_names = ['delete']
    pk_url_kwarg = 'gpid'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return self.render_to_response(dict())


class AdminMatchModifyView(CheckSecurityMixin, CheckAdminPermissionMixin,
                           StatusWrapMixin, JsonRequestMixin, JsonResponseMixin, DeleteView):
    model = Match
    http_method_names = ['delete', 'post']
    pk_url_kwarg = 'mid'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return self.render_to_response(dict())

    def post(self, request, *args, **kwargs):
        status = request.POST.get('status')
        mid = kwargs.get('mid')
        if status and mid:
            matches = Match.objects.filter(id=mid)
            if matches.exists():
                match = matches[0]
                match.status = int(status)
                match.save()
                return self.render_to_response(dict())
            else:
                self.message = '比赛不存在'
                self.status_code = INFO_NO_EXIST
                return self.render_to_response(dict())
        self.message = '参数缺失'
        self.message = ERROR_DATA
        return self.render_to_response(dict())


class AdminGameView(CheckSecurityMixin, CheckAdminPermissionMixin,
                    StatusWrapMixin, JsonRequestMixin, JsonResponseMixin, DetailView):
    model = Game
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        mid = unicode(kwargs.get('mid'))
        if mid:
            match = Match.objects.filter(id=mid)
            if match.exists():
                match = match[0]
                game_time = datetime.datetime.strptime(unicode(request.POST.get('game_time')), '%Y-%m-%d %H:%M:%S')
                duration = int(request.POST.get('duration'))
                tid1 = request.POST.get('team1')
                tid2 = request.POST.get('team2')
                team1 = Team.objects.get(id=tid1)
                team2 = Team.objects.get(id=tid2)
                win = request.POST.get('win')
                if win:
                    win = Team.objects.get(id=win)
                else:
                    win = Team.objects.get(id=tid1)
                team1_tower = int(request.POST.get('team1_tower', 0))
                team2_tower = int(request.POST.get('team2_tower', 0))
                team1_dragon = int(request.POST.get('team1_dragon', 0))
                team2_dragon = int(request.POST.get('team2_dragon', 0))
                team1_nashor = int(request.POST.get('team1_nahsor', 0))
                team2_nashor = int(request.POST.get('team2_nahsor', 0))
                video = request.POST.get('video', '')
                game_id = request.POST.get('game_id')
                over = request.POST.get('over')
                if game_id:
                    game = Game.objects.filter(game_id=game_id)
                    if game.exists():
                        game = game[0]
                        game.match = match
                        game.game_time = game_time
                        game.win = win
                        game.duration = duration
                        game.over = over
                        game.team1_dragon = team1_dragon
                        game.team2_dragon = team2_dragon
                        game.team1_tower = team1_tower
                        game.team2_tower = team2_tower
                        game.team1_nahsor = team1_nashor
                        game.team2_nahsor = team2_nashor
                        game.video = video
                        game.save()
                else:
                    game_id = create_game_id()
                    new_game = Game(match=match,
                                    game_id=game_id,
                                    game_time=game_time,
                                    win=win,
                                    duration=duration,
                                    team1=team1,
                                    team2=team2,
                                    team1_nahsor=team1_nashor,
                                    team2_nahsor=team2_nashor,
                                    team1_tower=team1_tower,
                                    team2_tower=team2_tower,
                                    team1_dragon=team1_dragon,
                                    team2_dragon=team2_dragon,
                                    over=over,
                                    video=video
                                    )
                    new_game.save()
                game = Game.objects.get(game_id=game_id)
                team1_ban_list = request.POST.get('team1_ban', [])
                team2_ban_list = request.POST.get('team2_ban', [])
                if "" in team1_ban_list:
                    team1_ban_list = None
                if "" in team2_ban_list:
                    team2_ban_list = None
                if team1_ban_list:
                    game.team1_ban.clear()
                    for hid in team1_ban_list:
                        hero = Hero.objects.get(id=hid)
                        game.team1_ban.add(hero)
                if team2_ban_list:
                    game.team2_ban.clear()
                    for hid in team2_ban_list:
                        hero = Hero.objects.get(id=hid)
                        game.team2_ban.add(hero)
                game.save()

                games = match.match_games.all()
                match.team2_score = 0
                match.team1_score = 0
                for ga in games:
                    if ga.over:
                        if ga.win_id == ga.team1_id:
                            match.team1_score += 1
                        else:
                            match.team2_score += 1
                match.save()
                return self.render_to_response(dict())
        self.message = 'error'
        self.secret = ERROR_DATA
        return self.render_to_response(dict())


class AdminGameDetailView(CheckSecurityMixin, CheckAdminPermissionMixin,
                          StatusWrapMixin, JsonRequestMixin, JsonResponseMixin, DetailView):
    model = GamePlayer
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        gid = request.POST.get('game_id')
        tid = request.POST.get('team_id')
        pid = request.POST.get('player_id')
        hid = request.POST.get('hero_id')
        if gid and tid and pid and hid:
            game = Game.objects.get(game_id=gid)
            team = Team.objects.get(id=tid)
            player = Player.objects.get(id=pid)
            hero = Hero.objects.get(id=hid)
            code = request.POST.get('position')
            summoner1 = SummonerSpells.objects.get(id=request.POST.get('summoner1'))
            summoner2 = SummonerSpells.objects.get(id=request.POST.get('summoner2'))
            guard = Equipment.objects.get(id=request.POST.get('guard'))
            level = request.POST.get('level', 0)
            kill = request.POST.get('kill', 0)
            dead = request.POST.get('dead', 0)
            assist = request.POST.get('assist', 0)
            war_rate = request.POST.get('war_rate', 0)
            damage_rate = request.POST.get('damage_rate', 0)
            farming = request.POST.get('farming', 0)
            economic = request.POST.get('economic', 0)
            game_player_id = request.POST.get('game_player_id', '')
            gid = '{0}{1}'.format(gid, len(game.game_gameps.all()) + 1)
            if GamePlayer.objects.filter(gid=game_player_id).exists():
                game_player = GamePlayer.objects.get(gid=game_player_id)
            else:
                game_player = GamePlayer()
                game_player.gid = gid
            game_player.game = game
            game_player.team = team
            game_player.player = player
            game_player.hero = hero
            game_player.position = Position.objects.get(code=code)
            game_player.summoner1 = summoner1
            game_player.summoner2 = summoner2
            game_player.guard = guard
            game_player.level = level
            game_player.kill = kill
            game_player.dead = dead
            game_player.assist = assist
            game_player.war_rate = war_rate
            game_player.damage_rate = damage_rate
            game_player.farming = farming
            game_player.economic = economic
            kill = float(kill)
            dead = float(dead)
            assist = float(assist)
            if int(dead) == 0:
                dead = 1.0
                game_player.kda = (kill + assist) / dead
            else:
                game_player.kda = (kill + assist) / dead
            game_player.save()
            equips = request.POST.get('equipments')
            calculate_game_data(game)
            if len(equips) > 0 and "" not in equips:
                game_player.equipments.clear()
                for equip in equips:
                    equipment = Equipment.objects.get(id=equip)
                    game_player.equipments.add(equipment)
            game_player.save()
            return self.render_to_response(dict())
        self.message = 'ERROR'
        self.status_code = ERROR_DATA
        return self.render_to_response(dict())


class AdminUserListView(CheckSecurityMixin, CheckAdminPermissionMixin,
                        StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    http_method_names = ['get']
    paginate_by = 50
    ordering = '-create_time'
    exclude_attr = ['token', 'password']
    model = EUser

    def get_queryset(self):
        queryset = super(AdminUserListView, self).get_queryset()
        queryset = queryset.annotate(comment_number=Count('user_news_comments'))
        query_str = self.request.GET.get('query')
        if query_str:
            queryset = queryset.filter(Q(nick__icontains=query_str) | Q(phone__icontains=query_str))
        return queryset


class AdminUserForbidView(CheckSecurityMixin, CheckAdminPermissionMixin,
                          StatusWrapMixin, JsonResponseMixin, DetailView):
    http_method_names = ['post']
    model = EUser
    pk_url_kwarg = 'uid'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.forbid = not self.object.forbid
        self.object.save()
        return self.render_to_response(dict())


class AdminUserDetailView(CheckSecurityMixin, CheckAdminPermissionMixin,
                          StatusWrapMixin, JsonResponseMixin, DeleteView):
    http_method_names = ['get', 'delete']
    model = EUser
    pk_url_kwarg = 'uid'
    foreign = True

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return self.render_to_response(dict())


class AdminPlayerView(CheckSecurityMixin, CheckAdminPermissionMixin,
                      StatusWrapMixin, JsonResponseMixin, DetailView):
    http_method_names = ['post']
    model = Player

    def post(self, request, *args, **kwargs):
        pid = request.POST.get('id')
        img = request.FILES.get('img')
        if img:
            re_path, save_path = upload_picture(img)
        else:
            re_path = ''
        nick = request.POST.get('nick')
        name = request.POST.get('name')
        position = request.POST.get('position')
        intro = request.POST.get('intro')
        nationality = request.POST.get('country')
        if nationality == 0 or nationality == 'null':
            nationality = Country.objects.get(name='未知')
        else:
            nationality = Country.objects.get(id=nationality)
        belong = request.POST.get('belong')
        belong = Team.objects.get(id=belong)
        position = Position.objects.get(id=position)
        player = Player.objects.filter(id=pid)
        if player.exists():
            player = player[0]
            player.name = name
            player.nick = nick
            player.position = position
            player.nationality = nationality
            player.intro = intro
            player.belong = belong
            if re_path != '':
                player.avatar = re_path
            player.save()
        else:
            Player(name=name,
                   nick=nick,
                   position=position,
                   nationality=nationality,
                   intro=intro,
                   avatar=re_path,
                   belong=belong).save()
        return self.render_to_response(dict())


class AdminPlayerDetailView(CheckSecurityMixin, CheckAdminPermissionMixin,
                            StatusWrapMixin, JsonResponseMixin, DeleteView):
    model = Player
    pk_url_kwarg = 'pid'
    http_method_names = ['get', 'delete']
    foreign = True

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return self.render_to_response(dict())


class AdminTeamDetailView(CheckSecurityMixin, CheckAdminPermissionMixin,
                          StatusWrapMixin, JsonResponseMixin, DeleteView):
    model = Team
    pk_url_kwarg = 'tid'
    http_method_names = ['get', 'delete']
    foreign = True

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return self.render_to_response(dict())


class AdminTeamView(CheckSecurityMixin, CheckAdminPermissionMixin,
                    StatusWrapMixin, JsonRequestMixin, JsonResponseMixin, DetailView):
    model = Team
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        logo = request.FILES.get('img')
        info = request.POST.get('info')
        abbreviation = request.POST.get('abbreviation')
        country = request.POST.get('country')
        world_rank = int(request.POST.get('world_rank', 0))
        country = Country.objects.get(id=country)
        tid = request.POST.get('id')
        if logo:
            data_path, save_path = upload_picture(logo)
        else:
            data_path = ''
        team = Team.objects.filter(id=tid)
        if team.exists():
            team = team[0]
            team.name = name
            team.info = info
            team.world_rank = world_rank
            team.abbreviation = abbreviation
            team.country = country
            if data_path != '':
                team.logo = data_path
            team.save()
        else:
            Team(name=name,
                 logo=data_path,
                 info=info,
                 world_rank=world_rank,
                 abbreviation=abbreviation,
                 country=country
                 ).save()
        return self.render_to_response(dict())


class AdminNewsView(CheckSecurityMixin, CheckAdminPermissionMixin,
                    StatusWrapMixin, JsonResponseMixin, DeleteView):
    model = News
    http_method_names = ['get', 'delete']
    pk_url_kwarg = 'nid'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.publish = not self.object.publish
        self.object.save()
        return self.render_to_response(dict())

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return self.render_to_response(dict())


class AdminInviteListView(CheckSecurityMixin, CheckAdminPermissionMixin,
                          StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    model = Invite
    http_method_names = ['get']
    paginate_by = 50

    def get_queryset(self):
        query = self.request.GET.get('query')
        queryset = super(AdminInviteListView, self).get_queryset()
        if query:
            queryset = queryset.filter(Q(code=query) | Q(belong__phone=query))
        return queryset


class AdminInviteView(CheckSecurityMixin, CheckAdminPermissionMixin,
                      StatusWrapMixin, JsonRequestMixin, JsonResponseMixin, DetailView):
    model = Invite
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        used = Invite.objects.filter(use=True).count()
        unuse = Invite.objects.filter(use=False).count()
        total = Invite.objects.all().count()
        context = {'used': used,
                   'unuse': unuse,
                   'total': total}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        numbers = int(request.POST.get('number'))
        if numbers:
            for i in range(1, (numbers + 1)):
                code = create_token(count=6)
                Invite(code=code).save()
            return self.render_to_response(dict())
        self.message = '参数缺失'
        self.status_code = ERROR_DATA
        return self.render_to_response(dict())
