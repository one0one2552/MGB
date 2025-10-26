# MGB - Mushroom Grow Box - Automatisierte Überwachung und Steuerung

🍄 **Automatisiertes System zur Überwachung und Regelung optimaler Wachstumsbedingungen für Kulturpilze**

Erstellt von Stefan Schaad (MGB)

---

[🇩🇪 Deutsche Version](README_DE.md) | [🇬🇧 English Version](README.md)

---

## 📋 Projektbeschreibung

Dieses System überwacht kontinuierlich die Umgebungsparameter (CO2, Temperatur, Luftfeuchtigkeit) in einer MGB - Mushroom Grow Box und steuert entsprechende Aktoren (Pumpe mit Sprühdüsen, Heizmatten, Lüfter), um ideale Wachstumsbedingungen aufrechtzuerhalten.

## ✨ Features

- **Sensoren:**
  - 🌡️ Temperaturmessung (10-35°C, ±0,5°C)
  - 💧 Luftfeuchtigkeitsmessung (50-95% RH, ±3%)
  - 🌫️ CO2-Messung (0-5000 ppm, ±50 ppm)

- **Automatische Regelung:**
  - PID-basierte Regelung für alle Parameter
  - Konfigurierbare Sollwerte und Toleranzen
  - Tag/Nacht-Rhythmus programmierbar

- **Aktoren:**
  - 💦 Wasserpumpe mit Sprühdüsen (Luftfeuchtigkeit)
  - 🔥 Heizmatten (Temperatur)
  - 🌀 Lüfter (CO2 und Luftzirkulation)

- **Webinterface:**
  - 📊 Echtzeit-Anzeige aller Messwerte
  - 📈 Historische Diagramme
  - ⚙️ Konfiguration und manuelle Steuerung
  - 🚨 Alarm-Management

## 🛠️ Technologie-Stack

- **Backend:** Python 3.x
- **Web-Framework:** Flask mit SocketIO
- **Frontend:** HTML5, CSS3, JavaScript, Chart.js
- **Datenbank:** SQLite
- **Hardware:** Raspberry Pi mit GPIO

## 🔌 Hardware-Setup

### Benötigte Komponenten

- **Raspberry Pi** (getestet mit Pi 3/4/5)
- **SCD30 Sensor** (CO2, Temperatur, Luftfeuchtigkeit)
  - I2C-Verbindung (Standard-Adresse: 0x61)
- **Relay-Modul** (3.3V kompatibel, HIGH-Level-Trigger)
  - GPIO 27: Heizmatten-Steuerung
  - GPIO 17: Pumpen-Steuerung
- **Aktoren:**
  - Heizmatte
  - Wasserpumpe mit Sprühdüsen
  - Lüfter (optional)

### GPIO Pin-Belegung

| Komponente | GPIO Pin (BCM) | Physischer Pin |
|-----------|----------------|----------------|
| SCD30 SDA | GPIO 2 | Pin 3 |
| SCD30 SCL | GPIO 3 | Pin 5 |
| Heizung Relay | GPIO 27 | Pin 13 |
| Pumpe Relay | GPIO 17 | Pin 11 |
| Lüfter PWM | GPIO 22 | Pin 15 |

### Relay-Modul

- **Typ:** HIGH-Level-Trigger (3.3V kompatibel)
- **Logik:** HIGH = AN, LOW = AUS
- **Anschlüsse:**
  - VCC → 5V (Pin 2 oder 4)
  - GND → GND (Pin 6, 9, 14, 20, 25, 30, 34 oder 39)
  - Signal → GPIO Pin (siehe Tabelle oben)

## 📦 Installation

### Voraussetzungen

- Python 3.8 oder höher
- pip (Python Package Manager)
- Raspberry Pi mit GPIO (für Hardware-Anbindung)

### Schritt 1: Repository klonen

```bash
git clone https://github.com/one0one2552/MGB.git
cd MGB
```

### Schritt 2: Abhängigkeiten installieren

**Für Raspberry Pi (mit GPIO-Zugriff):**

```bash
# System-weite Installation (erforderlich für GPIO/sudo)
sudo pip3 install -r requirements.txt
```

**Für Entwicklung/Tests (ohne Hardware):**

```bash
# Virtuelle Umgebung (optional)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Schritt 3: Konfiguration anpassen

Bearbeiten Sie `config/config.yaml` und passen Sie die Werte an Ihre Hardware an:

```yaml
sensors:
  temperature:
    target_value: 22.0  # Zieltemperatur in °C
    
  humidity:
    target_value: 85.0  # Ziel-Luftfeuchtigkeit in %
    
  co2:
    target_value: 800   # Ziel-CO2 in ppm
```

## 🚀 Start

### Auf Raspberry Pi (mit Hardware)

```bash
sudo python3 src/main.py
```

Der Webserver startet auf `http://raspberry-pi-ip:5000`

**Hinweis:** `sudo` ist für GPIO-Zugriff erforderlich.

### Entwicklungsmodus (Mock-Sensoren)

```bash
python3 src/main.py
```

Läuft mit simulierten Sensordaten zum Testen ohne Hardware.

### Produktionsmodus (Raspberry Pi)

Für den automatischen Start beim Booten, siehe vollständige Dokumentation.

## 📁 Projektstruktur

```
MGB/
├── config/               # Konfigurationsdateien
├── src/
│   ├── sensors/         # Sensormodule
│   ├── actuators/       # Aktormodule
│   ├── controllers/     # Regelungslogik (PID)
│   ├── web/            # Webinterface (Flask)
│   └── utils/          # Hilfsfunktionen
├── data/               # Datenbank
├── logs/               # Log-Dateien
├── tests/              # Unit-Tests
└── docs/               # Dokumentation
```

## 🔧 Konfiguration

Alle Einstellungen können in `config/config.yaml` angepasst werden, einschließlich:
- Sensor-Parameter und Grenzwerte
- GPIO-Pins für Aktoren
- PID-Regler Parameter
- Webserver-Einstellungen
- Tag/Nacht-Rhythmus

## 📊 Webinterface

Das Webinterface bietet:
- **Dashboard:** Aktuelle Messwerte und Status
- **Verlaufsdiagramme:** Historische Daten der letzten 24h
- **Steuerung:** Manuelle Kontrolle der Aktoren
- **Alarme:** Benachrichtigungen bei Grenzwertüberschreitungen

## 📖 Weitere Dokumentation

- [Lastenheft](Pilzzuchtbox_Lastenheft.md) - Detaillierte Anforderungen
- [Projektstruktur](docs/struktur.md) - Übersicht über die Code-Struktur
- [Adaptive PID](docs/adaptive_pid.md) - Dokumentation zur adaptiven PID-Regelung
- [Einstellungen](docs/settings_guide.md) - Benutzerhandbuch für Einstellungen
- [WiFi Setup](docs/wifi_setup.md) - WiFi Access Point Konfiguration

**Englische Dokumentation:**
- [Project Structure](docs/eng/structure.md) - Overview of the code structure
- [Adaptive PID](docs/eng/adaptive_pid.md) - Documentation on adaptive PID control
- [Settings Guide](docs/eng/settings_guide.md) - User guide for settings
- [WiFi Setup](docs/eng/wifi_setup.md) - WiFi Access Point configuration

## 📄 Lizenz

Siehe [LICENSE](LICENSE) Datei für Details.

## 👥 Autor

Stefan Schaad (MGB)

---

**Status:** 🚧 In Entwicklung
**Version:** 0.1.0
**Letzte Aktualisierung:** Oktober 2025
