from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^administration', views.index),
    url(r'^electionmanagement', views.election_management),
    url(r'^pupilmanagement', views.pupil_management),
    url(r'^', views.index)
]

