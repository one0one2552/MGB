#!/usr/bin/env python3
"""
Test: Pin-Zustand während und nach Initialisierung
"""
import RPi.GPIO as GPIO
import time

PIN = 27

print("=== PIN INITIALISIERUNGS-TEST ===\n")

# Test 1: Pin VOR jeder Initialisierung
print("TEST 1: Pin-Zustand VOR Setup")
print("-" * 40)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

try:
    # Pin als INPUT lesen (ohne Setup)
    GPIO.setup(PIN, GPIO.IN)
    state_before = GPIO.input(PIN)
    print(f"Pin {PIN} VOR Setup (als INPUT): {state_before} ({'HIGH' if state_before else 'LOW'})")
    GPIO.cleanup()
    time.sleep(1)
except Exception as e:
    print(f"Fehler: {e}")

input("\n>>> Ist Relay AN oder AUS? Drücke ENTER...\n")

# Test 2: Setup als OUTPUT OHNE initial Parameter
print("TEST 2: Setup als OUTPUT (OHNE initial)")
print("-" * 40)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

print("Cleanup...")
try:
    GPIO.cleanup(PIN)
except:
    pass
time.sleep(0.5)

print("Setup Pin als OUTPUT (kein initial Parameter)...")
GPIO.setup(PIN, GPIO.OUT)  # KEIN initial!
time.sleep(0.5)

state = GPIO.input(PIN)
print(f"Pin {PIN} nach Setup: {state} ({'HIGH' if state else 'LOW'})")

input("\n>>> Ist Relay AN oder AUS? Drücke ENTER...\n")

# Test 3: Explizit LOW setzen
print("TEST 3: Explizit GPIO.output(LOW)")
print("-" * 40)
GPIO.output(PIN, GPIO.LOW)
time.sleep(0.5)
state = GPIO.input(PIN)
print(f"Pin {PIN} nach output(LOW): {state} ({'HIGH' if state else 'LOW'}")

input("\n>>> Ist Relay AN oder AUS? Drücke ENTER...\n")

# Test 4: Explizit HIGH setzen
print("TEST 4: Explizit GPIO.output(HIGH)")
print("-" * 40)
GPIO.output(PIN, GPIO.HIGH)
time.sleep(0.5)
state = GPIO.input(PIN)
print(f"Pin {PIN} nach output(HIGH): {state} ({'HIGH' if state else 'LOW'}")

input("\n>>> Ist Relay AN oder AUS? Drücke ENTER...\n")

# Test 5: Wieder LOW
print("TEST 5: Wieder GPIO.output(LOW)")
print("-" * 40)
GPIO.output(PIN, GPIO.LOW)
time.sleep(0.5)
state = GPIO.input(PIN)
print(f"Pin {PIN} nach output(LOW): {state} ({'HIGH' if state else 'LOW'}")

input("\n>>> Ist Relay AN oder AUS? Drücke ENTER zum Beenden...\n")

# Cleanup
GPIO.cleanup()
print("\n✓ Test beendet")
print("\nWICHTIG: Notiere dir bei welchem TEST das Relay ANZIEHT!")
