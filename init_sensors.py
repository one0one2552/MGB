import time

import RPi.GPIO as GPIO

# Use BCM pin numbering
GPIO.setmode(GPIO.BCM)

# Set up GPIO pin 18 as an output
GPIO.setup(18, GPIO.OUT)

try:
    while True:
        GPIO.output(18, GPIO.HIGH)  # Turn on
        time.sleep(1)
        GPIO.output(18, GPIO.LOW)   # Turn off
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()