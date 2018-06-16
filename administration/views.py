# -*- coding: utf-8 -*-
import os

from django.template import loader
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from votes import models as model
from .utils import StudentDataFileParser, generate_pin
from claro.utils import get_context_manager
import datetime

BASE_CONTEXT = {}
with_metadata = get_context_manager(BASE_CONTEXT)


def index(request):
    """
        SHOWS
        ACTIONS co muze udelat
        PROCCESS co delat metoda
    """
    template = loader.get_template("administration_index.html")
    context = {}
    return HttpResponse(template.render(with_metadata(context), request))


def election_management(request):
    template = loader.get_template("administration_electionmanagement.html")
    context = {
        "election": False,
    }

    if request.method == 'POST':
        election_name = request.POST.get("election_name")
        date_election_start = request.POST.get("date_election_start")
        first_round_days = int(request.POST.get("first_round_days")) - 1
        second_round_days = int(request.POST.get("second_round_days")) - 1
        third_round_days = int(request.POST.get("third_round_days")) - 1

        first_round_end = (datetime.datetime.strptime(date_election_start, "%Y-%m-%d")
                           + datetime.timedelta(days=first_round_days)).date()
        second_round_start = first_round_end + datetime.timedelta(days=1)
        second_round_end = second_round_start + datetime.timedelta(days=second_round_days)

        third_round_start = second_round_end + datetime.timedelta(days=1)
        third_round_end = third_round_start + datetime.timedelta(days=third_round_days)

        election = model.Election(title=election_name)
        election.save()

        all_round_types = model.RoundType.objects.all()
        types = {t.name: t for t in all_round_types}

        model.Round.objects.bulk_create([
            model.Round(election_id=election, type_id=types['nomination'], round_number=1,
                        start=date_election_start, end=first_round_end),
            model.Round(election_id=election, type_id=types['nomination'], round_number=2,
                        start=second_round_start, end=second_round_end),
            model.Round(election_id=election, type_id=types['election'], round_number=3,
                        start=third_round_start, end=third_round_end)
        ])

        rounds = model.Round.objects.all().filter(election_id=election)
        students = model.Student.objects.all()

        pins = []
        for election_round in rounds:
            for student in students:
                pins.append(model.Pin(pin=generate_pin(),
                            student_id=student,
                            round_id=election_round))

        model.Pin.objects.bulk_create(pins)

    return HttpResponse(template.render(with_metadata(context), request))


def pupil_management(request):
    template = loader.get_template("administration_pupilmanagement.html")
    context = {
        "election": False
    }

    # proccess uploaded file
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        fs.save(myfile.name, myfile)
        filepath = os.path.join(settings.MEDIA_ROOT, myfile.name)

        StudentDataFileParser.proccess_file(filepath)




    return HttpResponse(template.render(with_metadata(context), request))
