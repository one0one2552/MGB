# Lastenheft: Automatisierte Pilzzuchtbox

## 1. Projektziel
Entwicklung einer automatisierten Pilzzuchtbox zur Überwachung und Regelung der optimalen Wachstumsbedingungen für Kulturpilze.

## 2. Systemüberblick
Das System überwacht kontinuierlich die Umgebungsparameter (CO2, Temperatur, Luftfeuchtigkeit) in der Zuchtbox und steuert entsprechende Aktoren (Pumpe mit Sprühdüsen, Heizmatten, Lüfter), um ideale Wachstumsbedingungen aufrechtzuerhalten.

## 3. Funktionale Anforderungen

### 3.1 Sensorik
- **FA-S1:** Kontinuierliche Messung des CO2-Gehalts mit einer Genauigkeit von ±50 ppm
- **FA-S2:** Temperaturmessung mit einer Genauigkeit von ±0,5°C im Bereich von 10°C bis 35°C
- **FA-S3:** Luftfeuchtigkeitsmessung mit einer Genauigkeit von ±3% im Bereich von 50% bis 95% RH
- **FA-S4:** Messintervall für alle Parameter: mindestens alle 60 Sekunden

### 3.2 Aktorik
- **FA-A1:** Steuerung einer Wasserpumpe mit Sprühdüsen zur Erhöhung der Luftfeuchtigkeit
- **FA-A2:** Steuerung von Heizmatten zur Temperaturregelung
- **FA-A3:** Steuerung von Lüftern zur CO2-Regulierung und Luftzirkulation
- **FA-A4:** Alle Aktoren müssen individuell ansteuerbar sein

### 3.3 Regelung
- **FA-R1:** Automatische Regelung der Luftfeuchtigkeit innerhalb definierter Grenzen (konfigurierbar)
- **FA-R2:** Temperaturregelung innerhalb definierter Grenzen (konfigurierbar)
- **FA-R3:** CO2-Regulation durch Frischluftzufuhr (konfigurierbar)
- **FA-R4:** Tag-/Nacht-Rhythmus für Temperatur- und Lüftungsparameter programmierbar

### 3.4 Benutzeroberfläche
- **FA-B1:** Anzeige der aktuellen Messwerte (CO2, Temperatur, Luftfeuchtigkeit)
- **FA-B2:** Einstellung der Sollwerte und Grenzwerte für alle Parameter
- **FA-B3:** Statusanzeige der Aktoren (aktiv/inaktiv)
- **FA-B4:** Alarmierung bei Grenzwertüberschreitungen

## 4. Nicht-funktionale Anforderungen

### 4.1 Zuverlässigkeit
- **NFA-Z1:** Systemverfügbarkeit von mindestens 99%
- **NFA-Z2:** Ausfallsichere Speicherung der Einstellungen bei Stromausfall
- **NFA-Z3:** Überwachung der Sensorik auf Fehlfunktionen

### 4.2 Sicherheit
- **NFA-S1:** Überspannungsschutz für alle elektronischen Komponenten
- **NFA-S2:** Wasserdichtes Gehäuse für die Elektronik (mindestens IP54)
- **NFA-S3:** Sicherheitsabschaltung der Heizmatten bei Überhitzung

### 4.3 Benutzerfreundlichkeit
- **NFA-B1:** Intuitive Bedienung ohne technisches Vorwissen
- **NFA-B2:** Dokumentation in deutscher Sprache
- **NFA-B3:** Inbetriebnahme innerhalb von 30 Minuten möglich

### 4.4 Erweiterbarkeit
- **NFA-E1:** Modularer Aufbau zur einfachen Erweiterung mit zusätzlichen Sensoren
- **NFA-E2:** Schnittstelle für optionale Datenübertragung (z.B. WLAN, Bluetooth)

## 5. Technische Spezifikationen

### 5.1 Hardware
- **TS-H1:** Mikrocontroller mit mindestens 6 analogen/digitalen Eingängen und 6 digitalen Ausgängen
- **TS-H2:** CO2-Sensor mit Messbereich 0-5000 ppm
- **TS-H3:** Temperatur-/Feuchtigkeitssensor mit den genannten Genauigkeitsanforderungen
- **TS-H4:** Relaissteuerung für Heizmatten (mindestens 100W belastbar)
- **TS-H5:** PWM-Steuerung für Lüfter
- **TS-H6:** Wasserpumpe mit feinen Sprühdüsen (Tropfengröße <100µm)
- **TS-H7:** Stromversorgung: 12V DC mit ausreichender Leistung (min. 3A)

### 5.2 Software
- **TS-S1:** Betriebsmodi: Automatik, Manuell, Aus
- **TS-S2:** PID-Regelung oder vergleichbare Regelungsalgorithmen
- **TS-S3:** Datenlogging mit Speicherung auf SD-Karte oder im internen Speicher
- **TS-S4:** Benutzeroberfläche über LCD/OLED-Display oder Webinterface

## 6. Schnittstellen
- **SI-1:** Stromversorgung: 230V AC oder 12V DC
- **SI-2:** Optional: Netzwerkschnittstelle (WLAN/Ethernet)
- **SI-3:** Optional: USB-Schnittstelle zur Konfiguration

## 7. Lieferumfang
- **LU-1:** Vollständig montierte Steuerungseinheit
- **LU-2:** Sensoren mit Anschlusskabeln
- **LU-3:** Aktoren (Pumpe, Heizmatten, Lüfter)
- **LU-4:** Montage- und Bedienungsanleitung
- **LU-5:** Quellcode und Softwarekonfiguration

## 8. Abnahmekriterien
- **AK-1:** Erfolgreiche Inbetriebnahme und Kalibrierung aller Sensoren
- **AK-2:** Nachweis der korrekten Funktionsweise aller Regelkreise
- **AK-3:** Test aller Benutzeroberflächen-Funktionen
- **AK-4:** Stabiler Betrieb über 72 Stunden mit definierten Parametern