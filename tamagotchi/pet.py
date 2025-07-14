from display import Display
from inputHandler import Sensors
import logging

MAX_STAT=10
MIN_STAT=0

class Appearance:
    def __init__(self, stats, display, sleepButton):
        self.pet = stats
        self.display = display
        self.sleepButton= sleepButton

    def changeFace(self):
        sleepButton=self.sleepButton
        if self.pet.hunger == 0 or self.pet.joy==0 or self.pet.sleep==0: #if any of these stats are zero, the pet is dead.
            self.pet.hunger = 0
            self.pet.joy = 0
            self.pet.sleep = 0
            self.display.screenChange("dead")
        elif self.pet.hunger>7 and self.pet.joy>7 and self.pet.sleep>7: #if all stats are above 7, the pet is happy
            self.display.screenChange("joy")
        elif self.pet.hunger<4 or self.pet.joy<4 or self.pet.sleep<4: #if the stats are below 4, the pet becomes angry
            self.display.screenChange("angry")
        elif self.sleepButton.was_pressed() and not Sensors.daylight(): #the pet can only sleep at nighttime.
            self.display.screenChange("sleep")
        else:
            self.display.screenChange("neutral")
    