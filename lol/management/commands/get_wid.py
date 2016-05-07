# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from lol.weibo import get_team_wid, get_player_wid


class Command(BaseCommand):
    def handle(self, *args, **options):
        get_team_wid()
        get_player_wid()
