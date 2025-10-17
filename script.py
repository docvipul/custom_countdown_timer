# Create the Home Assistant custom integration files for the countdown timer
import os
import json

# Create the directory structure
base_dir = "custom_countdown_timer"
os.makedirs(f"{base_dir}/custom_components/custom_countdown_timer", exist_ok=True)

# 1. Create manifest.json for HACS compatibility
manifest = {
    "domain": "custom_countdown_timer",
    "name": "Custom Countdown Timer",
    "version": "1.0.0",
    "documentation": "https://github.com/docvipul/custom_countdown_timer",
    "issue_tracker": "https://github.com/docvipul/custom_countdown_timer/issues",
    "dependencies": [],
    "codeowners": ["@docvipul"],
    "requirements": [],
    "config_flow": True,
    "iot_class": "calculated"
}

with open(f"{base_dir}/custom_components/custom_countdown_timer/manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)

print("Created manifest.json")
