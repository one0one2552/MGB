# SCD30 Sensor - Integration abgeschlossen! ✅

## Was wurde implementiert?

Die SCD30-Sensor-Integration ist vollständig und bereit für den Einsatz auf deinem Raspberry Pi!

### 📦 Neue Dateien

1. **`src/sensors/scd30_sensor.py`**
   - Vollständige SCD30-Implementierung
   - Mock-Modus für Windows-Entwicklung
   - Separate Wrapper für Temperatur, Luftfeuchtigkeit und CO2
   - Kalibrierungsfunktionen

2. **`docs/scd30_setup.md`**
   - Detaillierte Hardware-Anleitung
   - Pin-Belegung für Raspberry Pi
   - I2C-Setup
   - Kalibrierungs-Guide
   - Troubleshooting

3. **`test_scd30.py`**
   - Standalone Test-Script
   - Live-Anzeige der Messwerte
   - Kalibrierungs-Test

### 🔧 Geänderte Dateien

1. **`requirements.txt`**
   - `adafruit-circuitpython-scd30` hinzugefügt

2. **`src/sensors/__init__.py`**
   - SCD30-Klassen exportiert

3. **`src/main.py`**
   - SCD30 wird automatisch initialisiert
   - Messwerte werden geloggt
   - Sensoren werden an Web-App übergeben

4. **`src/web/app.py`**
   - SCD30-Daten werden in `/api/status` verwendet
   - Echte Sensor-Werte statt Mock-Daten

## 🚀 Wie geht's weiter?

### 1. Auf dem Raspberry Pi deployen

```bash
# Auf deinem Windows-Rechner
cd c:\python\MGB\MGB
git add .
git commit -m "Add SCD30 sensor implementation"
git push
```

### 2. Auf dem Raspberry Pi

```bash
cd ~/MGB
git pull

# Virtual Environment aktivieren
source venv/bin/activate

# Neue Abhängigkeiten installieren
pip install -r requirements.txt
```

### 3. I2C aktivieren (falls noch nicht geschehen)

```bash
sudo raspi-config
# → 3 Interface Options → I5 I2C → Enable
sudo reboot
```

### 4. Hardware anschließen

Verbinde den SCD30 wie in `docs/scd30_setup.md` beschrieben:

| SCD30 | Raspberry Pi |
|-------|--------------|
| VIN   | Pin 1 (3.3V) |
| GND   | Pin 6 (GND)  |
| SCL   | Pin 5 (GPIO 3) |
| SDA   | Pin 3 (GPIO 2) |

### 5. Sensor testen

```bash
cd ~/MGB

# I2C-Adresse überprüfen (sollte 0x61 zeigen)
sudo i2cdetect -y 1

# Test-Script ausführen
python test_scd30.py
```

### 6. System starten

```bash
# Normal starten
python src/main.py

# Oder als Service (falls eingerichtet)
sudo systemctl restart mgb
```

## 📊 Was passiert jetzt?

- Der SCD30 wird beim Start automatisch erkannt und initialisiert
- Alle 30 Sekunden (konfigurierbar in `config/config.yaml`) werden Messwerte erfasst:
  - 🌡️ Temperatur
  - 💧 Luftfeuchtigkeit
  - 🌫️ CO2-Konzentration
- Die Werte werden:
  - In der Datenbank gespeichert (via DataLogger)
  - Im Web-Interface angezeigt
  - Per WebSocket live aktualisiert
  - Für PID-Regelung verwendet (wenn konfiguriert)

## 🎛️ Kalibrierung (optional)

Der SCD30 ist werkskalibriert, aber für beste Ergebnisse:

### Temperatur-Offset setzen

Der Sensor erwärmt sich leicht im Betrieb:

```python
from sensors.scd30_sensor import SCD30Sensor

sensor = SCD30Sensor()
sensor.set_temperature_offset(3.0)  # Typisch: 2-4°C
```

### Höhenkompensation

Für präzisere CO2-Messungen:

```python
sensor.set_altitude_compensation(500)  # Höhe in Metern
```

### Frischluft-Kalibrierung

Nur wenn nötig (z.B. nach längerer Lagerung):

```python
# Sensor 5 Minuten in Frischluft halten, dann:
sensor.calibrate_forced_recalibration(400)
```

## 🐛 Troubleshooting

### Sensor wird nicht erkannt

```bash
# 1. I2C überprüfen
sudo i2cdetect -y 1

# 2. Verkabelung prüfen
# 3. System neu starten
sudo reboot
```

### Unrealistische Werte

- Warte 2 Minuten Aufwärmzeit
- Überprüfe Temperatur-Offset
- Führe Frischluft-Kalibrierung durch

### Mock-Modus auf dem Pi

Falls der Sensor im Mock-Modus läuft trotz korrekter Verkabelung:

```bash
# Bibliotheken neu installieren
pip install --upgrade --force-reinstall adafruit-circuitpython-scd30
```

## 📖 Weitere Dokumentation

Siehe `docs/scd30_setup.md` für:
- Detaillierte Hardware-Anleitung
- Pin-Belegung und Schaltplan
- Best Practices für Pilzzucht
- Erweiterte Kalibrierung
- Technische Spezifikationen

## ✨ Features

✅ Automatische Sensor-Erkennung
✅ Mock-Modus für Windows-Entwicklung
✅ Fehlerbehandlung und Logging
✅ Live-Updates im Web-Interface
✅ Datenbank-Integration
✅ Kalibrierungsfunktionen
✅ Test-Script inklusive
✅ Vollständige Dokumentation

## 🎉 Viel Erfolg!

Der SCD30 ist jetzt vollständig integriert. Viel Spaß bei der Pilzzucht! 🍄
