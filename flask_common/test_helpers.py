from freezegun import freeze_time

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


