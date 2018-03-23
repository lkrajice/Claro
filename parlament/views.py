# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from django.template import loader

# Create your views here.

def index(request):
    co_je_anime = "bullshit"
    template = loader.get_template('index.html')
    context = {
        "co_je_anime" : co_je_anime    
     }
    return HttpResponse(template.render(context, request))
