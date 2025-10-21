"""
WiFi-Setup Webinterface für Access Point Modus
"""

from flask import Blueprint, render_template, request, jsonify
import logging
import sys
from pathlib import Path

# Importiere WiFiManager
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.wifi_manager import WiFiManager

logger = logging.getLogger(__name__)

# Blueprint für WiFi-Setup
wifi_bp = Blueprint('wifi', __name__, url_prefix='/wifi')

# WiFi-Manager Instanz
wifi_manager = None


def init_wifi_manager(manager: WiFiManager):
    """
    Initialisiert den WiFi-Manager für dieses Blueprint
    
    Args:
        manager: WiFiManager Instanz
    """
    global wifi_manager
    wifi_manager = manager


@wifi_bp.route('/setup')
def setup_page():
    """
    Zeigt die WiFi-Setup Seite
    """
    return render_template('wifi_setup.html')


@wifi_bp.route('/api/scan', methods=['GET'])
def scan_networks():
    """
    Scannt nach verfügbaren WLAN-Netzwerken
    """
    try:
        if not wifi_manager:
            return jsonify({'error': 'WiFi-Manager nicht initialisiert'}), 500
        
        networks = wifi_manager.get_available_networks()
        
        return jsonify({
            'status': 'success',
            'networks': networks
        })
        
    except Exception as e:
        logger.error(f"Fehler beim Scannen: {e}")
        return jsonify({'error': str(e)}), 500


@wifi_bp.route('/api/connect', methods=['POST'])
def connect_network():
    """
    Verbindet mit einem WLAN-Netzwerk
    """
    try:
        if not wifi_manager:
            return jsonify({'error': 'WiFi-Manager nicht initialisiert'}), 500
        
        data = request.get_json()
        ssid = data.get('ssid')
        password = data.get('password')
        
        if not ssid:
            return jsonify({'error': 'SSID erforderlich'}), 400
        
        logger.info(f"Verbindungsversuch zu '{ssid}'...")
        
        # Versuche Verbindung
        success = wifi_manager.connect_to_network(ssid, password)
        
        if success:
            # Stoppe Access Point
            wifi_manager.stop_access_point()
            
            return jsonify({
                'status': 'success',
                'message': f'Erfolgreich mit {ssid} verbunden'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': f'Verbindung zu {ssid} fehlgeschlagen'
            }), 500
        
    except Exception as e:
        logger.error(f"Fehler beim Verbinden: {e}")
        return jsonify({'error': str(e)}), 500


@wifi_bp.route('/api/status', methods=['GET'])
def wifi_status():
    """
    Gibt den aktuellen WiFi-Status zurück
    """
    try:
        if not wifi_manager:
            return jsonify({'error': 'WiFi-Manager nicht initialisiert'}), 500
        
        return jsonify({
            'ap_mode': wifi_manager.ap_mode,
            'ap_ssid': wifi_manager.ap_ssid,
            'connected': wifi_manager.is_connected(),
            'is_raspberry_pi': wifi_manager.is_raspberry_pi
        })
        
    except Exception as e:
        logger.error(f"Fehler beim Abrufen des Status: {e}")
        return jsonify({'error': str(e)}), 500


@wifi_bp.route('/api/restart-ap', methods=['POST'])
def restart_ap():
    """
    Startet den Access Point neu
    """
    try:
        if not wifi_manager:
            return jsonify({'error': 'WiFi-Manager nicht initialisiert'}), 500
        
        wifi_manager.start_access_point()
        
        return jsonify({
            'status': 'success',
            'message': 'Access Point neu gestartet'
        })
        
    except Exception as e:
        logger.error(f"Fehler beim Neustart des AP: {e}")
        return jsonify({'error': str(e)}), 500
