# -*- coding: utf-8 -*-
import os
from django.template import loader
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from votes import models as model
from .utils import StudentDataFileParser
from claro.utils import get_context_manager
import datetime

BASE_CONTEXT = {}
with_metadata = get_context_manager(BASE_CONTEXT)


def index(request):
    template = loader.get_template("administration_index.html")
    context = {}
    return HttpResponse(template.render(with_metadata(context), request))


def election_management(request):
    """
        SHOWS
            App where you can manage elections and see their history
    """
    template = loader.get_template("administration_electionmanagement.html")
    today = datetime.datetime.today().strftime('%Y-%m-%d')

    el = model.ElectionController()
    context = {
        "today": today,
        "elcont" : el,
    }

    """
        Create new election
        --------------------
        This script will take all data from POST and creates correct times for election rounds and add record to database
    """
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
            model.Round(election_id=election, type_id=types['nomination'], round_number=1, start=date_election_start, end=first_round_end),
            model.Round(election_id=election, type_id=types['nomination'], round_number=2, start=second_round_start, end=second_round_end),
            model.Round(election_id=election, type_id=types['election'], round_number=3, start=third_round_start, end=third_round_end)
        ])
        context.update({'created_election':True})
    return HttpResponse(template.render(with_metadata(context), request))


def pupil_management(request):
    """
        SHOWS
            App where you can manage students that can vote
    """

    template = loader.get_template("administration_pupilmanagement.html")
    students = model.Student.objects.all()
    context = {
        "election": False,
        "students": students
    }
    if request.method == 'POST':
        if request.POST.get("remove_pupil"):
            print("Odebrat žáka")
            data = request.POST.get("remove_pupil")
            for student in model.Student.objects.all():
                if student.name == data:
                    student.delete()
            return HttpResponse(template.render(with_metadata(context), request))
        if request.POST.get("add_student"):
            print("Přidání studenta")
            st_class = request.POST.get("student_class")
            for cls in model.Class.objects.all():
                if cls.shortname == st_class:
                    st_class = cls
            pin = model.Pin(pin=StudentDataFileParser.generate_pin())
            pin.save()
            st_name = request.POST.get("student_name")
            st_email = request.POST.get("student_email")
            print(st_class, pin, st_name, st_email)
            new_student = model.Student(class_id = st_class, pin_id = pin, name = st_name, email = st_email, profile_image = "NaN")
            new_student.save()
            return HttpResponse(template.render(with_metadata(context), request))
        if request.POST.get("modify_student"):
            print("upravit zaka")
            st_name = request.POST.get("modify_student")
            new_st_name = request.POST.get("name_new_student")
            new_st_class = request.POST.get("new_student_class")
            new_student_mail = request.POST.get("new_student_mail")

            st_object=""
            print("JMENO: "+ st_name)
            for student in model.Student.objects.all():
                if student.name == st_name:
                    st_object = student

            st_class = ""
            for cls in model.Class.objects.all():
                if cls.shortname == new_st_class:
                    st_class = cls

            st_object.class_id = st_class
            st_object.name = new_st_name
            st_object.email = new_student_mail

            st_object.save()
            return HttpResponse(template.render(with_metadata(context), request))

    """
        Upload new file
        ------------------------
        This script takes file from computer, loads it into server and parse it
    """
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        fs.save(myfile.name, myfile)
        filepath = os.path.join(settings.MEDIA_ROOT, myfile.name)
        StudentDataFileParser.proccess_file(filepath)

    return HttpResponse(template.render(with_metadata(context), request))
