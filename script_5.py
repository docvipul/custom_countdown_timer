# 6. Create README.md with installation and usage instructions
readme_content = '''# Custom Countdown Timer for Home Assistant

A Home Assistant custom integration that provides a business hours countdown timer with automatic scheduling and holiday support.

## Features

- **Automatic Scheduling**: Starts every Wednesday at 9:15 AM, ends on following Tuesday at 3:30 PM
- **Business Hours Only**: Runs only during 9:15 AM - 3:30 PM on weekdays
- **Weekend Pausing**: Automatically pauses during weekends
- **Holiday Support**: Configure Thursday, Friday, or Monday as holidays
- **Multiple Sensors**: Provides countdown timer, work time remaining, and status sensors
- **Real-time Updates**: Updates every second during active periods

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Go to "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/yourusername/custom_countdown_timer`
6. Select "Integration" as the category
7. Click "Add"
8. Find "Custom Countdown Timer" in HACS and install it
9. Restart Home Assistant

### Manual Installation

1. Download the `custom_countdown_timer` folder
2. Copy it to your `custom_components` directory in your Home Assistant config folder
3. Restart Home Assistant

## Configuration

1. Go to Settings → Devices & Services
2. Click "Add Integration"
3. Search for "Custom Countdown Timer"
4. Configure your settings:
   - **Start Day**: Day of the week to start (default: Wednesday)
   - **Start Time**: Time to start each day (default: 09:15)
   - **End Day**: Day of the week to end (default: Tuesday)
   - **End Time**: Time to end (default: 15:30)
   - **Holiday Options**: Check Thursday/Friday/Monday as holidays if needed

## Sensors Created

The integration creates three sensors:

### 1. Custom Countdown Timer (`sensor.custom_countdown_timer`)
- **State**: Time remaining in format "Xd Yh Zm Ws"
- **Attributes**:
  - `status`: Current timer status
  - `start_datetime`: When the timer started
  - `end_datetime`: When the timer will end
  - `holidays`: List of configured holidays

### 2. Work Time Remaining (`sensor.work_time_remaining`)
- **State**: Remaining work minutes (excluding pauses)
- **Unit**: minutes
- **Attributes**:
  - `formatted`: Human-readable format "Xh Ym"
  - `hours`: Hours remaining
  - `minutes`: Minutes remaining

### 3. Timer Status (`sensor.timer_status`)
- **State**: Current status
  - "Not Started" - Before start time
  - "Running" - During business hours
  - "Paused (After Hours)" - Outside business hours
  - "Paused (Weekend)" - During weekends
  - "Paused (Holiday)" - During configured holidays
  - "Completed" - After end time

## Usage Examples

### Automation Example
```yaml
automation:
  - alias: "Notify when timer starts"
    trigger:
      - platform: state
        entity_id: sensor.timer_status
        to: "Running"
    action:
      - service: notify.mobile_app_your_phone
        data:
          message: "Countdown timer has started!"

  - alias: "Notify work time remaining"
    trigger:
      - platform: time_pattern
        hours: "12"
        minutes: "0"
    condition:
      - condition: state
        entity_id: sensor.timer_status
        state: "Running"
    action:
      - service: notify.mobile_app_your_phone
        data:
          message: "{{ states('sensor.work_time_remaining') }} minutes of work time remaining"
```

### Lovelace Card Example
```yaml
type: entities
title: Countdown Timer
entities:
  - entity: sensor.custom_countdown_timer
    name: Time Remaining
  - entity: sensor.work_time_remaining
    name: Work Hours Left
  - entity: sensor.timer_status
    name: Status
```

## Support

If you encounter any issues, please create an issue on the GitHub repository.

## License

This project is licensed under the MIT License.
'''

with open(f"{base_dir}/README.md", "w") as f:
    f.write(readme_content)

print("Created README.md")