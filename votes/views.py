# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import collections

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from claro.utils import get_context_manager

from .models import Class, Student, Election, Round, Vote, Pin


with_metadata = get_context_manager()


def get_sidebar_class_context():
    classes = collections.OrderedDict()
    for cls in Class.objects.all().order_by('shortname'):
        if cls.classtype not in classes:
            classes[cls.classtype] = collections.OrderedDict()

        grade = cls.shortname[1]
        if grade not in classes[cls.classtype]:
            classes[cls.classtype][grade] = []
        classes[cls.classtype][grade].append(cls.shortname)

    return {'classes': classes}


def get_error_response(request, message):
    """
    Render view with error
    """
    template = loader.get_template('vote_error.html')
    context = {'error': message}
    return HttpResponse(template.render(with_metadata(context), request))


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
    return get_error_response(request, 'Momentálně neprobíhá žádné volební kolo')


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

    class_name = request.GET.get('name', None)
    context = {
        'class_name': class_name,
    }

    if class_name is not None:
        try:
            cls = Class.objects.get(shortname=class_name)
        except Class.DoesNotExist:
            msg = "Třída '%s' nebyla nalezena, zkontrolujte si prosím název" % class_name
            return get_error_response(request, msg)

        students = Student.objects.all().filter(class_id=cls)
        context['students'] = students

    context.update(get_sidebar_class_context())
    return HttpResponse(template.render(with_metadata(context), request))


def proccess_vote(request):
    """
    Called when user want to vote for someone
    """
    template = loader.get_template('class_overview.html')

    me = Student.objects.get(id=505)
    print(me.name)
    print(', '.join(str([pin.pin, pin.round_id.round_number, pin.round_id.type_id.name]) for pin in Pin.objects.all().filter(student_id=me)))

    required = ['student_id', 'email', 'pin']
    if request.method != 'POST' or any(req not in request.POST for req in required):
        return get_error_response(request, "Špatný požadavek")

    student_id = int(request.POST.get("student_id"))
    email = request.POST.get("email")
    pin_code = request.POST.get("pin")

    try:
        student = Student.objects.get(id=student_id)
        election = Election.objects.latest('id')
    except Student.DoesNotExist:
        return get_error_response(request, "Student, pro kterého hlasujete, neexistuje")
    except Election.DoesNotExist:
        return get_error_response(request, "V systému nejsou žádné volby")

    active = election.active_round
    if active is None:
        return get_error_response(request, "Momentálně neprobíhají žádné volby")

    pins_list = Pin.objects.all().filter(pin=pin_code)
    pins = [pin for pin in pins_list if pin.student_id.email == email and pin.round_id.compare == 0]
    if len(pins) == 0:
        return get_error_response(
            request,
            "Aktivace pinu selhala. Zkontrolujte prosím jeho správnost.")

    # Pin and email is valid
    return get_error_response(request, "Pin prošel.")


    return HttpResponse(template.render(with_metadata({}), request))
