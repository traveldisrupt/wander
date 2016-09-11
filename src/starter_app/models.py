from django.db import models

# # Create your models here.
# from rest_framework.fields import JSONField
#
#
# class Guide(models.Model):
#     status_online = models.BooleanField(default=False)
#     status_on_trip = models.BooleanField(default=False)
#
#
# class Traveler(models.Model):
#     name = models.CharField(max_length=30, blank=True, null=True)
#     age = models.IntegerField(max_length=3, blank=True, null=True)
#     occupation = models.CharField(max_length=100, blank=True, null=True)
#     interest = JSONField(null=True, blank=True, default={})
#     country = models.CharField(max_length=100, blank=True, null=True)
#     bio = models.TextField(blank=True, null=True)
#
#
# class Trip(models.Model):
#     traveler = models.ForeignKey('start_app.Traveler')
#     start_time = models.DateTimeField(null=True, blank=True)
#     end_time = models.DateTimeField(null=True, blank=True)
#     start_location = JSONField(null=True, blank=True, default={})
#     end_location = JSONField(null=True, blank=True, default={})
#     rating = models.IntegerField(max_length=2, blank=True, null=True)