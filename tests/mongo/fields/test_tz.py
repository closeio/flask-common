from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

import pytz

from flask_common.mongo.fields import TimezoneField
from mongoengine import Document


class TimezoneFieldTestCase(unittest.TestCase):
    # TODO pytest-ify and test the field instance directly without persistence.

    def test_timezone_field(self):
        class Location(Document):
            timezone = TimezoneField()

        Location.drop_collection()

        location = Location()
        location.save()
        location = Location.objects.get(pk=location.pk)
        assert location.timezone == pytz.UTC
        location.timezone = 'America/Los_Angeles'
        location.save()
        location = Location.objects.get(pk=location.pk)
        assert location.timezone == pytz.timezone('America/Los_Angeles')
