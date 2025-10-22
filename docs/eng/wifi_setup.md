# WiFi Access Point Setup for MGB - Mushroom Grow Box

## Overview

The system features an automatic WiFi manager that creates an Access Point (AP) when no WLAN connection can be established. This enables easy initial configuration without monitor or keyboard.

## How It Works

1. **At startup**: System attempts to connect to saved WLAN
2. **On failure**: After 3 attempts, an Access Point is automatically created
3. **Setup portal**: User can connect to AP and configure WLAN
4. **After connection**: AP is terminated, normal operation continues

## Installation on Raspberry Pi

### Step 1: Clone Repository

```bash
git clone https://github.com/one0one2552/MGB.git
cd MGB
```

### Step 2: Install WiFi-AP Software

```bash
sudo bash install_wifi_ap.sh
```

This script installs:
- `hostapd` - Access Point software
- `dnsmasq` - DHCP/DNS server
- `dhcpcd` - DHCP client daemon

### Step 3: Install Python Dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 4: Start System

```bash
python src/main.py
```

## Access Point Mode

### Default Settings

- **SSID**: `MGB-Setup`
- **Password**: `pilzzucht2025`
- **IP Address**: `192.168.4.1`
- **Setup URL**: `http://192.168.4.1/wifi/setup`

### Customizing Settings

Edit `config/config.yaml`:

```yaml
wifi:
  ap_ssid: "MyCustomName"
  ap_password: "mysecurepassword"
  check_interval: 30
  max_retries: 3
```

**Important**: Password must be at least 8 characters long!

## Using the Setup Portal

### 1. Connect to Access Point

1. Search for the WLAN `MGB-Setup` on your smartphone/laptop
2. Connect with the password `pilzzucht2025`

### 2. Open Setup Page

- Open a browser
- Go to: `http://192.168.4.1/wifi/setup`

### 3. Configure WLAN

1. Click "Search for Networks"
2. Select your WLAN from the list
3. Enter the password
4. Click "Connect"

### 4. Done

- After successful connection, the AP is automatically terminated
- System is now accessible via your normal WLAN
- Main interface: `http://mgb.local` or the assigned IP

## Troubleshooting

### Access Point won't start

**Problem**: hostapd or dnsmasq are already running

```bash
sudo systemctl stop hostapd
sudo systemctl stop dnsmasq
sudo systemctl disable hostapd
sudo systemctl disable dnsmasq
```

### WLAN connection doesn't work

**Solution 1**: Manually configure WPA Supplicant

```bash
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```

Add:

```
network={
    ssid="YourWLAN"
    psk="YourPassword"
}
```

**Solution 2**: Manually restart Access Point

```bash
python -c "from src.utils.wifi_manager import WiFiManager; wm = WiFiManager(); wm.start_access_point()"
```

### Cannot reach setup page

1. Check connection: `ip addr show wlan0`
2. Should show `192.168.4.1`
3. Ping test: `ping 192.168.4.1`
4. Check firewall: `sudo iptables -L`

### Check Log Files

```bash
# System logs
sudo journalctl -u hostapd -n 50
sudo journalctl -u dnsmasq -n 50

# Application logs
tail -f logs/mgb_mushroom_grow_box_*.log
```

## API Endpoints

The WiFi setup portal offers the following API endpoints:

### Get Status
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

### Scan Networks
```
GET /wifi/api/scan
```

Response:
```json
{
  "status": "success",
  "networks": [
    {
      "ssid": "MyWLAN",
      "signal": "75",
      "security": "WPA2"
    }
  ]
}
```

### Connect to Network
```
POST /wifi/api/connect
Content-Type: application/json

{
  "ssid": "MyWLAN",
  "password": "mypassword"
}
```

Response:
```json
{
  "status": "success",
  "message": "Successfully connected to MyWLAN"
}
```

## Security Notes

1. **Change password**: Change the default AP password in the configuration
2. **Temporary only**: AP should only be used for setup
3. **Network isolation**: AP is isolated from home network
4. **HTTPS**: Configure HTTPS for production environment

## Automatic Startup (Systemd)

Create a service for automatic startup:

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

Enable:

```bash
sudo systemctl daemon-reload
sudo systemctl enable mgb
sudo systemctl start mgb
```

## Development Mode (without Hardware)

On Windows/Mac/Linux without Raspberry Pi, the WiFi manager works in simulation mode:
- Always returns "connected"
- Doesn't create real Access Points
- Shows example networks in scan

This enables development and testing of the interface without hardware.
