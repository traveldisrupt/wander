import urllib
import requests
from rest_framework import exceptions
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from wander.serializers import TripSerializer, CreateTripSerializer, ViewTripSerializer
from wander.models import Traveler, Trip, Guide


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
        elif action == 'cancelled':
            Trip.objects.filter(id=trip_id).update(guide=guide, status='cancelled')

        return Response({'status': 'success'})

    def get(self, request, *args, **kwargs):

        r = requests.get("https://thingspace.io/get/latest/dweet/for/padmaja-device")
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
                                    'distance': '0 miles'},
                                   {'category': 'Landmark', 'title': 'AT&T Park',
                                    'text': 'The park stands along the San Francisco Bay, a segment of which is named McCovey Cove in honor of former Giants player Willie McCovey.',
                                    'distance': '0.2 miles'},
                                   {'category': 'Restaurants',
                                    'title': "Pedro's Cantina",
                                    'text': 'Mexican food & margaritas served in a roomy converted warehouse outfitted with many high-def TVs.',
                                    'distance': '0.3 miles',
                                    'rating': 4},
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
        if Trip.objects.filter(traveler=traveler, status='Waiting').exists():
            Trip.objects.update(status='Cancelled')

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


            # class TwilioTokenView(GenericAPIView):
            #     """
            #     ### Twilio token.
            #
            #     """
            #     permission_classes = ()
            #     allowed_methods = ('GET',)
            #     serializer_class = TwilioTokenSerializer
            #
            # @app.route('/token', methods=['GET'])
            # def token():
            #     # get credentials for environment variables
            #     account_sid = os.environ['TWILIO_ACCOUNT_SID']
            #     auth_token = os.environ['TWILIO_AUTH_TOKEN']
            #     application_sid = os.environ['TWILIO_TWIML_APP_SID']
            #
            #     # Generate a random user name
            #     username = 'padmaja-device_123456789'
            #     identity = username
            #
            #     # Create a Capability Token
            #     capability = TwilioCapability(account_sid, auth_token)
            #     capability.allow_client_outgoing(application_sid)
            #     capability.allow_client_incoming(identity)
            #     token = capability.generate()
            #
            #     # Return token info as JSON
            #     return jsonify(identity=identity, token=token)
