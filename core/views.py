from django.http import HttpResponse
from django.shortcuts import render
from core.utils import check_sign


# Create your views here.


def check_signs(req):
    sign = req.GET.get('sign', '')
    timestamp = req.GET.get('timestamp', '')
    res = check_sign(timestamp, sign)
    return HttpResponse(res)
