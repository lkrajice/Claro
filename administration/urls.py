from django.conf.urls import include, url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^administration', views.index),
    url(r'^electionmanagement', views.election_management),
    url(r'^pupilmanagement', views.pupil_management),
    url(r'^', views.index)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
