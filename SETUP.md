# MGB Setup Guide - Komplette Neuinstallation

🍄 **Schritt-für-Schritt Anleitung für die Installation auf einem neuen System**

---

## 📋 Voraussetzungen

- Raspberry Pi (3, 4 oder 5)
- MicroSD-Karte (min. 16 GB, empfohlen 32 GB)
- Raspberry Pi OS (Lite oder Desktop)
- Internet-Verbindung
- SSH-Zugriff oder Monitor + Tastatur

---

## 🔧 1. Raspberry Pi OS vorbereiten

### 1.1 OS installieren

Mit Raspberry Pi Imager:
1. Raspberry Pi OS Lite (64-bit) wählen
2. WLAN und SSH konfigurieren
3. Auf SD-Karte schreiben

### 1.2 Erste Anmeldung

```bash
ssh pi@raspberrypi.local
# Standard-Passwort: raspberry (ändern!)
```

### 1.3 System aktualisieren

```bash
sudo apt update
sudo apt upgrade -y
```

### 1.4 Git installieren

```bash
sudo apt install git -y
git --version
# Sollte git version 2.x.x anzeigen
```

### 1.5 I2C aktivieren (für SCD30 Sensor)

```bash
sudo raspi-config
# Interface Options → I2C → Yes → Finish
sudo reboot
```

---

## 📦 2. Python und Dependencies installieren

### 2.1 Python 3 prüfen

```bash
python3 --version
# Sollte Python 3.11 oder höher sein
```

### 2.2 pip installieren/aktualisieren

```bash
sudo apt install python3-pip python3-venv -y
sudo pip3 install --upgrade pip
```

### 2.3 System-Bibliotheken für GPIO und I2C

```bash
sudo apt install python3-rpi.gpio python3-smbus i2c-tools -y
```

### 2.4 I2C-Geräte testen

```bash
sudo i2cdetect -y 1
# SCD30 sollte bei Adresse 0x61 erscheinen
```

---

## 🚀 3. MGB Software installieren

### 3.1 Repository klonen

```bash
cd ~
git clone https://github.com/one0one2552/MGB.git
cd MGB
```

### 3.2 Python-Pakete installieren

**Für Raspberry Pi OS Bookworm (ab 2024) oder neuere Systeme:**

```bash
sudo pip3 install -r requirements.txt --break-system-packages --ignore-installed PyYAML
```

**Für ältere Systeme (ohne externally-managed-environment):**

```bash
sudo pip3 install -r requirements.txt
```

**⚠️ Hinweis:** 
- Das `--break-system-packages` Flag ist nötig auf neueren Raspberry Pi OS Versionen und ist hier unbedenklich, da wir GPIO-Zugriff mit sudo benötigen.
- Das `--ignore-installed PyYAML` umgeht Konflikte mit dem System-PyYAML Paket.

**Wichtige Pakete:**
- Flask, Flask-SocketIO (Webserver)
- adafruit-circuitpython-scd30 (SCD30 Sensor)
- RPi.GPIO (GPIO-Steuerung)
- PyYAML (Konfiguration)

### 3.3 Verzeichnisse erstellen

```bash
mkdir -p data logs
```

---

## ⚙️ 4. Konfiguration anpassen

### 4.1 config.yaml bearbeiten

```bash
nano config/config.yaml
```

**Wichtige Einstellungen:**

```yaml
# Sensoren
sensors:
  temperature:
    target_value: 22.0  # Zieltemperatur °C
  humidity:
    target_value: 85.0  # Ziel-Luftfeuchtigkeit %
  co2:
    target_value: 800   # Ziel-CO2 ppm

# Aktoren
actuators:
  heater:
    pin: 27  # GPIO 27 für Heizmatte
  pump:
    pin: 17  # GPIO 17 für Pumpe

# Webserver
web:
  host: "0.0.0.0"  # Auf allen Interfaces
  port: 5000
```

Speichern: `Ctrl+O`, Beenden: `Ctrl+X`

---

## 🔌 5. Hardware anschließen

### 5.1 SCD30 Sensor (I2C)

| SCD30 Pin | Raspberry Pi Pin | Beschreibung |
|-----------|------------------|--------------|
| VIN | Pin 2 (5V) | Stromversorgung |
| GND | Pin 6 (GND) | Masse |
| SDA | Pin 3 (GPIO 2) | I2C Daten |
| SCL | Pin 5 (GPIO 3) | I2C Clock |

### 5.2 Relay-Module

**Heizmatte (GPIO 27):**

