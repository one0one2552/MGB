"""
PID-Regler für die Steuerung der Aktoren
"""

from datetime import datetime
from typing import Optional
from collections import deque
import math


class PIDController:
    """
    PID-Regler (Proportional-Integral-Derivative Controller)
    """
    
    def __init__(self, kp: float, ki: float, kd: float, 
                 setpoint: float = 0.0,
                 output_min: float = 0.0,
                 output_max: float = 100.0,
                 adaptive: bool = True,
                 learning_rate: float = 0.01):
        """
        Initialisiert den PID-Regler
        
        Args:
            kp: Proportional-Verstärkung
            ki: Integral-Verstärkung
            kd: Differential-Verstärkung
            setpoint: Sollwert
            output_min: Minimaler Ausgabewert
            output_max: Maximaler Ausgabewert
            adaptive: Aktiviert adaptive PID-Regelung
            learning_rate: Lernrate für die Parameteranpassung (0.001-0.1)
        """
        # Ursprüngliche Parameter (als Basis)
        self.kp_base = kp
        self.ki_base = ki
        self.kd_base = kd
        
        # Aktuelle Parameter (können sich anpassen)
        self.kp = kp
        self.ki = ki
        self.kd = kd
        
        self.setpoint = setpoint
        self.output_min = output_min
        self.output_max = output_max
        
        # Adaptive Regelung
        self.adaptive = adaptive
        self.learning_rate = learning_rate
        
        # Zustandsvariablen
        self._integral = 0.0
        self._last_error: Optional[float] = None
        self._last_time: Optional[datetime] = None
        
        # Performance-Tracking für adaptive Anpassung
        self._error_history = deque(maxlen=20)  # Letzte 20 Fehler
        self._output_history = deque(maxlen=20)  # Letzte 20 Ausgaben
        self._adaptation_counter = 0
        self._adaptation_interval = 10  # Passe alle 10 Updates an
    
    def update(self, measured_value: float, current_time: Optional[datetime] = None) -> float:
        """
        Berechnet die Stellgröße basierend auf dem gemessenen Wert
        
        Args:
            measured_value: Aktueller Messwert
            current_time: Aktueller Zeitpunkt (optional)
            
        Returns:
            Berechnete Stellgröße
        """
        if current_time is None:
            current_time = datetime.now()
        
        # Regelabweichung berechnen
        error = self.setpoint - measured_value
        
        # Zeitdifferenz berechnen
        if self._last_time is not None:
            dt = (current_time - self._last_time).total_seconds()
        else:
            dt = 0.0
        
        # P-Anteil
        p_term = self.kp * error
        
        # I-Anteil
        if dt > 0:
            self._integral += error * dt
        i_term = self.ki * self._integral
        
        # D-Anteil
        if self._last_error is not None and dt > 0:
            derivative = (error - self._last_error) / dt
            d_term = self.kd * derivative
        else:
            d_term = 0.0
        
        # Stellgröße berechnen
        output = p_term + i_term + d_term
        
        # Ausgabe begrenzen
        output = max(self.output_min, min(self.output_max, output))
        
        # Werte für nächste Iteration speichern
        self._last_error = error
        self._last_time = current_time
        
        # Performance-Tracking
        self._error_history.append(abs(error))
        self._output_history.append(output)
        
        # Adaptive Anpassung
        if self.adaptive:
            self._adaptation_counter += 1
            if self._adaptation_counter >= self._adaptation_interval:
                self._adapt_parameters()
                self._adaptation_counter = 0
        
        return output
    
    def reset(self):
        """
        Setzt den Regler zurück
        """
        self._integral = 0.0
        self._last_error = None
        self._last_time = None
    
    def set_setpoint(self, setpoint: float):
        """
        Setzt einen neuen Sollwert
        
        Args:
            setpoint: Neuer Sollwert
        """
        self.setpoint = setpoint
        self.reset()
    
    def _adapt_parameters(self):
        """
        Passt die PID-Parameter adaptiv an basierend auf der Performance
        
        Verwendet Ziegler-Nichols inspirierte Anpassungslogik:
        - Wenn Fehler zu groß: Erhöhe Kp
        - Wenn Oszillation: Reduziere Kp, erhöhe Kd
        - Wenn stationärer Fehler: Erhöhe Ki
        """
        if len(self._error_history) < 10:
            return  # Nicht genug Daten
        
        # Berechne Performance-Metriken
        recent_errors = list(self._error_history)[-10:]
        avg_error = sum(recent_errors) / len(recent_errors)
        error_variance = sum((e - avg_error) ** 2 for e in recent_errors) / len(recent_errors)
        error_std = math.sqrt(error_variance) if error_variance > 0 else 0
        
        # Erkenne Oszillation (hohe Standardabweichung bei mittlerem Fehler)
        is_oscillating = error_std > avg_error * 0.5 and error_std > 0.1
        
        # Erkenne stationären Fehler (niedriger Fehler aber nicht Null)
        has_steady_state_error = 0.1 < avg_error < 1.0 and error_std < 0.2
        
        # Erkenne großen Fehler
        has_large_error = avg_error > 2.0
        
        # Anpassungslogik
        if is_oscillating:
            # Reduziere P-Anteil, erhöhe D-Anteil
            self.kp *= (1 - self.learning_rate)
            self.kd *= (1 + self.learning_rate)
            
        elif has_large_error:
            # Erhöhe P-Anteil für schnellere Reaktion
            self.kp *= (1 + self.learning_rate * 2)
            
        elif has_steady_state_error:
            # Erhöhe I-Anteil für stationäre Genauigkeit
            self.ki *= (1 + self.learning_rate)
        
        # Begrenze Parameter auf sinnvolle Bereiche
        self.kp = max(self.kp_base * 0.1, min(self.kp_base * 5.0, self.kp))
        self.ki = max(self.ki_base * 0.1, min(self.ki_base * 5.0, self.ki))
        self.kd = max(self.kd_base * 0.1, min(self.kd_base * 5.0, self.kd))
    
    def get_tuning_info(self) -> dict:
        """
        Gibt Informationen über den aktuellen Tuning-Zustand zurück
        
        Returns:
            Dictionary mit Tuning-Informationen
        """
        return {
            'kp': self.kp,
            'ki': self.ki,
            'kd': self.kd,
            'kp_base': self.kp_base,
            'ki_base': self.ki_base,
            'kd_base': self.kd_base,
            'adaptive': self.adaptive,
            'avg_error': sum(self._error_history) / len(self._error_history) if self._error_history else 0,
            'error_count': len(self._error_history)
        }
    
    def set_adaptive(self, adaptive: bool):
        """
        Aktiviert oder deaktiviert die adaptive Regelung
        
        Args:
            adaptive: True für adaptive Regelung, False für fixe Parameter
        """
        self.adaptive = adaptive
        if not adaptive:
            # Setze auf Basis-Parameter zurück
            self.kp = self.kp_base
            self.ki = self.ki_base
            self.kd = self.kd_base
    
    def reset_to_base_parameters(self):
        """
        Setzt die Parameter auf die Basis-Werte zurück
        """
        self.kp = self.kp_base
        self.ki = self.ki_base
        self.kd = self.kd_base
        self._error_history.clear()
        self._output_history.clear()
        self._adaptation_counter = 0
