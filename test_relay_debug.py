#!/usr/bin/env python3
"""
Debug-Script für Relay - zeigt GPIO Pin Status an
"""
import RPi.GPIO as GPIO
import time
import sys

PIN = 27  # GPIO Pin

def main():
    print("=== Relay Debug Script ===\n")
    
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Pin als Input konfigurieren um aktuellen Zustand zu lesen
        GPIO.setup(PIN, GPIO.IN)
        current_state = GPIO.input(PIN)
        print(f"1. AKTUELLER ZUSTAND (vor Setup): Pin {PIN} = {'HIGH' if current_state else 'LOW'}")
        
        # Cleanup
        GPIO.cleanup(PIN)
        time.sleep(0.5)
        
        # Jetzt als Output konfigurieren
        GPIO.setup(PIN, GPIO.OUT)
        print(f"2. Pin {PIN} als OUTPUT konfiguriert")
        
        # HIGH setzen (sollte Relay AUSSCHALTEN bei LOW-Level-Trigger)
        print(f"\n3. Setze Pin {PIN} auf HIGH (Relay sollte AUS sein)")
        GPIO.output(PIN, GPIO.HIGH)
        time.sleep(1)
        actual = GPIO.input(PIN)
        print(f"   → Pin ist jetzt: {'HIGH' if actual else 'LOW'}")
        print(f"   → Relay Status? (sollte AUS sein - prüfe ob Relay-LED aus ist)")
        input("   → Drücke ENTER wenn du geprüft hast...")
        
        # LOW setzen (sollte Relay EINSCHALTEN bei LOW-Level-Trigger)
        print(f"\n4. Setze Pin {PIN} auf LOW (Relay sollte AN sein)")
        GPIO.output(PIN, GPIO.LOW)
        time.sleep(1)
        actual = GPIO.input(PIN)
        print(f"   → Pin ist jetzt: {'HIGH' if actual else 'LOW'}")
        print(f"   → Relay Status? (sollte AN sein - prüfe ob Relay-LED an ist)")
        input("   → Drücke ENTER wenn du geprüft hast...")
        
        # Wieder HIGH setzen
        print(f"\n5. Setze Pin {PIN} wieder auf HIGH (Relay sollte AUS sein)")
        GPIO.output(PIN, GPIO.HIGH)
        time.sleep(1)
        actual = GPIO.input(PIN)
        print(f"   → Pin ist jetzt: {'HIGH' if actual else 'LOW'}")
        print(f"   → Relay Status? (sollte AUS sein)")
        input("   → Drücke ENTER wenn du geprüft hast...")
        
        print("\n✓ Test abgeschlossen")
        
    except Exception as e:
        print(f"\n✗ Fehler: {e}")
        sys.exit(1)
    finally:
        # Cleanup - Pin auf HIGH lassen (AUS)
        try:
            GPIO.output(PIN, GPIO.HIGH)
            GPIO.cleanup()
            print("\n✓ GPIO cleanup durchgeführt")
        except:
            pass

if __name__ == "__main__":
    main()
