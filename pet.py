from display import Display
from tamagotchi.input_handler import Sensors
import logging

#max/min stats the pets stat can reach no matter input
MAX_STAT=10 
MIN_STAT=0

class Appearance:
    def __init__(self, stats, display, sleep_button):
        self.pet = stats
        self.display = display
        self.sleep_button= sleep_button

    def changeFace(self):
        sleep_button=self.sleep_button
        if self.pet.hunger == 0 or self.pet.joy==0 or self.pet.sleep==0: #if any of these stats are zero, the pet is dead.
            self.pet.hunger = 0
            self.pet.joy = 0
            self.pet.sleep = 0
            self.display.screen_change("dead")
        elif self.pet.hunger>7 and self.pet.joy>7 and self.pet.sleep>7: #if all stats are above 7, the pet is happy
            self.display.screen_change("joy")
        elif self.pet.hunger<4 or self.pet.joy<4 or self.pet.sleep<4: #if the stats are below 4, the pet becomes angry
            self.display.screen_change("angry")
        elif self.sleep_button.was_pressed() and not Sensors.daylight(): #the pet can only sleep at nighttime.
            self.display.screen_change("sleep")
        else:
            self.display.screen_change("neutral")
    
