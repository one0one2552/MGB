#!/usr/bin/env python3
"""
Relay Diagnose - prüft Pin-Zustand VOR jeder Aktion
"""
import RPi.GPIO as GPIO
import time

PIN = 27

print("=== RELAY DIAGNOSE ===\n")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# WICHTIG: Zuerst als INPUT lesen um zu sehen was der aktuelle Zustand ist
print("SCHRITT 1: Pin-Zustand OHNE Setup prüfen")
try:
    GPIO.setup(PIN, GPIO.IN)
    current = GPIO.input(PIN)
    print(f"   → Pin {PIN} ist aktuell: {'HIGH (1)' if current else 'LOW (0)'}")
    print(f"   → Relay Status: {'AUS' if current else 'AN (Relay zieht!)'}")
    GPIO.cleanup(PIN)
    time.sleep(0.5)
except Exception as e:
    print(f"   → Fehler beim Lesen: {e}")

input("\n>>> Drücke ENTER für nächsten Schritt...\n")

# Jetzt als OUTPUT mit HIGH
print("SCHRITT 2: Setup als OUTPUT mit initial=HIGH")
GPIO.setup(PIN, GPIO.OUT, initial=GPIO.HIGH)
actual = GPIO.input(PIN)
print(f"   → Pin nach Setup: {'HIGH (1)' if actual else 'LOW (0)'}")
print(f"   → Ist das Relay jetzt AUS? (sollte AUS sein)")

input("\n>>> Drücke ENTER für nächsten Schritt...\n")

# Explizit HIGH schreiben
print("SCHRITT 3: Explizit GPIO.output(HIGH) aufrufen")
GPIO.output(PIN, GPIO.HIGH)
actual = GPIO.input(PIN)
print(f"   → Pin nach output(HIGH): {'HIGH (1)' if actual else 'LOW (0)'}")
print(f"   → Ist das Relay AUS? (sollte AUS sein)")

input("\n>>> Drücke ENTER für nächsten Schritt...\n")

# LOW schreiben (Relay sollte anziehen)
print("SCHRITT 4: GPIO.output(LOW) - Relay sollte ANZIEHEN")
GPIO.output(PIN, GPIO.LOW)
actual = GPIO.input(PIN)
print(f"   → Pin nach output(LOW): {'HIGH (1)' if actual else 'LOW (0)'}")
print(f"   → Zieht das Relay jetzt AN? (sollte AN sein)")

input("\n>>> Drücke ENTER für nächsten Schritt...\n")

# Wieder HIGH (Relay sollte abfallen)
print("SCHRITT 5: GPIO.output(HIGH) - Relay sollte ABFALLEN")
GPIO.output(PIN, GPIO.HIGH)
actual = GPIO.input(PIN)
print(f"   → Pin nach output(HIGH): {'HIGH (1)' if actual else 'LOW (0)'}")
print(f"   → Ist das Relay wieder AUS? (sollte AUS sein)")

input("\n>>> Drücke ENTER zum Beenden...\n")

# Cleanup
GPIO.cleanup()
print("✓ GPIO cleanup durchgeführt\n")
