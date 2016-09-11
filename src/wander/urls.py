from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns

from wander import views

urlpatterns = (
    url(r'^trips/$', views.TripView.as_view(), name='trips'),
)

urlpatterns = format_suffix_patterns(urlpatterns)