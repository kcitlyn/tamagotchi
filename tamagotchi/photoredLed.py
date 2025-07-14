import RPi.GPIO as GPIO
import time
import smbus

#sets up i2c connection 
bus = smbus.SMBus(1)

ADCIdentity= 0x4B

#u can also write out the other channels/ A1-7 if you have multiple sensors, but since we are only
# using one sensor we dont need more than this below
CHANNELS=[
    0x84,
    0xC4,
]

def read_channel(channel):
    if channel <0 or channel > 7:
        raise ValueError("channel must be between 0-7")
    command=CHANNELS[channel]
    bus.write_byte(ADCIdentity, command)
    time.sleep(0.01)
    value= bus.read_byte(ADCIdentity)
    return value

ledPin=19
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT)
pwm=GPIO.PWM(ledPin, 1000)
pwm.start(0)

try:
    while True:
        rawVal=read_channel(1)
        brightness= rawVal/255
        pwm.ChangeDutyCycle(brightness*100)
        print(f"Brightness: {rawVal}, LED brightness: {brightness:.2f}")
        time.sleep(0.1)

except KeyboardInterrupt:
    pass

finally:
    pwm.stop()
    GPIO.cleanup()
