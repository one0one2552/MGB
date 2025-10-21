# Adaptive PID-Regelung - Dokumentation

## Übersicht

Die MGB - Mushroom Grow Box verwendet eine **adaptive PID-Regelung**, die sich automatisch an die Systemdynamik anpasst. Du musst die Parameter nicht mehr manuell über die YAML-Datei justieren!

## Was ist PID-Regelung?

Ein PID-Regler besteht aus drei Komponenten:

- **P (Proportional)**: Reagiert proportional zum aktuellen Fehler
- **I (Integral)**: Beseitigt stationäre Fehler über die Zeit
- **D (Derivative)**: Dämpft Überschwinger und Oszillationen

## Adaptive vs. Manuelle Regelung

### 🌟 Adaptive Regelung (EMPFOHLEN)

**Vorteile:**
- ✅ Passt sich automatisch an
- ✅ Lernt die optimalen Parameter selbst
- ✅ Kein manuelles Tuning erforderlich
- ✅ Funktioniert auch bei wechselnden Bedingungen
- ✅ Ideal für Anfänger

**Wie es funktioniert:**
1. Der Regler startet mit den Basis-Parametern aus der config.yaml
2. Alle 10 Messzyklen analysiert er die Performance:
   - Durchschnittlicher Fehler
   - Fehler-Varianz (Oszillation)
   - Stationärer Fehler
3. Basierend auf der Analyse passt er die Parameter an:
   - Bei Oszillation: Reduziert Kp, erhöht Kd
   - Bei großem Fehler: Erhöht Kp
   - Bei stationärem Fehler: Erhöht Ki
4. Parameter werden auf sinnvolle Bereiche begrenzt (0.1x - 5x der Basis-Werte)

### ⚙️ Manuelle Regelung

**Wann sinnvoll:**
- Du hast Erfahrung mit PID-Regelung
- Du möchtest sehr spezifische Parameter
- Das System verhält sich sehr ungewöhnlich

**Nachteile:**
- ❌ Erfordert Expertenwissen
- ❌ Zeitaufwendig (Trial-and-Error)
- ❌ Muss bei Änderungen neu justiert werden

## Konfiguration über das Web-Interface

### Adaptive Regelung aktivieren (Standard)

1. Öffne **Einstellungen** im Web-Interface
2. Scrolle zum Abschnitt **"🎛️ PID-Regelung"**
3. Aktiviere die Checkbox **"Adaptive PID-Regelung aktivieren"**
4. Speichere die Einstellungen

✨ **Fertig!** Das System lernt jetzt automatisch.

### Manuelle Parameter einstellen

1. Öffne **Einstellungen** im Web-Interface
2. Scrolle zum Abschnitt **"🎛️ PID-Regelung"**
3. Deaktiviere die Checkbox **"Adaptive PID-Regelung aktivieren"**
4. Die manuellen PID-Parameter werden sichtbar
5. Passe Kp, Ki, Kd für jeden Regler (Temperatur, Luftfeuchtigkeit, CO₂) an
6. Speichere die Einstellungen

## Parameter-Tuning (nur bei manueller Regelung)

### Allgemeine Richtlinien

**Kp (Proportional-Verstärkung):**
- Zu klein → Langsame Reaktion
- Zu groß → Überschwinger, Oszillation
- Empfohlen: 1.0 - 3.0

**Ki (Integral-Verstärkung):**
- Zu klein → Stationärer Fehler bleibt
- Zu groß → Langsame Oszillation
- Empfohlen: 0.1 - 1.0

**Kd (Differential-Verstärkung):**
- Zu klein → Überschwinger
- Zu groß → Empfindlich auf Rauschen
- Empfohlen: 0.3 - 2.0

### Ziegler-Nichols Methode

1. Setze Ki = 0, Kd = 0
2. Erhöhe Kp schrittweise, bis das System oszilliert
3. Notiere Kp_kritisch und Schwingungsdauer T
4. Berechne optimale Parameter:
   - Kp = 0.6 × Kp_kritisch
   - Ki = 1.2 × Kp_kritisch / T
   - Kd = 0.075 × Kp_kritisch × T

## Empfohlene Startwerte

### Temperatur-Regler
```yaml
kp: 2.0   # Moderate Reaktion
ki: 0.5   # Mittlere Integral-Wirkung
kd: 1.0   # Dämpfung
```

### Luftfeuchtigkeit-Regler
```yaml
kp: 1.5   # Etwas schwächere Reaktion (träges System)
ki: 0.3   # Geringe Integral-Wirkung
kd: 0.5   # Leichte Dämpfung
```

### CO₂-Regler
```yaml
kp: 1.0   # Moderate Reaktion
ki: 0.2   # Geringe Integral-Wirkung
kd: 0.3   # Leichte Dämpfung
```

## Diagnose von Regelproblemen

