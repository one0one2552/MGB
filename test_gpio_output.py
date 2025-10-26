#!/usr/bin/env python3
"""
Relay Test - GPIO.output() vs Re-Setup
Testet ob GPIO.output() funktioniert oder ob Re-Setup nötig ist
"""
import RPi.GPIO as GPIO
import time

PIN = 27

print("=== RELAY TEST - GPIO.output() Test ===\n")
print(f"GPIO Pin: {PIN}\n")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Cleanup
try:
    GPIO.cleanup(PIN)
except:
    pass

time.sleep(0.5)

# Setup mit LOW (Relay sollte AUS sein bei HIGH-Level-Trigger)
print("1. Setup Pin mit initial=LOW")
GPIO.setup(PIN, GPIO.OUT, initial=GPIO.LOW)
time.sleep(0.5)
actual = GPIO.input(PIN)
print(f"   → Pin: {'HIGH' if actual else 'LOW'}")
print(f"   → Relay AUS? (sollte AUS sein)")
input("   >>> ENTER...\n")

# GPIO.output(HIGH) - Relay sollte ANZIEHEN
print("2. GPIO.output(HIGH) aufrufen")
GPIO.output(PIN, GPIO.HIGH)
time.sleep(0.5)
actual = GPIO.input(PIN)
print(f"   → Pin: {'HIGH' if actual else 'LOW'}")
print(f"   → Relay AN? (sollte ANZIEHEN)")
input("   >>> ENTER...\n")

# GPIO.output(LOW) - Relay sollte ABFALLEN
print("3. GPIO.output(LOW) aufrufen")
GPIO.output(PIN, GPIO.LOW)
time.sleep(0.5)
actual = GPIO.input(PIN)
print(f"   → Pin: {'HIGH' if actual else 'LOW'}")
print(f"   → Relay AUS? (sollte ABFALLEN)")
input("   >>> ENTER...\n")

# GPIO.output(HIGH) - Relay sollte ANZIEHEN
print("4. GPIO.output(HIGH) aufrufen")
GPIO.output(PIN, GPIO.HIGH)
time.sleep(0.5)
actual = GPIO.input(PIN)
print(f"   → Pin: {'HIGH' if actual else 'LOW'}")
print(f"   → Relay AN? (sollte ANZIEHEN)")
input("   >>> ENTER...\n")

# Warte 5 Sekunden mit HIGH
print("5. Warte 5 Sekunden (Pin bleibt HIGH)...")
for i in range(5, 0, -1):
    print(f"   {i}...")
    time.sleep(1)
actual = GPIO.input(PIN)
print(f"   → Pin: {'HIGH' if actual else 'LOW'}")
print(f"   → Relay noch AN?")
input("   >>> ENTER...\n")

# GPIO.output(LOW) - Relay sollte ABFALLEN
print("6. GPIO.output(LOW) aufrufen")
GPIO.output(PIN, GPIO.LOW)
time.sleep(0.5)
actual = GPIO.input(PIN)
print(f"   → Pin: {'HIGH' if actual else 'LOW'}")
print(f"   → Relay AUS? (sollte ABFALLEN)")
input("   >>> ENTER zum Beenden...\n")

# Cleanup
GPIO.cleanup()
print("\n✓ Test abgeschlossen")
