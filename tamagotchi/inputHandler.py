import RPi.GPIO as GPIO
import smbus
import time
from pet import Stats, hunger, sleep, happiness

#channels for ADC module, if more sensors are added
class Sensors:
    channels=[
        10000100, #input channel a2
        10010100, #input channel a1
        10100100, #input channel a2
        10110100, #input channel a3
        11000100, #input channel a4
        11010100, #input channel a5
        11100100, #input channel a6
        11110100 #input channel a7
    ]

    def readChannel(address, channel):
        bus= smbus.SMBus(1)
        command=Sensors.channels[channel]
        if address==0x4B:
            if channel>0 and channel<7:
                try:
                    bus.write_byte(address, command)
                    time.sleep(0.1)
                    value = bus.read_byte(address)
                    return value
                except IOError:
                    print("I²C read/write error.")
                    return 0
            else:
                print("there is no such channel as "+ channel)
        else:
            print("address for i2c connection not found")
        #if address== insertDiffi2cAddress: <-- if u want to use multiple adc devices
    def daylight():
        brightness=Sensors.readChannel(0x4B,1)/255
        if 0<brightness<.5:
            dayTrue=False
        else:
            dayTrue=True
        return dayTrue
    @staticmethod
    def touch(pet):
        ifTouched= Sensors.readChannel(0x4B, 0)
        if ifTouched>0:
            pet.happinessChange("petting")
        else:
            pet.happinessChange("no petting")
    @staticmethod
    def hunger(pet):
        hungerPin=0; #add later
        hungerButton= Button(hungerPin, "down")
        if hungerButton.was_pressed():
            pet.hungerChange("eat")
            pet.sleepChange("eating")
        else:
            pet.hungerChange("no eat")
    @staticmethod
    def sleep(pet):
        sleepPin=0 #add later
        sleepButton= Button(sleepPin, "down")
        if sleepButton.was_pressed() and Sensors.daylight()==False:
            pet.sleepChange("sleep")
            pet.hungerChange("sleep")
        if sleepButton.was_pressed() and Sensors.daylight()==True:
            print("it must be night for her to sleep.")
        else:
            pet.sleepChange("no sleep")
class Button():
    def __init__(self, pin, pullState):
        self.pin = pin
        self._pressed_and_released = False
        self._pressed = False
        self._press_time = None  # store time when button was pressed
        self._hold_triggered = False

        if pullState == "down":
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        elif pullState == "up":
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        else:
            GPIO.setup(self.pin, GPIO.IN)

        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=self._on_press, bouncetime=50)
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self._on_release, bouncetime=50)

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
                self._hold_triggered = True  # only trigger once per hold
                return True
        return False
startPin=0 #add later
start_button = Button(startPin, "down")