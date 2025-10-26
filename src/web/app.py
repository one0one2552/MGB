"""
Flask-Webserver für die MGB - Mushroom Grow Box
"""

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import yaml
from pathlib import Path
import logging
import sys

# Pfad für Imports hinzufügen
sys.path.insert(0, str(Path(__file__).parent.parent))

# WiFi-Setup und Übersetzungen importieren
from web.wifi_setup import wifi_bp, init_wifi_manager
from utils.wifi_manager import WiFiManager
from utils.translations import get_translations, get_available_languages

# Logger einrichten
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask-App initialisieren
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mgb_mushroom_grow_box_secret_key_2025'
socketio = SocketIO(app, cors_allowed_origins="*")

# WiFi-Blueprint registrieren
app.register_blueprint(wifi_bp)

# Konfiguration laden
config_path = Path(__file__).parent.parent.parent / 'config' / 'config.yaml'
with open(config_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

# WiFi-Manager initialisieren
wifi_manager = WiFiManager(
    ap_ssid=config.get('wifi', {}).get('ap_ssid', 'MGB-Setup'),
    ap_password=config.get('wifi', {}).get('ap_password', 'pilzzucht2025')
)
init_wifi_manager(wifi_manager)

# Globale Variable für Sensoren (wird von main.py gesetzt)
sensors = {}


@app.route('/')
def index():
    """
    Hauptseite der Weboberfläche
    """
    return render_template('index.html')


@app.route('/settings')
def settings():
    """
    Einstellungsseite
    """
    return render_template('settings.html')


@app.route('/api/status')
def get_status():
    """
    API-Endpunkt für den aktuellen Status
    """
    # Echte Daten von SCD30 Sensor holen (wenn verfügbar)
    temp_value = 22.5
    humidity_value = 87.3
    co2_value = 850
    
    if 'scd30' in sensors:
        scd30 = sensors['scd30']
        result = scd30.read_all()
        if result:
            temp_value = result['temperature']
            humidity_value = result['humidity']
            co2_value = result['co2']
    
    status = {
        'sensors': {
            'temperature': {
                'value': temp_value,
                'unit': '°C',
                'target': config['sensors']['temperature']['target_value'],
                'status': 'ok'
            },
            'humidity': {
                'value': humidity_value,
                'unit': '%',
                'target': config['sensors']['humidity']['target_value'],
                'status': 'ok'
            },
            'co2': {
                'value': co2_value,
                'unit': 'ppm',
                'target': config['sensors']['co2']['target_value'],
                'status': 'ok'
            }
        },
        'actuators': {
            'pump': {'active': False, 'available': True},
            'heater': {'active': True, 'available': True},
            'fan': {'active': False, 'available': True, 'speed': 0}
        },
        'mode': 'automatic',
        'alarms': []
    }
    return jsonify(status)


@app.route('/api/config', methods=['GET'])
def get_config():
    """
    API-Endpunkt zum Lesen der Konfiguration
    """
    return jsonify(config)


@app.route('/api/history')
def get_history():
    """
    API-Endpunkt für historische Sensor-Daten
    
    Query-Parameter:
        hours: Anzahl der Stunden (z.B. 1, 12, 24, 168=Woche, 720=Monat)
    """
    from utils.data_logger import DataLogger
    from datetime import datetime, timedelta
    
    # Zeitbereich aus Query-Parameter lesen
    hours = request.args.get('hours', default=24, type=int)
    
    # DataLogger initialisieren
    data_logger = DataLogger()
    
    # Zeitstempel berechnen
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=hours)
    
    # Intervall für Datenpunkte bestimmen (in Sekunden)
    # Ziel: ca. 100-200 Datenpunkte für optimale Chart-Darstellung
    if hours <= 1:
        interval_seconds = 60  # 1 Stunde: alle 60s = ~60 Punkte
    elif hours <= 12:
        interval_seconds = 300  # 12 Stunden: alle 5min = ~144 Punkte
    elif hours <= 24:
        interval_seconds = 600  # 24 Stunden: alle 10min = ~144 Punkte
    elif hours <= 168:  # 1 Woche
        interval_seconds = 3600  # 1 Woche: alle 60min = ~168 Punkte
    else:  # 1 Monat
        interval_seconds = 7200  # 1 Monat: alle 2h = ~360 Punkte
    
    # Daten aus DB holen mit Zeitfilter
    all_data = data_logger.get_sensor_data(
        limit=10000, 
        start_time=start_time, 
        end_time=end_time
    )
    
    # Nach Sensor gruppieren und nach Zeitstempel sortieren
    sensor_data = {
        'temperature': [],
        'humidity': [],
        'co2': []
    }
    
    for record in all_data:
        try:
            if record['sensor_name'] == 'temperature':
                sensor_data['temperature'].append({
                    'timestamp': datetime.fromisoformat(record['timestamp']),
                    'value': record['value']
                })
            elif record['sensor_name'] == 'humidity':
                sensor_data['humidity'].append({
                    'timestamp': datetime.fromisoformat(record['timestamp']),
                    'value': record['value']
                })
            elif record['sensor_name'] == 'co2':
                sensor_data['co2'].append({
                    'timestamp': datetime.fromisoformat(record['timestamp']),
                    'value': record['value']
                })
        except Exception as e:
            logger.error(f"Fehler beim Verarbeiten von Datensatz: {e}")
            continue
    
    # Daten nach Zeitstempel sortieren (älteste zuerst)
    for sensor_name in sensor_data:
        sensor_data[sensor_name].sort(key=lambda x: x['timestamp'])
    
    # Daten reduzieren basierend auf Intervall
    def reduce_data(data, interval_seconds):
        """Reduziert Datenpunkte basierend auf Zeitintervall mit gleichmäßiger Verteilung"""
        if not data:
            return []
        
        if len(data) == 1:
            return [{
                'timestamp': data[0]['timestamp'].isoformat(),
                'value': data[0]['value']
            }]
        
        reduced = []
        
        # Ersten Punkt immer nehmen
        reduced.append({
            'timestamp': data[0]['timestamp'].isoformat(),
            'value': data[0]['value']
        })
        
        last_added_timestamp = data[0]['timestamp']
        
        # Durch alle Datenpunkte iterieren (außer erster und letzter)
        for i in range(1, len(data) - 1):
            point = data[i]
            time_diff = (point['timestamp'] - last_added_timestamp).total_seconds()
            
            # Nur Punkte nehmen, die mindestens interval_seconds auseinander liegen
            if time_diff >= interval_seconds:
                reduced.append({
                    'timestamp': point['timestamp'].isoformat(),
                    'value': point['value']
                })
                last_added_timestamp = point['timestamp']
        
        # Letzten Punkt nur hinzufügen, wenn er weit genug vom vorletzten entfernt ist
        last_point = data[-1]
        time_diff_last = (last_point['timestamp'] - last_added_timestamp).total_seconds()
        
        if time_diff_last >= interval_seconds or len(reduced) == 1:
            # Letzten Punkt hinzufügen, wenn Intervall erfüllt oder nur ein Punkt vorhanden
            reduced.append({
                'timestamp': last_point['timestamp'].isoformat(),
                'value': last_point['value']
            })
        else:
            # Letzten hinzugefügten Punkt durch aktuellsten ersetzen
            reduced[-1] = {
                'timestamp': last_point['timestamp'].isoformat(),
                'value': last_point['value']
            }
        
        return reduced
    
    # Daten für jeden Sensor reduzieren
    temperature_data = reduce_data(sensor_data['temperature'], interval_seconds)
    humidity_data = reduce_data(sensor_data['humidity'], interval_seconds)
    co2_data = reduce_data(sensor_data['co2'], interval_seconds)
    
    return jsonify({
        'temperature': temperature_data,
        'humidity': humidity_data,
        'co2': co2_data,
        'timeRange': {
            'start': start_time.isoformat(),
            'end': end_time.isoformat(),
            'hours': hours,
            'interval_seconds': interval_seconds
        }
    })


