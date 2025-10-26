import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT, initial=GPIO.LOW)  # Test mit LOW

time.sleep(5)
GPIO.output(27, GPIO.HIGH)  # Umschalten auf HIGH
time.sleep(5)

time.sleep(5)
GPIO.output(27, GPIO.LOW)  # Umschalten auf HIGH
time.sleep(5)

time.sleep(5)
GPIO.output(27, GPIO.HIGH)  # Umschalten auf HIGH
time.sleep(5)

GPIO.cleanup()