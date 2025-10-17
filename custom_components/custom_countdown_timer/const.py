"""Constants for Custom Countdown Timer integration."""

DOMAIN = "custom_countdown_timer"
PLATFORMS = ["sensor"]

# Default configuration
DEFAULT_START_DAY = "Wednesday"
DEFAULT_START_TIME = "09:15"
DEFAULT_END_DAY = "Tuesday"
DEFAULT_END_TIME = "15:30"
DEFAULT_DAILY_START = "09:15"
DEFAULT_DAILY_END = "15:30"

# Weekdays
WEEKDAYS = {
    0: "Monday",
    1: "Tuesday", 
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
}

WORKING_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
WEEKEND_DAYS = ["Saturday", "Sunday"]

# Business hours per day in minutes
BUSINESS_MINUTES_PER_DAY = 375  # 6 hours 15 minutes (09:15 to 15:30)
