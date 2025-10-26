"""
SCD30 CO2, Temperature and Humidity Sensor
Sensirion SCD30 - NDIR CO2 Sensor with integrated temperature and humidity sensor
"""

import time
import logging
from typing import Optional, Dict, Any
from .base_sensor import BaseSensor

# Hardware-Imports
try:
    import board
    import busio
    import adafruit_scd30
    HARDWARE_AVAILABLE = True
    print("✓ SCD30 Hardware-Bibliotheken geladen")
except (ImportError, NotImplementedError, RuntimeError) as e:
    HARDWARE_AVAILABLE = False
    print(f"⚠️  SCD30 Hardware nicht verfügbar: {e}")

logger = logging.getLogger(__name__)


class SCD30Sensor(BaseSensor):
    """SCD30 Sensor für CO2, Temperatur und Luftfeuchtigkeit"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialisiert den SCD30 Sensor
        
        Args:
            config: Sensor-Konfiguration mit temperature_offset, etc.
        """
        super().__init__("SCD30", config)
        
        self.sensor = None
        self.i2c = None
        self._mock_mode = not HARDWARE_AVAILABLE
        self._last_values = {
            'temperature': 22.0,
            'humidity': 80.0,
            'co2': 800
        }
        
        # Initialisiere Sensor
        if HARDWARE_AVAILABLE:
            try:
                # I2C Bus initialisieren
                self.i2c = busio.I2C(board.SCL, board.SDA)
                
                # SCD30 Sensor initialisieren
                self.sensor = adafruit_scd30.SCD30(self.i2c)
                
                # Konfiguration anwenden
                if 'temperature_offset' in config:
                    self.sensor.temperature_offset = config['temperature_offset']
                
                if 'altitude' in config:
                    self.sensor.altitude = config.get('altitude', 0)
                
                # Messintervall setzen (2-1800 Sekunden, Standard: 2)
                measurement_interval = config.get('measurement_interval', 2)
                self.sensor.measurement_interval = measurement_interval
                
                self._mock_mode = False
                self._available = True
                logger.info(f"✓ SCD30 Sensor erfolgreich initialisiert (Hardware-Modus)")
                print(f"✓ SCD30 Sensor gefunden und initialisiert!")
                
            except Exception as e:
                logger.error(f"Fehler bei SCD30-Initialisierung: {e}")
                print(f"✗ SCD30 Hardware-Fehler: {e}")
                self._mock_mode = True
                self._available = True  # Mock ist verfügbar
                print("⚠️  Wechsle zu Mock-Modus")
        else:
            logger.warning("SCD30 im Mock-Modus (Hardware nicht verfügbar)")
            print("✓ SCD30 Mock-Modus aktiviert")
            self._available = True
    
    def initialize(self) -> bool:
        """
        Initialisiert den Sensor (erforderlich von BaseSensor)
        
        Returns:
            True wenn erfolgreich initialisiert
        """
        return self._available
    
    def read(self) -> Optional[float]:
        """
        Liest Sensor-Werte (Hauptmethode für BaseSensor)
        Gibt Temperatur zurück für Kompatibilität
        """
        data = self.read_all()
        return data.get('temperature') if data else None
    
    def read_all(self) -> Optional[Dict[str, float]]:
        """
        Liest alle Sensor-Werte (CO2, Temperatur, Luftfeuchtigkeit)
        
        Returns:
            Dict mit 'temperature', 'humidity', 'co2' oder None bei Fehler
        """
        if self._mock_mode:
            return self._read_mock_values()
        
        try:
            # Warte auf verfügbare Daten
            max_retries = 10
            for i in range(max_retries):
                if self.sensor.data_available:
                    # Lese Werte
                    temperature = self.sensor.temperature
                    humidity = self.sensor.relative_humidity
                    co2 = self.sensor.CO2
                    
                    # Speichere letzte Werte
                    self._last_values = {
                        'temperature': round(temperature, 1),
                        'humidity': round(humidity, 1),
                        'co2': int(co2)
                    }
                    
                    return self._last_values
                
                # Warte kurz
                time.sleep(0.2)
            
            logger.warning("SCD30: Keine Daten verfügbar nach 10 Versuchen")
            return self._last_values  # Gib letzte bekannte Werte zurück
            
        except Exception as e:
            logger.error(f"Fehler beim Lesen des SCD30: {e}")
            return None
    
    def _read_mock_values(self) -> Dict[str, float]:
        """Generiert Mock-Werte für Tests"""
        import random
        
        # Simuliere leichte Schwankungen
        self._last_values['temperature'] += random.uniform(-0.5, 0.5)
        self._last_values['humidity'] += random.uniform(-2, 2)
        self._last_values['co2'] += random.randint(-50, 50)
        
        # Halte Werte in realistischen Bereichen
        self._last_values['temperature'] = max(15, min(30, self._last_values['temperature']))
        self._last_values['humidity'] = max(40, min(95, self._last_values['humidity']))
        self._last_values['co2'] = max(400, min(2000, self._last_values['co2']))
        
        return {
            'temperature': round(self._last_values['temperature'], 1),
            'humidity': round(self._last_values['humidity'], 1),
            'co2': int(self._last_values['co2'])
        }
    
    def calibrate_forced_recalibration(self, reference_co2: int = 400):
        """
        Führt eine erzwungene Kalibrierung durch (FRC - Forced Recalibration)
        
        Args:
            reference_co2: Referenz CO2-Wert in ppm (Standard: 400 ppm = Außenluft)
        """
        if self._mock_mode:
            logger.warning("Kalibrierung im Mock-Modus nicht möglich")
            return
        
        try:
            self.sensor.forced_recalibration_reference = reference_co2
            logger.info(f"SCD30 Kalibrierung durchgeführt (Referenz: {reference_co2} ppm)")
            print(f"✓ CO2-Kalibrierung erfolgreich ({reference_co2} ppm)")
        except Exception as e:
            logger.error(f"Fehler bei SCD30-Kalibrierung: {e}")
    
    def set_temperature_offset(self, offset: float):
        """
        Setzt den Temperatur-Offset zur Kompensation der Eigenerwärmung
        
        Args:
            offset: Temperatur-Offset in °C (typisch 2-4°C)
        """
        if self._mock_mode:
            logger.warning("Temperatur-Offset im Mock-Modus nicht möglich")
            return
        
        try:
            self.sensor.temperature_offset = offset
            self.config['temperature_offset'] = offset
            logger.info(f"SCD30 Temperatur-Offset gesetzt: {offset}°C")
            print(f"✓ Temperatur-Offset gesetzt: {offset}°C")
        except Exception as e:
            logger.error(f"Fehler beim Setzen des Temperatur-Offsets: {e}")
    
    def is_mock_mode(self) -> bool:
        """Gibt zurück, ob der Sensor im Mock-Modus läuft"""
        return self._mock_mode
    
    def get_sensor_info(self) -> Dict[str, Any]:
        """Gibt Sensor-Informationen zurück"""
        info = {
            'name': self.name,
            'type': 'SCD30',
            'available': self._available,
            'mock_mode': self._mock_mode,
            'measures': ['temperature', 'humidity', 'co2']
        }
        
        if not self._mock_mode and self.sensor:
            info.update({
                'temperature_offset': self.sensor.temperature_offset,
                'altitude': self.sensor.altitude,
                'measurement_interval': self.sensor.measurement_interval
            })
        
        return info