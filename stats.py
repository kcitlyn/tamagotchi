MIN_STAT = 0
MAX_STAT = 10

class Stats:
    def __init__(self):
        self._joy = 5
        self._hunger = 5
        self._sleep = 5

    @property
    def joy(self):
        return self._joy

    @joy.setter
    def joy(self, value):
        self._joy = max(MIN_STAT, min(MAX_STAT, value))

    @property
    def hunger(self):
        return self._hunger

    @hunger.setter
    def hunger(self, value):
        self._hunger = max(MIN_STAT, min(MAX_STAT, value))

    @property
    def sleep(self):
        return self._sleep

    @sleep.setter
    def sleep(self, value):
        self._sleep = max(MIN_STAT, min(MAX_STAT, value))

    def joy_change(self, reason):
        if reason == "petting":
            self.joy += 1
        elif reason == "no petting":
            self.joy -= 0.2

    def hunger_change(self, reason):
        if reason == "eat":
            self.hunger += 1
        elif reason == "no eat":
            self.hunger -= 0.2
        elif reason == "sleep":
            self.hunger -= 0.5

    def sleep_change(self, reason, state=None):  # kept your parameter for compatibility
        if reason == "eating":
            self.sleep -= 0.5
        elif reason == "sleep":
            self.sleep += 1
        elif reason == "no sleep":
            self.sleep -= 0.1
