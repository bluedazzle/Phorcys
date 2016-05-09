# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from lol.models import Tournament
from lol.signal_work import generate_player_tournament_theme_info, generate_total_team_info


class Command(BaseCommand):
    def handle(self, *args, **options):
        t_id = args[0]
        generate_player_tournament_theme_info(t_id)
        generate_total_team_info(t_id)
