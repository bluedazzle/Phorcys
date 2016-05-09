# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from lol.models import Weibo, Team


class Command(BaseCommand):
    def handle(self, *args, **options):
        weibo_list = Weibo.objects.all()
        for weibo in weibo_list:
            if weibo.type != 2:
                continue
            content = eval(weibo.content)
            uid = content.get('user').get('idstr')
            team = Team.objects.filter(wid=uid)
            if team.exists():
                weibo.team_author = team
                weibo.save()
            else:
                weibo.delete()

