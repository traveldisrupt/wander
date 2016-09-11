import urllib
import re
import requests
from django.conf import settings
from rest_framework import exceptions
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from wander.serializers import TripSerializer
from wander.models import Traveler
from wander.serializers import CreateTripSerializer
from wander.models import Trip
from wander.serializers import ViewTripSerializer

from twilio.util import TwilioCapability
import twilio.twiml

phone_pattern = re.compile(r"^[\d\+\-\(\) ]+$")

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

        data = {'trip_id': traveler.username}

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

        data = {'trip_id': trip_id, 'status': 'waiting'}

        return Response({'status': 'success', 'data': data})


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

        username = 'padmaja-device'
        identity = username

        # Create a Capability Token
        capability = TwilioCapability(account_sid, auth_token)
        capability.allow_client_outgoing(application_sid)
        capability.allow_client_incoming(identity)
        token = capability.generate()

        return Response({'identity': identity, 'toke ': token})


# class TwilioVoiceView(GenericAPIView):
#     """
#     ### Twilio token.
#
#     """
#     permission_classes = ()
#     allowed_methods = ('POST',)
#
#     def post(self, request, *args, **kwargs):
#         resp = twilio.twiml.Response()
#         if "To" in request.data and request.data["To"] != '':
#             dial = resp.dial(callerId=getattr(settings,'TWILIO_CALLER_ID'))
#             # wrap the phone number or client name in the appropriate TwiML verb
#             # by checking if the number given has only digits and format symbols
#             if phone_pattern.match(request.data["To"]):
#                 dial.number(request.form["To"])
#             else:
#                 dial.client(request.form["To"])
#         else:
#             resp.say("Thanks for calling!")
#
#         return Response({'identity': identity, 'toke ': token})
