# coding: utf-8

from __future__ import unicode_literals

from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from core.models import BaseModel

# Create your models here.

class EUser(BaseModel, AbstractBaseUser):
    phone = models.CharField(max_length=13, unique=True)
    nick = models.CharField(max_length=100, unique=True)
    avatar = models.URLField()
    token = models.CharField(max_length=64)

    USERNAME_FIELD = 'phone'

    def __unicode__(self):
        return '{0}-{1}'.format(self.phone, self.nick)
