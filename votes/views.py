# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from django.template import loader


DEFAULT_CONTEXT = {'active_app': 'votes'}


def overview(request):
    """
    Shown nomination or election overview based on which procces is active
    """
    return nomination_overview(request)


### VIEWS #########################################################################################

def nomination_overview(request):
    """
    Shows nominated students for every class

    SHOWS:
        3 nominated students per each class with highest points
            student's name
            number of points

    ACTIONS:
        Go to class overview

    PROCCESS:
        Load students per each class with highest points
        Filter out students with 0 points

    """
    template = loader.get_template('nomination_overview.html')
    context = {
        'classes': {
            'V*': {
                '2': ['V2A', 'V2B', 'V2C', 'V2D'],
                '3': ['V3A', 'V3B', 'V3C', 'V3D'],
                '4': ['V4A', 'V4B', 'V4C', 'V4D'],
            },
            'S*': {
                '2': ['S2A', 'S2B', 'S2C'],
                '3': ['S3A', 'S3B', 'S3C'],
                '4': ['S4A', 'S4B', 'S4C'],
            },
        },
    }
    context.update(DEFAULT_CONTEXT)
    return HttpResponse(template.render(context, request))


def class_overview(request):
    """
    Shows people in given class

    SHOWS:
        All candidated
            name
            picture
            number of points

    ACTIONS:
        Trigger dialog which shown detailed info about a student
        Vote for an candidate which is showed in triggered dialog

    PROCCESS:
        Extract from request which class should be shown
        Load all students from given class willing to candidate

    """
    template = loader.get_template('class_everview.html')
    context = {
        'key': 'value'
    }
    return HttpResponse(template.render(context, request))


def election_overview(request):
    """
    Shows candidates and progress of election

    SHOWS:
        All candidated
            name
            picture
            number of points

    ACTIONS:
        Trigger dialog which shown detailed info about a candidate
        Vote for an candidate which is showed in triggered dialog

    PROCCESS:
        Load all candidate

    """
    template = loader.get_template('election_everview.html')
    context = {
        'key': 'value'
    }
    return HttpResponse(template.render(context, request))