| Relay Pin | Raspberry Pi Pin |
|-----------|------------------|
| VCC | Pin 2 oder 4 (5V) |
| GND | Pin 6, 9, 14, 20, 25, 30, 34 oder 39 (GND) |
| Signal | Pin 13 (GPIO 27) |

**Pumpe (GPIO 17):**

| Relay Pin | Raspberry Pi Pin |
|-----------|------------------|
| VCC | Pin 2 oder 4 (5V) |
| GND | Pin 6, 9, 14, 20, 25, 30, 34 oder 39 (GND) |
| Signal | Pin 11 (GPIO 17) |

**⚠️ WICHTIG:** Relay-Modul muss **3.3V-kompatibel** und **HIGH-Level-Trigger** sein!

---

## ✅ 6. System testen

### 6.1 Sensor-Test

```bash
cd ~/MGB
sudo python3 test_scd30.py
```

Erwartete Ausgabe:
```
✓ SCD30 bereit
Temperatur: 21.5°C
Luftfeuchtigkeit: 80.2%
CO2: 780 ppm
```

### 6.2 Relay-Test

```bash
sudo python3 test_relay.py
```

Das Relay sollte:
- Beim Start AUS bleiben
- Bei Test 1 ANZIEHEN (Klicken hörbar)
- Bei Test 2 ABFALLEN
- Bei Test 3 wieder ANZIEHEN

### 6.3 Hauptanwendung starten

```bash
sudo python3 src/main.py
```

Erwartete Ausgabe:
```
============================================================
MGB - Mushroom Grow Box
============================================================
✓ Heizmatte initialisiert auf GPIO Pin 27
✓ Pumpe initialisiert auf GPIO Pin 17
✓ SCD30 bereit
Webserver gestartet auf http://0.0.0.0:5000
```

### 6.4 Webinterface öffnen

Im Browser: `http://raspberry-pi-ip:5000`

Du solltest sehen:
- Aktuelle Sensor-Werte
- Historische Charts
- Heizung/Pumpe Ein/Aus-Buttons

---

## 🔄 7. Autostart einrichten (optional)

### 7.1 Systemd Service erstellen

```bash
sudo nano /etc/systemd/system/mgb.service
```

Inhalt:

```ini
[Unit]
Description=MGB Mushroom Grow Box
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/pi/MGB
ExecStart=/usr/bin/python3 /home/pi/MGB/src/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 7.2 Service aktivieren

```bash
sudo systemctl daemon-reload
sudo systemctl enable mgb.service
sudo systemctl start mgb.service
```

### 7.3 Status prüfen

```bash
sudo systemctl status mgb.service
```

### 7.4 Logs anzeigen

```bash
sudo journalctl -u mgb.service -f
```

---

## 🛠️ 8. Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'flask'"

**Lösung:**
```bash
sudo pip3 install flask flask-socketio
```

### Problem: "No module named 'board'" (SCD30)

**Lösung:**
```bash
sudo pip3 install adafruit-circuitpython-scd30
```

### Problem: Relay zieht nicht an

**Prüfen:**
1. Relay-Modul ist 3.3V-kompatibel
2. Verkabelung korrekt (VCC, GND, Signal)
3. GPIO-Pin in config.yaml stimmt mit Hardware überein

**Test:**
```bash
# Manueller GPIO-Test
sudo python3 -c "
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT, initial=GPIO.LOW)
import time
print('Relay AN in 2 Sek...')
time.sleep(2)
GPIO.output(27, GPIO.HIGH)
time.sleep(5)
print('Relay AUS')
GPIO.output(27, GPIO.LOW)
GPIO.cleanup()
"
```

### Problem: SCD30 nicht gefunden

**Prüfen:**
```bash
sudo i2cdetect -y 1
```

Sollte `61` anzeigen. Wenn nicht:
- I2C in raspi-config aktiviert?
- Verkabelung korrekt?
- Sensor mit 5V versorgt?

### Problem: Permission denied (GPIO)

**Lösung:** Immer mit `sudo` starten:
```bash
sudo python3 src/main.py
```

---

## 📚 Weitere Informationen

- [README.md](README.md) - Projekt-Übersicht
- [docs/settings_guide.md](docs/settings_guide.md) - Einstellungen
- [docs/wifi_setup.md](docs/wifi_setup.md) - WiFi Access Point
- [config/config.yaml](config/config.yaml) - Konfigurationsdatei

---

**Status:** Getestet mit Raspberry Pi 4 + Python 3.13 + SCD30 Sensor
**Letzte Aktualisierung:** Oktober 2025
