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
    
    # Konfiguration für Heizmatte
    config = {
        'inverted': True,  # LOW-Level-Trigger (Standard)
        'min_runtime': 5,  # Min 5 Sekunden laufen lassen
        'max_runtime': 30,  # Max 30 Sekunden für Test
        'cooldown': 10  # 10 Sekunden Pause zwischen Aktivierungen
    }
    
    # Relay initialisieren (GPIO 27 für Heizmatte)
    print("\nInitialisiere Relay auf GPIO Pin 27...")
    relay = RelayActuator(name='heater', pin=27, config=config)
    
    if not relay.is_available:
        print("✗ Relay nicht verfügbar!")
        return
    
    if relay.is_mock_mode():
        print("⚠ Relay läuft im Mock-Modus (keine echte Hardware)")
    else:
        print("✓ Relay bereit (Hardware-Modus)")
    
    print("\nStatus:", relay.get_status())
    
    try:
        # Test 1: Einschalten
        print("\n" + "=" * 60)
        print("Test 1: Relay einschalten")
        print("=" * 60)
        
        if relay.turn_on():
            print("✓ Relay eingeschaltet")
            print(f"  Laufzeit: {relay.get_runtime():.1f}s")
            
            # 10 Sekunden warten
            for i in range(10):
                time.sleep(1)
                print(f"  Laufzeit: {relay.get_runtime():.1f}s")
        else:
            print("✗ Fehler beim Einschalten")
        
        # Test 2: Ausschalten
        print("\n" + "=" * 60)
        print("Test 2: Relay ausschalten")
        print("=" * 60)
        
        if relay.turn_off():
            print("✓ Relay ausgeschaltet")
        else:
            print("✗ Fehler beim Ausschalten")
        
        # Test 3: Cooldown Test
        print("\n" + "=" * 60)
        print("Test 3: Cooldown-Test (sollte fehlschlagen)")
        print("=" * 60)
        
        print("Versuche sofort wieder einzuschalten...")
        if relay.turn_on():
            print("✓ Eingeschaltet (Cooldown umgangen?)")
        else:
            print("✓ Cooldown funktioniert - Einschalten blockiert")
        
        print(f"\nWarte {config['cooldown']} Sekunden für Cooldown...")
        time.sleep(config['cooldown'])
        
        # Test 4: Nach Cooldown
        print("\n" + "=" * 60)
        print("Test 4: Einschalten nach Cooldown")
        print("=" * 60)
        
        if relay.turn_on():
            print("✓ Relay eingeschaltet nach Cooldown")
            time.sleep(2)
        else:
            print("✗ Fehler beim Einschalten nach Cooldown")
        
    except KeyboardInterrupt:
        print("\n\n⚠ Abbruch durch Benutzer")
    
    finally:
        # Cleanup
        print("\n" + "=" * 60)
        print("Cleanup")
        print("=" * 60)
        relay.turn_off()
        relay.cleanup()
        print("✓ Relay ausgeschaltet und aufgeräumt")
        print("\nTest beendet!")


if __name__ == '__main__':
    test_relay()
