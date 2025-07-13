from display import Display
from inputHandler import sleepButton, Button, Sensors
import logging

MAX_STAT=10
MIN_STAT=0
class Stats:
    def __init__(self):
        self.joy = 5
        self.hunger =5
        self.sleep =5
    def joyChange(self, reason):
        if self.joy>MIN_STAT and self.joy<MAX_STAT:
            if reason=="petting":
                self.joy+=1
            elif reason== "no petting":
                self.joy-=.2
            else:
                logging.error("The reason for joy change is undefined")
        else:
            logging.info("shes already so happy!")
    def hungerChange(self, reason):
        if self.hunger>MIN_STAT and self.hunger<MAX_STAT:
            if reason =="eat":
                self.hunger+=1
            if reason=="no eat":
                self.hunger-=.2
            if reason=="sleep":
                self.hunger-=.5
        else:
            logging.info("shes not hungry!")

    def sleepChange(self, reason):
        if self.sleep>MIN_STAT and self.sleep<MAX_STAT:
            if reason=="eating":
                self.sleep-=.5
            if reason=="sleep":
                self.sleep+=1
            if reason=="no sleep":
                self.sleep-=.1
        else:
            logging.info("she only sleeps at night")

class Appearance:
    def __init__(self, stats, display):
        self.pet = stats
        self.display = display

    def changeFace(self):
        if self.pet.hunger == 0 or self.pet.joy==0 or self.pet.sleep==0: #if any of these stats are zero, the pet is dead.
            self.display.screenChange("dead")
        elif self.pet.hunger>7 and self.pet.joy>7 and self.pet.sleep>7: #if all stats are above 7, the pet is happy
            self.display.screenChange("joy")
        elif self.pet.hunger<4 or self.pet.joy<4 or self.pet.sleep<4: #if the stats are below 4, the pet becomes angry
            self.display.screenChange("angry")
        elif sleepButton.was_pressed() and not Sensors.daylight(): #the pet can only sleep at nighttime.
            self.display.screenChange("sleep")
        else:
            self.display.screenChange("neutral")
    