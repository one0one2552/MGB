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


def monitoring_loop(config: dict, data_logger: DataLogger, sensors: dict):
    """
    Hauptschleife für Überwachung und Regelung
    
    Args:
        config: Konfiguration
        data_logger: DataLogger-Instanz
        sensors: Dictionary mit Sensor-Instanzen
    """
    interval = config['measurement']['interval']
    logger.info(f"Starte Monitoring-Loop (Intervall: {interval}s)")
    
    while not stop_event.is_set():
        try:
            # Sensoren auslesen
            if 'scd30' in sensors:
                scd30 = sensors['scd30']
                result = scd30.read_all()
                
                if result:
                    temperature, humidity, co2 = result
                    logger.info(f"SCD30: Temp={temperature}°C, Humidity={humidity}%, CO2={co2}ppm")
                    
                    # Daten loggen
                    data_logger.log_measurement('temperature', temperature)
                    data_logger.log_measurement('humidity', humidity)
                    data_logger.log_measurement('co2', co2)
            
            # TODO: Regelung durchführen
            # TODO: Aktoren steuern
            
            # Auf nächsten Zyklus warten
            stop_event.wait(interval)
            
        except Exception as e:
            logger.error(f"Fehler im Monitoring-Loop: {e}", exc_info=True)
            time.sleep(5)  # Kurze Pause bei Fehler


def start_web_server(config: dict, sensors: dict):
    """
    Startet den Webserver in einem separaten Thread
    
    Args:
        config: Konfiguration
        sensors: Dictionary mit Sensor-Instanzen
    """
    from web.app import app, socketio
    import web.app as web_app
    
    # Sensoren an Web-App übergeben
    web_app.sensors = sensors
    
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
        scd30 = SCD30Sensor()
        if scd30.is_available:
            sensors['scd30'] = scd30
            logger.info("✓ SCD30 Sensor initialisiert")
        else:
            logger.warning("✗ SCD30 Sensor nicht verfügbar")
    except Exception as e:
        logger.error(f"✗ Fehler beim Initialisieren des SCD30: {e}")
    
    # TODO: Aktoren initialisieren
    
    # Webserver in separatem Thread starten
    web_thread = Thread(target=start_web_server, args=(config, sensors), daemon=True)
    web_thread.start()
    logger.info("Webserver-Thread gestartet")
    
    # Monitoring-Loop starten
    try:
        monitoring_loop(config, data_logger, sensors)
    except Exception as e:
        logger.error(f"Kritischer Fehler: {e}", exc_info=True)
    finally:
        # Aufräumen
        logger.info("Fahre System herunter...")
        # TODO: Alle Aktoren ausschalten
        # TODO: Verbindungen schließen
        logger.info("System beendet")


if __name__ == '__main__':
    main()
