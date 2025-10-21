#!/bin/bash

# Installationsskript für Raspberry Pi WiFi Access Point
# Dieses Skript installiert und konfiguriert alle notwendigen Pakete

echo "=========================================="
echo "MGB - Mushroom Grow Box - WiFi Access Point Setup"
echo "=========================================="
echo ""

# Prüfe ob Root
if [ "$EUID" -ne 0 ]; then 
    echo "Bitte als root ausführen (sudo bash install_wifi_ap.sh)"
    exit 1
fi

echo "1. Aktualisiere System..."
apt-get update

echo ""
echo "2. Installiere notwendige Pakete..."
apt-get install -y hostapd dnsmasq dhcpcd

echo ""
echo "3. Stoppe Services (werden bei Bedarf vom System gestartet)..."
systemctl stop hostapd
systemctl stop dnsmasq

echo ""
echo "4. Deaktiviere automatischen Start (WiFi-Manager übernimmt Steuerung)..."
systemctl disable hostapd
systemctl disable dnsmasq

echo ""
echo "5. Konfiguriere dhcpcd..."
# Backup erstellen
cp /etc/dhcpcd.conf /etc/dhcpcd.conf.backup

# Füge Konfiguration hinzu falls nicht vorhanden
if ! grep -q "interface wlan0" /etc/dhcpcd.conf; then
    cat >> /etc/dhcpcd.conf << EOF

# MGB - Mushroom Grow Box WiFi Configuration
# Diese Zeilen werden nur im AP-Modus aktiv
#interface wlan0
#    static ip_address=192.168.4.1/24
#    nohook wpa_supplicant
EOF
fi

echo ""
echo "6. Erstelle Beispiel-Konfigurationsdateien..."

# hostapd Beispielkonfiguration
cat > /etc/hostapd/hostapd.conf.example << EOF
# Beispielkonfiguration - wird vom WiFi-Manager überschrieben
interface=wlan0
driver=nl80211
ssid=MGB-Setup
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=pilzzucht2025
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
EOF

# dnsmasq Beispielkonfiguration
cat > /etc/dnsmasq.conf.example << EOF
# Beispielkonfiguration - wird vom WiFi-Manager überschrieben
interface=wlan0
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
EOF

echo ""
echo "7. Setze Berechtigungen..."
chmod 600 /etc/hostapd/hostapd.conf.example
chmod 644 /etc/dnsmasq.conf.example

echo ""
echo "=========================================="
echo "Installation abgeschlossen!"
echo "=========================================="
echo ""
echo "Der WiFi-Manager kann jetzt verwendet werden."
echo "Bei fehlender WLAN-Verbindung wird automatisch"
echo "ein Access Point erstellt."
echo ""
echo "SSID: MGB-Setup"
echo "Passwort: pilzzucht2025"
echo "Setup-URL: http://192.168.4.1/wifi/setup"
echo ""
echo "Starten Sie die MGB-Anwendung:"
echo "cd /home/pi/MGB"
echo "python src/main.py"
echo ""
