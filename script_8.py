# 10. Show the complete directory structure and create a zip file
import zipfile

print("=== Custom Countdown Timer HACS Integration ===")
print("\nDirectory Structure:")
print("custom_countdown_timer/")
print("├── README.md")
print("├── hacs.json")
print("├── version.json")
print("├── install.sh")
print("└── custom_components/")
print("    └── custom_countdown_timer/")
print("        ├── __init__.py")
print("        ├── manifest.json")
print("        ├── const.py")
print("        ├── config_flow.py") 
print("        └── sensor.py")

# Create a zip file with all the integration files
zip_filename = "custom_countdown_timer_hacs.zip"
with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    # Add all files to the zip
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            file_path = os.path.join(root, file)
            arc_path = os.path.relpath(file_path, base_dir)
            zipf.write(file_path, arc_path)

print(f"\n✅ Created {zip_filename} with complete HACS integration")

# List the contents of the zip file
print(f"\nZip Contents:")
with zipfile.ZipFile(zip_filename, 'r') as zipf:
    for file_info in zipf.filelist:
        print(f"  {file_info.filename}")

print(f"\n📦 Integration package ready: {zip_filename}")
print("\n🚀 Installation Options:")
print("1. HACS: Upload to GitHub and add as custom repository")
print("2. Manual: Extract to custom_components/ directory")
print("3. Script: Run install.sh from Home Assistant")