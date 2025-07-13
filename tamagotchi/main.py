from display import Display
from inputHandler import Sensors, Button
from pet import Appearance
from stats import Stats

import RPi.GPIO as GPIO
import time
import os
import sys
import logging

GPIO.setmode(GPIO.BCM)

REBOOT_HOLD_TIME = 15

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
hungerButton = Button(21, "down")
sleepButton = Button(20, "down")
startButton = Button(16, "down")

def main():
    screen.screenChange("starting")
    time.sleep(2)

    # Idle loop for detecting long press reboot
    while True:
        try:
            sensors = Sensors(sleepButton, hungerButton)
            face = Appearance(pet, screen, sleepButton)
            screen.screenChange("joy")  # example state
            while True:
                screen.display_stats(pet.hunger, pet.sleep, pet.joy)
                sensors.touch(pet)
                sensors.hunger(pet)
                sensors.sleep(pet)
                face.changeFace()
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("Program stopped by user.")
        finally:
            GPIO.cleanup()
            
        if startButton.is_held_for(REBOOT_HOLD_TIME):
            reboot_program()
        time.sleep(0.1)

if __name__ == "__main__":
    main()