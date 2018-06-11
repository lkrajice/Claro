from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'welcome', views.home_welcome),
    url(r'about', views.home_about),
    url(r'help', views.home_help),
    url(r'', views.home_welcome),
]
