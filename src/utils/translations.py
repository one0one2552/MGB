"""
MGB - Mushroom Grow Box
Multi-Language Translation System
Dictionary-based translations for easy expansion
"""

# German Translations (Default)
TRANSLATIONS_DE = {
    # Header
    "app_title": "🍄 Pilzzuchtbox Steuerung",
    "system_status": "System-Status",
    "status_online": "Online",
    "status_offline": "Offline",
    
    # Navigation
    "nav_dashboard": "Dashboard",
    "nav_settings": "Einstellungen",
    "nav_logs": "Logs",
    "nav_alarms": "Alarme",
    "nav_terminal": "Terminal",
    
    # Sensors Section
    "section_sensors": "Sensordaten",
    "sensor_temperature": "Temperatur",
    "sensor_humidity": "Luftfeuchtigkeit",
    "sensor_co2": "CO₂-Gehalt",
    "target_value": "Zielwert",
    "current_value": "Aktuell",
    
    # Sensor Status
    "status_ok": "OK",
    "status_warning": "Warnung",
    "status_critical": "Kritisch",
    
    # Actuators Section
    "section_actuators": "Aktoren",
    "actuator_heater": "Heizung",
    "actuator_humidifier": "Luftbefeuchter",
    "actuator_fan": "Lüfter",
    "actuator_light": "Beleuchtung",
    "fan_speed": "Drehzahl",
    
    # Actuator Controls
    "btn_on": "EIN",
    "btn_off": "AUS",
    "btn_auto": "AUTO",
    "btn_manual": "MANUELL",
    "status_active": "Aktiv",
    "status_inactive": "Inaktiv",
    
    # Charts Section
    "section_charts": "Verlaufsdiagramme",
    "chart_temperature": "Temperaturverlauf",
    "chart_humidity": "Feuchtigkeitsverlauf",
    "chart_co2": "CO₂-Verlauf",
    "time_period": "Zeitraum",
    "period_1h": "1 Stunde",
    "period_6h": "6 Stunden",
    "period_24h": "24 Stunden",
    "period_7d": "7 Tage",
    
    # PID Section
    "section_pid": "PID-Regler Status",
    "pid_temperature": "Temperatur PID",
    "pid_humidity": "Luftfeuchte PID",
    "pid_co2": "CO₂ PID",
    "pid_kp": "Kp (Proportional)",
    "pid_ki": "Ki (Integral)",
    "pid_kd": "Kd (Differential)",
    "pid_output": "Ausgang",
    "pid_setpoint": "Sollwert",
    "pid_error": "Abweichung",
    "adaptive_change": "Adaptiv",
    
    # Alarms Section
    "section_alarms": "Alarme & Warnungen",
    "no_alarms": "Keine aktiven Alarme",
    "alarm_temp_high": "Temperatur zu hoch",
    "alarm_temp_low": "Temperatur zu niedrig",
    "alarm_humidity_high": "Luftfeuchtigkeit zu hoch",
    "alarm_humidity_low": "Luftfeuchtigkeit zu niedrig",
    "alarm_co2_high": "CO₂ zu hoch",
    "alarm_sensor_error": "Sensor-Fehler",
    "alarm_time": "Zeit",
    "alarm_clear": "Löschen",
    
    # Terminal Section
    "section_terminal": "System-Terminal",
    "terminal_title": "Terminal",
    "terminal_clear": "Löschen",
    "terminal_prompt": "mgb@system:~$",
    "terminal_placeholder": "Befehl eingeben...",
    
    # Settings Page
    "settings_title": "Systemeinstellungen",
    "settings_save": "Einstellungen speichern",
    "settings_saved": "Einstellungen erfolgreich gespeichert!",
    "settings_error": "Fehler beim Speichern der Einstellungen",
    
    # Settings - General
    "settings_general": "Allgemeine Einstellungen",
    "settings_device_name": "Gerätename",
    "settings_location": "Standort",
    "settings_timezone": "Zeitzone",
    
    # Settings - Targets
    "settings_targets": "Zielwerte",
    "settings_temp_target": "Ziel-Temperatur",
    "settings_temp_tolerance": "Temperatur-Toleranz",
    "settings_humidity_target": "Ziel-Luftfeuchtigkeit",
    "settings_humidity_tolerance": "Luftfeuchte-Toleranz",
    "settings_co2_target": "Ziel-CO₂",
    "settings_co2_tolerance": "CO₂-Toleranz",
    
    # Settings - PID
    "settings_pid": "PID-Parameter",
    "settings_pid_temp": "Temperatur PID",
    "settings_pid_humidity": "Luftfeuchte PID",
    "settings_pid_co2": "CO₂ PID",
    "settings_pid_enable_adaptive": "Adaptive PID aktivieren",
    
    # Settings - Schedule
    "settings_schedule": "Zeitplan",
    "settings_light_schedule": "Beleuchtungsplan",
    "settings_light_on": "Licht EIN",
    "settings_light_off": "Licht AUS",
    "settings_fan_schedule": "Lüfterplan",
    
    # Settings - Alarms
    "settings_alarms": "Alarm-Einstellungen",
    "settings_enable_alarms": "Alarme aktivieren",
    "settings_alarm_sound": "Alarm-Ton",
    "settings_alarm_email": "E-Mail-Benachrichtigungen",
    "settings_email_address": "E-Mail-Adresse",
    
    # Settings - WiFi
    "settings_wifi": "WiFi-Einstellungen",
    "settings_wifi_ssid": "Netzwerk-Name (SSID)",
    "settings_wifi_password": "Passwort",
    "settings_wifi_connect": "Verbinden",
    "settings_ap_mode": "Access Point Modus",
    "settings_ap_ssid": "AP-Name",
    
    # Units
    "unit_celsius": "°C",
    "unit_percent": "%",
    "unit_ppm": "ppm",
    "unit_rpm": "U/min",
    
    # Common
    "loading": "Lade...",
    "error": "Fehler",
    "success": "Erfolg",
    "cancel": "Abbrechen",
    "confirm": "Bestätigen",
    "close": "Schließen",
    "yes": "Ja",
    "no": "Nein",
    
    # Footer
    "footer_version": "Version",
    "footer_license": "Lizenz",
    "footer_copyright": "© 2024 MGB - Mushroom Grow Box",
}

