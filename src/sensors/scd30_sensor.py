"""
SCD30 Sensor für Temperatur, Luftfeuchtigkeit und CO2-Messung
"""

import time
from typing import Optional, Dict, Any, Tuple
from .base_sensor import BaseSensor

try:
    import board
    import adafruit_scd30
    MOCK_MODE = False
except (ImportError, NotImplementedError):
    MOCK_MODE = True
    print("⚠️  SCD30-Bibliotheken nicht verfügbar - verwende Mock-Modus für Entwicklung")


class SCD30Sensor:
    """
    SCD30 Sensor für kombinierte Messungen von Temperatur, Luftfeuchtigkeit und CO2
    """
    
    def __init__(self, i2c_bus=None):
        """
        Initialisiert den SCD30 Sensor
        
        Args:
            i2c_bus: I2C-Bus (optional, wird automatisch erkannt wenn None)
        """
        self.is_available = False
        self.scd30 = None
        self.last_temperature: Optional[float] = None
        self.last_humidity: Optional[float] = None
        self.last_co2: Optional[float] = None
        self.last_read_time: Optional[float] = None
        self.mock_mode = MOCK_MODE
        
        if not self.mock_mode:
            try:
                # I2C-Bus initialisieren
                if i2c_bus is None:
                    i2c_bus = board.I2C()
                
                # SCD30 initialisieren
                self.scd30 = adafruit_scd30.SCD30(i2c_bus)
                
                # Messintervall setzen (in Sekunden)
                # Der SCD30 benötigt mindestens 2 Sekunden zwischen Messungen
                self.scd30.measurement_interval = 2
                
                self.is_available = True
                print("✓ SCD30 Sensor erfolgreich initialisiert")
                
            except Exception as e:
                print(f"✗ Fehler beim Initialisieren des SCD30: {e}")
                self.is_available = False
        else:
            # Mock-Modus für Entwicklung
            self.is_available = True
            print("✓ SCD30 Mock-Modus aktiviert")
    
    def read_all(self) -> Optional[Tuple[float, float, float]]:
        """
        Liest alle Werte vom Sensor (Temperatur, Luftfeuchtigkeit, CO2)
        
        Returns:
            Tuple (temperature, humidity, co2) oder None bei Fehler
        """
        if not self.is_available:
            return None
        
        try:
            if self.mock_mode:
                # Mock-Daten für Entwicklung
                import random
                temperature = 22.0 + random.uniform(-2, 2)
                humidity = 85.0 + random.uniform(-5, 5)
                co2 = 800.0 + random.uniform(-100, 100)
            else:
                # Warte auf neue Daten (SCD30 benötigt Zeit für Messung)
                if not self.scd30.data_available:
                    time.sleep(0.5)
                    if not self.scd30.data_available:
                        return None
                
                # Daten auslesen
                temperature = self.scd30.temperature
                humidity = self.scd30.relative_humidity
                co2 = self.scd30.CO2
            
            # Werte speichern
            self.last_temperature = round(temperature, 2)
            self.last_humidity = round(humidity, 2)
            self.last_co2 = round(co2, 1)
            self.last_read_time = time.time()
            
            return (self.last_temperature, self.last_humidity, self.last_co2)
            
        except Exception as e:
            print(f"✗ Fehler beim Lesen des SCD30: {e}")
            return None
    
    def read_temperature(self) -> Optional[float]:
        """
        Liest nur die Temperatur
        
        Returns:
            Temperatur in °C oder None bei Fehler
        """
        result = self.read_all()
        return result[0] if result else None
    
    def read_humidity(self) -> Optional[float]:
        """
        Liest nur die Luftfeuchtigkeit
        
        Returns:
            Luftfeuchtigkeit in % oder None bei Fehler
        """
        result = self.read_all()
        return result[1] if result else None
    
    def read_co2(self) -> Optional[float]:
        """
        Liest nur den CO2-Wert
        
        Returns:
            CO2 in ppm oder None bei Fehler
        """
        result = self.read_all()
        return result[2] if result else None
    
    def get_status(self) -> Dict[str, Any]:
        """
        Gibt den Status des Sensors zurück
        
        Returns:
            Dictionary mit Statusinformationen
        """
        return {
            'sensor': 'SCD30',
            'available': self.is_available,
            'mock_mode': self.mock_mode,
            'last_values': {
                'temperature': self.last_temperature,
                'humidity': self.last_humidity,
                'co2': self.last_co2
            },
            'last_read_time': self.last_read_time
        }
    
    def calibrate_forced_recalibration(self, co2_ppm: int = 400):
        """
        Erzwingt eine CO2-Kalibrierung (Forced Recalibration - FRC)
        Verwende dies nur, wenn du sicher bist, dass der aktuelle CO2-Wert bekannt ist!
        
        Args:
            co2_ppm: Bekannter CO2-Wert in ppm (Standard: 400 ppm für Frischluft)
        """
        if not self.is_available or self.mock_mode:
            print("⚠️  Kalibrierung nicht verfügbar (Mock-Modus oder Sensor nicht verfügbar)")
            return
        
        try:
            self.scd30.forced_recalibration_reference = co2_ppm
            print(f"✓ CO2-Kalibrierung auf {co2_ppm} ppm gesetzt")
        except Exception as e:
            print(f"✗ Fehler bei der Kalibrierung: {e}")
    
    def set_temperature_offset(self, offset_celsius: float):
        """
        Setzt einen Temperatur-Offset zur Kompensation von Eigenerwärmung
        
        Args:
            offset_celsius: Offset in °C (typisch 2-4°C)
        """
        if not self.is_available or self.mock_mode:
            print("⚠️  Temperatur-Offset nicht verfügbar (Mock-Modus oder Sensor nicht verfügbar)")
            return
        
        try:
            self.scd30.temperature_offset = offset_celsius
            print(f"✓ Temperatur-Offset auf {offset_celsius}°C gesetzt")
        except Exception as e:
            print(f"✗ Fehler beim Setzen des Temperatur-Offsets: {e}")
    
    def set_altitude_compensation(self, altitude_meters: int):
        """
        Setzt die Höhenkompensation für präzisere CO2-Messungen
        
        Args:
            altitude_meters: Höhe über dem Meeresspiegel in Metern
        """
        if not self.is_available or self.mock_mode:
            print("⚠️  Höhenkompensation nicht verfügbar (Mock-Modus oder Sensor nicht verfügbar)")
            return
        
        try:
            self.scd30.altitude = altitude_meters
            print(f"✓ Höhenkompensation auf {altitude_meters}m gesetzt")
        except Exception as e:
            print(f"✗ Fehler beim Setzen der Höhenkompensation: {e}")


