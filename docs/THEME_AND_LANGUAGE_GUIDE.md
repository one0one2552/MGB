# MGB Web Interface - Theme & Language System

## Übersicht

Das MGB Web Interface unterstützt jetzt:
- **2 Themes**: Dark (klassisch) und Psychedelic (bunt animiert)
- **2 Sprachen**: Deutsch (Standard) und Englisch
- **Persistente Einstellungen**: Alle Präferenzen werden im Browser gespeichert

## Theme System

### Verfügbare Themes

#### 🌙 Dark Theme
- Klassisches, professionelles Dark Theme
- Dezente Animationen und Effekte
- Gut lesbar und augenfreundlich
- CSS-Datei: `theme-dark.css`

#### 🌈 Psychedelic Theme
- Buntes, animiertes Design
- Neon-Farben und Gradient-Effekte
- Pulsende Animationen und Glows
- CSS-Datei: `theme-psychedelic.css`

### Theme wechseln

1. Klicke auf den Theme-Button im Header (🌙 oder 🌈)
2. Wähle das gewünschte Theme aus dem Dropdown
3. Das Theme wird sofort angewendet und gespeichert

### Technische Details

- **JavaScript**: `theme-switcher.js`
- **CSS**: `theme-dark.css`, `theme-psychedelic.css`, `switchers.css`
- **Persistenz**: `localStorage.getItem('mgb-theme')`
- **Standard**: Dark Theme

## Multi-Language System

### Verfügbare Sprachen

- 🇩🇪 **Deutsch** (Standard)
- 🇬🇧 **English**

### Sprache wechseln

1. Klicke auf den Language-Button im Header (🇩🇪 oder 🇬🇧)
2. Wähle die gewünschte Sprache aus dem Dropdown
3. Die gesamte UI wird sofort übersetzt

### Neue Sprache hinzufügen

1. Öffne `src/utils/translations.py`
2. Erstelle neues Dictionary `TRANSLATIONS_XX` (XX = Sprachcode)
3. Füge alle Übersetzungsschlüssel hinzu
4. Registriere Sprache in `AVAILABLE_LANGUAGES`

Beispiel für Französisch:

```python
TRANSLATIONS_FR = {
    "app_title": "🍄 Contrôle de Champignonnière",
    "sensor_temperature": "Température",
    # ... weitere Übersetzungen
}

AVAILABLE_LANGUAGES = {
    'de': {...},
    'en': {...},
    'fr': {
        'name': 'Français',
        'flag': '🇫🇷',
        'translations': TRANSLATIONS_FR
    }
}
```

### HTML mit Übersetzungen versehen

Füge `data-i18n` Attribute zu allen Elementen hinzu, die übersetzt werden sollen:

```html
<!-- Text-Übersetzung -->
<h2 data-i18n="section_sensors">Sensordaten</h2>

<!-- Placeholder-Übersetzung -->
<input data-i18n="search_placeholder" data-i18n-placeholder />
```

### Technische Details

- **Python**: `src/utils/translations.py`
- **JavaScript**: `static/js/i18n.js`
- **API-Endpoints**:
  - `GET /api/translations/<lang>` - Übersetzungen abrufen
  - `GET /api/languages` - Verfügbare Sprachen abrufen
- **Persistenz**: `localStorage.getItem('mgb-language')`
- **Standard**: Deutsch (de)

## Dateistruktur

```
src/
├── web/
│   ├── app.py                          # Flask-App mit Translation-Endpoints
│   ├── templates/
│   │   ├── index.html                  # Hauptseite mit data-i18n Attributen
│   │   └── settings.html               # Einstellungsseite
│   └── static/
│       ├── css/
│       │   ├── theme-dark.css          # Dark Theme
│       │   ├── theme-psychedelic.css   # Psychedelic Theme
│       │   └── switchers.css           # Switcher-Komponenten
│       └── js/
│           ├── theme-switcher.js       # Theme-Verwaltung
│           ├── i18n.js                 # Internationalisierung
│           └── main.js                 # Hauptlogik mit i18n-Support
└── utils/
    └── translations.py                 # Übersetzungs-Dictionaries
```

## API-Referenz

### GET /api/translations/\<lang\>

Gibt alle Übersetzungen für eine Sprache zurück.

**Parameter:**
- `lang` - Sprachcode (de, en)

**Response:**
```json
{
    "app_title": "🍄 Mushroom Grow Box Control",
    "sensor_temperature": "Temperature",
    ...
}
```

### GET /api/languages

Gibt alle verfügbaren Sprachen zurück.

**Response:**
```json
{
    "de": {
        "name": "Deutsch",
        "flag": "🇩🇪"
    },
    "en": {
        "name": "English",
        "flag": "🇬🇧"
    }
}
```

## Browser-Kompatibilität

- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Mobile Browser (responsive Design)

## localStorage Keys

- `mgb-theme` - Ausgewähltes Theme ('dark' oder 'psychedelic')
- `mgb-language` - Ausgewählte Sprache ('de' oder 'en')

## Entwicklung

### Neues Theme hinzufügen

1. Erstelle neue CSS-Datei in `src/web/static/css/`
2. Registriere Theme in `theme-switcher.js`:
   ```javascript
   this.themes = {
       dark: {...},
       psychedelic: {...},
       newtheme: {
           name: 'New Theme',
           icon: '🎨',
           cssFile: '/static/css/theme-newtheme.css'
       }
   }
   ```

### Neue Übersetzungsschlüssel hinzufügen

1. Füge Schlüssel zu allen Sprachen in `translations.py` hinzu
2. Verwende `data-i18n` Attribut im HTML:
   ```html
   <span data-i18n="new_key">Standardtext</span>
   ```
3. Oder nutze JavaScript-API:
   ```javascript
   const text = window.i18n.t('new_key');
   ```

## Events

### Theme Changed Event

Wird ausgelöst, wenn das Theme gewechselt wird:

```javascript
window.addEventListener('themeChanged', (event) => {
    console.log('Neues Theme:', event.detail.theme);
    // Custom-Logik hier
});
```

### Language Changed Event

Wird ausgelöst, wenn die Sprache gewechselt wird:

```javascript
window.addEventListener('languageChanged', (event) => {
    console.log('Neue Sprache:', event.detail.language);
    // Charts neu beschriften, etc.
});
```

## Troubleshooting

### Theme wird nicht geladen
- Browser-Cache leeren (Strg+F5)
- Prüfen ob CSS-Datei existiert
- Browser-Console auf Fehler prüfen

### Übersetzungen fehlen
- Server neu starten
- Prüfen ob `translations.py` korrekt importiert wird
- API-Endpoint testen: `http://localhost:5000/api/translations/de`

### Präferenzen werden nicht gespeichert
- localStorage aktiviert?
- Private/Inkognito-Modus?
- Browser-Einstellungen prüfen

## Performance

- Themes: CSS wird dynamisch geladen, keine Duplikate
- Übersetzungen: Einmalig bei Sprachwechsel geladen
- localStorage: Sofortiger Zugriff auf Präferenzen
- Keine Server-Requests nach initialer Ladung

## Credits

Entwickelt für MGB - Mushroom Grow Box
Version: 2.0
Datum: Januar 2025
