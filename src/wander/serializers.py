from logging import getLogger
from rest_framework import serializers

logger = getLogger('django')


class TripSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    action = serializers.CharField(required=True)
    trip_id = serializers.IntegerField(required=True)


class CreateTripSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)


class ViewTripSerializer(serializers.Serializer):
    trip_id = serializers.CharField(required=True)


class CancelTripSerializer(serializers.Serializer):
    trip_id = serializers.CharField(required=False)


class TwilioVoiceSerializer(serializers.Serializer):
    To = serializers.CharField()
