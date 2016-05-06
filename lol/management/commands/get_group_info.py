# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from lol.models import Tournament
from lol.signal_work import get_player_info
from lol.spider import get_summoner, get_hero, get_equipment, get_area, get_position, get_teams, get_players


class Command(BaseCommand):
    def handle(self, *args, **options):
        name = args[0]
        t = Tournament.objects.filter(uuid=name)
        if t.exists():
            t = t[0]
            get_player_info(t.id)
        else:
            print u'联赛数据未找到'