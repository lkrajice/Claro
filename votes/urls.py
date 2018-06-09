from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'overview', views.overview),
    url(r'class', views.class_overview),
    url(r'', views.overview),
]
