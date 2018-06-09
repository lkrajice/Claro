from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
# Create your views here.

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
    return HttpResponse(template.render(context, request))
