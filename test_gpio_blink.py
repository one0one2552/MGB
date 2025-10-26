#!/usr/bin/env python3
"""
GPIO Output Test - Testet ob GPIO.output() funktioniert
Blink-Test für Pin 27
"""
import RPi.GPIO as GPIO
import time

PIN = 27

print("=== GPIO BLINK TEST ===\n")
print(f"GPIO Pin: {PIN}")
print("Dieser Test lässt den Pin 10x blinken (HIGH/LOW wechseln)")
print("Wenn du ein Multimeter hast, miss die Spannung am Pin")
print("Oder schließe eine LED an (mit Vorwiderstand 220-330 Ohm!)\n")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Cleanup
try:
    GPIO.cleanup(PIN)
except:
    pass

time.sleep(0.5)

# Setup mit LOW
print("Setup Pin als OUTPUT mit initial=LOW...\n")
GPIO.setup(PIN, GPIO.OUT, initial=GPIO.LOW)
time.sleep(1)

# 10x blinken
for i in range(1, 11):
    print(f"Blink {i}/10: HIGH")
    GPIO.output(PIN, GPIO.HIGH)
    actual = GPIO.input(PIN)
    print(f"  → Pin liest: {'HIGH' if actual else 'LOW'}")
    time.sleep(1)
    
    print(f"Blink {i}/10: LOW")
    GPIO.output(PIN, GPIO.LOW)
    actual = GPIO.input(PIN)
    print(f"  → Pin liest: {'LOW' if actual == 0 else 'HIGH'}")
    time.sleep(1)
    print()

# Cleanup
GPIO.output(PIN, GPIO.LOW)
GPIO.cleanup()
print("✓ Test abgeschlossen")
print("\nWenn der Pin-Wert sich ändert (HIGH/LOW wechselt),")
print("dann funktioniert GPIO.output() und das Problem ist dein Relay-Modul!")
