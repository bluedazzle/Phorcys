# coding: utf-8
from __future__ import unicode_literals
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response

# Create your views here.
from django.views.generic import UpdateView, DetailView, TemplateView, ListView

from lol.models import News, Tournament, Team, Player, Topic
from myadmin.forms import AdminLoginForm
from myadmin.models import EAdmin


class AdminView(UpdateView):
    model = EAdmin
    form_class = AdminLoginForm
    http_method_names = ['get', 'post']
    success_url = '/admin/index'
    res_dict = {'username': True,
                'password': True,
                'username_value': '',
                'password_value': '',
                'username_info': '',
                'password_info': ''}

    def get(self, request, *args, **kwargs):
        self.res_dict['username'] = True
        self.res_dict['password'] = True
        self.res_dict['username_info'] = ''
        self.res_dict['password_info'] = ''
        self.res_dict['password_value'] = ''
        self.res_dict['username_info'] = ''
        return render_to_response('admin/admin_login.html', self.res_dict)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = unicode(request.POST.get('password'))
        if password:
            if not username:
                self.res_dict['username_info'] = '请输入帐号'
                self.res_dict['username'] = False
                return render_to_response('admin/admin_login.html', self.res_dict)
            users = EAdmin.objects.filter(phone=username)
            if users.exists():
                user = users[0]
                if user.check_password(password):
                    return HttpResponseRedirect(self.success_url)
                self.res_dict['password_info'] = '密码不正确'
                self.res_dict['password'] = False
            else:
                self.res_dict['username_info'] = '用户不存在'
                self.res_dict['username'] = False
        else:
            self.res_dict['password_info'] = '请输入密码'
            self.res_dict['password'] = False
        self.res_dict['username_value'] = username
        self.res_dict['password_value'] = password
        return render_to_response('admin/admin_login.html', self.res_dict)


class AdminIndexView(TemplateView):
    model = EAdmin
    http_method_names = ['get']
    template_name = 'admin/admin_index.html'


class AdminNewsListView(ListView):
    model = News
    template_name = 'admin/admin_news.html'
    paginate_by = 20


class AdminTournamentListView(ListView):
    model = Tournament
    template_name = 'admin/admin_tournaments.html'
    paginate_by = 20


class AdminTeamListView(ListView):
    model = Team
    template_name = 'admin/admin_teams.html'
    paginate_by = 20


class AdminPlayerListView(ListView):
    model = Player
    template_name = 'admin/admin_players.html'
    paginate_by = 20


class AdminTopicListView(ListView):
    model = Topic
    template_name = 'admin/admin_topics.html'
    paginate_by = 20




