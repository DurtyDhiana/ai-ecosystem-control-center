# AI Ecosystem Control Center Makefile

.PHONY: help install dev-up dev-down gui menubar cli test clean

# Default target
help:
	@echo "🤖 AI Ecosystem Control Center"
	@echo ""
	@echo "Available commands:"
	@echo "  make install     - Install dependencies"
	@echo "  make dev-up      - Start development environment"
	@echo "  make dev-down    - Stop development environment"
	@echo "  make gui         - Launch main GUI"
	@echo "  make menubar     - Launch menu bar app"
	@echo "  make cli         - Show CLI options"
	@echo "  make test        - Run system tests"
	@echo "  make clean       - Clean generated files"

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	pip3 install -r requirements.txt
	@echo "✅ Dependencies installed!"

# Start development environment
dev-up:
	@echo "🚀 Starting AI Ecosystem Control Center..."
	./scripts/setup-automation.sh
	@echo "🎯 Development environment ready!"
	@echo "Run 'make gui' to launch the interface"

# Stop development environment
dev-down:
	@echo "🛑 Stopping background services..."
	-launchctl unload ~/Library/LaunchAgents/smart.file.organizer.plist 2>/dev/null
	-launchctl unload ~/Library/LaunchAgents/code.quality.monitor.plist 2>/dev/null
	-launchctl unload ~/Library/LaunchAgents/enhanced.email.final.plist 2>/dev/null
	-launchctl unload ~/Library/LaunchAgents/health.intelligence.plist 2>/dev/null
	@echo "✅ Services stopped!"

# Launch main GUI
gui:
	@echo "🖥️ Launching main GUI..."
	python3 gui/ai_ecosystem_app_fixed.py

# Launch menu bar app
menubar:
	@echo "🤖 Launching menu bar app..."
	python3 gui/ai_menubar_app.py

# Show CLI options
cli:
	@echo "⚡ CLI Commands:"
	@echo ""
	@echo "Email Intelligence:"
	@echo "  python3 cli/email_cli.py stats"
	@echo "  python3 cli/email_cli.py ls --urgent"
	@echo "  python3 cli/email_cli.py drafts"
	@echo ""
	@echo "Health Data:"
	@echo "  python3 cli/health_cli.py score"
	@echo "  python3 cli/health_cli.py insights"
	@echo "  python3 cli/health_cli.py reports"
	@echo ""
	@echo "Direct System Execution:"
	@echo "  python3 src/smart_file_organizer.py"
	@echo "  python3 src/code_quality_monitor.py"
	@echo "  python3 src/email_intelligence_complete.py"
	@echo "  python3 src/health_data_interpreter.py"

# Test all systems
test:
	@echo "🧪 Running all system tests..."
	@echo "Testing file organizer..."
	python3 src/smart_file_organizer.py > /dev/null && echo "✅ File organizer OK" || echo "❌ File organizer failed"
	@echo "Testing code monitor..."
	python3 src/code_quality_monitor.py > /dev/null && echo "✅ Code monitor OK" || echo "❌ Code monitor failed"
	@echo "Testing email intelligence..."
	python3 -c "import sys; sys.path.append('src'); exec(open('src/email_intelligence_complete.py').read())" > /dev/null && echo "✅ Email intelligence OK" || echo "❌ Email intelligence failed"
	@echo "Testing health interpreter..."
	python3 -c "import sys; sys.path.append('src'); exec(open('src/health_data_interpreter.py').read())" > /dev/null && echo "✅ Health interpreter OK" || echo "❌ Health interpreter failed"
	@echo "Testing GUI applications..."
	python3 -c "import tkinter; print('✅ Tkinter available')" && echo "✅ GUI dependencies OK" || echo "❌ GUI dependencies failed"
	@echo "🎉 All tests completed!"

# Run system tests
test-systems:
	@echo "🧪 Running system integration tests..."
	python3 src/smart_file_organizer.py > /dev/null && echo "✅ File organizer OK" || echo "❌ File organizer failed"
	python3 src/code_quality_monitor.py > /dev/null && echo "✅ Code monitor OK" || echo "❌ Code monitor failed"

# Clean generated files
clean:
	@echo "🧹 Cleaning generated files..."
	-rm -f ~/code_quality_dashboard.html
	-rm -f ~/email_dashboard.html
	-rm -f ~/health_dashboard.html
	-rm -f ~/code_quality_report.json
	-rm -f ~/email_intelligence.json
	-rm -f ~/health_intelligence.json
	-rm -f ~/*.log
	@echo "✅ Cleanup complete!"

# Development shortcuts
run-file:
	python3 src/smart_file_organizer.py

run-code:
	python3 src/code_quality_monitor.py

run-email:
	python3 -c "import sys; sys.path.append('src'); exec(open('src/email_intelligence_complete.py').read())"

run-health:
	python3 -c "import sys; sys.path.append('src'); exec(open('src/health_data_interpreter.py').read())"

# Dashboard shortcuts
dash-code:
	open ~/code_quality_dashboard.html

dash-email:
	open ~/email_dashboard.html

dash-health:
	open ~/health_dashboard.html

dash-all:
	make dash-code dash-email dash-health
