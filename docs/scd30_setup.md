# SCD30 Sensor Setup Guide

## Übersicht

Der **Sensirion SCD30** ist ein hochwertiger NDIR-CO2-Sensor mit integrierter Temperatur- und Feuchtigkeitsmessung. Er ist ideal für die Pilzzucht, da er alle wichtigen Umgebungsparameter in einem Sensor vereint.

## Hardware-Spezifikationen

- **CO2-Messbereich**: 400 - 10.000 ppm
- **CO2-Genauigkeit**: ±(30 ppm + 3% des Messwerts)
- **Temperaturbereich**: -40°C bis +70°C
- **Temperaturgenauigkeit**: ±0.4°C
- **Feuchtigkeitsbereich**: 0 - 100% RH
- **Feuchtigkeitsgenauigkeit**: ±3% RH
- **Schnittstelle**: I2C (Standard-Adresse: 0x61)
- **Betriebsspannung**: 3.3V - 5V
- **Messintervall**: 2 - 1800 Sekunden (Standard: 2s)

## Hardware-Anschluss (Raspberry Pi)

### Pin-Belegung

| SCD30 Pin | Raspberry Pi Pin | Beschreibung |
|-----------|------------------|--------------|
| VIN       | Pin 1 (3.3V)     | Stromversorgung |
| GND       | Pin 6 (GND)      | Masse |
| SCL       | Pin 5 (GPIO 3)   | I2C Clock |
| SDA       | Pin 3 (GPIO 2)   | I2C Data |

### Schaltung

```
Raspberry Pi          SCD30
┌────────────┐      ┌──────────┐
│ Pin 1 (3.3V)├──────┤ VIN      │
│ Pin 3 (SDA) ├──────┤ SDA      │
│ Pin 5 (SCL) ├──────┤ SCL      │
│ Pin 6 (GND) ├──────┤ GND      │
└────────────┘      └──────────┘
```

⚠️ **Wichtig**: 
- Der SCD30 benötigt eine stabile Stromversorgung
- Pull-Up-Widerstände (4.7kΩ) sind meist bereits auf dem Breakout-Board vorhanden
- Bei längeren Kabeln (>30cm) sollten externe Pull-Ups in Betracht gezogen werden

## Software-Installation

### 1. I2C auf dem Raspberry Pi aktivieren

```bash
sudo raspi-config
```

- Wähle: `3 Interface Options`
- Wähle: `I5 I2C`
- Aktiviere I2C

Neustart durchführen:
```bash
sudo reboot
```

### 2. I2C-Tools installieren und testen

```bash
sudo apt-get update
sudo apt-get install -y i2c-tools
```

Sensor erkennen:
```bash
sudo i2cdetect -y 1
```

Erwartete Ausgabe (Adresse 0x61):
```
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- 61 -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
```

### 3. Python-Bibliotheken installieren

Die Bibliotheken sind bereits in `requirements.txt` enthalten:

```bash
cd ~/MGB
source venv/bin/activate
pip install -r requirements.txt
```

## Verwendung im Code

### Einfaches Beispiel

```python
from sensors.scd30_sensor import SCD30Sensor

# Sensor initialisieren
sensor = SCD30Sensor()

if sensor.is_available:
    # Alle Werte auslesen
    result = sensor.read_all()
    if result:
        temperature, humidity, co2 = result
        print(f"Temperatur: {temperature}°C")
        print(f"Luftfeuchtigkeit: {humidity}%")
        print(f"CO2: {co2} ppm")
    
    # Einzelne Werte auslesen
    temp = sensor.read_temperature()
    humidity = sensor.read_humidity()
    co2 = sensor.read_co2()
```

### Integration mit BaseSensor-Wrapper

```python
from sensors.scd30_sensor import SCD30Sensor, SCD30Temperature, SCD30Humidity, SCD30CO2

# Haupt-Sensor initialisieren
scd30 = SCD30Sensor()

# Wrapper für einzelne Werte erstellen
temp_sensor = SCD30Temperature(scd30)
humidity_sensor = SCD30Humidity(scd30)
co2_sensor = SCD30CO2(scd30)

# Verwenden wie andere Sensoren
temperature = temp_sensor.read()
humidity = humidity_sensor.read()
co2 = co2_sensor.read()
```

## Kalibrierung

### Automatische Selbstkalibrierung (ASC)

Der SCD30 hat eine automatische Selbstkalibrierung aktiviert, die nach 7 Tagen kontinuierlicher Betriebszeit den niedrigsten gemessenen CO2-Wert als 400 ppm annimmt (Frischluft-Referenz).

