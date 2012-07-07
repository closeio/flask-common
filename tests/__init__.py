import pytz
import unittest
from flask import Flask
from flask.ext.mongoengine import MongoEngine, ValidationError

from flask_common.fields import PhoneField, TimezoneField

app = Flask(__name__)

app.config.update(
    DEBUG = True,
    TESTING = True,
    MONGODB_HOST = 'localhost',
    MONGODB_PORT = '27017',
    MONGODB_DB = 'common_example_app',
)

db = MongoEngine(app)

class Phone(db.Document):
    phone = PhoneField()

class Location(db.Document):
    timezone = TimezoneField()

class FieldTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        Phone.drop_collection()
        Location.drop_collection()

    def test_format_number(self):
        phone = Phone(phone='4151231234')
        assert phone.phone == '+14151231234'
        phone.validate()

        phone.phone = 'notaphone'
        assert phone.phone == 'notaphone'
        self.assertRaises(ValidationError, phone.validate)
        self.assertRaises(ValidationError, phone.save)

        phone.phone = '+1 (650) 618 - 1234 x 768'
        assert phone.phone == '+16506181234x768'
        phone.validate()

        phone.save()

        assert phone.id == Phone.objects.get(phone='6506181234x768').id
        assert phone.id == Phone.objects.get(phone='+1 650-618-1234 ext 768').id

    def test_timezone_field(self):
        location = Location() 
        location.save()
        location = Location.objects.get(id=location.id) 
        assert location.timezone == pytz.UTC
        location.timezone = 'America/Los_Angeles'
        location.save()
        location = Location.objects.get(id=location.id) 
        assert location.timezone == pytz.timezone('America/Los_Angeles')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()


