from logging import getLogger
from rest_framework import serializers

logger = getLogger('django')


class TripSerializer(serializers.Serializer):
    pass


class CreateTripSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)


class ViewTripSerializer(serializers.Serializer):
    trip_id = serializers.CharField(required=True)