### Manuelle Kalibrierung (FRC - Forced Recalibration)

Falls du eine präzisere Kalibrierung brauchst:

1. **Frischluft-Kalibrierung (400 ppm)**:
   ```python
   sensor.calibrate_forced_recalibration(400)
   ```

2. **Kalibrierung mit Referenzgas**:
   ```python
   # Wenn du ein Referenzgas mit bekanntem CO2-Wert hast
   sensor.calibrate_forced_recalibration(1000)  # z.B. 1000 ppm
   ```

⚠️ **Vorsicht**: Verwende FRC nur, wenn du sicher bist, dass der aktuelle CO2-Wert bekannt ist!

### Temperatur-Offset

Der SCD30 erwärmt sich leicht während des Betriebs. Um dies zu kompensieren:

```python
# Typisch: 2-4°C Offset
sensor.set_temperature_offset(3.0)
```

Den richtigen Offset findest du durch Vergleich mit einem kalibrierten Referenz-Thermometer.

### Höhenkompensation

Für präzisere CO2-Messungen sollte die Höhe über dem Meeresspiegel gesetzt werden:

```python
# Beispiel: 500 Meter über Meeresspiegel
sensor.set_altitude_compensation(500)
```

## Troubleshooting

### Sensor wird nicht erkannt (i2cdetect zeigt nichts)

1. **Verkabelung überprüfen**:
   - Alle Verbindungen fest?
   - Richtige Pins verwendet?
   - 3.3V Spannung vorhanden?

2. **I2C aktiviert?**:
   ```bash
   sudo raspi-config
   ```

3. **Pull-Up-Widerstände**:
   - Sind Pull-Ups auf dem Breakout-Board vorhanden?
   - Bei langen Kabeln: externe 4.7kΩ Pull-Ups hinzufügen

### Sensor gibt unrealistische Werte aus

1. **Aufwärmzeit**: Der Sensor benötigt ca. 2 Minuten nach dem Einschalten
2. **Kalibrierung**: Führe eine Frischluft-Kalibrierung durch
3. **Temperatur-Offset**: Setze einen passenden Offset (2-4°C)

### CO2-Wert steigt kontinuierlich an

- **Belüftung**: Sensor benötigt gelegentlich Frischluft für ASC
- **ASC deaktiviert**: Überprüfe, ob automatische Kalibrierung aktiv ist

### Sensor reagiert zu langsam

- **Messintervall**: Standard ist 2 Sekunden (minimum)
- Der Sensor benötigt Zeit für genaue NDIR-Messungen
- Schnellere Updates sind technisch nicht möglich

## Best Practices für Pilzzucht

### Platzierung

✅ **Empfohlen**:
- In Höhe der Pilze montieren
- Gute Luftzirkulation um den Sensor
- Geschützt vor direktem Wasserstrahl/Nebel
- Nicht zu nah an Heizung/Lüftung

❌ **Vermeiden**:
- Direkt über dem Wassertank
- In Ecken ohne Luftzirkulation
- Direkt neben der Heizung
- Im direkten Luftstrom des Ventilators

### Messintervalle

Für Pilzzucht empfohlen:
- **Normal**: 30-60 Sekunden
- **Kritische Phase**: 10-20 Sekunden
- **Energiesparmodus**: 2-5 Minuten

### Wartung

- **Monatlich**: Sensor vorsichtig mit Druckluft reinigen
- **Jährlich**: Kalibrierung mit Frischluft überprüfen
- **Bei Bedarf**: Temperatur-Offset neu justieren

## Technische Hinweise

### Messgenauigkeit

Der SCD30 verwendet **NDIR (Non-Dispersive Infrared)** Technologie für CO2-Messungen:
- Sehr genau und langzeitstabil
- Keine Querempfindlichkeit zu anderen Gasen
- Kalibrierung bleibt über Jahre erhalten

### Stromverbrauch

- **Durchschnitt**: ~19 mA @ 3.3V
- **Peak**: ~75 mA während Messung

### Lebensdauer

- **CO2-Sensor**: >15 Jahre
- **Temperatur/Feuchte**: >5 Jahre

## Weiterführende Informationen

- [Sensirion SCD30 Datasheet](https://www.sensirion.com/en/environmental-sensors/carbon-dioxide-sensors/carbon-dioxide-sensors-scd30/)
- [Adafruit SCD30 Guide](https://learn.adafruit.com/adafruit-scd30)
- [CircuitPython SCD30 Library](https://github.com/adafruit/Adafruit_CircuitPython_SCD30)
