import RPi.GPIO as GPIO #for rp5 model b, rpi-lgpio library used
GPIO.setmode(GPIO.BCM)
import smbus2 as smbus
import time
import logging
from stats import Stats

class Button:
    def __init__(self, pin, pullState="none"):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)

        # Determine pull-up/down configuration
        if pullState == "down":
            pud = GPIO.PUD_DOWN
        elif pullState == "up":
            pud = GPIO.PUD_UP
        elif pullState == "none":
            pud = GPIO.PUD_OFF
        else:
            raise ValueError("Invalid pullState. Choose 'up', 'down', or 'none'.")

        # Setup the pin with pull config
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=pud)

        # Initialize button state
        self._pressed = False
        self._pressed_and_released = False
        self._press_time = None
        self._hold_triggered = False

        # Set up event detection for both press and release
        GPIO.remove_event_detect(self.pin)
        GPIO.add_event_detect(self.pin, GPIO.BOTH, bouncetime=200)
        GPIO.add_event_callback(self.pin, self._handle_edge)

    def _handle_edge(self, channel):
        if GPIO.input(self.pin):  # Rising edge (button pressed)
            self._on_press(channel)
        else:  # Falling edge (button released)
            self._on_release(channel)

    def _on_press(self, channel):
        self._pressed = True
        self._press_time = time.time()
        self._hold_triggered = False

    def _on_release(self, channel):
        if self._pressed:
            self._pressed_and_released = True
            self._pressed = False
        self._press_time = None
        self._hold_triggered = False

    def was_pressed(self):
        if self._pressed_and_released:
            self._pressed_and_released = False
            return True
        return False

    def is_held_for(self, seconds=15):
        if self._pressed and self._press_time is not None:
            held_time = time.time() - self._press_time
            if held_time >= seconds and not self._hold_triggered:
                self._hold_triggered = True
                return True
        return False

ADC_ADDRESS = 0X4B
TOUCH_THRESHOLD = 10
BRIGHTNESS_THRESHOLD = .5
class Sensors:
    channels=[
        10000100, #input channel a0
        10010100, #input channel a1
        10100100, #input channel a2
        10110100, #input channel a3
        11000100, #input channel a4
        11010100, #input channel a5
        11100100, #input channel a6
        11110100 #input channel a7
    ]

    def __init__(self, sleepButton, hungerButton):
        self.sleepButton = sleepButton
        self.hungerButton=hungerButton
        
    @staticmethod
    def readChannel(address, channel):
        bus= smbus.SMBus(1)
        command=Sensors.channels[channel] #this assigns sensor to specified channel in method
        if address==ADC_ADDRESS:
            if channel>-1 and channel<7:
                try:
                    bus.write_byte(address, command)
                    time.sleep(0.1)
                    value = bus.read_byte(address)
                    return value
                except IOError:
                    logging.error("I²C read/write error with "+ str(channel))
                    return 0
            else:
                logging.error("there is no such channel as "+ str(channel))
        else:
            logging.error("address for i2c connection not found")
        
    @staticmethod
    def daylight():
        brightness=(Sensors.readChannel(ADC_ADDRESS,1))/255
        if 0 < brightness < BRIGHTNESS_THRESHOLD:
            is_day=False
        else:
            is_day=True
        return is_day
    
    @staticmethod
    def touch(pet):
        ifTouched= Sensors.readChannel(ADC_ADDRESS, 0)
        if ifTouched>TOUCH_THRESHOLD:
            pet.joyChange("petting")
        else:
            pet.joyChange("no petting")

    def hunger(self,pet):
        if self.hungerButton.was_pressed():
            pet.hungerChange("eat")
            pet.sleepChange("eating")
        else:
            pet.hungerChange("no eat")

    def sleep(self,pet):
        if self.sleepButton.was_pressed():
            if not Sensors.daylight():
                pet.sleepChange("sleep")
                pet.hungerChange("sleep")
            else:
                logging.info("It must be night for her to sleep.")
        else:
            pet.sleepChange("no sleep")
