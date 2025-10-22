# Project Structure - MGB - Mushroom Grow Box

```
MGB/
│
├── config/                      # Configuration files
│   └── config.yaml             # Main configuration
│
├── src/                        # Source code
│   ├── __init__.py
│   ├── main.py                 # Main program
│   │
│   ├── sensors/                # Sensor modules
│   │   ├── __init__.py
│   │   ├── base_sensor.py      # Base class for sensors
│   │   ├── temperature_sensor.py   # TODO
│   │   ├── humidity_sensor.py      # TODO
│   │   └── co2_sensor.py          # TODO
│   │
│   ├── actuators/              # Actuator modules
│   │   ├── __init__.py
│   │   ├── base_actuator.py    # Base class for actuators
│   │   ├── pump.py             # TODO
│   │   ├── heater.py           # TODO
│   │   └── fan.py              # TODO
│   │
│   ├── controllers/            # Control logic
│   │   ├── __init__.py
│   │   ├── pid_controller.py   # PID controller
│   │   └── system_controller.py    # TODO
│   │
│   ├── web/                    # Web interface
│   │   ├── app.py              # Flask server
│   │   ├── templates/
│   │   │   └── index.html      # Main page
│   │   └── static/
│   │       ├── css/
│   │       │   └── style.css   # Styles
│   │       └── js/
│   │           └── main.js     # JavaScript
│   │
│   └── utils/                  # Helper functions
│       ├── __init__.py
│       ├── logger.py           # Logging
│       └── data_logger.py      # Database logger
│
├── data/                       # Databases and logs
│   └── mgb_mushroom_grow_box.db        # SQLite database (will be created)
│
├── logs/                       # Log files (will be created)
│
├── tests/                      # Unit tests (TODO)
│
├── docs/                       # Documentation
│   └── structure.md           # This file
│
├── requirements.txt            # Python dependencies
├── README.md                   # Project description
├── LICENSE                     # License
└── Pilzzuchtbox_Lastenheft.md # Requirements specification

```

## Next Steps

1. **Create sensor implementations**
   - temperature_sensor.py (DHT22/DHT11)
   - humidity_sensor.py (included in DHT22)
   - co2_sensor.py (SCD30 or MH-Z19)

2. **Create actuator implementations**
   - pump.py (relay control)
   - heater.py (relay control with overtemperature protection)
   - fan.py (PWM control)

3. **Create system controller**
   - system_controller.py (orchestration of all components)

4. **Write tests**
   - Unit tests for all modules

5. **Prepare deployment**
   - Systemd service for automatic startup
   - Installation on Raspberry Pi
