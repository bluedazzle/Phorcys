# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from lol.spider import get_summoner, get_hero, get_equipment, get_area, get_position, get_teams, get_players


class Command(BaseCommand):
    def handle(self, *args, **options):
        # get_hero()
        # get_equipment()
        get_summoner()
        # get_area()
        # get_position()
        # get_teams()
        # get_players()
