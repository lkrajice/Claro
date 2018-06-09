from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'', views.overview),
    url(r'nomination', views.nomination_overview),
    url(r'class', views.class_overview),
    url(r'election', views.election_overview)
]
