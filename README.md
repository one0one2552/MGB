# MGB - Mushroom Grow Box - Automated Monitoring and Control

🍄 **Automated system for monitoring and regulating optimal growth conditions for cultivated mushrooms**

Created by Stefan Schaad (MGB)

---

[🇩🇪 Deutsche Version](README_DE.md) | [🇬🇧 English Version](README.md)

---

## 📋 Project Description

This system continuously monitors environmental parameters (CO2, temperature, humidity) in a MGB - Mushroom Grow Box and controls corresponding actuators (pump with spray nozzles, heating mats, fans) to maintain ideal growth conditions.

## ✨ Features

- **Sensors:**
  - 🌡️ Temperature measurement (10-35°C, ±0.5°C)
  - 💧 Humidity measurement (50-95% RH, ±3%)
  - 🌫️ CO2 measurement (0-5000 ppm, ±50 ppm)

- **Automatic Control:**
  - PID-based control for all parameters
  - Configurable setpoints and tolerances
  - Programmable day/night rhythm

- **Actuators:**
  - 💦 Water pump with spray nozzles (humidity)
  - 🔥 Heating mats (temperature)
  - 🌀 Fan (CO2 and air circulation)

- **Web Interface:**
  - 📊 Real-time display of all measurements
  - 📈 Historical charts
  - ⚙️ Configuration and manual control
  - 🚨 Alarm management

## 🛠️ Technology Stack

- **Backend:** Python 3.x
- **Web Framework:** Flask with SocketIO
- **Frontend:** HTML5, CSS3, JavaScript, Chart.js
- **Database:** SQLite
- **Hardware:** Raspberry Pi with GPIO

## 🔌 Hardware Setup

### Required Components

- **Raspberry Pi** (tested with Pi 3/4/5)
- **SCD30 Sensor** (CO2, Temperature, Humidity)
  - I2C connection (default address: 0x61)
- **Relay Module** (3.3V compatible, HIGH-Level-Trigger)
  - GPIO 27: Heating mat control
  - GPIO 17: Pump control
- **Actuators:**
  - Heating mat
  - Water pump with spray nozzles
  - Fan (optional)

### GPIO Pin Assignment

| Component | GPIO Pin (BCM) | Physical Pin |
|-----------|----------------|--------------|
| SCD30 SDA | GPIO 2 | Pin 3 |
| SCD30 SCL | GPIO 3 | Pin 5 |
| Heater Relay | GPIO 27 | Pin 13 |
| Pump Relay | GPIO 17 | Pin 11 |
| Fan PWM | GPIO 22 | Pin 15 |

### Relay Module

- **Type:** HIGH-Level-Trigger (3.3V compatible)
- **Logic:** HIGH = ON, LOW = OFF
- **Connections:**
  - VCC → 5V (Pin 2 or 4)
  - GND → GND (Pin 6, 9, 14, 20, 25, 30, 34, or 39)
  - Signal → GPIO pin (see table above)

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python Package Manager)
- Raspberry Pi with GPIO (for hardware integration)

### Step 1: Clone Repository

```bash
git clone https://github.com/one0one2552/MGB.git
cd MGB
```

### Step 2: Install Dependencies

**For Raspberry Pi (with GPIO access):**

```bash
# System-wide installation (required for GPIO/sudo access)
sudo pip3 install -r requirements.txt
```

**For development/testing (without hardware):**

```bash
# Virtual environment (optional)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Adjust Configuration

Edit `config/config.yaml` and adjust the values to your hardware:

```yaml
sensors:
  temperature:
    target_value: 22.0  # Target temperature in °C
    
  humidity:
    target_value: 85.0  # Target humidity in %
    
  co2:
    target_value: 800   # Target CO2 in ppm
```

## 🚀 Start

### On Raspberry Pi (with Hardware)

```bash
sudo python3 src/main.py
```

The web server starts on `http://raspberry-pi-ip:5000`

**Note:** `sudo` is required for GPIO access.

### Development Mode (Mock Sensors)

```bash
python3 src/main.py
```

Runs with simulated sensor data for testing without hardware.

## 📁 Project Structure

```
MGB/
├── config/               # Configuration files
├── src/
│   ├── sensors/         # Sensor modules
│   ├── actuators/       # Actuator modules
│   ├── controllers/     # Control logic (PID)
│   ├── web/            # Web interface (Flask)
│   └── utils/          # Helper functions
├── data/               # Database
├── logs/               # Log files
├── tests/              # Unit tests
└── docs/               # Documentation
```

## 🔧 Configuration

All settings can be adjusted in `config/config.yaml`, including:
- Sensor parameters and limits
- GPIO pins for actuators
- PID controller parameters
- Web server settings
- Day/night rhythm

## 📊 Web Interface

The web interface offers:
- **Dashboard:** Current measurements and status
- **History Charts:** Historical data of the last 24h
- **Control:** Manual control of actuators
- **Alarms:** Notifications when limits are exceeded

## 📖 Further Documentation

- [Requirements Specification](Pilzzuchtbox_Lastenheft.md) - Detailed requirements (German)
- [Project Structure](docs/eng/structure.md) - Overview of the code structure
- [Adaptive PID](docs/eng/adaptive_pid.md) - Documentation on adaptive PID control
- [Settings Guide](docs/eng/settings_guide.md) - User guide for settings
- [WiFi Setup](docs/eng/wifi_setup.md) - WiFi Access Point configuration

**German Documentation:**
- [Projektstruktur](docs/struktur.md) - Übersicht über die Code-Struktur
- [Adaptive PID](docs/adaptive_pid.md) - Dokumentation zur adaptiven PID-Regelung
- [Einstellungen](docs/settings_guide.md) - Benutzerhandbuch für Einstellungen
- [WiFi Setup](docs/wifi_setup.md) - WiFi Access Point Konfiguration

## 📄 License

See [LICENSE](LICENSE) file for details.

## 👥 Author

Stefan Schaad (MGB)

---

**Status:** 🚧 In Development
**Version:** 0.1.0
**Last Update:** October 2025



