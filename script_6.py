# 7. Create hacs.json for HACS compatibility
hacs_json = {
    "name": "Custom Countdown Timer",
    "hacs": "1.6.0",
    "domains": ["sensor"],
    "iot_class": "Calculated",
    "homeassistant": "2023.1.0"
}

with open(f"{base_dir}/hacs.json", "w") as f:
    json.dump(hacs_json, f, indent=2)

# 8. Create version info
version_info = {
    "version": "1.0.0",
    "release_date": "2025-10-17",
    "changelog": [
        "Initial release",
        "Business hours countdown timer",
        "Holiday support",
        "Multiple sensor entities",
        "Real-time updates"
    ]
}

with open(f"{base_dir}/version.json", "w") as f:
    json.dump(version_info, f, indent=2)

print("Created hacs.json and version.json")