@app.route('/api/pid/status')
def get_pid_status():
    """
    API-Endpunkt für aktuellen PID-Status (Live-Werte)
    """
    # TODO: Echte Daten von den PID-Controllern holen
    # Für jetzt Beispieldaten mit simulierten aktuellen Werten
    pid_status = {
        'temperature': {
            'kp_current': 2.15,
            'ki_current': 0.48,
            'kd_current': 1.23,
            'kp_base': config['pid']['temperature']['kp'],
            'ki_base': config['pid']['temperature']['ki'],
            'kd_base': config['pid']['temperature']['kd'],
            'avg_error': 0.3,
            'updates': 47
        },
        'humidity': {
            'kp_current': 1.58,
            'ki_current': 0.32,
            'kd_current': 0.54,
            'kp_base': config['pid']['humidity']['kp'],
            'ki_base': config['pid']['humidity']['ki'],
            'kd_base': config['pid']['humidity']['kd'],
            'avg_error': 1.2,
            'updates': 47
        },
        'co2': {
            'kp_current': 1.12,
            'ki_current': 0.19,
            'kd_current': 0.35,
            'kp_base': config['pid']['co2']['kp'],
            'ki_base': config['pid']['co2']['ki'],
            'kd_base': config['pid']['co2']['kd'],
            'avg_error': 15.5,
            'updates': 47
        },
        'adaptive': config['pid'].get('adaptive', True)
    }
    return jsonify(pid_status)


