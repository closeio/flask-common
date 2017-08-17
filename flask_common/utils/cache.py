from .objects import freeze

from weakref import WeakValueDictionary


class WeakValueCache(WeakValueDictionary):
    """This is a local in-process cache that holds
    an object for as long as there's a live reference to it.

    Subclass and implement lookup method, then use indexing
    cache[key] to retrieve values.
    """

    def __contains__(self, key):
        return WeakValueDictionary.__contains__(self, freeze(key))

    def __setitem__(self, key, value):
        WeakValueDictionary.__setitem__(self, freeze(key), value)

    def __getitem__(self, key):
        frozen_key = freeze(key)
        if frozen_key in self:
            return WeakValueDictionary.__getitem__(self, frozen_key)
        value = self.lookup(key)
        self[frozen_key] = value
        return value

    def lookup(self, key):
        raise NotImplementedError("Implement lookup for the actual item")
