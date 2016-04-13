# coding: utf-8
from __future__ import unicode_literals

from django.db import models


# Create your models here.

class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Country(BaseModel):
    name = models.CharField(max_length=30)
    flag = models.ImageField()

    def __unicode__(self):
        return self.name


class BaseNews(BaseModel):
    title = models.CharField(max_length=100)
    content = models.TextField()

    class Meta:
        abstract = True


class BaseTournament(BaseModel):
    name = models.CharField(max_length=100)
    start_time = models.DateField()
    end_time = models.DateField()
    thumb = models.IntegerField(default=0)

    class Meta:
        abstract = True


class BaseComment(BaseModel):
    content = models.TextField()
    thumb = models.IntegerField(default=0)

    class Meta:
        abstract = True


class BasePlayer(BaseModel):
    name = models.CharField(max_length=50)
    nick = models.CharField(max_length=50)
    avatar = models.ImageField()
    nationality = models.ForeignKey(Country, related_name='country_players', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        abstract = True


class BaseTopic(BaseModel):
    title = models.CharField(max_length=100)
    content = models.TextField()
    thumb = models.IntegerField(default=0)

    class Meta:
        abstract = True


class BaseWeibo(BaseModel):
    title = models.CharField(max_length=100)
    content = models.TextField()
    thumb = models.IntegerField(default=0)

    class Meta:
        abstract = True


class BaseTeam(BaseModel):
    short_name = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    logo = models.ImageField()
    info = models.TextField()
    country = models.ForeignKey(Country, related_name='country_teams', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        abstract = True


class Secret(BaseModel):
    secret = models.CharField(max_length=64)
    info = models.CharField(max_length=20, default='system')

    def __unicode__(self):
        return self.info