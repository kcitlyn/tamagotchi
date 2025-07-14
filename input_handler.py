import RPi.GPIO as GPIO #for rp5 model b, rpi-lgpio library used
import smbus2 as smbus
import time
import logging
from stats import Stats

bus = smbus.SMBus(1)

class Button:
    def __init__(self, pin, pullState="none", press_callback=None):
        self.pin = pin
        self.press_callback = press_callback

        if pullState == "down":
            pud = GPIO.PUD_DOWN
        elif pullState == "up":
            pud = GPIO.PUD_UP
        elif pullState == "none":
            pud = GPIO.PUD_OFF
        else:
            logging.error("Invalid pullState. Choose 'up', 'down', or 'none'.")

        GPIO.setup(self.pin, GPIO.IN, pull_up_down=pud)

        self._pressed = False
        self._pressed_and_released = False
        self._press_time = None
        self._hold_triggered = False

        GPIO.remove_event_detect(self.pin)
        GPIO.add_event_detect(self.pin, GPIO.BOTH, bouncetime=75)
        GPIO.add_event_callback(self.pin, self._handle_edge)

    def _handle_edge(self, channel):
        if GPIO.input(self.pin):  # rising edge (press)
            self._on_press(channel)
        else:  # falling edge (release)
            self._on_release(channel)

    def _on_press(self, channel):
        self._pressed = True
        self._press_time = time.time()
        self._hold_triggered = False

        if self.press_callback:
            self.press_callback()

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
TOUCH_THRESHOLD = 60
BRIGHTNESS_THRESHOLD = .5

class Sensors:
    channels = [
    0x84,  # channel 0
    0xC4,  # channel 1
    0x94,  # channel 2
    0xD4,  # channel 3
    0xA4,  # channel 4
    0xE4,  # channel 5
    0xB4,  # channel 6
    0xF4   # channel 7
]

    def __init__(self, sleep_button, hunger_button):
        self.sleep_button = sleep_button
        self.hunger_button=hunger_button
        
    @staticmethod
    def read_channel(address, channel):
        command=Sensors.channels[channel] #this assigns sensor to specified channel in method
        if address==ADC_ADDRESS:
            if channel>-1 and channel<7: #there are only 8 channels on ADC module (ADS7830)
                try:
                    bus.write_byte(address, command)
                    time.sleep(0.1)
                    value = bus.read_byte(address)
                    return value
                except IOError:
                    logging.error("I2C read/write error with "+ str(channel))
                    return 0
            else:
                logging.error("there is no such channel as "+ str(channel))
        else:
            logging.error("address for i2c connection not found")
    @staticmethod
    def daylight():
        brightness=(Sensors.read_channel(ADC_ADDRESS,1))/255
        print(brightness)
        if 0 < brightness < BRIGHTNESS_THRESHOLD:
            is_day=False
        else:
            is_day=True
        return is_day
    
    @staticmethod
    def touch(pet):
        _if_touched= Sensors.read_channel(ADC_ADDRESS, 0)
        if _if_touched>TOUCH_THRESHOLD:
            pet.joy_change("petting")
        else:
            pet.joy_change("no petting")

    def hunger(self,pet):
        if self.hunger_button.was_pressed():
            pet.hunger_change("eat")
            pet.sleep_change("eating")
        else:
            pet.hunger_change("no eat")

    def sleep(self,pet):
        if self.sleep_button.was_pressed():
            if not Sensors.daylight():
                pet.sleep_change("sleep")
                pet.hunger_change("sleep")
            else:
                logging.info("It must be night for her to sleep.")
        else:
            pet.sleep_change("no sleep")
