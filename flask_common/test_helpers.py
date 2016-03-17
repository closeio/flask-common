from freezegun import freeze_time

# Inspired by http://stackoverflow.com/a/13875412
class ContextMixin(object):
    def __init__(self, *args, **kwargs):
        super(ContextMixin, self).__init__(*args, **kwargs)

        # List of open contexts
        self._ctxs = []

        # In case setup fails, we still want to tear down any open contexts
        self.addCleanup(self.teardown_context)

    def setUp(self):
        super(ContextMixin, self).setUp()
        self.setup_context()

    def tearDown(self):
        self.teardown_context()
        super(ContextMixin, self).tearDown()

    def setup_context(self):
        ctxs = []
        for cls in reversed(self.__class__.mro()):
            context_method = cls.__dict__.get('context')
            if context_method:
                ctxs.append(context_method(self))
        for ctx in ctxs:
            next(ctx)
            self._ctxs.append(ctx)

    def teardown_context(self):
        for ctx in reversed(self._ctxs):
            # Safe to run multiple times -- we will only execute the code after
            # the context's yield statement once.
            for _ in ctx:
                raise RuntimeError('{}.context() must not yield more than once'.format(cls.__name__))


class FreezeTimeMixin():
    """
    Helper to use freeze_gun for unit tests.
    ----
    Use self.freeze(datetime.datetime())` to mock `datetime.datetime.now()` and `self.unfreeze()` to revert the mock.
    `freeze` can be called to replace a mock or to create a new one. There is no need to call `unfreeze` before calling
    `freeze a second time. `unfreeze` can be called safely even if `freeze` was never called.

    """
    frozen = False

    def freeze(self, d):
        if self.frozen:
            self.freezer.stop()
        self.freezer = freeze_time(d)
        self.freezer.start()
        self.frozen = True
        self.now = d

    def unfreeze(self):
        if self.frozen:
            self.now = None
            self.freezer.stop()
            self.frozen = False


