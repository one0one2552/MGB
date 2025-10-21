"""
Datenlogger für Sensordaten
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class DataLogger:
    """
    Speichert Sensordaten in einer SQLite-Datenbank
    """
    
    def __init__(self, db_path: str = "data/mgb_mushroom_grow_box.db"):
        """
        Initialisiert den DataLogger
        
        Args:
            db_path: Pfad zur Datenbank-Datei
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self._initialize_db()
    
    def _initialize_db(self):
        """
        Initialisiert die Datenbank-Tabellen
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabelle für Sensordaten
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sensor_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    sensor_name TEXT NOT NULL,
                    value REAL NOT NULL,
                    unit TEXT NOT NULL
                )
            ''')
            
            # Tabelle für Aktor-Status
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS actuator_status (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    actuator_name TEXT NOT NULL,
                    state INTEGER NOT NULL
                )
            ''')
            
            # Tabelle für Alarme
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS alarms (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    alarm_type TEXT NOT NULL,
                    message TEXT NOT NULL,
                    acknowledged INTEGER DEFAULT 0
                )
            ''')
            
            conn.commit()
    
    def log_sensor_data(self, sensor_name: str, value: float, unit: str, 
                       timestamp: Optional[datetime] = None):
        """
        Speichert einen Sensorwert
        
        Args:
            sensor_name: Name des Sensors
            value: Gemessener Wert
            unit: Einheit des Werts
            timestamp: Zeitstempel (optional, sonst aktuell)
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO sensor_data (timestamp, sensor_name, value, unit) VALUES (?, ?, ?, ?)',
                (timestamp.isoformat(), sensor_name, value, unit)
            )
            conn.commit()
    
    def log_actuator_state(self, actuator_name: str, state: bool,
                          timestamp: Optional[datetime] = None):
        """
        Speichert einen Aktor-Status
        
        Args:
            actuator_name: Name des Aktors
            state: Status (True=Ein, False=Aus)
            timestamp: Zeitstempel (optional, sonst aktuell)
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO actuator_status (timestamp, actuator_name, state) VALUES (?, ?, ?)',
                (timestamp.isoformat(), actuator_name, int(state))
            )
            conn.commit()
    
    def log_alarm(self, alarm_type: str, message: str,
                 timestamp: Optional[datetime] = None):
        """
        Speichert einen Alarm
        
        Args:
            alarm_type: Typ des Alarms
            message: Alarm-Nachricht
            timestamp: Zeitstempel (optional, sonst aktuell)
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO alarms (timestamp, alarm_type, message) VALUES (?, ?, ?)',
                (timestamp.isoformat(), alarm_type, message)
            )
            conn.commit()
    
    def get_sensor_data(self, sensor_name: Optional[str] = None, 
                       limit: int = 100) -> List[Dict[str, Any]]:
        """
        Liest Sensordaten aus der Datenbank
        
        Args:
            sensor_name: Name des Sensors (optional, sonst alle)
            limit: Maximale Anzahl der Datensätze
            
        Returns:
            Liste mit Sensordaten
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if sensor_name:
                cursor.execute(
                    'SELECT timestamp, sensor_name, value, unit FROM sensor_data '
                    'WHERE sensor_name = ? ORDER BY timestamp DESC LIMIT ?',
                    (sensor_name, limit)
                )
            else:
                cursor.execute(
                    'SELECT timestamp, sensor_name, value, unit FROM sensor_data '
                    'ORDER BY timestamp DESC LIMIT ?',
                    (limit,)
                )
            
            rows = cursor.fetchall()
            return [
                {
                    'timestamp': row[0],
                    'sensor_name': row[1],
                    'value': row[2],
                    'unit': row[3]
                }
                for row in rows
            ]
