#!/usr/bin/env python3
"""
Create macOS App Bundle for AI Ecosystem GUI
"""
import os
import shutil
import subprocess

def create_app_bundle():
    """Create a proper macOS app bundle"""
    
    app_name = "AI Ecosystem Control Center"
    bundle_name = "AI_Ecosystem_Control_Center.app"
    bundle_path = os.path.expanduser(f"~/Applications/{bundle_name}")
    
    print(f"🚀 Creating macOS app bundle: {bundle_name}")
    
    # Remove existing bundle if it exists
    if os.path.exists(bundle_path):
        shutil.rmtree(bundle_path)
    
    # Create bundle directory structure
    contents_dir = os.path.join(bundle_path, "Contents")
    macos_dir = os.path.join(contents_dir, "MacOS")
    resources_dir = os.path.join(contents_dir, "Resources")
    
    os.makedirs(macos_dir, exist_ok=True)
    os.makedirs(resources_dir, exist_ok=True)
    
    # Create Info.plist
    info_plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>ai_ecosystem_launcher</string>
    <key>CFBundleIdentifier</key>
    <string>com.user.ai-ecosystem</string>
    <key>CFBundleName</key>
    <string>{app_name}</string>
    <key>CFBundleDisplayName</key>
    <string>{app_name}</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>AIEC</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSRequiresAquaSystemAppearance</key>
    <false/>
</dict>
</plist>"""
    
    with open(os.path.join(contents_dir, "Info.plist"), 'w') as f:
        f.write(info_plist)
    
    # Create launcher script
    launcher_script = f"""#!/bin/bash
# AI Ecosystem Control Center Launcher

# Set up environment
export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
export PYTHONPATH="/Users/MAC:$PYTHONPATH"

# Change to the correct directory
cd /Users/MAC

# Launch the Python GUI application
/usr/bin/python3 /Users/MAC/ai_ecosystem_app.py
"""
    
    launcher_path = os.path.join(macos_dir, "ai_ecosystem_launcher")
    with open(launcher_path, 'w') as f:
        f.write(launcher_script)
    
    # Make launcher executable
    os.chmod(launcher_path, 0o755)
    
    # Copy Python files to Resources (optional, for bundling)
    python_files = [
        "ai_ecosystem_gui.py",
        "ai_gui_actions.py", 
        "ai_ecosystem_app.py"
    ]
    
    for file in python_files:
        src = f"/Users/MAC/{file}"
        if os.path.exists(src):
            shutil.copy2(src, resources_dir)
    
    print(f"✅ App bundle created successfully!")
    print(f"📍 Location: {bundle_path}")
    print(f"🚀 You can now launch the app from Applications or Spotlight!")
    
    # Try to open the Applications folder
    try:
        subprocess.run(['open', os.path.dirname(bundle_path)])
    except:
        pass
    
    return bundle_path

if __name__ == "__main__":
    create_app_bundle()
