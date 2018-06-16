from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'proccess_vote', views.proccess_vote),

    url(r'overview', views.overview),
    url(r'class', views.class_overview),
    url(r'', views.overview),
]
