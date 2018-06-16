from pprint import pprint
import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from claro.utils import get_context_manager

from votes.models import Election, Round


with_metadata = get_context_manager()


# Create your views here.
def home_welcome(request):
    """
    Welcome page + show current active election

    SHOWS:
        Welcome page
        List of Rounds per currently active ellection

    PROCCESS:
        Get last election
        Get it's rounds
        Check if election is active
        IF election is active
            Append table with overview

    """
    template = loader.get_template('home_welcome.html')

    context = {}
    try:
        election = Election.objects.latest('id')
        rounds = Round.objects.all().filter(election_id=election).order_by('round_number')

        context['election'] = election
        context['rounds'] = rounds
        if all(r.compare == -1 for r in rounds):
            context['election_state'] = -1
        elif all(r.compare == 1 for r in rounds):
            context['election_state'] = 1
        else:
            context['election_state'] = 0

    except Election.DoesNotExist:
        context['election'] = None

    return HttpResponse(template.render(with_metadata(context), request))

def home_help(request):
    template = loader.get_template('home_help.html')
    context = {}
    return HttpResponse(template.render(with_metadata(context), request))
