# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from lol.models import Hero, SummonerSpells, Player, Team, Equipment, TournamentTheme, TotalTeamInfo, TotalPlayerInfo


class Command(BaseCommand):
    def handle(self, *args, **options):
        t_list = TotalPlayerInfo.objects.all()
        for itm in t_list:
            itm.uuid = u'{0}p{1}'.format(itm.tournament_id, itm.player_id)
            itm.save()