@app.route('/api/settings', methods=['POST'])
def update_settings():
    """
    API-Endpunkt zum Aktualisieren der Einstellungen
    """
    try:
        new_settings = request.get_json()
        logger.info(f"Neue Einstellungen erhalten: {new_settings}")
        
        # Konfiguration aktualisieren
        if 'sensors' in new_settings:
            if 'temperature' in new_settings['sensors']:
                config['sensors']['temperature']['target_value'] = new_settings['sensors']['temperature']['target_value']
                config['sensors']['temperature']['tolerance'] = new_settings['sensors']['temperature']['tolerance']
            
            if 'humidity' in new_settings['sensors']:
                config['sensors']['humidity']['target_value'] = new_settings['sensors']['humidity']['target_value']
                config['sensors']['humidity']['tolerance'] = new_settings['sensors']['humidity']['tolerance']
            
            if 'co2' in new_settings['sensors']:
                config['sensors']['co2']['target_value'] = new_settings['sensors']['co2']['target_value']
                config['sensors']['co2']['tolerance'] = new_settings['sensors']['co2']['tolerance']
        
        if 'schedule' in new_settings:
            config['schedule']['day_start'] = new_settings['schedule']['day_start']
            config['schedule']['night_start'] = new_settings['schedule']['night_start']
            config['schedule']['day_temperature'] = new_settings['schedule']['day_temperature']
            config['schedule']['night_temperature'] = new_settings['schedule']['night_temperature']
            config['schedule']['day_humidity'] = new_settings['schedule']['day_humidity']
            config['schedule']['night_humidity'] = new_settings['schedule']['night_humidity']
        
        if 'pid' in new_settings:
            # Adaptive Regelung aktivieren/deaktivieren
            config['pid']['adaptive'] = new_settings['pid'].get('adaptive', True)
            
            # Nur PID-Parameter aktualisieren, wenn adaptive Regelung deaktiviert ist
            if not config['pid']['adaptive']:
                if 'temperature' in new_settings['pid']:
                    config['pid']['temperature']['kp'] = new_settings['pid']['temperature']['kp']
                    config['pid']['temperature']['ki'] = new_settings['pid']['temperature']['ki']
                    config['pid']['temperature']['kd'] = new_settings['pid']['temperature']['kd']
                
                if 'humidity' in new_settings['pid']:
                    config['pid']['humidity']['kp'] = new_settings['pid']['humidity']['kp']
                    config['pid']['humidity']['ki'] = new_settings['pid']['humidity']['ki']
                    config['pid']['humidity']['kd'] = new_settings['pid']['humidity']['kd']
                
                if 'co2' in new_settings['pid']:
                    config['pid']['co2']['kp'] = new_settings['pid']['co2']['kp']
                    config['pid']['co2']['ki'] = new_settings['pid']['co2']['ki']
                    config['pid']['co2']['kd'] = new_settings['pid']['co2']['kd']
        
        # Konfiguration in Datei speichern
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
        
        logger.info("Einstellungen erfolgreich gespeichert")
        return jsonify({'status': 'success', 'message': 'Einstellungen gespeichert'})
        
    except Exception as e:
        logger.error(f"Fehler beim Speichern der Einstellungen: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/actuator/<actuator_name>/<action>', methods=['POST'])
def control_actuator(actuator_name, action):
    """
    API-Endpunkt zur manuellen Steuerung von Aktoren
    """
    if action not in ['on', 'off']:
        return jsonify({'status': 'error', 'message': 'Ungültige Aktion'}), 400
    
    # TODO: Aktor steuern
    logger.info(f"Aktor {actuator_name} wird {action} geschaltet")
    
    return jsonify({
        'status': 'success',
        'actuator': actuator_name,
        'action': action
    })


@app.route('/api/translations/<lang>')
def get_translations_endpoint(lang):
    """
    API-Endpunkt für Übersetzungen
    
    Args:
        lang: Sprachcode (de, en)
    """
    translations = get_translations(lang)
    return jsonify(translations)


@app.route('/api/languages')
def get_languages():
    """
    API-Endpunkt für verfügbare Sprachen
    """
    languages = get_available_languages()
    return jsonify(languages)


@socketio.on('connect')
def handle_connect():
    """
    WebSocket-Verbindung hergestellt
    """
    logger.info('Client verbunden')
    emit('connection_response', {'status': 'connected'})


@socketio.on('disconnect')
def handle_disconnect():
    """
    WebSocket-Verbindung getrennt
    """
    logger.info('Client getrennt')


def emit_sensor_update(sensor_data):
    """
    Sendet Sensor-Updates an alle verbundenen Clients
    
    Args:
        sensor_data: Dictionary mit Sensordaten
    """
    socketio.emit('sensor_update', sensor_data)


def emit_alarm(alarm_data):
    """
    Sendet Alarm an alle verbundenen Clients
    
    Args:
        alarm_data: Dictionary mit Alarm-Informationen
    """
    socketio.emit('alarm', alarm_data)


if __name__ == '__main__':
    # Server starten
    host = config['web']['host']
    port = config['web']['port']
    debug = config['web']['debug']
    
    logger.info(f"Starte Webserver auf {host}:{port}")
    socketio.run(app, host=host, port=port, debug=debug, allow_unsafe_werkzeug=True)
