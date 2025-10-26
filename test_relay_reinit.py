#!/usr/bin/env python3
"""
Relay Test - Vollständiger Re-Init bei jedem Schritt
"""
import RPi.GPIO as GPIO
import time

PIN = 27

def set_pin_state(state_name, state_value):
    """Setzt Pin-Zustand mit komplettem Re-Init"""
    print(f"\n{'='*50}")
    print(f"Setze Pin auf {state_name} ({state_value})")
    print('='*50)
    
    # Cleanup
    try:
        GPIO.cleanup()
    except:
        pass
    
    time.sleep(0.5)
    
    # Setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Pin mit initial state
    GPIO.setup(PIN, GPIO.OUT, initial=state_value)
    time.sleep(0.2)
    
    # Status prüfen
    actual = GPIO.input(PIN)
    print(f"→ Pin ist: {'HIGH (1)' if actual else 'LOW (0)'}")
    print(f"→ Relay Status? (bitte prüfen)")
    
    input(">>> ENTER für nächsten Schritt...")

def main():
    print("=== RELAY TEST - Vollständiger Re-Init ===\n")
    print(f"GPIO Pin: {PIN}\n")
    
    try:
        # Test 1: LOW
        set_pin_state("LOW", GPIO.LOW)
        
        # Test 2: HIGH
        set_pin_state("HIGH", GPIO.HIGH)
        
        # Test 3: LOW
        set_pin_state("LOW", GPIO.LOW)
        
        # Test 4: HIGH
        set_pin_state("HIGH", GPIO.HIGH)
        
        # Test 5: LOW
        set_pin_state("LOW", GPIO.LOW)
        
        print("\n" + "="*50)
        print("✓ Test abgeschlossen")
        print("="*50)
        
    except KeyboardInterrupt:
        print("\n✗ Test abgebrochen")
    except Exception as e:
        print(f"\n✗ Fehler: {e}")
    finally:
        GPIO.cleanup()
        print("\n✓ GPIO cleanup")

if __name__ == "__main__":
    main()