# English Translations
TRANSLATIONS_EN = {
    # Header
    "app_title": "🍄 Mushroom Grow Box Control",
    "system_status": "System Status",
    "status_online": "Online",
    "status_offline": "Offline",
    
    # Navigation
    "nav_dashboard": "Dashboard",
    "nav_settings": "Settings",
    "nav_logs": "Logs",
    "nav_alarms": "Alarms",
    "nav_terminal": "Terminal",
    
    # Sensors Section
    "section_sensors": "Sensor Data",
    "sensor_temperature": "Temperature",
    "sensor_humidity": "Humidity",
    "sensor_co2": "CO₂ Level",
    "target_value": "Target",
    "current_value": "Current",
    
    # Sensor Status
    "status_ok": "OK",
    "status_warning": "Warning",
    "status_critical": "Critical",
    
    # Actuators Section
    "section_actuators": "Actuators",
    "actuator_heater": "Heater",
    "actuator_humidifier": "Humidifier",
    "actuator_fan": "Fan",
    "actuator_light": "Light",
    "fan_speed": "Speed",
    
    # Actuator Controls
    "btn_on": "ON",
    "btn_off": "OFF",
    "btn_auto": "AUTO",
    "btn_manual": "MANUAL",
    "status_active": "Active",
    "status_inactive": "Inactive",
    
    # Charts Section
    "section_charts": "Historical Charts",
    "chart_temperature": "Temperature History",
    "chart_humidity": "Humidity History",
    "chart_co2": "CO₂ History",
    "time_period": "Time Period",
    "period_1h": "1 Hour",
    "period_6h": "6 Hours",
    "period_24h": "24 Hours",
    "period_7d": "7 Days",
    
    # PID Section
    "section_pid": "PID Controller Status",
    "pid_temperature": "Temperature PID",
    "pid_humidity": "Humidity PID",
    "pid_co2": "CO₂ PID",
    "pid_kp": "Kp (Proportional)",
    "pid_ki": "Ki (Integral)",
    "pid_kd": "Kd (Derivative)",
    "pid_output": "Output",
    "pid_setpoint": "Setpoint",
    "pid_error": "Error",
    "adaptive_change": "Adaptive",
    
    # Alarms Section
    "section_alarms": "Alarms & Warnings",
    "no_alarms": "No active alarms",
    "alarm_temp_high": "Temperature too high",
    "alarm_temp_low": "Temperature too low",
    "alarm_humidity_high": "Humidity too high",
    "alarm_humidity_low": "Humidity too low",
    "alarm_co2_high": "CO₂ too high",
    "alarm_sensor_error": "Sensor error",
    "alarm_time": "Time",
    "alarm_clear": "Clear",
    
    # Terminal Section
    "section_terminal": "System Terminal",
    "terminal_title": "Terminal",
    "terminal_clear": "Clear",
    "terminal_prompt": "mgb@system:~$",
    "terminal_placeholder": "Enter command...",
    
    # Settings Page
    "settings_title": "System Settings",
    "settings_save": "Save Settings",
    "settings_saved": "Settings saved successfully!",
    "settings_error": "Error saving settings",
    
    # Settings - General
    "settings_general": "General Settings",
    "settings_device_name": "Device Name",
    "settings_location": "Location",
    "settings_timezone": "Timezone",
    
    # Settings - Targets
    "settings_targets": "Target Values",
    "settings_temp_target": "Target Temperature",
    "settings_temp_tolerance": "Temperature Tolerance",
    "settings_humidity_target": "Target Humidity",
    "settings_humidity_tolerance": "Humidity Tolerance",
    "settings_co2_target": "Target CO₂",
    "settings_co2_tolerance": "CO₂ Tolerance",
    
    # Settings - PID
    "settings_pid": "PID Parameters",
    "settings_pid_temp": "Temperature PID",
    "settings_pid_humidity": "Humidity PID",
    "settings_pid_co2": "CO₂ PID",
    "settings_pid_enable_adaptive": "Enable Adaptive PID",
    
    # Settings - Schedule
    "settings_schedule": "Schedule",
    "settings_light_schedule": "Light Schedule",
    "settings_light_on": "Light ON",
    "settings_light_off": "Light OFF",
    "settings_fan_schedule": "Fan Schedule",
    
    # Settings - Alarms
    "settings_alarms": "Alarm Settings",
    "settings_enable_alarms": "Enable Alarms",
    "settings_alarm_sound": "Alarm Sound",
    "settings_alarm_email": "Email Notifications",
    "settings_email_address": "Email Address",
    
    # Settings - WiFi
    "settings_wifi": "WiFi Settings",
    "settings_wifi_ssid": "Network Name (SSID)",
    "settings_wifi_password": "Password",
    "settings_wifi_connect": "Connect",
    "settings_ap_mode": "Access Point Mode",
    "settings_ap_ssid": "AP Name",
    
    # Units
    "unit_celsius": "°C",
    "unit_percent": "%",
    "unit_ppm": "ppm",
    "unit_rpm": "RPM",
    
    # Common
    "loading": "Loading...",
    "error": "Error",
    "success": "Success",
    "cancel": "Cancel",
    "confirm": "Confirm",
    "close": "Close",
    "yes": "Yes",
    "no": "No",
    
    # Footer
    "footer_version": "Version",
    "footer_license": "License",
    "footer_copyright": "© 2024 MGB - Mushroom Grow Box",
}

# Available languages
AVAILABLE_LANGUAGES = {
    'de': {
        'name': 'Deutsch',
        'flag': '🇩🇪',
        'translations': TRANSLATIONS_DE
    },
    'en': {
        'name': 'English',
        'flag': '🇬🇧',
        'translations': TRANSLATIONS_EN
    }
}

def get_translations(language_code='de'):
    """
    Get translations for a specific language
    
    Args:
        language_code: Language code ('de' or 'en')
        
    Returns:
        Dictionary with translations
    """
    if language_code in AVAILABLE_LANGUAGES:
        return AVAILABLE_LANGUAGES[language_code]['translations']
    else:
        # Fallback to German if language not found
        return TRANSLATIONS_DE

def get_available_languages():
    """
    Get list of available languages
    
    Returns:
        Dictionary with available languages
    """
    return {
        code: {
            'name': lang['name'],
            'flag': lang['flag']
        }
        for code, lang in AVAILABLE_LANGUAGES.items()
    }
