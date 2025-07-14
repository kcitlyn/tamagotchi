from display import Display
from tamagotchi.input_handler import Sensors, Button
from pet import Appearance
from stats import Stats

import RPi.GPIO as GPIO
import time
import os
import sys
import logging

GPIO.setmode(GPIO.BCM)

REBOOT_HOLD_TIME = 5

# These are global so callback can access them
pet = Stats()
screen = Display()
sensors = None  # We'll assign it after buttons
face = None

def reboot_program():
    logging.info("Rebooting program...")
    GPIO.cleanup()
    python = sys.executable
    os.execl(python, python, *sys.argv)

# Setup buttons with callbacks
hunger_button = Button(21, "down")
sleep_button = Button(20, "down")
start_button = Button(16, "down")

def main():
    screen.screen_change("starting")
    time.sleep(2)

    while True:
        try:
            sensors = Sensors(sleep_button, hunger_button)
            face = Appearance(pet, screen, sleep_button)
            screen.screen_change("joy")  # example state
            while True:
                #checks sensor data if user is interacting
                sensors.touch(pet)
                sensors.hunger(pet)
                sensors.sleep(pet)

                face.changeFace()

                if pet.hunger!=0 and pet.joy!=0 and pet.sleep!=0:
                    screen.display_stats(pet.hunger, pet.sleep, pet.joy) #constantly reupdates pet stats to lcd
        
                if start_button.is_held_for(REBOOT_HOLD_TIME): #if start button is held for reboot time, the game restarts
                    reboot_program()
                time.sleep(1)
    
        except KeyboardInterrupt:
            logging.info("Program stopped by user.")
        finally:
            GPIO.cleanup()

        time.sleep(0.1)

if __name__ == "__main__":
    main()
