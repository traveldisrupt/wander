from logging import getLogger
from rest_framework import serializers

logger = getLogger('django')


class TripSerializer(serializers.Serializer):

    def get_traveler(self, obj):
        return "Traveler"


class CreateTripSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)

