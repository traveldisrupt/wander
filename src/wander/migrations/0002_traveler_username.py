# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-11 05:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wander', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='traveler',
            name='username',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]