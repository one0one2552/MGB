#!/usr/bin/env python3
"""
Kalibrierungs-Tool für SCD30 Sensor
Hilft beim Setzen des Temperatur-Offsets
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from sensors.scd30_sensor import SCD30Sensor


def main():
    print("=" * 60)
    print("SCD30 Temperatur-Kalibrierung")
    print("=" * 60)
    print()
    
    # Sensor initialisieren
    config = {'enabled': True, 'measurement_interval': 2}
    sensor = SCD30Sensor(config)
    
    if not sensor._available:
        print("✗ Sensor nicht verfügbar!")
        return
    
    if sensor.is_mock_mode():
        print("⚠️  Mock-Modus aktiv - Kalibrierung nicht möglich")
        print("   Dieses Tool funktioniert nur mit echter Hardware auf dem Raspberry Pi")
        return
    
    print("Schritt 1: Aktuelle Temperatur messen")
    print("-" * 60)
    print()
    print("Warte 2 Minuten auf Stabilisierung...")
    print("(Der Sensor erwärmt sich durch den CO2-Sensor)")
    print()
    
    # Mehrere Messungen für Durchschnitt
    measurements = []
    for i in range(12):  # 12 Messungen á 10 Sekunden = 2 Minuten
        time.sleep(10)
        result = sensor.read_all()
        if result:
            temp = result['temperature']
            measurements.append(temp)
            print(f"Messung {i+1}/12: {temp:.2f}°C", end='\r', flush=True)
    
    print()
    print()
    
    if not measurements:
        print("✗ Keine Messungen erhalten!")
        return
    
    avg_temp = sum(measurements) / len(measurements)
    min_temp = min(measurements)
    max_temp = max(measurements)
    
    print("Ergebnisse der Stabilisierungsphase:")
    print(f"  Durchschnitt: {avg_temp:.2f}°C")
    print(f"  Minimum:      {min_temp:.2f}°C")
    print(f"  Maximum:      {max_temp:.2f}°C")
    print(f"  Schwankung:   ±{(max_temp - min_temp) / 2:.2f}°C")
    print()
    
    print("Schritt 2: Referenztemperatur eingeben")
    print("-" * 60)
    print()
    print("Messe jetzt die Temperatur mit einem kalibrierten Thermometer")
    print("in der Nähe des SCD30 (ca. 10-20cm Abstand).")
    print()
    print("⚠️  WICHTIG:")
    print("   - Nicht zu nah am SCD30 messen (Eigenerwärmung!)")
    print("   - Nicht zu nah an Heizung oder Lüftung")
    print("   - Warte bis das Thermometer stabil ist")
    print()
    
    try:
        ref_temp = float(input("Referenztemperatur (°C): "))
    except ValueError:
        print("✗ Ungültige Eingabe!")
        return
    
    # Offset berechnen
    offset = avg_temp - ref_temp
    
    print()
    print("=" * 60)
    print("Berechneter Offset:")
    print("=" * 60)
    print(f"  Sensor zeigt:  {avg_temp:.2f}°C")
    print(f"  Referenz:      {ref_temp:.2f}°C")
    print(f"  Offset:        {offset:.2f}°C")
    print("=" * 60)
    print()
    
    if abs(offset) < 0.5:
        print("✓ Sensor ist bereits gut kalibriert!")
        print("  Kein Offset notwendig.")
        return
    
    if abs(offset) > 10:
        print(f"⚠️  WARNUNG: Offset sehr groß ({offset:.2f}°C)!")
        print("  Bitte Sensormessung und Referenz überprüfen.")
        print("  Typischer Offset: 2-4°C")
        print()
        confirm = input("Trotzdem fortfahren? (j/N): ")
        if confirm.lower() != 'j':
            return
    
    print()
    confirm = input(f"Offset {offset:.2f}°C setzen? (j/N): ")
    
    if confirm.lower() == 'j':
        sensor.set_temperature_offset(offset)
        print()
        print("✓ Offset gesetzt!")
        print()
        print("Warte 30 Sekunden und teste neue Werte...")
        time.sleep(30)
        
        # Test mit neuem Offset
        result = sensor.read_all()
        if result:
            new_temp = result['temperature']
            print()
            print("Neue Messung mit Offset:")
            print(f"  Temperatur: {new_temp:.2f}°C")
            print(f"  Differenz zur Referenz: {abs(new_temp - ref_temp):.2f}°C")
            print()
            
            if abs(new_temp - ref_temp) < 1.0:
                print("✓ Kalibrierung erfolgreich!")
            else:
                print("⚠️  Kalibrierung könnte noch verbessert werden.")
                print("   Wiederhole den Vorgang bei Bedarf.")
        
        print()
        print("=" * 60)
        print("WICHTIG: Offset im Code speichern!")
        print("=" * 60)
        print()
        print("Der Offset geht beim Neustart verloren!")
        print("Füge folgende Zeile in die Sensor-Konfiguration ein:")
        print()
        print(f"    'temperature_offset': {offset:.2f}")
        print()
        print("In config/config.yaml unter sensors.co2:")
        print()
        print("  co2:")
        print("    enabled: true")
        print(f"    temperature_offset: {offset:.2f}")
        print("    ...")
        print()
    else:
        print("Kalibrierung abgebrochen.")
    
    print()
    print("=" * 60)


if __name__ == '__main__':
    main()
