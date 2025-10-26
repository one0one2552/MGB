#!/usr/bin/env python3
"""
Test-Script für Relay-Aktoren (Heizmatte, Pumpe)
"""

import sys
import time
from pathlib import Path

# Pfad für Imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from actuators.relay_actuator import RelayActuator


def test_relay():
    """Testet das Relay"""
    print("=" * 60)
    print("MGB - Relay Test")
    print("=" * 60)
    
    # Relay initialisieren (GPIO 27 für Heizmatte) - LEERE CONFIG!
    print("\nInitialisiere Relay auf GPIO Pin 27...")
    relay = RelayActuator(name='heater', pin=27, config={})
    
    print('Initialisiert:', relay.is_available)
    print('Aktiv:', relay.is_active)
    
    if not relay.is_available:
        print("✗ Relay nicht verfügbar!")
        return
    
    if relay.is_mock_mode():
        print("⚠ Relay läuft im Mock-Modus (keine echte Hardware)")
    else:
        print("✓ Relay bereit (Hardware-Modus)")
    
    try:
        # Test 1: Einschalten
        print("\n" + "=" * 60)
        print("Test 1: Relay einschalten")
        print("=" * 60)
        
        print("Warte 2 Sekunden...")
        time.sleep(2)
        
        print("turn_on()...")
        if relay.turn_on():
            print("✓ Relay eingeschaltet")
        else:
            print("✗ Fehler beim Einschalten")
        
        print("Warte 5 Sekunden...")
        time.sleep(5)
        
        # Test 2: Ausschalten
        print("\n" + "=" * 60)
        print("Test 2: Relay ausschalten")
        print("=" * 60)
        
        print("turn_off()...")
        if relay.turn_off():
            print("✓ Relay ausgeschaltet")
        else:
            print("✗ Fehler beim Ausschalten")
        
        print("Warte 3 Sekunden...")
        time.sleep(3)
        
        # Test 3: Nochmal einschalten
        print("\n" + "=" * 60)
        print("Test 3: Nochmal einschalten")
        print("=" * 60)
        
        print("turn_on()...")
        if relay.turn_on():
            print("✓ Relay eingeschaltet")
        else:
            print("✗ Fehler beim Einschalten")
        
        print("Warte 3 Sekunden...")
        time.sleep(3)
        
    except KeyboardInterrupt:
        print("\n\n⚠ Abbruch durch Benutzer")
    
    finally:
        # Cleanup
        print("\n" + "=" * 60)
        print("Cleanup")
        print("=" * 60)
        relay.cleanup()
        print("✓ Cleanup abgeschlossen")
        print("\nTest beendet!")


if __name__ == '__main__':
    test_relay()
