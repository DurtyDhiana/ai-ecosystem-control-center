#!/bin/bash
# AI Ecosystem Control Center - Setup Automation Script

set -e

echo "🤖 Setting up AI Ecosystem Control Center automation..."

# Get the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "📁 Project directory: $PROJECT_DIR"

# Create necessary directories
echo "📂 Creating directories..."
mkdir -p ~/SmartOrganized/{Documents/{Papers,Code},Media/{Images,Videos},Archives,Data,Applications,Miscellaneous}
mkdir -p ~/EmailDrafts
mkdir -p ~/LargeAttachments
mkdir -p ~/HealthInsights

# Copy LaunchAgent files to the correct location
echo "🔄 Setting up LaunchAgents..."
mkdir -p ~/Library/LaunchAgents

# Create LaunchAgent files
cat > ~/Library/LaunchAgents/smart.file.organizer.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>smart.file.organizer</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>PROJECT_DIR/src/smart_file_organizer.py</string>
    </array>
    <key>StartInterval</key>
    <integer>600</integer>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>HOME/smart_organizer.log</string>
    <key>StandardErrorPath</key>
    <string>HOME/smart_organizer_error.log</string>
</dict>
</plist>
EOF

cat > ~/Library/LaunchAgents/code.quality.monitor.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>code.quality.monitor</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>PROJECT_DIR/src/code_quality_monitor.py</string>
    </array>
    <key>StartInterval</key>
    <integer>300</integer>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>HOME/code_suggestions.log</string>
    <key>StandardErrorPath</key>
    <string>HOME/code_monitor_error.log</string>
</dict>
</plist>
EOF

# Replace placeholders in LaunchAgent files
sed -i '' "s|PROJECT_DIR|$PROJECT_DIR|g" ~/Library/LaunchAgents/*.plist
sed -i '' "s|HOME|$HOME|g" ~/Library/LaunchAgents/*.plist

# Set up shell aliases
echo "🔧 Setting up shell aliases..."
if [[ -f ~/.zshrc ]]; then
    if ! grep -q "ai-ecosystem-control-center" ~/.zshrc; then
        echo "" >> ~/.zshrc
        echo "# AI Ecosystem Control Center aliases" >> ~/.zshrc
        echo "source $PROJECT_DIR/config/.zshrc_ai_gui_fixed" >> ~/.zshrc
        echo "✅ Added aliases to ~/.zshrc"
    else
        echo "ℹ️ Aliases already configured in ~/.zshrc"
    fi
fi

# Make scripts executable
echo "🔐 Setting permissions..."
chmod +x "$PROJECT_DIR"/scripts/*.sh
chmod +x "$PROJECT_DIR"/src/*.py
chmod +x "$PROJECT_DIR"/gui/*.py
chmod +x "$PROJECT_DIR"/cli/*.py

# Load LaunchAgents (optional - user can do this manually)
echo "🚀 LaunchAgents created. To start automation, run:"
echo "   launchctl load ~/Library/LaunchAgents/smart.file.organizer.plist"
echo "   launchctl load ~/Library/LaunchAgents/code.quality.monitor.plist"

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Install dependencies: pip3 install -r requirements.txt"
echo "2. Start automation: launchctl load ~/Library/LaunchAgents/*.plist"
echo "3. Launch GUI: python3 gui/ai_ecosystem_app_fixed.py"
echo "4. Or use aliases: source ~/.zshrc && ai-gui"
echo ""
echo "🎉 Your AI Ecosystem Control Center is ready!"
