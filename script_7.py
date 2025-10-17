# 9. Create installation script
install_script = '''#!/bin/bash

# Custom Countdown Timer Installation Script for Home Assistant

echo "Installing Custom Countdown Timer integration..."

# Check if Home Assistant config directory exists
if [ ! -d "/config" ]; then
    echo "Error: Home Assistant config directory not found at /config"
    echo "Please run this script from within Home Assistant or adjust the path"
    exit 1
fi

# Create custom_components directory if it doesn't exist
mkdir -p /config/custom_components

# Copy integration files
echo "Copying integration files..."
cp -r custom_components/custom_countdown_timer /config/custom_components/

echo "Installation complete!"
echo ""
echo "Next steps:"
echo "1. Restart Home Assistant"
echo "2. Go to Settings → Devices & Services"
echo "3. Click 'Add Integration'"
echo "4. Search for 'Custom Countdown Timer'"
echo "5. Configure your timer settings"
echo ""
echo "The integration will create three sensors:"
echo "- sensor.custom_countdown_timer (main countdown)"
echo "- sensor.work_time_remaining (business hours only)"
echo "- sensor.timer_status (current status)"
'''

with open(f"{base_dir}/install.sh", "w") as f:
    f.write(install_script)

# Make the script executable (on Unix systems)
import stat
os.chmod(f"{base_dir}/install.sh", stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)

print("Created install.sh")