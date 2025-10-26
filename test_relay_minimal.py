#!/usr/bin/env python3
"""
Minimal Relay Test - nur HIGH setzen
"""
import RPi.GPIO as GPIO
import time

PIN = 27  # Dein GPIO Pin

print("=== MINIMAL TEST ===")
print(f"Pin: GPIO {PIN}")
print()

# BCM Mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

print("1. Setup Pin als OUTPUT mit initial=HIGH...")
GPIO.setup(PIN, GPIO.OUT, initial=GPIO.HIGH)
print(f"   → Pin sollte HIGH sein = Relay AUS")
print()

# 10 Sekunden warten
for i in range(10, 0, -1):
    print(f"   Warte {i} Sekunden... (Relay sollte AUS bleiben)")
    time.sleep(1)

print()
print("✓ Test beendet - Relay sollte die ganze Zeit AUS gewesen sein")
print()

# Cleanup
GPIO.cleanup()
print("✓ GPIO cleanup")
