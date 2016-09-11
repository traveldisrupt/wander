import urllib
import datetime
from pytz import utc
import requests
from django.conf import settings
from rest_framework import exceptions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from wander.serializers import TripSerializer, CreateTripSerializer, ViewTripSerializer, CancelTripSerializer, TwilioVoiceSerializer
from wander.models import Traveler, Trip, Guide
from rest_framework.reverse import reverse
from collections import OrderedDict
from django.http import HttpResponse
import re

alphanumeric_only = re.compile('[\W_]+')
phone_pattern = re.compile(r"^[\d\+\-\(\) ]+$")

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def api_root(request, format=None):
    """
    ### API documentation for the Rehive digital currency platform.
    ---
    """
    return Response(
        [
            {'Guide': OrderedDict(
                [('View, Accept, Decline and Cancel Trips', reverse('wander-api:trips', request=request, format=format)),
                 ]
            )},
            {'Traveler': OrderedDict(
                [('View Trip', reverse('wander-api:view_trip', request=request, format=format)),
                 ('Create Trip', reverse('wander-api:create_trip', request=request, format=format)),
                 ('Cancel Trip', reverse('wander-api:cancel_trip', request=request, format=format)),
                 ]
            )},
            {'Twilio': OrderedDict(
                [('Twilio Token', reverse('wander-api:twilio_token_view', request=request, format=format)),
                 ]
            )}
        ])

from twilio.util import TwilioCapability
import twilio.twiml

class TripView(GenericAPIView):
    """
    ### Get the available trips.

    """
    permission_classes = ()
    allowed_methods = ('POST', 'GET')
    serializer_class = TripSerializer

    def post(self, request, *args, **kwargs):

        action = request.data.get('action')
        trip_id = request.data.get('trip_id')
        guide = request.data.get('username')

        guide, created = Guide.objects.get_or_create(username=guide)

        if action == 'accept':
            Trip.objects.filter(id=trip_id).update(guide=guide, status='live')
        elif action == 'cancel':
            Trip.objects.filter(id=trip_id).update(guide=guide, status='cancelled', end_time=datetime.datetime.now(tz=utc))

        return Response({'status': 'success'})

    def get(self, request, *args, **kwargs):

        r = requests.get("https://thingspace.io/get/latest/dweet/for/arthur")
        current_location = r.json()['with'][0]['content']

        # Hard code get latest trip created.
        trip = Trip.objects.latest('id')

        data = {'trip': {'id': trip.id,
                         'start_time': trip.start_time,
                         'traveler':
                             {'name': trip.traveler.name,
                              'age': trip.traveler.age,
                              'occupation': trip.traveler.occupation,
                              'country': trip.traveler.country,
                              'city': trip.traveler.city,
                              'interest': trip.traveler.interest,
                              'bio': trip.traveler.bio,
                              'profile': trip.traveler.profile},
                         'start_location': {'lat': '37.7786', 'lon': '122.3893'},
                         'end_location': {'lat': '37.7786', 'lon': '122.3893'},
                         'facts': [{'category': 'History',
                                    'title': 'Pier 43',
                                    'text': 'Built 1914. Pier 43 and its headhouse, a decorated hoisting tower for loading and unloading rail cars on and off ferries, was built in 1914 to serve the Belt Railroad.',
                                    'distance': '0 miles',
                                    'lat': '37.809382',
                                    'lon': '-122.414465'},
                                   {'category': 'Landmark', 'title': 'AT&T Park',
                                    'text': 'The park stands along the San Francisco Bay, a segment of which is named McCovey Cove in honor of former Giants player Willie McCovey.',
                                    'distance': '0.2 miles',
                                    'lat': '37.7786',
                                    'lon': '-122.3893'},
                                   {'category': 'Restaurants',
                                    'title': "Pedro's Cantina",
                                    'text': 'Mexican food & margaritas served in a roomy converted warehouse outfitted with many high-def TVs.',
                                    'distance': '0.3 miles',
                                    'rating': 4,
                                    'lat': '37.77935',
                                    'lon': '-122.39051'},
                                   ],
                         'current_location': current_location,
                         'status': trip.status,
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
        if Trip.objects.filter(traveler=traveler, status='waiting').exists():
            Trip.objects.filter(traveler=traveler).update(status='cancelled', end_time=datetime.datetime.now(tz=utc))

        trip = Trip.objects.create(traveler=traveler)

        data = {'trip_id': trip.id}

        return Response({'status': 'success', 'data': data})


class ViewTripView(GenericAPIView):
    """
    ### Get the trip info for Traveler.

    """
    permission_classes = ()
    allowed_methods = ('POST',)
    serializer_class = ViewTripSerializer

    def post(self, request, *args, **kwargs):

        # If user creates a trip, check if there is more than one trip entry for the user. If so, then cancel previous
        # and create a new trip.
        trip_id = request.data.get('trip_id')

        if Trip.objects.filter(id=trip_id).exists():
            trip = Trip.objects.get(id=trip_id)
            data = {'trip_id': trip_id, 'status': trip.status}
            return Response({'status': 'success', 'data': data})
        else:
            return Response({'status': 'error', 'message': 'Trip does not exist.'})


class CancelTripView(GenericAPIView):
    """
    ### Get the trip info for Traveler.

    """
    permission_classes = ()
    allowed_methods = ('POST',)
    serializer_class = CancelTripSerializer

    def post(self, request, *args, **kwargs):

        # If user creates a trip, check if there is more than one trip entry for the user. If so, then cancel previous
        # and create a new trip.
        trip_id = request.data.get('trip_id')

        if Trip.objects.filter(id=trip_id).exists():
            trip = Trip.objects.get(id=trip_id)
            trip.end_time = datetime.datetime.now(tz=utc)
            trip.status = 'cancelled'
            trip.save()
            data = {'trip_id': trip_id, 'status': trip.status}
            return Response({'status': 'success', 'data': data})
        else:
            return Response({'status': 'error', 'message': 'Trip does not exist.'})


class TwilioTokenView(GenericAPIView):
    """
    ### Twilio token.

    """
    permission_classes = ()
    allowed_methods = ('GET',)

    def get(self, request, *args, **kwargs):

        # get credentials for environment variables
        account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID')
        auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN')
        application_sid = getattr(settings, 'TWILIO_TWIML_APP_SID')

        # Generate a random user name
        user = self.request.query_params.get('user', '')
        if user:
            identity = alphanumeric_only.sub('', user)
        else:
            identity = alphanumeric_only.sub('', 'default')

        # Create a Capability Token
        capability = TwilioCapability(account_sid, auth_token)
        capability.allow_client_outgoing(application_sid)
        capability.allow_client_incoming(identity)
        token = capability.generate()

        return Response(OrderedDict([('identity', identity), ('token', token)]))


class TwilioVoiceView(GenericAPIView):
    """
    ### Twilio token.

    """
    permission_classes = ()
    allowed_methods = ('POST',)
    serializer_class = TwilioVoiceSerializer

    def post(self, request, *args, **kwargs):
        resp = twilio.twiml.Response()
        if "To" in request.data and request.data["To"] != '':
            dial = resp.dial(callerId=getattr(settings,'TWILIO_CALLER_ID'))
            # wrap the phone number or client name in the appropriate TwiML verb
            # by checking if the number given has only digits and format symbols
            if phone_pattern.match(request.data["To"]):
                dial.number(request.data["To"])
            else:
                dial.client(request.data["To"])
        else:
            resp.say("Thanks for calling!")

        return HttpResponse(str(resp), content_type='text/xml')

