import os
import datetime
from zbase62 import zbase62
from mongoengine import * 
from mongoengine.base import ValidationError
from mongoengine.queryset import OperationError


class RandomPKDocument(Document):
    id = StringField(unique=True, primary_key=True)

    def get_pk_prefix(self):
        return self._get_collection_name()[:4]

    def save(self, *args, **kwargs):
        old_id = self.id

        try:
            if not self.id:
                self.id = u'%s_%s' % (self.get_pk_prefix(), zbase62.b2a(os.urandom(32)))

                # Don't cascade saves by default.
                kwargs['cascade'] = kwargs.get('cascade', False)

                # Throw an exception if another object with this id already exists.
                kwargs['force_insert'] = True

                # But don't do that when cascading.
                kwargs['cascade_kwargs'] = { 'force_insert': False }

            return super(RandomPKDocument, self).save(*args, **kwargs)
        except OperationError, err:
            self.id = old_id

            # Use "startswith" instead of "in". Otherwise, if a free form
            # StringField had a unique constraint someone could inject that
            # string into the error message.
            if unicode(err).startswith(u'Tried to save duplicate unique keys (E11000 duplicate key error index: %s.%s.$_id_ ' % (self._get_db().name, self._get_collection_name())):
                self.save(*args, **kwargs)            
            else:
                raise

    meta = {
        'allow_inheritance': True,
        'abstract': True,
    }

class DocumentBase(Document):
    date_created = DateTimeField()
    date_updated = DateTimeField()

    def _type(self):
        return unicode(self.__class__.__name__)

    def save(self, *args, **kwargs):
        now = datetime.datetime.utcnow()
        if not self.date_created:
            self.date_created = now
        self.date_updated = now
        return super(DocumentBase, self).save(*args, **kwargs)

    meta = {
        'allow_inheritance': True,
        'abstract': True,
    }

