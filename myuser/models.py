# coding: utf-8

from __future__ import unicode_literals

from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from core.models import BaseModel


# Create your models here.

class EUser(BaseModel, AbstractBaseUser):
    from lol.models import LOLInfoExtend
    phone = models.CharField(max_length=13, unique=True)
    nick = models.CharField(max_length=100, unique=True)
    avatar = models.URLField(null=True, blank=True)
    token = models.CharField(max_length=64)

    lol = models.OneToOneField('lol.LOLInfoExtend', related_name='lol_info_user', null=True, blank=True)

    USERNAME_FIELD = 'phone'

    def __unicode__(self):
        return '{0}-{1}'.format(self.phone, self.nick)


class Verify(BaseModel):
    code = models.CharField(max_length=10)
    phone = models.CharField(max_length=13)

    def __unicode__(self):
        return self.phone
