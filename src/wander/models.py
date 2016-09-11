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
    total_trips = models.IntegerField(blank=True, null=True)
    avg_rating = models.IntegerField(blank=True, null=True)


class Traveler(models.Model):
    username = models.CharField(max_length=30, blank=True, null=True)
    profile = models.URLField(
        default='https://scontent-sjc2-1.xx.fbcdn.net/v/t1.0-9/12688174_10207842733043301_2986078780578216664_n.jpg?oh=8c537cad4e8cb989e42a718cdea69eb2&oe=58481E5B')
    name = models.CharField(max_length=30, default="Arthur Dent")
    age = models.IntegerField(blank=True, default="23")
    occupation = models.CharField(max_length=100, default="Developer")
    interest = JSONField(null=True, blank=True, default={"all": ["Movies", "Running", "Food", "Technology"]})
    country = models.CharField(max_length=100, default="South Africa")
    city = models.CharField(max_length=100, default="Cape Town")
    bio = models.TextField(default="I recently moved to San Francisco. I love exploring - it is the answer to everything.")


class Trip(models.Model):
    guide = models.ForeignKey('wander.Guide', null=True, blank=True)
    traveler = models.ForeignKey('wander.Traveler')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    start_location = JSONField(null=True, blank=True, default={})
    end_location = JSONField(null=True, blank=True, default={})
    rating = models.IntegerField(blank=True, null=True)
    facts = JSONField(null=True, blank=True, default={})
    status = models.CharField(max_length=12, default='waiting')

    def save(self, *args, **kwargs):
        """ On save, update timestamps"""
        if not self.id:  # On create
            self.start_time = datetime.datetime.now(tz=utc)
        return super(Trip, self).save(*args, **kwargs)


class Counter(models.Model):
    counter = models.IntegerField(blank=True, null=True, default=0)
    coordinates = JSONField(null=True, blank=True, default={})
