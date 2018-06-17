# -*- coding: utf-8 -*-
import os
import datetime

from django.template import loader
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from votes import models as model
from claro.utils import get_context_manager

from .utils import StudentDataFileParser, generate_pin
from . import utils as util


BASE_CONTEXT = {}
with_metadata = get_context_manager()


def index(request):
    is_logged = request.session.get('pass_verified', False)
    if not is_logged:
        new_request, logged = login(request)
        if not logged:
            return new_request

    context = {}
    template = loader.get_template("administration_index.html")
    return HttpResponse(template.render(with_metadata(context), request))


def context_update():
    context = {}
    elections = model.Election.objects.all()
    today = datetime.datetime.today().strftime('%Y-%m-%d')

    context.update(
        {
            "message_active": False,
            "active_elections": False,
            "today": today,
            "elections": elections
        }
    )

    # Check if active elections
    for election in elections:
        for round in election.get_rounds:
            if round.compare == 0:
                context.update(
                    {
                        "active_elections": True,
                        "first_round": election.get_first_round,
                        "second_round": election.get_second_round,
                        "third_round": election.get_third_round,
                        "today": today,
                        "elections": elections,
                        "active_round": round
                    }
                )
    return context


def election_management(request):
    is_logged = request.session.get('pass_verified', False)
    if not is_logged:
        new_request, logged = login(request)
        if not logged:
            return new_request

    context = context_update()
    template = loader.get_template("administration_electionmanagement.html")

    if request.POST.get("new_election"):
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

        types = {t.name: t for t in model.RoundType.objects.all()}

        model.Round.objects.bulk_create([
            model.Round(election_id=election, type_id=types['nomination'], round_number=1,
                        start=date_election_start, end=first_round_end),
            model.Round(election_id=election, type_id=types['nomination'], round_number=2,
                        start=second_round_start, end=second_round_end),
            model.Round(election_id=election, type_id=types['election'], round_number=3,
                        start=third_round_start, end=third_round_end)
        ])

        # Add pins for each student per each created round
        rounds = election.get_rounds
        students = model.Student.objects.all()
        pins = []
        for election_round in rounds:
            for student in students:
                pins.append(model.Pin(pin=generate_pin(),
                            student_id=student,
                            round_id=election_round))
        model.Pin.objects.bulk_create(pins)

        message = util.MessageToPage("success", "Výborně!", "Úspěšně jste vytvořil nové volby", "")
        model.schedule_db_updates()
        context = context_update()
        context.update({"message_active": True, "message": message, "active_elections": True})
        return HttpResponse(template.render(with_metadata(context), request))

    if request.POST.get("first_save_changes"):
        original_name = request.POST.get("first_save_changes")
        election_name = request.POST.get("election_name")
        second_round_start = request.POST.get("second_round_start")
        second_round_end = request.POST.get("second_round_end")
        third_round_start = request.POST.get("third_round_start")
        third_round_end = request.POST.get("third_round_end")

        selected_election = model.Election.objects.all().get(title=original_name)
        selected_election.title = election_name
        selected_election.save()

        rounds = selected_election.get_rounds
        second_round = rounds[1]
        second_round.start = second_round_start
        second_round.end = second_round_end
        second_round.save()
        third_round = rounds[2]
        third_round.start = third_round_start
        third_round.end = third_round_end
        third_round.save()

        message = util.MessageToPage("success", "Výborně!", "Úspěšně jste uložil změny")
        model.schedule_db_updates()
        context = context_update()

        context.update({"message_active": True, "message": message, "active_elections": True})
        return HttpResponse(template.render(with_metadata(context), request))

    if request.POST.get("second_save_changes"):
        original_name = request.POST.get("second_save_changes")
        election_name = request.POST.get("election_name")
        third_round_start = request.POST.get("third_round_start")
        third_round_end = request.POST.get("third_round_end")

        selected_election = model.Election.objects.all().get(title=original_name)
        selected_election.title = election_name
        selected_election.save()

        rounds = selected_election.get_rounds

        third_round = rounds[2]
        third_round.start = third_round_start
        third_round.end = third_round_end
        third_round.save()

        message = util.MessageToPage("success", "Výborně!", "Úspěšně jste uložil změny", "")
        model.schedule_db_updates()
        context = context_update()
        context.update({"message_active": True, "message": message, "active_elections": True})
        return HttpResponse(template.render(with_metadata(context), request))

    if request.POST.get("third_save_changes"):
        original_name = request.POST.get("third_save_changes")
        election_name = request.POST.get("election_name")

        selected_election = model.Election.objects.all().get(title=original_name)
        selected_election.title = election_name
        selected_election.save()

        message = util.MessageToPage("success", "Výborně!", "Úspěšně jste uložil změny", "")
        model.schedule_db_updates()
        context = context_update()
        context.update({"message_active": True, "message": message, "active_elections": True})
        return HttpResponse(template.render(with_metadata(context), request))

    if request.POST.get("cancel_election"):
        election_name = request.POST.get("cancel_election")
        elections = model.Election.objects.all()
        active_elections = elections.filter(title=election_name)
        for election in active_elections:
            rounds = election.get_rounds
            for rnd in rounds:
                rnd.delete()
            election.delete()

        message = util.MessageToPage("success", "Výborně!", "Úspěšně jste zrušil volby")
        model.schedule_db_updates()
        context = context_update()
        context.update({"message_active": True, "message": message})
        return HttpResponse(template.render(with_metadata(context), request))
    return HttpResponse(template.render(with_metadata(context), request))


def pupil_management(request):
    is_logged = request.session.get('pass_verified', False)
    if not is_logged:
        new_request, logged = login(request)
        if not logged:
            return new_request

    context = {"message_active": False}
    template = loader.get_template("administration_pupilmanagement.html")
    students = model.Student.objects.all()
    classes = model.Class.objects.all().order_by('shortname')
    context.update(
        {
            "students": students,
            "classes": classes
        }
    )
    if request.POST.get("add_student"):
        st_class_input = request.POST.get("student_class")
        st_name = request.POST.get("student_name")
        st_email = request.POST.get("student_email")
        st_class = model.Class.objects.get(shortname=st_class_input)

        # pin = model.Pin(pin=StudentDataFileParser.generate_pin())
        # pin.save()

        model.Student(class_id=st_class, name=st_name, email=st_email, profile_image="NaN").save()
        message = util.MessageToPage("success", "Výborně!", "Úspěšně jste přidal studenta", "")
        context.update({"message_active": True, "message": message})
        return HttpResponse(template.render(with_metadata(context), request))
    if request.POST.get("remove_student"):
        st_name = request.POST.get("remove_student")
        students.filter(name=st_name).delete()
        message = util.MessageToPage("success", "Výborně!", "Úspěšně jste smazal studenta", "")
        context.update({"message_active": True, "message": message})
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
        message = util.MessageToPage("success", "Výborně!", "Úspěšně jste nahrál soubor")
        context.update({"message_active": True, "message": message})
    return HttpResponse(template.render(with_metadata(context), request))


def login(request):
    """
    Check if user is logged in, Returns HttpResponse if not, othervise True
    """
    request.session['pass_verified'] = False
    admin_pwd = "WeLoveAnime"
    template = loader.get_template("login.html")
    context = {}

    if request.POST.get("log_in"):
        pwd = request.POST.get("user_type_password")
        if pwd == admin_pwd:
            request.session['pass_verified'] = True
            index(request)
            return None, True

    return HttpResponse(template.render(with_metadata(context), request)), False
