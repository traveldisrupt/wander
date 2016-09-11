import datetime
from django.db import models

# Create your models here.
from pytz import utc
from django.contrib.postgres.fields import JSONField


class Guide(models.Model):
    username = models.CharField(max_length=30, blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    status_online = models.BooleanField(default=False)
    status_on_trip = models.BooleanField(default=False)


class Traveler(models.Model):
    username = models.CharField(max_length=30, blank=True, null=True)
    profile = models.URLField(default='https://scontent-sjc2-1.xx.fbcdn.net/v/t1.0-9/12688174_10207842733043301_2986078780578216664_n.jpg?oh=8c537cad4e8cb989e42a718cdea69eb2&oe=58481E5B')
    name = models.CharField(max_length=30, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    interest = JSONField(null=True, blank=True, default={})
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)


class Trip(models.Model):
    guide = models.ForeignKey('wander.Guide', null=True, blank=True)
    traveler = models.ForeignKey('wander.Traveler')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    start_location = JSONField(null=True, blank=True, default={})
    end_location = JSONField(null=True, blank=True, default={})
    rating = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=12, default='waiting')

    def save(self, *args, **kwargs):
        """ On save, update timestamps"""
        if not self.id:  # On create
            self.start_time = datetime.datetime.now(tz=utc)
        return super(Trip, self).save(*args, **kwargs)
