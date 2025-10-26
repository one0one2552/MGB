"""
Relay-Aktor für Heizmatte und andere On/Off-Geräte
"""

import logging
from datetime import datetime
from typing import Optional, Dict, Any
from .base_actuator import BaseActuator

logger = logging.getLogger(__name__)


class RelayActuator(BaseActuator):
    """
    Steuert ein Relay-Modul über GPIO
    
    Einfache Logik:
    - GPIO HIGH = Relay AN
    - GPIO LOW = Relay AUS
    """
    
    def __init__(self, name: str, pin: int, config: Dict[str, Any]):
        """
        Initialisiert den Relay-Aktor
        
        Args:
            name: Name des Aktors (z.B. "heater", "pump")
            pin: GPIO Pin-Nummer (BCM-Nummerierung)
            config: Konfiguration mit optionalen Parametern
        """
        super().__init__(name, "relay")
        self.pin = pin
        self.config = config
        self._gpio = None
        self._mock_mode = False
        
        # Konfiguration
        self.min_runtime = config.get('min_runtime', 0)  # Minimale Laufzeit in Sekunden
        self.max_runtime = config.get('max_runtime', 0)  # Maximale Laufzeit in Sekunden
        self.cooldown = config.get('cooldown', 0)  # Wartezeit zwischen Aktivierungen
        
        self.last_activation_time: Optional[datetime] = None
        self.activation_start_time: Optional[datetime] = None
        
        # Initialisierung
        self.initialize()
    
    def initialize(self) -> bool:
        """
        Initialisiert das GPIO-Interface
        
        Returns:
            True bei Erfolg, False bei Fehler
        """
        try:
            import RPi.GPIO as GPIO
            self._gpio = GPIO
            
            # GPIO Mode nur setzen wenn noch nicht gesetzt
            # (vermeidet Probleme bei mehreren Relays)
            try:
                GPIO.setmode(GPIO.BCM)
            except:
                pass  # Mode ist schon gesetzt
            
            GPIO.setwarnings(False)
            
            # Pin als Output mit initial LOW (Relay AUS)
            GPIO.setup(self.pin, GPIO.OUT, initial=GPIO.LOW)
            
            self.is_active = False
            self.is_available = True
            self._mock_mode = False
            
            logger.info(f"✓ Relay '{self.name}' initialisiert auf GPIO Pin {self.pin}")
            return True
            
        except ImportError:
            logger.warning(f"✗ RPi.GPIO nicht verfügbar - Relay '{self.name}' im Mock-Modus")
            self._mock_mode = True
            self.is_available = True
            return True
        except Exception as e:
            logger.error(f"✗ Fehler beim Initialisieren von Relay '{self.name}': {e}")
            self._mock_mode = True
            self.is_available = False
            return False
    
    def turn_on(self) -> bool:
        """
        Schaltet das Relay ein (GPIO HIGH)
        
        Returns:
            True bei Erfolg, False bei Fehler
        """
        try:
            # Cooldown prüfen
            if self.last_activation_time and self.cooldown > 0:
                time_since_last = (datetime.now() - self.last_activation_time).total_seconds()
                if time_since_last < self.cooldown:
                    remaining = self.cooldown - time_since_last
                    logger.warning(f"Relay '{self.name}' im Cooldown (noch {remaining:.1f}s)")
                    return False
            
            if self._mock_mode:
                logger.info(f"[MOCK] Relay '{self.name}' EIN")
                self.is_active = True
                self.activation_start_time = datetime.now()
                self.last_state_change = datetime.now()
                return True
            
            if self._gpio:
                # GPIO HIGH = Relay AN
                self._gpio.output(self.pin, self._gpio.HIGH)
                
                self.is_active = True
                self.activation_start_time = datetime.now()
                self.last_state_change = datetime.now()
                
                logger.info(f"✓ Relay '{self.name}' eingeschaltet (Pin {self.pin} = HIGH)")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"✗ Fehler beim Einschalten von Relay '{self.name}': {e}")
            return False
    
    def turn_off(self) -> bool:
        """
        Schaltet das Relay aus (GPIO LOW)
        
        Returns:
            True bei Erfolg, False bei Fehler
        """
        try:
            # Min-Runtime prüfen
            if self.is_active and self.activation_start_time and self.min_runtime > 0:
                runtime = (datetime.now() - self.activation_start_time).total_seconds()
                if runtime < self.min_runtime:
                    remaining = self.min_runtime - runtime
                    logger.warning(f"Relay '{self.name}' min-runtime nicht erreicht (noch {remaining:.1f}s)")
                    return False
            
            if self._mock_mode:
                logger.info(f"[MOCK] Relay '{self.name}' AUS")
                self.is_active = False
                if self.activation_start_time:
                    self.last_activation_time = self.activation_start_time
                self.activation_start_time = None
                self.last_state_change = datetime.now()
                return True
            
            if self._gpio:
                # GPIO LOW = Relay AUS
                self._gpio.output(self.pin, self._gpio.LOW)
                
                self.is_active = False
                if self.activation_start_time:
                    self.last_activation_time = self.activation_start_time
                self.activation_start_time = None
                self.last_state_change = datetime.now()
                
                logger.info(f"✓ Relay '{self.name}' ausgeschaltet (Pin {self.pin} = LOW)")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"✗ Fehler beim Ausschalten von Relay '{self.name}': {e}")
            return False
    
    def is_mock_mode(self) -> bool:
        """
        Prüft, ob der Aktor im Mock-Modus läuft
        
        Returns:
            True wenn Mock-Modus, False wenn Hardware
        """
        return self._mock_mode
    
    def check_max_runtime(self) -> bool:
        """
        Prüft ob maximale Laufzeit überschritten wurde
        
        Returns:
            True wenn max-runtime überschritten, False sonst
        """
        if self.is_active and self.activation_start_time and self.max_runtime > 0:
            runtime = (datetime.now() - self.activation_start_time).total_seconds()
            if runtime >= self.max_runtime:
                logger.warning(f"Relay '{self.name}' max-runtime erreicht ({runtime:.1f}s)")
                return True
        return False
    
    def get_runtime(self) -> float:
        """
        Gibt die aktuelle Laufzeit zurück (wenn aktiv)
        
        Returns:
            Laufzeit in Sekunden, 0 wenn nicht aktiv
        """
        if self.is_active and self.activation_start_time:
            return (datetime.now() - self.activation_start_time).total_seconds()
        return 0.0
    
    def get_status(self) -> Dict[str, Any]:
        """
        Gibt erweiterten Status zurück
        
        Returns:
            Dictionary mit Statusinformationen
        """
        status = super().get_status()
        status.update({
            'pin': self.pin,
            'mock_mode': self._mock_mode,
            'runtime': self.get_runtime(),
            'min_runtime': self.min_runtime,
            'max_runtime': self.max_runtime,
            'cooldown': self.cooldown
        })
        return status
    
    def cleanup(self):
        """
        Räumt GPIO-Ressourcen auf
        """
        try:
            if self._gpio and not self._mock_mode:
                self.turn_off()
                self._gpio.cleanup(self.pin)
                logger.info(f"✓ GPIO Pin {self.pin} cleanup")
        except Exception as e:
            logger.error(f"Fehler beim GPIO cleanup: {e}")
