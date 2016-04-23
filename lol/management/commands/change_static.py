# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from lol.models import Hero, SummonerSpells, Player, Team, Equipment


class Command(BaseCommand):
    def handle(self, *args, **options):
        for itm in Player.objects.all():
            itm.avatar = unicode(itm.avatar).replace('static', 's')
            itm.save()
        for itm in Hero.objects.all():
            itm.picture = unicode(itm.picture).replace('static', 's')
            itm.save()
        for itm in SummonerSpells.objects.all():
            itm.picture = unicode(itm.picture).replace('static', 's')
            itm.save()
        for itm in Team.objects.all():
            itm.logo = unicode(itm.logo).replace('static', 's')
            itm.save()
        for itm in Equipment.objects.all():
            itm.picture = unicode(itm.picture).replace('static', 's')
            itm.save()
