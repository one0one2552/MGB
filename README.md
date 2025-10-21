# MGB - Mushroom Grow Box - Automatisierte Überwachung und Steuerung

🍄 **Automatisiertes System zur Überwachung und Regelung optimaler Wachstumsbedingungen für Kulturpilze**

Erstellt von Stefan Schaad (MGB)

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
- **Hardware:** Raspberry Pi (empfohlen)

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

### Schritt 2: Virtuelle Umgebung erstellen (empfohlen)

```bash
python -m venv venv
source venv/bin/activate  # Auf Windows: venv\Scripts\activate
```

### Schritt 3: Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### Schritt 4: Konfiguration anpassen

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

### Entwicklungsmodus

```bash
python src/main.py
```

Der Webserver startet standardmäßig auf `http://localhost:5000`

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

## 📄 Lizenz

Siehe [LICENSE](LICENSE) Datei für Details.

## 👥 Autor

Stefan Schaad (MGB)

---

**Status:** 🚧 In Entwicklung
**Version:** 0.1.0
**Letzte Aktualisierung:** Oktober 2025



