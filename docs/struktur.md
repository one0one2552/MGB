# Projektstruktur - MGB - Mushroom Grow Box

```
MGB/
│
├── config/                      # Konfigurationsdateien
│   └── config.yaml             # Hauptkonfiguration
│
├── src/                        # Quellcode
│   ├── __init__.py
│   ├── main.py                 # Hauptprogramm
│   │
│   ├── sensors/                # Sensormodule
│   │   ├── __init__.py
│   │   ├── base_sensor.py      # Basis-Klasse für Sensoren
│   │   ├── temperature_sensor.py   # TODO
│   │   ├── humidity_sensor.py      # TODO
│   │   └── co2_sensor.py          # TODO
│   │
│   ├── actuators/              # Aktormodule
│   │   ├── __init__.py
│   │   ├── base_actuator.py    # Basis-Klasse für Aktoren
│   │   ├── pump.py             # TODO
│   │   ├── heater.py           # TODO
│   │   └── fan.py              # TODO
│   │
│   ├── controllers/            # Regelungslogik
│   │   ├── __init__.py
│   │   ├── pid_controller.py   # PID-Regler
│   │   └── system_controller.py    # TODO
│   │
│   ├── web/                    # Webinterface
│   │   ├── app.py              # Flask-Server
│   │   ├── templates/
│   │   │   └── index.html      # Hauptseite
│   │   └── static/
│   │       ├── css/
│   │       │   └── style.css   # Styles
│   │       └── js/
│   │           └── main.js     # JavaScript
│   │
│   └── utils/                  # Hilfsfunktionen
│       ├── __init__.py
│       ├── logger.py           # Logging
│       └── data_logger.py      # Datenbank-Logger
│
├── data/                       # Datenbanken und Logs
│   └── mgb_mushroom_grow_box.db        # SQLite-Datenbank (wird erstellt)
│
├── logs/                       # Log-Dateien (werden erstellt)
│
├── tests/                      # Unit-Tests (TODO)
│
├── docs/                       # Dokumentation
│   └── struktur.md            # Diese Datei
│
├── requirements.txt            # Python-Abhängigkeiten
├── README.md                   # Projektbeschreibung
├── LICENSE                     # Lizenz
└── Pilzzuchtbox_Lastenheft.md # Lastenheft

```

## Nächste Schritte

1. **Sensor-Implementierungen erstellen**
   - temperature_sensor.py (DHT22/DHT11)
   - humidity_sensor.py (im DHT22 enthalten)
   - co2_sensor.py (SCD30 oder MH-Z19)

2. **Aktor-Implementierungen erstellen**
   - pump.py (Relais-Steuerung)
   - heater.py (Relais-Steuerung mit Übertemperaturschutz)
   - fan.py (PWM-Steuerung)

3. **System-Controller erstellen**
   - system_controller.py (Orchestrierung aller Komponenten)

4. **Tests schreiben**
   - Unit-Tests für alle Module

5. **Deployment vorbereiten**
   - Systemd-Service für automatischen Start
   - Installation auf Raspberry Pi
