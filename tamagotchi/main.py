import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

import time
import os
import sys
import logging

from display import Display
from inputHandler import Sensors, Button
from pet import Appearance
import stats

hungerButton = Button(21, "down")
sleepButton = Button(20, "down")
startButton = Button(16, "none")

def main():
    pet = stats()
    screen = Display()
    face = Appearance(pet, screen)
    REBOOT_HOLD_TIME = 15  # seconds to hold button to reboot

    screen.screenChange("starting")
    time.sleep(2)

    while True:
        if Button.startButton.was_pressed() and screen.mode == "start":
            try:
                while True:
                    Sensors.touch(pet)
                    Sensors.hunger(pet)
                    Sensors.sleep(pet)

                    face.changeFace()
                    time.sleep(1)
            except KeyboardInterrupt:
                logging.info("Program stopped by user.")
            finally:
                GPIO.cleanup()
        if Button.is_held_for(REBOOT_HOLD_TIME):
            reboot_program()
        time.sleep(0.1)  # to avoid busy waiting

def reboot_program(): #reboots and restarts program from beginning
    logging.info("Rebooting program...")
    GPIO.cleanup()  # clean up before reboot
    python = sys.executable
    os.execl(python, python, *sys.argv)

if __name__ == "__main__":
    main()