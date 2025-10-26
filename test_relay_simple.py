#!/usr/bin/env python3
"""
Einfacher Relay Test - exakt wie das funktionierende Inline-Script
"""

import sys
import time
sys.path.insert(0, 'src')

from actuators.relay_actuator import RelayActuator

print("=" * 60)
print("EINFACHER RELAY TEST")
print("=" * 60)

# Initialisierung mit leerer Config (wie im funktionierenden Script)
print("\n1. Initialisiere Relay...")
heater = RelayActuator('heater', 27, {})

print('   Initialisiert:', heater.is_available)
print('   Aktiv:', heater.is_active)
print('   Mock Mode:', heater.is_mock_mode())

# Warten
print("\n2. Warte 3 Sekunden...")
time.sleep(3)

# Einschalten
print("\n3. turn_on()...")
result = heater.turn_on()
print('   Erfolgreich:', result)
print('   Aktiv:', heater.is_active)
time.sleep(3)

# Ausschalten
print("\n4. turn_off()...")
result = heater.turn_off()
print('   Erfolgreich:', result)
print('   Aktiv:', heater.is_active)
time.sleep(3)

# Nochmal einschalten
print("\n5. Nochmal turn_on()...")
result = heater.turn_on()
print('   Erfolgreich:', result)
print('   Aktiv:', heater.is_active)
time.sleep(3)

# Cleanup
print("\n6. cleanup()...")
heater.cleanup()

print("\n" + "=" * 60)
print("TEST ABGESCHLOSSEN")
print("=" * 60)
