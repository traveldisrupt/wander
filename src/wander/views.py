from rest_framework import exceptions
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from wander.serializers import TripSerializer


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
        data = {'trip': 'trip_123',
                'traveler':
                    {'name': 'Daniela',
                     'age': '26',
                     'occupation': 'Web Designer',
                     'country': 'United States',
                     'city': 'New York',
                     'interest': {'Movies', 'Restuarants', 'Baseball'}}
                }

        return Response({'status': 'success', 'data': data})


        # class Guide(models.Model):
        #     status_online = models.BooleanField(default=False)
        #     status_on_trip = models.BooleanField(default=False)
        #
        #
        # class Traveler(models.Model):
        #     name = models.CharField(max_length=30, blank=True, null=True)
        #     age = models.IntegerField(blank=True, null=True)
        #     occupation = models.CharField(max_length=100, blank=True, null=True)
        #     interest = JSONField(default={})
        #     country = models.CharField(max_length=100, blank=True, null=True)
        #     bio = models.TextField(blank=True, null=True)
        #
        #
        # class Trip(models.Model):
        #     traveler = models.ForeignKey('wander.Traveler')
        #     start_time = models.DateTimeField(null=True, blank=True)
        #     end_time = models.DateTimeField(null=True, blank=True)
        #     start_location = JSONField(default={})
        #     end_location = JSONField(default={})
        #     rating = models.IntegerField(blank=True, null=True)
