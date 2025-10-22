# Settings - User Guide

## Accessing the Settings Page

The settings page is accessible via the web interface:
- URL: `http://mgb.local:5000/settings` or `http://localhost:5000/settings`
- Click on the **"⚙️ Settings"** button in the dashboard

## Available Settings

### 🌡️ Temperature

**Target Value (°C)**
- Range: 10-35°C
- Recommended: 20-24°C for most mushroom species
- This is the desired temperature in the grow box

**Tolerance (±°C)**
- Range: 0.1-5°C
- Recommended: 1°C
- Allowed deviation from target value before heating is activated

### 💧 Humidity

**Target Value (%)**
- Range: 50-95%
- Recommended: 80-90% for fruiting phase
- This is the desired relative humidity

**Tolerance (±%)**
- Range: 1-10%
- Recommended: 5%
- Allowed deviation from target value before pump is activated

### 🌬️ CO₂ Level

**Target Value (ppm)**
- Range: 400-2000 ppm
- Recommended: 600-1000 ppm
- Fresh air has approx. 400 ppm, higher values promote mycelium growth

**Tolerance (±ppm)**
- Range: 10-200 ppm
- Recommended: 100 ppm
- Allowed deviation from target value before fan is activated

### 🌓 Day/Night Rhythm

The MGB supports different settings for day and night:

**Times**
- **Day starts at**: Start time of day phase (e.g., 06:00)
- **Night starts at**: Start time of night phase (e.g., 22:00)

**Day Values**
- **Day temperature**: Target temperature during day phase
- **Day humidity**: Target humidity during day phase

**Night Values**
- **Night temperature**: Target temperature during night phase (usually 2-4°C lower)
- **Night humidity**: Target humidity during night phase (usually 5% higher)

## Recommended Settings by Mushroom Species

### Oyster Mushrooms (Pleurotus)
- **Temperature**: 18-24°C (day), 15-18°C (night)
- **Humidity**: 85-95%
- **CO₂**: 500-800 ppm

### Shiitake
- **Temperature**: 18-22°C (day), 15-18°C (night)
- **Humidity**: 80-90%
- **CO₂**: 600-1000 ppm

### Button Mushrooms
- **Temperature**: 16-20°C (day), 14-16°C (night)
- **Humidity**: 85-95%
- **CO₂**: 800-1200 ppm

## Saving Settings

1. Adjust the desired values
2. Click on **"Save Settings"**
3. A confirmation message appears
4. The new values become active immediately and are saved in the configuration file

## Resetting Settings

Click on **"Reset"** to restore the form fields to the currently saved values.

## Technical Details

- Settings are saved in `config/config.yaml`
- Changes take effect immediately (no restart required)
- API endpoints:
  - GET `/api/config` - Load current configuration
  - POST `/api/settings` - Save new settings

## Troubleshooting

**Settings are not saved**
- Check write permissions for `config/config.yaml`
- Check browser console for error messages

**Changes have no effect**
- Wait 1-2 measurement cycles (default 60 seconds)
- Check if automatic mode is enabled

**Form doesn't load**
- Check network connection
- Make sure the server is running
- Open browser console for details
