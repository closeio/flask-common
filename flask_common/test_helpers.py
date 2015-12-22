from freezegun import freeze_time

class FreezeTimeMixin():
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


