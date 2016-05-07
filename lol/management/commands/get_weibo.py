# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from lol.weibo_spider import get_data


class Command(BaseCommand):
    def handle(self, *args, **options):
        get_data()
