import RPi.GPIO as GPIO
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

import time
import os
import sys
import logging

from display import Display
from inputHandler import Sensors, Button
from pet import Appearance
from stats import Stats

hungerButton = Button(21, "down")
sleepButton = Button(20, "down")
startButton = Button(16, "down")

def main():
    pet = Stats()
    screen = Display()
    face = Appearance(pet, screen, sleepButton)
    sensors = Sensors(sleepButton, hungerButton)
    REBOOT_HOLD_TIME = 15  # seconds to hold button to reboot
    screen.screenChange("starting")
    time.sleep(2)

    while True:
        if startButton.was_pressed() and screen.mode == "start":
            try:
                while True:
                    sensors.touch(pet)
                    sensors.hunger(pet)
                    sensors.sleep(pet)

                    face.changeFace()

                    # Update the stats display here with latest values
                    screen.display_stats(pet.hunger, pet.sleep, pet.joy)

                    time.sleep(1)
            except KeyboardInterrupt:
                logging.info("Program stopped by user.")
            finally:
                screen.lcd.clear()
                GPIO.cleanup()
        if startButton.is_held_for(REBOOT_HOLD_TIME):
            reboot_program()
        time.sleep(0.1)  # to avoid busy waiting

def reboot_program(): #reboots and restarts program from beginning
    logging.info("Rebooting program...")
    GPIO.cleanup()  # clean up before reboot
    python = sys.executable
    os.execl(python, python, *sys.argv)

if __name__ == "__main__":
    main()