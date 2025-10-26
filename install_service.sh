#!/bin/bash
#
# MGB Systemd Service Installation Script
# Installiert und aktiviert den MGB Service für automatischen Start
#

set -e  # Bei Fehler abbrechen

echo "============================================================"
echo "MGB Systemd Service Installation"
echo "============================================================"
echo ""

# Prüfen ob als root ausgeführt
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Fehler: Dieses Script muss als root ausgeführt werden"
    echo "Verwende: sudo ./install_service.sh"
    exit 1
fi

# Aktuelles Verzeichnis ermitteln
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "📁 MGB Verzeichnis: $SCRIPT_DIR"
echo ""

# Service-Datei nach /etc/systemd/system kopieren
echo "📋 Kopiere Service-Datei..."
cp "$SCRIPT_DIR/mgb.service" /etc/systemd/system/mgb.service
echo "✓ Service-Datei kopiert"
echo ""

# Systemd neu laden
echo "🔄 Lade systemd Konfiguration neu..."
systemctl daemon-reload
echo "✓ Systemd neu geladen"
echo ""

# Service aktivieren (Autostart)
echo "🚀 Aktiviere Autostart..."
systemctl enable mgb.service
echo "✓ Autostart aktiviert"
echo ""

# Service starten
echo "▶️  Starte MGB Service..."
systemctl start mgb.service
echo "✓ Service gestartet"
echo ""

# Status anzeigen
echo "============================================================"
echo "Installation abgeschlossen!"
echo "============================================================"
echo ""
echo "📊 Service Status:"
systemctl status mgb.service --no-pager -l
echo ""
echo "============================================================"
echo "Nützliche Befehle:"
echo "============================================================"
echo "Status prüfen:        sudo systemctl status mgb"
echo "Service stoppen:      sudo systemctl stop mgb"
echo "Service starten:      sudo systemctl start mgb"
echo "Service neustarten:   sudo systemctl restart mgb"
echo "Logs anzeigen:        sudo journalctl -u mgb -f"
echo "Logs der letzten 100: sudo journalctl -u mgb -n 100"
echo "Autostart aus:        sudo systemctl disable mgb"
echo "============================================================"
