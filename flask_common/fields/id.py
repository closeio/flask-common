import uuid

from mongoengine import UUIDField

from ..utils.id import id_to_uuid, uuid_to_id


try:
    string_types = (basestring,) # Python 2
except NameError:
    string_types = (str,) # Python 3


class IDField(UUIDField):
    """
    MongoEngine field type representing a zbase62-encoded ID, stored as a UUID.

    IDs are prefixed with the prefix (given to the constructor), followed by an
    underscore, followed by the zbase62-encoded ID.
    """
    def __init__(self, **kwargs):
        self.prefix = kwargs.pop('prefix')
        if 'default' not in kwargs:
            kwargs['default'] = self.generate_id
        super(IDField, self).__init__(**kwargs)

    def generate_id(self):
        return uuid_to_id(uuid.uuid4(), self.prefix)

    def to_python(self, value):
        if isinstance(value, uuid.UUID):
            return uuid_to_id(value, self.prefix)
        else:
            return value

    def to_mongo(self, value):
        if isinstance(value, string_types):
            value = id_to_uuid(value)
        return super(IDField, self).to_mongo(value)

    def prepare_query_value(self, op, value):
        if isinstance(value, string_types):
            try:
                value = id_to_uuid(value)
            except ValueError:
                value = None
        return super(IDField, self).prepare_query_value(op, value)

    def validate(self, value):
        try:
            id_to_uuid(value)
        except Exception as exc:
            self.error('Could not convert to UUID: %s' % exc)
