# -*- coding: utf-8 -*-
import json

from django.core.management.base import BaseCommand
from lol.models import Weibo


class Command(BaseCommand):
    def handle(self, *args, **options):
        weibo_list = Weibo.objects.all()
        for weibo in weibo_list:
            weibo.content = json.loads(weibo.content)
            weibo.save()
