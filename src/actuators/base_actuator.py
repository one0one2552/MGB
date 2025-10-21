"""
Basis-Klasse für alle Aktoren
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Dict, Any


class BaseActuator(ABC):
    """
    Abstrakte Basisklasse für alle Aktoren
    """
    
    def __init__(self, name: str, actuator_type: str):
        """
        Initialisiert den Aktor
        
        Args:
            name: Name des Aktors
            actuator_type: Typ des Aktors (z.B. "pump", "heater", "fan")
        """
        self.name = name
        self.actuator_type = actuator_type
        self.is_active: bool = False
        self.is_available: bool = False
        self.last_state_change: Optional[datetime] = None
    
    @abstractmethod
    def turn_on(self) -> bool:
        """
        Schaltet den Aktor ein
        
        Returns:
            True bei Erfolg, False bei Fehler
        """
        pass
    
    @abstractmethod
    def turn_off(self) -> bool:
        """
        Schaltet den Aktor aus
        
        Returns:
            True bei Erfolg, False bei Fehler
        """
        pass
    
    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialisiert den Aktor
        
        Returns:
            True bei Erfolg, False bei Fehler
        """
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """
        Gibt den Status des Aktors zurück
        
        Returns:
            Dictionary mit Statusinformationen
        """
        return {
            'name': self.name,
            'type': self.actuator_type,
            'active': self.is_active,
            'available': self.is_available,
            'last_state_change': self.last_state_change.isoformat() if self.last_state_change else None
        }
