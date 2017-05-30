from blist import sortedset
from mongoengine.fields import ListField

from ..utils import isortedset


class SortedSetField(ListField):
    """Like a ListField but sorts and de-duplicates items in the list before
    writing to the database in order to ensure that a sorted list is always retrieved.

    key = key to sort by

    .. warning::
        There is a potential race condition when handling lists.  If you set /
        save the whole list then other processes trying to save the whole list
        as well could overwrite changes.  The safest way to append to a list is
        to perform a push operation.
    """

    _key = None
    set_class = sortedset

    def __init__(self, field, **kwargs):
        if 'key' in kwargs.keys():
            self._key = kwargs.pop('key')
        super(SortedSetField, self).__init__(field, **kwargs)

    def to_mongo(self, value):
        value = super(SortedSetField, self).to_mongo(value) or []
        if self._key is not None:
            return list(self.set_class(value, key=self._key)) or None
        else:
            return list(self.set_class(value)) or None


class ISortedSetField(SortedSetField):
    set_class = isortedset

    def __init__(self, field, **kwargs):
        kwargs['key'] = lambda s: s.lower()
        super(ISortedSetField, self).__init__(field, **kwargs)