### Problem: System oszilliert (schwingt hin und her)

**Symptom:** Temperatur/Feuchtigkeit schwankt stark um den Sollwert

**Lösung bei manueller Regelung:**
1. Reduziere Kp um 20-30%
2. Erhöhe Kd um 20-30%

**Bei adaptiver Regelung:** 
- Wird automatisch erkannt und korrigiert
- Nach 2-3 Stunden sollte sich das System stabilisieren

### Problem: System erreicht Sollwert nicht

**Symptom:** Konstanter Abstand zum Sollwert bleibt

**Lösung bei manueller Regelung:**
1. Erhöhe Ki um 20-30%

**Bei adaptiver Regelung:**
- Wird automatisch erkannt und korrigiert
- Nach 1-2 Stunden sollte der Fehler verschwinden

### Problem: System reagiert zu langsam

**Symptom:** Dauert sehr lange, bis Sollwert erreicht wird

**Lösung bei manueller Regelung:**
1. Erhöhe Kp um 20-30%

**Bei adaptiver Regelung:**
- Wird automatisch erkannt und korrigiert
- Nach 1 Stunde sollte die Reaktion schneller sein

### Problem: Überschwinger (overshooting)

**Symptom:** System schießt über den Sollwert hinaus

**Lösung bei manueller Regelung:**
1. Erhöhe Kd um 30-50%
2. Reduziere Kp um 10-20%

**Bei adaptiver Regelung:**
- Wird automatisch erkannt und korrigiert

## API-Zugriff

### Aktuellen Tuning-Status abrufen

Die PID-Controller-Objekte bieten eine `get_tuning_info()` Methode:

```python
from controllers.pid_controller import PIDController

# Controller erstellen
pid = PIDController(kp=2.0, ki=0.5, kd=1.0, adaptive=True)

# Nach einigen Updates...
info = pid.get_tuning_info()
print(info)
# {
#     'kp': 2.15,        # Aktueller Kp (wurde angepasst)
#     'ki': 0.48,        # Aktueller Ki
#     'kd': 1.23,        # Aktueller Kd
#     'kp_base': 2.0,    # Basis-Kp
#     'ki_base': 0.5,    # Basis-Ki
#     'kd_base': 1.0,    # Basis-Kd
#     'adaptive': True,
#     'avg_error': 0.3,  # Durchschnittsfehler
#     'error_count': 20
# }
```

### Adaptive Regelung programmatisch umschalten

```python
# Adaptive Regelung deaktivieren
pid.set_adaptive(False)  # Verwendet wieder Basis-Parameter

# Adaptive Regelung aktivieren
pid.set_adaptive(True)   # Startet adaptive Anpassung

# Auf Basis-Parameter zurücksetzen
pid.reset_to_base_parameters()
```

## Best Practices

### ✅ DO's

- Verwende adaptive Regelung als Standard
- Gib dem System 2-4 Stunden zum Lernen
- Überwache die Performance im Dashboard
- Nutze die Basis-Parameter als guten Startpunkt

### ❌ DON'Ts

- Schalte nicht zu oft zwischen adaptiv/manuell um
- Ändere nicht täglich die PID-Parameter manuell
- Verwende keine extremen Werte (z.B. Kp > 10)
- Setze Ki nicht zu hoch (führt zu Instabilität)

## Technische Details

### Adaptions-Algorithmus

```python
# Alle 10 Messungen:
if oszillierend:
    kp *= 0.99  # 1% Reduktion
    kd *= 1.01  # 1% Erhöhung
elif großer_fehler:
    kp *= 1.02  # 2% Erhöhung
elif stationärer_fehler:
    ki *= 1.01  # 1% Erhöhung

# Begrenzung
kp = clamp(kp, kp_base * 0.1, kp_base * 5.0)
ki = clamp(ki, ki_base * 0.1, ki_base * 5.0)
kd = clamp(kd, kd_base * 0.1, kd_base * 5.0)
```

### Lernrate

Die Lernrate (learning_rate) bestimmt, wie schnell sich die Parameter ändern:
- Standard: 0.01 (1% pro Anpassung)
- Schneller: 0.05 (5% pro Anpassung) - kann instabil werden
- Langsamer: 0.005 (0.5% pro Anpassung) - sehr stabil, aber langsam

## Zusammenfassung

Die **adaptive PID-Regelung** ist die empfohlene Lösung für die meisten Benutzer:

- ✨ Keine manuelle Justierung erforderlich
- 🧠 Lernt automatisch die optimalen Parameter
- 🔄 Passt sich an veränderte Bedingungen an
- 📊 Verbessert sich kontinuierlich

Nur Experten sollten die manuelle Regelung verwenden, wenn sehr spezifische Anforderungen bestehen oder das adaptive System in Ausnahmefällen nicht funktioniert.
