from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage


def index(request):
    """
        SHOWS
        ACTIONS co muze udelat
        PROCCESS co delat metoda
    """
    template = loader.get_template("administration_index.html")
    context = {}
    return HttpResponse(template.render(context, request))


def election_management(request):
    template = loader.get_template("administration_electionmanagement.html")
    context = {}
    return HttpResponse(template.render(context, request))


def pupil_management(request):
    template = loader.get_template("administration_pupilmanagement.html")
    context = {}
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
    return HttpResponse(template.render(context, request))
