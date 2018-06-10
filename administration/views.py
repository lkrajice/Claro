import os

from django.template import loader
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from .utils import StudentDataFileParser

from claro.utils import get_context_manager

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
        "election": False
    }
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
