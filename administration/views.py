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

    # e = Election.objects.latest()
    # print(e.title)


    if request.method == 'POST':
        # Election
        election = model.Election(title=request.POST.get("election_name"))
        election.save()

        # RoundTypes
        all_round_types = model.RoundType.objects.all()
        types = {t.name: t for t in all_round_types}

        # Round
        start = datetime.datetime.strptime(request.POST.get("date_election_start"), "%Y-%m-%d")
        round1_delta = datetime.timedelta(days=int(request.POST.get("first_round_days")))
        round2_delta = datetime.timedelta(days=int(request.POST.get("second_round_days")))
        round3_delta = datetime.timedelta(days=int(request.POST.get("third_round_days")))

        round1_end_date = (start + round1_delta).date()
        round2_end_date = (start + round1_delta + round2_delta).date()
        round3_end_date = (start + round1_delta + round2_delta + round3_delta).date()
        round_ends = [round1_end_date, round2_end_date, round3_end_date]

        round_list = []
        for index, r in enumerate(round_ends):
            round_type = types['nomination'] if index < 2 else types['election']
            round_list.append(model.Round(election_id=election,
                                          type_id=round_type,
                                          round_number=index+1,
                                          start=round_ends[index],
                                          end=round_ends[index]))

        model.Round.objects.bulk_create(round_list)
        #context.update({'zprava':True})
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
