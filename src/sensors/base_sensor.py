"""
Basis-Klasse für alle Sensoren
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Dict, Any


class BaseSensor(ABC):
    """
    Abstrakte Basisklasse für alle Sensoren
    """
    
    def __init__(self, name: str, unit: str):
        """
        Initialisiert den Sensor
        
        Args:
            name: Name des Sensors
            unit: Einheit der Messwerte (z.B. "°C", "%", "ppm")
        """
        self.name = name
        self.unit = unit
        self.last_value: Optional[float] = None
        self.last_read_time: Optional[datetime] = None
        self.is_available: bool = False
    
    @abstractmethod
    def read(self) -> Optional[float]:
        """
        Liest den aktuellen Wert vom Sensor
        
        Returns:
            Gemessener Wert oder None bei Fehler
        """
        pass
    
    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialisiert den Sensor
        
        Returns:
            True bei Erfolg, False bei Fehler
        """
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """
        Gibt den Status des Sensors zurück
        
        Returns:
            Dictionary mit Statusinformationen
        """
        return {
            'name': self.name,
            'unit': self.unit,
            'available': self.is_available,
            'last_value': self.last_value,
            'last_read_time': self.last_read_time.isoformat() if self.last_read_time else None
        }
