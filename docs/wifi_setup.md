# WiFi Access Point Setup für MGB - Mushroom Grow Box

## Übersicht

Das System verfügt über einen automatischen WiFi-Manager, der einen Access Point (AP) erstellt, wenn keine WLAN-Verbindung hergestellt werden kann. Dies ermöglicht eine einfache Erstkonfiguration ohne Monitor oder Tastatur.

## Funktionsweise

1. **Beim Start**: System versucht sich mit gespeichertem WLAN zu verbinden
2. **Bei Fehler**: Nach 3 Versuchen wird automatisch ein Access Point erstellt
3. **Setup-Portal**: Benutzer kann sich mit AP verbinden und WLAN konfigurieren
4. **Nach Verbindung**: AP wird beendet, normale Funktion wird fortgesetzt

## Installation auf Raspberry Pi

### Schritt 1: Repository klonen

```bash
git clone https://github.com/one0one2552/MGB.git
cd MGB
```

### Schritt 2: WiFi-AP Software installieren

```bash
sudo bash install_wifi_ap.sh
```

Dieses Skript installiert:
- `hostapd` - Access Point Software
- `dnsmasq` - DHCP/DNS Server
- `dhcpcd` - DHCP Client Daemon

### Schritt 3: Python-Abhängigkeiten installieren

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Schritt 4: System starten

```bash
python src/main.py
```

## Access Point Modus

### Standardeinstellungen

- **SSID**: `MGB-Setup`
- **Passwort**: `pilzzucht2025`
- **IP-Adresse**: `192.168.4.1`
- **Setup-URL**: `http://192.168.4.1/wifi/setup`

### Anpassung der Einstellungen

Bearbeiten Sie `config/config.yaml`:

```yaml
wifi:
  ap_ssid: "MeinCustomName"
  ap_password: "meinsicherespasswort"
  check_interval: 30
  max_retries: 3
```

**Wichtig**: Passwort muss mindestens 8 Zeichen lang sein!

## Setup-Portal Nutzung

### 1. Mit Access Point verbinden

1. Suchen Sie auf Ihrem Smartphone/Laptop nach dem WLAN `MGB-Setup`
2. Verbinden Sie sich mit dem Passwort `pilzzucht2025`

### 2. Setup-Seite öffnen

- Öffnen Sie einen Browser
- Gehen Sie zu: `http://192.168.4.1/wifi/setup`

### 3. WLAN konfigurieren

1. Klicken Sie auf "Nach Netzwerken suchen"
2. Wählen Sie Ihr WLAN aus der Liste
3. Geben Sie das Passwort ein
4. Klicken Sie auf "Verbinden"

### 4. Fertig

- Nach erfolgreicher Verbindung wird der AP automatisch beendet
- System ist nun über Ihr normales WLAN erreichbar
- Hauptoberfläche: `http://mgb.local` oder die zugewiesene IP

## Fehlerbehebung

### Access Point startet nicht

**Problem**: hostapd oder dnsmasq laufen bereits

```bash
sudo systemctl stop hostapd
sudo systemctl stop dnsmasq
sudo systemctl disable hostapd
sudo systemctl disable dnsmasq
```

### WLAN-Verbindung funktioniert nicht

**Lösung 1**: Manuell WPA Supplicant konfigurieren

```bash
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```

Fügen Sie hinzu:

```
network={
    ssid="IhrWLAN"
    psk="IhrPasswort"
}
```

**Lösung 2**: Access Point manuell neu starten

```bash
python -c "from src.utils.wifi_manager import WiFiManager; wm = WiFiManager(); wm.start_access_point()"
```

### Kann Setup-Seite nicht erreichen

1. Prüfen Sie die Verbindung: `ip addr show wlan0`
2. Sollte `192.168.4.1` anzeigen
3. Ping-Test: `ping 192.168.4.1`
4. Firewall prüfen: `sudo iptables -L`

### Log-Dateien prüfen

```bash
# System-Logs
sudo journalctl -u hostapd -n 50
sudo journalctl -u dnsmasq -n 50

# Anwendungs-Logs
tail -f logs/mgb_mushroom_grow_box_*.log
```

## API-Endpunkte

Das WiFi-Setup-Portal bietet folgende API-Endpunkte:

### Status abrufen
```
GET /wifi/api/status
```

Response:
```json
{
  "ap_mode": true,
  "ap_ssid": "MGB-Setup",
  "connected": false,
  "is_raspberry_pi": true
}
```

### Netzwerke scannen
```
GET /wifi/api/scan
```

Response:
```json
{
  "status": "success",
  "networks": [
    {
      "ssid": "MeinWLAN",
      "signal": "75",
      "security": "WPA2"
    }
  ]
}
```

### Mit Netzwerk verbinden
```
POST /wifi/api/connect
Content-Type: application/json

{
  "ssid": "MeinWLAN",
  "password": "meinpasswort"
}
```

Response:
```json
{
  "status": "success",
  "message": "Erfolgreich mit MeinWLAN verbunden"
}
```

## Sicherheitshinweise

1. **Passwort ändern**: Ändern Sie das Standard-AP-Passwort in der Konfiguration
2. **Nur temporär**: AP sollte nur für Setup verwendet werden
3. **Netzwerk-Isolation**: AP ist vom Hausnetzwerk isoliert
4. **HTTPS**: Für Produktivumgebung HTTPS konfigurieren

## Automatischer Start (Systemd)

Erstellen Sie einen Service für automatischen Start:

```bash
sudo nano /etc/systemd/system/mgb.service
```

```ini
[Unit]
Description=MGB - Mushroom Grow Box Monitoring System
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/MGB
ExecStart=/home/pi/MGB/venv/bin/python /home/pi/MGB/src/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Aktivieren:

```bash
sudo systemctl daemon-reload
sudo systemctl enable mgb
sudo systemctl start mgb
```

## Entwicklungsmodus (ohne Hardware)

Auf Windows/Mac/Linux ohne Raspberry Pi funktioniert der WiFi-Manager im Simulationsmodus:
- Gibt immer "verbunden" zurück
- Erstellt keine echten Access Points
- Zeigt Beispiel-Netzwerke im Scan

Dies ermöglicht Entwicklung und Testing der Oberfläche ohne Hardware.
