# Custom Countdown Timer - Home Assistant HACS Integration

## 🎯 What This Creates

This integration converts your countdown timer app into a Home Assistant custom component that can be installed via HACS (Home Assistant Community Store).

## 📋 Features Implemented

### ✅ Core Functionality
- Automatic Wednesday 9:15 AM to Tuesday 3:30 PM schedule
- Business hours only operation (9:15 AM - 3:30 PM)
- Weekend pausing (Saturday/Sunday)
- Holiday support (Thursday, Friday, Monday)
- Real-time updates every second

### 🎛️ Home Assistant Integration
- **Config Flow UI**: Easy setup through Home Assistant interface
- **Multiple Sensors**: Three distinct sensors for different data
- **Persistent Configuration**: Settings saved across restarts
- **HACS Compatible**: Proper manifest and structure for HACS

## 📊 Sensors Created

1. **sensor.custom_countdown_timer**
   - Shows full countdown: "5d 12h 30m 45s"
   - Attributes: status, start_datetime, end_datetime, holidays

2. **sensor.work_time_remaining** 
   - Shows work minutes only: "1125" (minutes)
   - Attributes: formatted ("18h 45m"), hours, minutes

3. **sensor.timer_status**
   - Current status: "Running", "Paused (Weekend)", etc.

## 🔧 Installation Methods

### Method 1: HACS (Recommended)
1. Upload files to GitHub repository
2. Add repository to HACS as custom integration
3. Install through HACS interface
4. Restart Home Assistant
5. Add integration via UI

### Method 2: Manual Installation
1. Extract zip file
2. Copy custom_components/custom_countdown_timer to your config folder
3. Restart Home Assistant
4. Add integration via UI

### Method 3: Installation Script
1. Run install.sh from Home Assistant environment
2. Restart Home Assistant
3. Add integration via UI

## 📝 Configuration Options

When setting up the integration, you can configure:
- Start day (default: Wednesday)
- Start time (default: 09:15)
- End day (default: Tuesday)  
- End time (default: 15:30)
- Thursday holiday checkbox
- Friday holiday checkbox
- Monday holiday checkbox

## 🏠 Home Assistant Usage

### Lovelace Dashboard
```yaml
type: entities
title: Project Timer
entities:
  - entity: sensor.custom_countdown_timer
    name: Time Remaining
  - entity: sensor.work_time_remaining  
    name: Work Hours Left
  - entity: sensor.timer_status
    name: Current Status
```

### Automations
```yaml
automation:
  - alias: "Project Timer Started"
    trigger:
      - platform: state
        entity_id: sensor.timer_status
        to: "Running"
    action:
      - service: notify.mobile_app
        data:
          message: "Project timer is now running!"
```

### Template Sensors
```yaml
template:
  - sensor:
      - name: "Work Days Remaining"
        state: "{{ (states('sensor.work_time_remaining') | int / 375) | round(1) }}"
        unit_of_measurement: "days"
```

## 🔄 Technical Implementation

### Coordinator Pattern
- Uses DataUpdateCoordinator for efficient updates
- Updates every second during active periods
- Calculates complex business logic for work time

### State Management
- Handles timezone calculations
- Manages business hours vs calendar time
- Accounts for holidays dynamically

### Error Handling
- Validates time formats in config flow
- Handles edge cases for date calculations
- Provides meaningful error messages

## 🎯 Benefits Over Web App

1. **Native Integration**: Works with all Home Assistant features
2. **Automation Ready**: Trigger automations based on timer state
3. **Dashboard Integration**: Add to any Lovelace dashboard
4. **Persistent**: Survives restarts and updates
5. **Mobile Access**: Available in Home Assistant mobile app
6. **Voice Control**: Works with Alexa/Google Assistant via HA
7. **Notifications**: Send alerts when status changes

## 📱 Mobile & Voice Examples

"Hey Google, what's the status of my project timer?"
→ "The timer status is currently running"

"Alexa, how much work time is remaining?"
→ "There are 18 hours and 45 minutes remaining"

## 🔧 Files Included

- `manifest.json` - Integration metadata
- `__init__.py` - Main integration setup
- `const.py` - Constants and configuration
- `config_flow.py` - UI configuration flow
- `sensor.py` - Sensor entities and logic
- `hacs.json` - HACS compatibility
- `README.md` - Documentation
- `install.sh` - Installation script

This integration brings your countdown timer into the Home Assistant ecosystem with full native support and automation capabilities!
