# MGB - Mushroom Grow Box - Automated Monitoring and Control

🍄 **Automated system for monitoring and regulating optimal growth conditions for cultivated mushrooms**

Created by Stefan Schaad (MGB)

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
- **Hardware:** Raspberry Pi (recommended)

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

### Step 2: Create Virtual Environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Adjust Configuration

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

### Development Mode

```bash
python src/main.py
```

The web server starts by default on `http://localhost:5000`

### Production Mode (Raspberry Pi)

For automatic startup on boot, see full documentation.

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

- [Requirements Specification](Pilzzuchtbox_Lastenheft.md) - Detailed requirements
- [Project Structure](docs/eng/structure.md) - Overview of the code structure

## 📄 License

See [LICENSE](LICENSE) file for details.

## 👥 Author

Stefan Schaad (MGB)

---

**Status:** 🚧 In Development
**Version:** 0.1.0
**Last Update:** October 2025
