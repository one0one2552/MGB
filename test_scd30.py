#!/usr/bin/env python3
"""
Test-Script für SCD30 Sensor
Testet die Grundfunktionalität des SCD30 und zeigt Live-Werte an
"""

import sys
import time
from pathlib import Path

# Pfad zum src-Verzeichnis hinzufügen
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from sensors.scd30_sensor import SCD30Sensor


def test_scd30():
    """
    Testet den SCD30 Sensor und zeigt Live-Werte an
    """
    print("=" * 60)
    print("SCD30 Sensor Test")
    print("=" * 60)
    print()
    
    # Sensor initialisieren
    print("Initialisiere SCD30 Sensor...")
    sensor = SCD30Sensor()
    
    if not sensor.is_available:
        print("✗ FEHLER: SCD30 Sensor nicht verfügbar!")
        print()
        print("Mögliche Ursachen:")
        print("- I2C nicht aktiviert (sudo raspi-config)")
        print("- Sensor nicht korrekt angeschlossen")
        print("- Bibliotheken nicht installiert")
        print()
        print("Auf dem Raspberry Pi ausführen:")
        print("  sudo i2cdetect -y 1")
        print()
        return False
    
    print("✓ SCD30 Sensor initialisiert!")
    print()
    
    if sensor.mock_mode:
        print("⚠️  MOCK-MODUS aktiv (nur für Entwicklung)")
        print("   Auf dem Raspberry Pi werden echte Werte angezeigt.")
        print()
    
    # Status anzeigen
    status = sensor.get_status()
    print("Sensor-Status:")
    print(f"  - Sensor: {status['sensor']}")
    print(f"  - Verfügbar: {status['available']}")
    print(f"  - Mock-Modus: {status['mock_mode']}")
    print()
    
    # Aufwärmzeit
    print("Warte auf Aufwärmphase (2 Sekunden)...")
    time.sleep(2)
    print()
    
    # Live-Messungen
    print("Live-Messungen (Strg+C zum Beenden):")
    print("-" * 60)
    
    try:
        measurement_count = 0
        while True:
            result = sensor.read_all()
            
            if result:
                temperature, humidity, co2 = result
                measurement_count += 1
                
                # Statuszeile anzeigen
                print(f"\rMessung #{measurement_count:04d} | "
                      f"Temp: {temperature:5.1f}°C | "
                      f"Humid: {humidity:5.1f}% | "
                      f"CO2: {co2:6.0f} ppm", end='', flush=True)
                
                # Bewertung der CO2-Werte
                if measurement_count % 10 == 0:
                    print()  # Neue Zeile alle 10 Messungen
                    if co2 < 800:
                        print("   → CO2-Wert: Ausgezeichnet ✓")
                    elif co2 < 1000:
                        print("   → CO2-Wert: Gut")
                    elif co2 < 1500:
                        print("   → CO2-Wert: Mäßig (Lüftung empfohlen)")
                    else:
                        print("   → CO2-Wert: Hoch! (Lüftung notwendig)")
                    print()
            else:
                print("\r✗ Fehler beim Lesen des Sensors", end='', flush=True)
            
            # Wartezeit zwischen Messungen
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n")
        print("-" * 60)
        print(f"Test beendet nach {measurement_count} Messungen")
        print()
        
        # Finale Statistik
        if sensor.last_temperature is not None:
            print("Letzte Messwerte:")
            print(f"  Temperatur:       {sensor.last_temperature}°C")
            print(f"  Luftfeuchtigkeit: {sensor.last_humidity}%")
            print(f"  CO2:              {sensor.last_co2} ppm")
        
        return True


def test_calibration():
    """
    Testet die Kalibrierungsfunktionen (optional)
    """
    print()
    print("=" * 60)
    print("Kalibrierungs-Test (optional)")
    print("=" * 60)
    print()
    print("⚠️  WARNUNG: Kalibrierung sollte nur durchgeführt werden,")
    print("   wenn der aktuelle CO2-Wert bekannt ist!")
    print()
    
    response = input("Möchtest du die Kalibrierungsfunktionen testen? (j/N): ")
    
    if response.lower() != 'j':
        print("Überspringe Kalibrierungs-Test")
        return
    
    sensor = SCD30Sensor()
    
    if not sensor.is_available or sensor.mock_mode:
        print("Kalibrierung nur mit echtem Sensor möglich!")
        return
    
    print()
    print("Verfügbare Kalibrierungsoptionen:")
    print("1. Temperatur-Offset setzen")
    print("2. Höhenkompensation setzen")
    print("3. Frischluft-Kalibrierung (400 ppm)")
    print()
    
    choice = input("Wähle eine Option (1-3) oder Enter zum Überspringen: ")
    
    if choice == '1':
        offset = float(input("Temperatur-Offset in °C (empfohlen: 2-4): "))
        sensor.set_temperature_offset(offset)
        
    elif choice == '2':
        altitude = int(input("Höhe über Meeresspiegel in Metern: "))
        sensor.set_altitude_compensation(altitude)
        
    elif choice == '3':
        print()
        print("⚠️  Stelle sicher, dass der Sensor mindestens 5 Minuten")
        print("   in frischer Außenluft steht (ca. 400 ppm CO2)!")
        confirm = input("Fortfahren? (j/N): ")
        if confirm.lower() == 'j':
            sensor.calibrate_forced_recalibration(400)


if __name__ == '__main__':
    print()
    success = test_scd30()
    
    if success:
        test_calibration()
    
    print()
    print("=" * 60)
    print("Test abgeschlossen!")
    print("=" * 60)
    print()
