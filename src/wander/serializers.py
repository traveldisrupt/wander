from logging import getLogger
from rest_framework import serializers

logger = getLogger('django')


class TripSerializer(serializers.Serializer):
    traveler = serializers.SerializerMethodField(source='get_traveler')

    def get_traveler(self, obj):
        return "Traveler"

