"""
Hauptprogramm für die MGB - Mushroom Grow Box
"""

import sys
import time
import yaml
import signal
from pathlib import Path
from threading import Thread, Event
from datetime import datetime

# Lokale Imports
sys.path.insert(0, str(Path(__file__).parent))

from utils.logger import setup_logger
from utils.data_logger import DataLogger

# Logger einrichten
logger = setup_logger('mgb_mushroom_grow_box')

# Stop-Event für sauberes Beenden
stop_event = Event()


def load_config(config_path: str = 'config/config.yaml') -> dict:
    """
    Lädt die Konfiguration
    
    Args:
        config_path: Pfad zur Konfigurationsdatei
        
    Returns:
        Konfiguration als Dictionary
    """
    config_file = Path(config_path)
    if not config_file.exists():
        logger.error(f"Konfigurationsdatei nicht gefunden: {config_path}")
        sys.exit(1)
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    logger.info("Konfiguration geladen")
    return config


def signal_handler(signum, frame):
    """
    Handler für Beendigungssignale
    """
    logger.info("Beendigungssignal empfangen")
    stop_event.set()


def monitoring_loop(config: dict, data_logger: DataLogger, sensors: dict, actuators: dict, controllers: dict, config_path: str):
    """
    Hauptschleife für Überwachung und Regelung
    
    Args:
        config: Konfiguration
        data_logger: DataLogger-Instanz
        sensors: Dictionary mit Sensor-Instanzen
        actuators: Dictionary mit Aktor-Instanzen
        controllers: Dictionary mit PID-Controller-Instanzen
        config_path: Pfad zur Konfigurationsdatei für Live-Reload
    """
    interval = config['measurement']['interval']
    logger.info(f"Starte Monitoring-Loop (Intervall: {interval}s)")
    
    while not stop_event.is_set():
        try:
            # Konfiguration neu laden (für Live-Updates aus Webinterface)
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
            except Exception as e:
                logger.warning(f"Fehler beim Neuladen der Config: {e}")
            
            # Sensoren auslesen
            if 'scd30' in sensors:
                scd30 = sensors['scd30']
                result = scd30.read_all()
                
                if result:
                    # Temperaturkorrektur anwenden
                    temp_offset = config['sensors']['temperature'].get('offset', 0.0)
                    temperature = result['temperature'] + temp_offset
                    humidity = result['humidity']
                    co2 = result['co2']
                    
                    logger.info(f"SCD30: Temp={temperature}°C (raw={result['temperature']}°C, offset={temp_offset}°C), Humidity={humidity}%, CO2={co2}ppm")
                    
                    # Daten loggen
                    data_logger.log_sensor_data('temperature', temperature, '°C')
                    data_logger.log_sensor_data('humidity', humidity, '%')
                    data_logger.log_sensor_data('co2', co2, 'ppm')
                    
                    # Temperatur-Regelung mit PID
                    if 'temperature' in controllers and 'heater' in actuators:
                        temp_controller = controllers['temperature']
                        heater = actuators['heater']
                        
                        # Zielwert aus aktueller Konfiguration holen (Live-Update)
                        target_temp = config['sensors']['temperature']['target_value']
                        temp_controller.set_setpoint(target_temp)
                        
                        # PID-Parameter aktualisieren falls adaptive Regelung deaktiviert wurde
                        pid_config = config.get('pid', {})
                        temp_pid_config = pid_config.get('temperature', {})
                        
                        # Adaptive Modus aktualisieren
                        current_adaptive = pid_config.get('adaptive', True)
                        if temp_controller.adaptive != current_adaptive:
                            temp_controller.set_adaptive(current_adaptive)
                            logger.info(f"PID adaptive Modus geändert: {current_adaptive}")
                        
                        # Wenn nicht adaptive: manuelle Parameter aktualisieren
                        if not current_adaptive:
                            new_kp = temp_pid_config.get('kp', 2.0)
                            new_ki = temp_pid_config.get('ki', 0.5)
                            new_kd = temp_pid_config.get('kd', 1.0)
                            
                            if (new_kp != temp_controller.kp_base or 
                                new_ki != temp_controller.ki_base or 
                                new_kd != temp_controller.kd_base):
                                temp_controller.kp_base = new_kp
                                temp_controller.ki_base = new_ki
                                temp_controller.kd_base = new_kd
                                temp_controller.kp = new_kp
                                temp_controller.ki = new_ki
                                temp_controller.kd = new_kd
                                logger.info(f"PID Parameter aktualisiert: Kp={new_kp}, Ki={new_ki}, Kd={new_kd}")
                        
                        # PID-Berechnung (update verwendet den gespeicherten setpoint)
                        control_output = temp_controller.update(temperature)
                        
                        # Heizung steuern (nur wenn nicht manuell gesteuert)
                        # Control output > 0 = heizen erforderlich
                        if control_output > 0:
                            if not heater.is_active:
                                heater.turn_on()
                                logger.info(f"🔥 Heizung AN (Temp: {temperature}°C, Ziel: {target_temp}°C, PID: {control_output:.2f})")
                        else:
                            if heater.is_active:
                                heater.turn_off()
                                logger.info(f"❄️  Heizung AUS (Temp: {temperature}°C, Ziel: {target_temp}°C, PID: {control_output:.2f})")
            
            # Auf nächsten Zyklus warten
            stop_event.wait(interval)
            
        except Exception as e:
            logger.error(f"Fehler im Monitoring-Loop: {e}", exc_info=True)
            time.sleep(5)  # Kurze Pause bei Fehler


