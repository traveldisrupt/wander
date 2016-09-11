import urllib
import requests
from rest_framework import exceptions
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from wander.serializers import TripSerializer
from wander.models import Traveler
from wander.serializers import CreateTripSerializer
from wander.models import Trip


class TripView(GenericAPIView):
    """
    ### Get the available trips.

    """
    permission_classes = ()
    allowed_methods = ('POST', 'GET')
    serializer_class = TripSerializer

    def post(self, request, *args, **kwargs):
        user = request.user

        data = {'trip': 'trip_123'}

        return Response({'status': 'success', 'data': data})

    def get(self, request, *args, **kwargs):

        r = requests.get("https://thingspace.io/get/latest/dweet/for/padmaja-device")
        current_location = r.json()['with'][0]['content']
        print(current_location)

        data = {'trip': {'id': 'trip_123',
                         'start_time': '2015-08-1 11:01',
                         'traveler':
                             {'name': 'Daniela',
                              'age': '26',
                              'occupation': 'Web Designer',
                              'country': 'United States',
                              'city': 'New York',
                              'interest': {'Movies', 'Restuarants', 'Baseball'},
                              'bio': 'I love exploring and learning. The world is flat.'},
                         'start_location': {'lat': '37.7786', 'lon': '122.3893'},
                         'end_location': {'lat': '37.7786', 'lon': '122.3893'},
                         'current_location': current_location,
                         'status': 'live',
                         }
                }

        return Response({'status': 'success', 'data': data})


class CreateTripView(GenericAPIView):
    """
    ### Get the available trips.

    """
    permission_classes = ()
    allowed_methods = ('POST',)
    serializer_class = CreateTripSerializer

    def post(self, request, *args, **kwargs):

        # If user creates a trip, check if there is more than one trip entry for the user. If so, then cancel previous
        # and create a new trip.
        username = request.data.get('username')
        traveler, created = Traveler.objects.get_or_create(username=username)

        # Create trip
        if Trip.objects.filter(traveler=traveler, status='Waiting').exists():
            Trip.objects.update(status='Cancelled')

        trip = Trip.objects.create(traveler=traveler)

        data = {'trip': traveler.username}

        return Response({'status': 'success', 'data': data})