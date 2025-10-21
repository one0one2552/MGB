# Einstellungen - Benutzerhandbuch

## Zugriff auf die Einstellungsseite

Die Einstellungsseite ist über das Web-Interface erreichbar:
- URL: `http://mgb.local:5000/settings` oder `http://localhost:5000/settings`
- Klicken Sie im Dashboard auf den Button **"⚙️ Einstellungen"**

## Verfügbare Einstellungen

### 🌡️ Temperatur

**Zielwert (°C)**
- Bereich: 10-35°C
- Empfohlen: 20-24°C für die meisten Pilzarten
- Dies ist die gewünschte Temperatur in der Zuchtbox

**Toleranz (±°C)**
- Bereich: 0.1-5°C
- Empfohlen: 1°C
- Erlaubte Abweichung vom Zielwert, bevor die Heizung aktiviert wird

### 💧 Luftfeuchtigkeit

**Zielwert (%)**
- Bereich: 50-95%
- Empfohlen: 80-90% für die Fruchtungsphase
- Dies ist die gewünschte relative Luftfeuchtigkeit

**Toleranz (±%)**
- Bereich: 1-10%
- Empfohlen: 5%
- Erlaubte Abweichung vom Zielwert, bevor die Pumpe aktiviert wird

### 🌬️ CO₂-Gehalt

**Zielwert (ppm)**
- Bereich: 400-2000 ppm
- Empfohlen: 600-1000 ppm
- Frischluft hat ca. 400 ppm, höhere Werte fördern das Myzelwachstum

**Toleranz (±ppm)**
- Bereich: 10-200 ppm
- Empfohlen: 100 ppm
- Erlaubte Abweichung vom Zielwert, bevor der Lüfter aktiviert wird

### 🌓 Tag/Nacht-Rhythmus

Die MGB unterstützt unterschiedliche Einstellungen für Tag und Nacht:

**Zeiten**
- **Tag beginnt um**: Startzeitpunkt der Tagesphase (z.B. 06:00)
- **Nacht beginnt um**: Startzeitpunkt der Nachtphase (z.B. 22:00)

**Tagwerte**
- **Tagtemperatur**: Zieltemperatur während der Tagesphase
- **Tagfeuchtigkeit**: Ziel-Luftfeuchtigkeit während der Tagesphase

**Nachtwerte**
- **Nachttemperatur**: Zieltemperatur während der Nachtphase (meist 2-4°C niedriger)
- **Nachtfeuchtigkeit**: Ziel-Luftfeuchtigkeit während der Nachtphase (meist 5% höher)

## Empfohlene Einstellungen nach Pilzart

### Austernpilze (Pleurotus)
- **Temperatur**: 18-24°C (Tag), 15-18°C (Nacht)
- **Luftfeuchtigkeit**: 85-95%
- **CO₂**: 500-800 ppm

### Shiitake
- **Temperatur**: 18-22°C (Tag), 15-18°C (Nacht)
- **Luftfeuchtigkeit**: 80-90%
- **CO₂**: 600-1000 ppm

### Champignons
- **Temperatur**: 16-20°C (Tag), 14-16°C (Nacht)
- **Luftfeuchtigkeit**: 85-95%
- **CO₂**: 800-1200 ppm

## Einstellungen speichern

1. Passen Sie die gewünschten Werte an
2. Klicken Sie auf **"Einstellungen speichern"**
3. Eine Bestätigungsmeldung erscheint
4. Die neuen Werte werden sofort aktiv und in der Konfigurationsdatei gespeichert

## Einstellungen zurücksetzen

Klicken Sie auf **"Zurücksetzen"**, um die Formularfelder wieder auf die aktuell gespeicherten Werte zu setzen.

## Technische Details

- Die Einstellungen werden in `config/config.yaml` gespeichert
- Änderungen sind sofort wirksam (kein Neustart erforderlich)
- Die API-Endpunkte:
  - GET `/api/config` - Aktuelle Konfiguration laden
  - POST `/api/settings` - Neue Einstellungen speichern

## Fehlerbehebung

**Einstellungen werden nicht gespeichert**
- Überprüfen Sie die Schreibrechte für `config/config.yaml`
- Prüfen Sie die Browser-Konsole auf Fehlermeldungen

**Änderungen haben keine Wirkung**
- Warten Sie 1-2 Messzyklen (standardmäßig 60 Sekunden)
- Überprüfen Sie, ob der automatische Modus aktiviert ist

**Formular lädt nicht**
- Überprüfen Sie die Netzwerkverbindung
- Stellen Sie sicher, dass der Server läuft
- Öffnen Sie die Browser-Konsole für Details
