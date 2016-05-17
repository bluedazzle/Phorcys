# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from lol.models import Tmp, Player, Team


class Command(BaseCommand):
    def handle(self, *args, **options):
        tmps = Tmp.objects.all()
        for tmp in tmps:
            tmp.delete()

        Tmp(pic_type=1, player=Player.objects.get(nick__iexact='clearlove'), url='/s/tmp/1.png').save()
        Tmp(pic_type=1, player=Player.objects.get(nick__iexact='easyhoon'), url='/s/tmp/2.png').save()
        Tmp(pic_type=2, team=Team.objects.get(abbreviation__iexact='edg'), url='/s/tmp/3.png').save()
        Tmp(pic_type=2, team=Team.objects.get(abbreviation__iexact='ig'), url='/s/tmp/4.png').save()
        Tmp(pic_type=1, player=Player.objects.get(nick__iexact='imp'), url='/s/tmp/5.png').save()
        Tmp(pic_type=2, team=Team.objects.get(abbreviation__iexact='lgd'), url='/s/tmp/6.png').save()
        Tmp(pic_type=1, player=Player.objects.get(nick__iexact='mlxg'), url='/s/tmp/7.png').save()
        Tmp(pic_type=2, team=Team.objects.get(abbreviation__iexact='qg'), url='/s/tmp/8.png').save()
        Tmp(pic_type=2, team=Team.objects.get(abbreviation__iexact='omg'), url='/s/tmp/9.png').save()
        Tmp(pic_type=2, team=Team.objects.get(abbreviation__iexact='rng'), url='/s/tmp/10.png').save()
        Tmp(pic_type=1, player=Player.objects.get(nick__iexact='rookie'), url='/s/tmp/11.png').save()
        Tmp(pic_type=2, team=Team.objects.get(abbreviation__iexact='ss'), url='/s/tmp/12.png').save()
        Tmp(pic_type=1, player=Player.objects.get(nick__iexact='uzi'), url='/s/tmp/13.png').save()
        Tmp(pic_type=2, team=Team.objects.get(abbreviation__iexact='vg'), url='/s/tmp/14.png').save()
        Tmp(pic_type=2, team=Team.objects.get(abbreviation__iexact='we'), url='/s/tmp/15.png').save()
