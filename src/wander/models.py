import datetime
from django.db import models

# Create your models here.
from pytz import utc
from rest_framework.fields import JSONField


class Guide(models.Model):
    status_online = models.BooleanField(default=False)
    status_on_trip = models.BooleanField(default=False)


class Traveler(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    interest = JSONField(default={})
    country = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)


class Trip(models.Model):
    traveler = models.ForeignKey('wander.Traveler')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    start_location = JSONField(default={})
    end_location = JSONField(default={})
    rating = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """ On save, update timestamps"""
        if not self.id:  # On create
            self.start_time = datetime.datetime.now(tz=utc)