def start_web_server(config: dict, sensors: dict, actuators: dict):
    """
    Startet den Webserver in einem separaten Thread
    
    Args:
        config: Konfiguration
        sensors: Dictionary mit Sensor-Instanzen
        actuators: Dictionary mit Aktor-Instanzen
    """
    from web.app import app, socketio
    import web.app as web_app
    
    # Sensoren und Aktoren an Web-App übergeben
    web_app.sensors = sensors
    web_app.actuators = actuators
    
    host = config['web']['host']
    port = config['web']['port']
    debug = config['web']['debug']
    
    logger.info(f"Starte Webserver auf {host}:{port}")
    socketio.run(app, host=host, port=port, debug=debug, allow_unsafe_werkzeug=True)


def main():
    """
    Hauptfunktion
    """
    logger.info("=" * 60)
    logger.info("MGB - Mushroom Grow Box - Automatisierte Überwachung und Steuerung")
    logger.info("=" * 60)
    
    # Signal-Handler registrieren
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Konfiguration laden
    config = load_config()
    config_path = Path('config/config.yaml')
    
    # WiFi-Manager initialisieren und prüfen
    logger.info("Prüfe WiFi-Verbindung...")
    from utils.wifi_manager import WiFiManager
    wifi_config = config.get('wifi', {})
    wifi_manager = WiFiManager(
        ap_ssid=wifi_config.get('ap_ssid', 'MGB-Setup'),
        ap_password=wifi_config.get('ap_password', 'pilzzucht2025'),
        check_interval=wifi_config.get('check_interval', 30),
        max_retries=wifi_config.get('max_retries', 3)
    )
    
    # Automatische WiFi-Verwaltung (startet AP falls keine Verbindung)
    wifi_manager.auto_manage()
    
    if wifi_manager.ap_mode:
        logger.info("=" * 60)
        logger.info("WICHTIG: System läuft im Access Point Modus!")
        logger.info(f"SSID: {wifi_manager.ap_ssid}")
        logger.info(f"Passwort: {wifi_manager.ap_password}")
        logger.info("Verbinden Sie sich mit diesem Netzwerk und öffnen Sie:")
        logger.info("http://192.168.4.1/wifi/setup")
        logger.info("=" * 60)
    
    # DataLogger initialisieren
    data_logger = DataLogger()
    logger.info("DataLogger initialisiert")
    
    # Sensoren initialisieren
    logger.info("Initialisiere Sensoren...")
    sensors = {}
    
    try:
        from sensors.scd30_sensor import SCD30Sensor
        
        # Sensor-Konfiguration aus config.yaml
        sensor_config = config.get('sensors', {}).get('co2', {})
        scd30 = SCD30Sensor(sensor_config)
        
        if scd30._available:
            sensors['scd30'] = scd30
            if scd30.is_mock_mode():
                logger.warning("✗ SCD30 im Mock-Modus (nur Testwerte)")
            else:
                logger.info("✓ SCD30 Sensor initialisiert (Hardware-Modus)")
        else:
            logger.warning("✗ SCD30 Sensor nicht verfügbar")
    except Exception as e:
        logger.error(f"✗ Fehler beim Initialisieren des SCD30: {e}", exc_info=True)
    
    # Aktoren initialisieren
    logger.info("Initialisiere Aktoren...")
    actuators = {}
    
    try:
        from actuators.relay_actuator import RelayActuator
        
        # Heizmatte (Relay)
        heater_config = config.get('actuators', {}).get('heater', {})
        if heater_config.get('enabled', False):
            heater = RelayActuator(
                name='heater',
                pin=heater_config.get('pin', 27),
                config=heater_config
            )
            if heater.is_available:
                actuators['heater'] = heater
                if heater.is_mock_mode():
                    logger.warning("✗ Heizmatte im Mock-Modus (nur Testwerte)")
                else:
                    logger.info("✓ Heizmatte initialisiert auf GPIO Pin " + str(heater_config.get('pin', 27)))
            else:
                logger.warning("✗ Heizmatte nicht verfügbar")
        
        # Pumpe (Relay)
        pump_config = config.get('actuators', {}).get('pump', {})
        if pump_config.get('enabled', False):
            pump = RelayActuator(
                name='pump',
                pin=pump_config.get('pin', 17),
                config=pump_config
            )
            if pump.is_available:
                actuators['pump'] = pump
                if pump.is_mock_mode():
                    logger.warning("✗ Pumpe im Mock-Modus (nur Testwerte)")
                else:
                    logger.info("✓ Pumpe initialisiert auf GPIO Pin " + str(pump_config.get('pin', 17)))
            else:
                logger.warning("✗ Pumpe nicht verfügbar")
                
    except Exception as e:
        logger.error(f"✗ Fehler beim Initialisieren der Aktoren: {e}", exc_info=True)
    
    # PID-Controller initialisieren
    logger.info("Initialisiere PID-Controller...")
    controllers = {}
    
    try:
        from controllers.pid_controller import PIDController
        
        # Temperatur-Controller
        pid_config = config.get('pid', {})
        temp_pid_config = pid_config.get('temperature', {})
        
        temp_controller = PIDController(
            kp=temp_pid_config.get('kp', 2.0),
            ki=temp_pid_config.get('ki', 0.5),
            kd=temp_pid_config.get('kd', 1.0),
            setpoint=config['sensors']['temperature']['target_value'],
            output_min=0.0,
            output_max=100.0,
            adaptive=pid_config.get('adaptive', True),
            learning_rate=pid_config.get('learning_rate', 0.01)
        )
        
        # Log-Ausgabe
        if pid_config.get('adaptive', True):
            logger.info("✓ Temperatur-PID-Controller initialisiert (Adaptive Regelung AN)")
        else:
            logger.info("✓ Temperatur-PID-Controller initialisiert (Manuelle Parameter)")
        
        controllers['temperature'] = temp_controller
        
    except Exception as e:
        logger.error(f"✗ Fehler beim Initialisieren der PID-Controller: {e}", exc_info=True)
    
    # Webserver in separatem Thread starten
    web_thread = Thread(target=start_web_server, args=(config, sensors, actuators), daemon=True)
    web_thread.start()
    logger.info("Webserver-Thread gestartet")
    
    # Monitoring-Loop starten
    try:
        monitoring_loop(config, data_logger, sensors, actuators, controllers, str(config_path))
    except Exception as e:
        logger.error(f"Kritischer Fehler: {e}", exc_info=True)
    finally:
        # Aufräumen
        logger.info("Fahre System herunter...")
        
        # Alle Aktoren ausschalten
        for name, actuator in actuators.items():
            try:
                actuator.turn_off()
                actuator.cleanup()
                logger.info(f"✓ Aktor '{name}' heruntergefahren")
            except Exception as e:
                logger.error(f"Fehler beim Herunterfahren von '{name}': {e}")
        
        logger.info("System beendet")


if __name__ == '__main__':
    main()
