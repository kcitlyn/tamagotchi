import time
from display import Display
from inputHandler import Sensors, Button, start_button
from pet import Stats, Appearance
import RPi.GPIO as GPIO
import os
import sys

GPIO.setmode(GPIO.BCM)
def main():
    pet = Stats()
    screen = Display()
    face = Appearance(pet, screen)
    
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
                print("Program stopped by user.")
                GPIO.cleanup()
                break  # optional: to exit the outer loop as well
        if Button.is_held_for(15):
            reboot_program()
        time.sleep(0.1)  # to avoid busy waiting

def reboot_program():
    print("Rebooting program...")
    GPIO.cleanup()  # clean up before reboot
    print("Rebooting program...")
    python = sys.executable
    os.execl(python, python, *sys.argv)

if __name__ == "__main__":
    main()