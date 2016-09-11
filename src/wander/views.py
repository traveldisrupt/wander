from rest_framework import exceptions
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from src.wander.serializers import TripSerializer


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

        data = {'trip': 'trip_123'}

        return Response({'status': 'success', 'data': data})