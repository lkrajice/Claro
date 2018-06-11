# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from claro.utils import get_context_manager

from .models import Class, Student, Election, Round, Vote


with_metadata = get_context_manager()


def get_sidebar_class_context():
    classes = {}
    for cls in Class.objects.all():
        if cls.classtype not in classes:
            classes[cls.classtype] = {}

        grade = cls.shortname[1]
        if grade not in classes[cls.classtype]:
            classes[cls.classtype][grade] = []
        classes[cls.classtype][grade].append(cls.shortname)

    return {'classes': classes}


### VIEWS #########################################################################################

def overview(request):
    """
    Shown nomination or election overview based on which procces is active

    PROCCESS:
        Get latest election
        IF no election exists
            notify the user

        Get currently active round of election
        IF no active round
            get latest row and present it's results
        ELIF active round exists
            run nomination_overview or election_overview depending on round type
    """
    try:
        election = Election.objects.latest('id')
        rounds = Round.objects.all().filter(election_id=election)
        active = [r for r in rounds if r.compare == 0]
        if len(active) != 0:
            if active[0].type_id.name == 'nomination':
                nomination_overview(request, election, active[0])
            else:
                election_overview(request, election, active[0])
    except Election.DoesNotExist:
        pass
    template = loader.get_template('no_active_row.html')
    return HttpResponse(template.render(with_metadata({}), request))


def nomination_overview(request, election, active_round):
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
        'key': 'value'
    }
    return HttpResponse(template.render(with_metadata(context), request))


def election_overview(request, election, active_round):
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
    return HttpResponse(template.render(with_metadata(context), request))


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
    template = loader.get_template('class_overview.html')
    return HttpResponse(template.render(with_metadata(get_sidebar_class_context()), request))
