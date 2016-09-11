from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns

from wander import views

urlpatterns = (

    # Return available trip and accept POST request for accepting a trip.
    url(r'^trips/$', views.TripView.as_view(), name='trips'),

    url(r'^trip/create/$', views.CreateTripView.as_view(), name='create_trip'),
    url(r'^trip/view/$', views.ViewTripView.as_view(), name='view_trip'),
    # url(r'^trip/cancel/$', views.CancelTripView.as_view(), name='cancel_trip'),
)

urlpatterns = format_suffix_patterns(urlpatterns)