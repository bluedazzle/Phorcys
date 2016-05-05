# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from lol.models import GamePlayer
from lol.spider import get_summoner, get_hero, get_equipment, get_area, get_position, get_teams, get_players


class Command(BaseCommand):
    def handle(self, *args, **options):
        game_player_list = GamePlayer.objects.all()
        for itm in game_player_list:
            dead = itm.dead
            if dead == 0:
                dead = 1.0
                itm.kda = (itm.kill + itm.assist) / dead
            else:
                kill = float(itm.kill)
                itm.kda = (kill + itm.assist) / dead
            itm.save()
