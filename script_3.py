# 4. Create config_flow.py for UI configuration
config_flow_py_content = '''"""Config flow for Custom Countdown Timer integration."""

import voluptuous as vol
from typing import Any, Dict, Optional

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN,
    DEFAULT_START_DAY,
    DEFAULT_START_TIME,
    DEFAULT_END_DAY,
    DEFAULT_END_TIME,
    WORKING_DAYS
)

class CustomCountdownTimerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Custom Countdown Timer."""

    VERSION = 1

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate time format
            try:
                # Basic validation - you might want more sophisticated validation
                start_time = user_input["start_time"]
                end_time = user_input["end_time"]
                
                return self.async_create_entry(
                    title="Custom Countdown Timer",
                    data=user_input,
                )
            except Exception:
                errors["base"] = "invalid_time"

        data_schema = vol.Schema({
            vol.Required("start_day", default=DEFAULT_START_DAY): vol.In(WORKING_DAYS + ["Saturday", "Sunday"]),
            vol.Required("start_time", default=DEFAULT_START_TIME): str,
            vol.Required("end_day", default=DEFAULT_END_DAY): vol.In(WORKING_DAYS + ["Saturday", "Sunday"]),
            vol.Required("end_time", default=DEFAULT_END_TIME): str,
            vol.Optional("thursday_holiday", default=False): bool,
            vol.Optional("friday_holiday", default=False): bool,
            vol.Optional("monday_holiday", default=False): bool,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )
'''

with open(f"{base_dir}/custom_components/custom_countdown_timer/config_flow.py", "w") as f:
    f.write(config_flow_py_content)

print("Created config_flow.py")