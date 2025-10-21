"""
WiFi-Manager für automatisches Fallback auf Access Point
"""

import subprocess
import time
import os
import logging
from pathlib import Path
from typing import Optional, List, Dict

logger = logging.getLogger(__name__)


class WiFiManager:
    """
    Verwaltet WiFi-Verbindungen und erstellt bei Bedarf einen Access Point
    """
    
    def __init__(self, 
                 ap_ssid: str = "MGB-Setup",
                 ap_password: str = "pilzzucht2025",
                 check_interval: int = 30,
                 max_retries: int = 3):
        """
        Initialisiert den WiFi-Manager
        
        Args:
            ap_ssid: SSID des Access Points
            ap_password: Passwort des Access Points (min. 8 Zeichen)
            check_interval: Intervall für Verbindungsprüfung in Sekunden
            max_retries: Maximale Anzahl Verbindungsversuche
        """
        self.ap_ssid = ap_ssid
        self.ap_password = ap_password
        self.check_interval = check_interval
        self.max_retries = max_retries
        self.ap_mode = False
        self.is_raspberry_pi = self._check_if_raspberry_pi()
    
    def _check_if_raspberry_pi(self) -> bool:
        """
        Prüft, ob das System ein Raspberry Pi ist
        
        Returns:
            True wenn Raspberry Pi, sonst False
        """
        try:
            with open('/proc/cpuinfo', 'r') as f:
                cpuinfo = f.read()
                return 'Raspberry Pi' in cpuinfo or 'BCM' in cpuinfo
        except:
            return False
    
    def is_connected(self) -> bool:
        """
        Prüft, ob eine WLAN-Verbindung besteht
        
        Returns:
            True wenn verbunden, sonst False
        """
        if not self.is_raspberry_pi:
            logger.info("Kein Raspberry Pi - simuliere Verbindung")
            return True
        
        try:
            # Prüfe WLAN-Status
            result = subprocess.run(
                ['iwgetid', '-r'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            connected = result.returncode == 0 and result.stdout.strip() != ''
            
            if connected:
                ssid = result.stdout.strip()
                logger.info(f"Mit WLAN '{ssid}' verbunden")
            else:
                logger.warning("Keine WLAN-Verbindung")
            
            return connected
            
        except Exception as e:
            logger.error(f"Fehler beim Prüfen der WLAN-Verbindung: {e}")
            return False
    
    def get_available_networks(self) -> List[Dict[str, str]]:
        """
        Scannt nach verfügbaren WLAN-Netzwerken
        
        Returns:
            Liste von Netzwerken mit SSID und Signalstärke
        """
        if not self.is_raspberry_pi:
            return [
                {'ssid': 'Beispiel-WLAN', 'signal': '75', 'security': 'WPA2'},
                {'ssid': 'Nachbar-WiFi', 'signal': '45', 'security': 'WPA2'}
            ]
        
        try:
            result = subprocess.run(
                ['sudo', 'iwlist', 'wlan0', 'scan'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            networks = []
            current_network = {}
            
            for line in result.stdout.split('\n'):
                line = line.strip()
                
                if 'ESSID:' in line:
                    ssid = line.split('ESSID:')[1].strip('"')
                    if ssid:
                        current_network['ssid'] = ssid
                
                elif 'Quality=' in line:
                    # Extrahiere Signalqualität
                    quality = line.split('Quality=')[1].split()[0]
                    current_network['signal'] = quality
                
                elif 'Encryption key:' in line:
                    encrypted = 'on' in line.lower()
                    current_network['security'] = 'WPA2' if encrypted else 'Open'
                    
                    if current_network.get('ssid'):
                        networks.append(current_network.copy())
                        current_network = {}
            
            return networks
            
        except Exception as e:
            logger.error(f"Fehler beim Scannen nach Netzwerken: {e}")
            return []
    
    def connect_to_network(self, ssid: str, password: str) -> bool:
        """
        Verbindet mit einem WLAN-Netzwerk
        
        Args:
            ssid: SSID des Netzwerks
            password: Passwort des Netzwerks
            
        Returns:
            True bei Erfolg, sonst False
        """
        if not self.is_raspberry_pi:
            logger.info(f"Simuliere Verbindung zu '{ssid}'")
            return True
        
        try:
            logger.info(f"Versuche Verbindung zu '{ssid}'...")
            
            # WPA Supplicant Konfiguration erstellen
            wpa_config = f"""
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=DE

network={{
    ssid="{ssid}"
    psk="{password}"
    key_mgmt=WPA-PSK
}}
"""
            
            # Backup der alten Konfiguration
            config_path = '/etc/wpa_supplicant/wpa_supplicant.conf'
            backup_path = '/etc/wpa_supplicant/wpa_supplicant.conf.backup'
            
            subprocess.run(['sudo', 'cp', config_path, backup_path], check=False)
            
            # Neue Konfiguration schreiben
            with open('/tmp/wpa_supplicant.conf', 'w') as f:
                f.write(wpa_config)
            
            subprocess.run(
                ['sudo', 'mv', '/tmp/wpa_supplicant.conf', config_path],
                check=True
            )
            
            # WPA Supplicant neu starten
            subprocess.run(['sudo', 'wpa_cli', '-i', 'wlan0', 'reconfigure'], check=True)
            
            # Warte auf Verbindung
            time.sleep(5)
            
            # Prüfe Verbindung
            for attempt in range(self.max_retries):
                if self.is_connected():
                    logger.info(f"Erfolgreich mit '{ssid}' verbunden")
                    return True
                time.sleep(2)
            
            logger.error(f"Verbindung zu '{ssid}' fehlgeschlagen")
            return False
            
        except Exception as e:
            logger.error(f"Fehler beim Verbinden: {e}")
            return False
    
    def start_access_point(self) -> bool:
        """
        Startet den Access Point Modus
        
        Returns:
            True bei Erfolg, sonst False
        """
        if not self.is_raspberry_pi:
            logger.info("Simuliere Access Point Start")
            self.ap_mode = True
            return True
        
        try:
            logger.info(f"Starte Access Point '{self.ap_ssid}'...")
            
            # Stoppe WPA Supplicant
            subprocess.run(['sudo', 'systemctl', 'stop', 'wpa_supplicant'], check=False)
            
            # Erstelle hostapd Konfiguration
            hostapd_config = f"""
interface=wlan0
driver=nl80211
ssid={self.ap_ssid}
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase={self.ap_password}
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
"""
            
            with open('/tmp/hostapd.conf', 'w') as f:
                f.write(hostapd_config)
            
            subprocess.run(['sudo', 'mv', '/tmp/hostapd.conf', '/etc/hostapd/hostapd.conf'], check=True)
            
            # Erstelle dnsmasq Konfiguration
            dnsmasq_config = """
interface=wlan0
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
"""
            
            with open('/tmp/dnsmasq.conf', 'w') as f:
                f.write(dnsmasq_config)
            
            subprocess.run(['sudo', 'mv', '/tmp/dnsmasq.conf', '/etc/dnsmasq.conf'], check=True)
            
            # Konfiguriere Netzwerk-Interface
            subprocess.run(['sudo', 'ip', 'link', 'set', 'wlan0', 'down'], check=True)
            subprocess.run(['sudo', 'ip', 'addr', 'flush', 'dev', 'wlan0'], check=True)
            subprocess.run(['sudo', 'ip', 'addr', 'add', '192.168.4.1/24', 'dev', 'wlan0'], check=True)
            subprocess.run(['sudo', 'ip', 'link', 'set', 'wlan0', 'up'], check=True)
            
            # Starte Services
            subprocess.run(['sudo', 'systemctl', 'start', 'hostapd'], check=True)
            subprocess.run(['sudo', 'systemctl', 'start', 'dnsmasq'], check=True)
            
            self.ap_mode = True
            logger.info(f"Access Point '{self.ap_ssid}' gestartet auf 192.168.4.1")
            logger.info(f"Passwort: {self.ap_password}")
            
            return True
            
        except Exception as e:
            logger.error(f"Fehler beim Starten des Access Points: {e}")
            return False
    
    def stop_access_point(self) -> bool:
        """
        Stoppt den Access Point Modus
        
        Returns:
            True bei Erfolg, sonst False
        """
        if not self.is_raspberry_pi:
            logger.info("Simuliere Access Point Stop")
            self.ap_mode = False
            return True
        
        try:
            logger.info("Stoppe Access Point...")
            
            # Stoppe Services
            subprocess.run(['sudo', 'systemctl', 'stop', 'hostapd'], check=False)
            subprocess.run(['sudo', 'systemctl', 'stop', 'dnsmasq'], check=False)
            
            # Stelle normale WLAN-Verbindung wieder her
            subprocess.run(['sudo', 'systemctl', 'start', 'wpa_supplicant'], check=True)
            subprocess.run(['sudo', 'wpa_cli', '-i', 'wlan0', 'reconfigure'], check=True)
            
            self.ap_mode = False
            logger.info("Access Point gestoppt, normale WLAN-Verbindung wiederhergestellt")
            
            return True
            
        except Exception as e:
            logger.error(f"Fehler beim Stoppen des Access Points: {e}")
            return False
    
    def auto_manage(self) -> None:
        """
        Automatische Verwaltung: Startet AP wenn keine Verbindung besteht
        """
        logger.info("Starte automatische WiFi-Verwaltung...")
        
        # Prüfe initial die Verbindung
        retries = 0
        while retries < self.max_retries:
            if self.is_connected():
                logger.info("WLAN-Verbindung erfolgreich")
                return
            
            retries += 1
            logger.warning(f"Keine WLAN-Verbindung (Versuch {retries}/{self.max_retries})")
            time.sleep(5)
        
        # Keine Verbindung - starte Access Point
        logger.warning("Keine WLAN-Verbindung möglich - starte Access Point Modus")
        self.start_access_point()
