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
    
    # Minimale Konfiguration
    config = {
        'enabled': True,
        'measurement_interval': 2
    }
    
    sensor = SCD30Sensor(config)
    
    if not sensor._available:
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
    
    print()
    
    if sensor.is_mock_mode():
        print("⚠️  MOCK-MODUS aktiv (nur für Entwicklung)")
        print("   Auf dem Raspberry Pi werden echte Werte angezeigt.")
        print()
    else:
        print("✓ Hardware-Modus aktiv - echte Sensor-Werte!")
        print()
    
    # Sensor-Info anzeigen
    info = sensor.get_sensor_info()
    print("Sensor-Informationen:")
    print(f"  - Name:       {info['name']}")
    print(f"  - Typ:        {info['type']}")
    print(f"  - Verfügbar:  {info['available']}")
    print(f"  - Mock-Modus: {info['mock_mode']}")
    print(f"  - Messungen:  {', '.join(info['measures'])}")
    print()
    
    # Aufwärmzeit
    if not sensor.is_mock_mode():
        print("Warte auf erste Messung (ca. 2-3 Sekunden)...")
        time.sleep(3)
        print()
    
    # Live-Messungen
    print("Live-Messungen (Strg+C zum Beenden):")
    print("-" * 60)
    
    try:
        measurement_count = 0
        while True:
            result = sensor.read_all()
            
            if result:
                temperature = result['temperature']
                humidity = result['humidity']
                co2 = result['co2']
                measurement_count += 1
                
                # Statuszeile anzeigen
                print(f"\rMessung #{measurement_count:04d} | "
                      f"Temp: {temperature:5.1f}°C | "
                      f"Humid: {humidity:5.1f}% | "
                      f"CO2: {co2:6.0f} ppm", end='', flush=True)
                
                # Bewertung der Werte alle 10 Messungen
                if measurement_count % 10 == 0:
                    print()  # Neue Zeile
                    
                    # Temperatur-Bewertung
                    if 18 <= temperature <= 25:
                        print(f"   → Temperatur: Optimal für Pilze ✓")
                    elif temperature < 15:
                        print(f"   → Temperatur: Zu kalt!")
                    elif temperature > 28:
                        print(f"   → Temperatur: Zu warm!")
                    
                    # Luftfeuchtigkeit-Bewertung
                    if 80 <= humidity <= 95:
                        print(f"   → Luftfeuchtigkeit: Optimal für Pilze ✓")
                    elif humidity < 70:
                        print(f"   → Luftfeuchtigkeit: Zu trocken!")
                    elif humidity > 98:
                        print(f"   → Luftfeuchtigkeit: Zu feucht!")
                    
                    # CO2-Bewertung
                    if co2 < 800:
                        print(f"   → CO2: Ausgezeichnet ✓")
                    elif co2 < 1000:
                        print(f"   → CO2: Gut")
                    elif co2 < 1500:
                        print(f"   → CO2: Mäßig (Lüftung empfohlen)")
                    else:
                        print(f"   → CO2: Hoch! (Lüftung notwendig)")
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
        
        # Finale Werte
        if result:
            print("Letzte Messwerte:")
            print(f"  Temperatur:       {result['temperature']:.1f}°C")
            print(f"  Luftfeuchtigkeit: {result['humidity']:.1f}%")
            print(f"  CO2:              {result['co2']} ppm")
        
        return True


def test_calibration():
    """
    Zeigt Kalibrierungsoptionen (optional)
    """
    print()
    print("=" * 60)
    print("Kalibrierungs-Optionen")
    print("=" * 60)
    print()
    print("Der SCD30 bietet folgende Kalibrierungsmöglichkeiten:")
    print()
    print("1. Temperatur-Offset setzen")
    print("   - Kompensiert die Eigenerwärmung des Sensors (2-4°C)")
    print("   - Vergleiche mit einem kalibrierten Thermometer")
    print()
    print("2. Höhenkompensation")
    print("   - Verbessert die CO2-Genauigkeit")
    print("   - Höhe über Meeresspiegel in Metern")
    print()
    print("3. CO2-Kalibrierung (Forced Recalibration)")
    print("   - Nur bei bekanntem CO2-Referenzwert!")
    print("   - Z.B. 400 ppm in frischer Außenluft")
    print()
    print("Für detaillierte Kalibrierung siehe:")
    print("  python calibrate_scd30.py")
    print()


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
