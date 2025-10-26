import RPi.GPIO as GPIO
import time

# GPIO-Modus (BCM)
GPIO.setmode(GPIO.BCM)

# GPIO 27 als Ausgang festlegen
GPIO.setup(27, GPIO.OUT)

try:
    while True:
        GPIO.output(27, GPIO.HIGH)  # Einschalten
        time.sleep(1)               # 1 Sekunde warten
        GPIO.output(27, GPIO.LOW)   # Ausschalten
        time.sleep(1)               # 1 Sekunde warten
except KeyboardInterrupt:
    print("Beende das Programm…")
finally:
    GPIO.cleanup()  # GPIO-Zustand zurücksetzen
