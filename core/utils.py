# coding: utf-8
from __future__ import unicode_literals

import hashlib

import requests
import time

from PIL import Image

from Phorcys.settings import BASE_DIR
from core.models import Secret

import random
import string

UPLOAD_PATH = BASE_DIR + '/static'


def create_secret(count=64):
    return string.join(
        random.sample('''ZYXWVUTSRQPONMLKJIHGFEDCBA1234567890zyxwvutsrqponmlkjihgfedcbazyxwvutsrqponmlkjihgfedcba''',
                      count)).replace(" ", "")


def create_token(count=32):
    return string.join(
        random.sample('''ZYXWVUTSRQPONMLKJIHGFEDCBA1234567890zyxwvutsrqponmlkjihgfedcba''',
                      count)).replace(" ", "")


def check_sign(timestamp, sign):
    secret = Secret.objects.all()[0].secret
    check = unicode(hashlib.md5('{0}{1}'.format(timestamp, secret)).hexdigest()).upper()
    if check == unicode(sign).upper():
        return True
    return False


def save_image(url, type='lol/hero', name="default.jpg"):
    dir_path = '/image/{0}/{1}'.format(type, name)
    save_path = '{0}{1}'.format(UPLOAD_PATH, dir_path)
    response = requests.get(url, stream=True)
    image = response.content
    img = Image.open(image)
    img.save(save_path)
    return '/s{0}'.format(dir_path), save_path


def upload_picture(pic_file, folder='lol'):
    pic_name = "{0}{1}".format(unicode(int(time.time())), pic_file.name)
    pic_path = '/image/upload/{0}/{1}'.format(folder, pic_name)
    save_path = UPLOAD_PATH + pic_path
    try:
        img = Image.open(pic_file)
        img.save(save_path)
    except:
        return False, None
    return True, '/s{0}'.format(pic_path)


def create_game_id(type='01'):
    return '{0}{1}{2}'.format(unicode(time.time()).replace('.', ''), type, random.randint(1000, 9999))
