# 5. Create sensor.py - the main sensor platform
sensor_py_content = '''"""Sensor platform for Custom Countdown Timer integration."""

import logging
from datetime import datetime, time, timedelta
from typing import Any, Dict, Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, WEEKDAYS, WORKING_DAYS, BUSINESS_MINUTES_PER_DAY

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Custom Countdown Timer sensors."""
    coordinator = CustomCountdownTimerCoordinator(hass, config_entry)
    await coordinator.async_config_entry_first_refresh()

    sensors = [
        CountdownTimerSensor(coordinator, config_entry),
        WorkTimeRemainingSensor(coordinator, config_entry),
        TimerStatusSensor(coordinator, config_entry),
    ]

    async_add_entities(sensors, True)

class CustomCountdownTimerCoordinator(DataUpdateCoordinator):
    """Custom countdown timer coordinator."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=1),
        )
        self.config_entry = config_entry
        self._calculate_schedule()

    def _calculate_schedule(self):
        """Calculate the schedule based on config."""
        now = datetime.now()
        
        # Find next occurrence of start day
        start_day = self.config_entry.data.get("start_day", "Wednesday")
        start_time_str = self.config_entry.data.get("start_time", "09:15")
        end_day = self.config_entry.data.get("end_day", "Tuesday")
        end_time_str = self.config_entry.data.get("end_time", "15:30")
        
        # Parse times
        start_hour, start_minute = map(int, start_time_str.split(":"))
        end_hour, end_minute = map(int, end_time_str.split(":"))
        
        # Find start date (next occurrence of start_day)
        days_ahead = (list(WEEKDAYS.values()).index(start_day) - now.weekday()) % 7
        if days_ahead == 0 and now.time() > time(start_hour, start_minute):
            days_ahead = 7
        
        self.start_datetime = (now + timedelta(days=days_ahead)).replace(
            hour=start_hour, minute=start_minute, second=0, microsecond=0
        )
        
        # Find end date
        end_days_ahead = (list(WEEKDAYS.values()).index(end_day) - self.start_datetime.weekday()) % 7
        if end_day == start_day:
            end_days_ahead = 7
        elif end_days_ahead <= 0:
            end_days_ahead += 7
            
        self.end_datetime = (self.start_datetime + timedelta(days=end_days_ahead)).replace(
            hour=end_hour, minute=end_minute, second=0, microsecond=0
        )
        
        # Get holidays
        self.holidays = []
        if self.config_entry.data.get("thursday_holiday", False):
            self.holidays.append("Thursday")
        if self.config_entry.data.get("friday_holiday", False):
            self.holidays.append("Friday")
        if self.config_entry.data.get("monday_holiday", False):
            self.holidays.append("Monday")

    async def _async_update_data(self) -> Dict[str, Any]:
        """Update timer data."""
        now = datetime.now()
        
        # Calculate status
        if now < self.start_datetime:
            status = "Not Started"
            time_remaining = self.end_datetime - self.start_datetime
        elif now > self.end_datetime:
            status = "Completed"
            time_remaining = timedelta(0)
        else:
            current_day = WEEKDAYS[now.weekday()]
            current_time = now.time()
            
            # Check if it's a working day and time
            if (current_day in WORKING_DAYS and 
                current_day not in self.holidays and
                time(9, 15) <= current_time <= time(15, 30)):
                status = "Running"
            elif current_day in ["Saturday", "Sunday"]:
                status = "Paused (Weekend)"
            elif current_day in self.holidays:
                status = "Paused (Holiday)"
            else:
                status = "Paused (After Hours)"
            
            time_remaining = self.end_datetime - now
        
        # Calculate work time remaining
        work_minutes_remaining = self._calculate_work_time_remaining(now)
        
        return {
            "status": status,
            "time_remaining": time_remaining,
            "work_minutes_remaining": work_minutes_remaining,
            "start_datetime": self.start_datetime,
            "end_datetime": self.end_datetime,
            "holidays": self.holidays,
        }

    def _calculate_work_time_remaining(self, now: datetime) -> int:
        """Calculate remaining work time in minutes."""
        if now >= self.end_datetime:
            return 0
        
        total_minutes = 0
        current_date = max(now.date(), self.start_datetime.date())
        end_date = self.end_datetime.date()
        
        while current_date <= end_date:
            day_name = WEEKDAYS[current_date.weekday()]
            
            # Skip weekends and holidays
            if day_name in ["Saturday", "Sunday"] or day_name in self.holidays:
                current_date += timedelta(days=1)
                continue
            
            # Calculate minutes for this day
            if current_date == end_date:
                # Last day - only count until end time
                if current_date == now.date() and now.time() > time(9, 15):
                    # Current day, already started
                    start_time = max(now.time(), time(9, 15))
                    end_time = min(time(15, 30), self.end_datetime.time())
                else:
                    start_time = time(9, 15)
                    end_time = self.end_datetime.time()
            elif current_date == now.date():
                # Current day
                start_time = max(now.time(), time(9, 15))
                end_time = time(15, 30)
            else:
                # Future day
                start_time = time(9, 15)
                end_time = time(15, 30)
            
            if start_time < end_time:
                day_minutes = (datetime.combine(current_date, end_time) - 
                              datetime.combine(current_date, start_time)).total_seconds() / 60
                total_minutes += day_minutes
            
            current_date += timedelta(days=1)
        
        return int(total_minutes)

class CountdownTimerSensor(CoordinatorEntity, SensorEntity):
    """Countdown timer sensor."""

    def __init__(self, coordinator: CustomCountdownTimerCoordinator, config_entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._attr_name = "Custom Countdown Timer"
        self._attr_unique_id = f"{config_entry.entry_id}_countdown"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return "unknown"
        
        time_remaining = self.coordinator.data["time_remaining"]
        days = time_remaining.days
        hours, remainder = divmod(time_remaining.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        return f"{days}d {hours}h {minutes}m {seconds}s"

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return extra state attributes."""
        if not self.coordinator.data:
            return {}
        
        return {
            "status": self.coordinator.data["status"],
            "start_datetime": self.coordinator.data["start_datetime"].isoformat(),
            "end_datetime": self.coordinator.data["end_datetime"].isoformat(),
            "holidays": self.coordinator.data["holidays"],
        }

class WorkTimeRemainingSensor(CoordinatorEntity, SensorEntity):
    """Work time remaining sensor."""

    def __init__(self, coordinator: CustomCountdownTimerCoordinator, config_entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._attr_name = "Work Time Remaining"
        self._attr_unique_id = f"{config_entry.entry_id}_work_time"
        self._attr_unit_of_measurement = "minutes"

    @property
    def state(self) -> int:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return 0
        return self.coordinator.data["work_minutes_remaining"]

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return extra state attributes."""
        if not self.coordinator.data:
            return {}
        
        minutes = self.coordinator.data["work_minutes_remaining"]
        hours = minutes // 60
        mins = minutes % 60
        
        return {
            "formatted": f"{hours}h {mins}m",
            "hours": hours,
            "minutes": mins,
        }

class TimerStatusSensor(CoordinatorEntity, SensorEntity):
    """Timer status sensor."""

    def __init__(self, coordinator: CustomCountdownTimerCoordinator, config_entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._attr_name = "Timer Status"
        self._attr_unique_id = f"{config_entry.entry_id}_status"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return "unknown"
        return self.coordinator.data["status"]
'''

with open(f"{base_dir}/custom_components/custom_countdown_timer/sensor.py", "w") as f:
    f.write(sensor_py_content)

print("Created sensor.py")