# Kompatibilitäts-Wrapper für einzelne Sensoren
class SCD30Temperature(BaseSensor):
    """Temperatur-Sensor-Wrapper für SCD30"""
    
    def __init__(self, scd30_instance: SCD30Sensor):
        super().__init__("Temperature (SCD30)", "°C")
        self.scd30 = scd30_instance
        self.is_available = scd30_instance.is_available
    
    def initialize(self) -> bool:
        return self.is_available
    
    def read(self) -> Optional[float]:
        value = self.scd30.read_temperature()
        if value is not None:
            self.last_value = value
            from datetime import datetime
            self.last_read_time = datetime.now()
        return value


class SCD30Humidity(BaseSensor):
    """Luftfeuchtigkeits-Sensor-Wrapper für SCD30"""
    
    def __init__(self, scd30_instance: SCD30Sensor):
        super().__init__("Humidity (SCD30)", "%")
        self.scd30 = scd30_instance
        self.is_available = scd30_instance.is_available
    
    def initialize(self) -> bool:
        return self.is_available
    
    def read(self) -> Optional[float]:
        value = self.scd30.read_humidity()
        if value is not None:
            self.last_value = value
            from datetime import datetime
            self.last_read_time = datetime.now()
        return value


class SCD30CO2(BaseSensor):
    """CO2-Sensor-Wrapper für SCD30"""
    
    def __init__(self, scd30_instance: SCD30Sensor):
        super().__init__("CO2 (SCD30)", "ppm")
        self.scd30 = scd30_instance
        self.is_available = scd30_instance.is_available
    
    def initialize(self) -> bool:
        return self.is_available
    
    def read(self) -> Optional[float]:
        value = self.scd30.read_co2()
        if value is not None:
            self.last_value = value
            from datetime import datetime
            self.last_read_time = datetime.now()
        return value
