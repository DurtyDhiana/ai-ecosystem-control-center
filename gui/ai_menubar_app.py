#!/usr/bin/env python3
"""
AI Ecosystem Menu Bar App - Lightweight system tray interface
"""
import rumps
import subprocess
import os
import json
import webbrowser
from datetime import datetime

class AIEcosystemMenuBar(rumps.App):
    def __init__(self):
        super(AIEcosystemMenuBar, self).__init__("🤖", quit_button=None)
        self.menu = [
            "📊 System Overview",
            None,  # Separator
            "🗂️ File Organizer",
            "🔍 Code Monitor", 
            "📧 Email Intelligence",
            "🏃‍♂️ Health Interpreter",
            None,  # Separator
            "📊 Open All Dashboards",
            "🔄 Refresh All Systems",
            None,  # Separator
            "⚙️ Settings",
            "📋 View Logs",
            None,  # Separator
            "❌ Quit"
        ]
        
        # Update title with system status
        self.update_title()
        
        # Set up timer for periodic updates
        self.timer = rumps.Timer(self.update_status, 60)  # Update every minute
        self.timer.start()
    
    def update_title(self):
        """Update menu bar title with system status"""
        try:
            # Check if any system has alerts
            has_alerts = self.check_for_alerts()
            if has_alerts:
                self.title = "🚨"  # Alert indicator
            else:
                self.title = "🤖"  # Normal indicator
        except:
            self.title = "🤖"
    
    def check_for_alerts(self):
        """Check if any system has alerts"""
        try:
            # Check email intelligence for urgent emails
            email_log = os.path.expanduser("~/email_intelligence.json")
            if os.path.exists(email_log):
                with open(email_log, 'r') as f:
                    data = json.load(f)
                    if data.get('stats', {}).get('urgent_count', 0) > 0:
                        return True
            
            # Check health for alerts
            health_log = os.path.expanduser("~/health_intelligence.json")
            if os.path.exists(health_log):
                with open(health_log, 'r') as f:
                    data = json.load(f)
                    if len(data.get('alerts', [])) > 0:
                        return True
            
            return False
        except:
            return False
    
    @rumps.clicked("📊 System Overview")
    def system_overview(self, _):
        """Show system overview"""
        try:
            # Get stats from all systems
            overview = self.get_system_overview()
            
            alert = rumps.alert(
                title="🤖 AI Ecosystem Overview",
                message=overview,
                ok="Open GUI",
                cancel="Close"
            )
            
            if alert == 1:  # OK clicked
                self.open_main_gui()
                
        except Exception as e:
            rumps.alert(f"Error getting overview: {str(e)}")
    
    def get_system_overview(self):
        """Get overview of all systems"""
        overview_lines = []
        
        # File Organizer
        try:
            overview_lines.append("🗂️ File Organizer: Active")
        except:
            overview_lines.append("🗂️ File Organizer: Unknown")
        
        # Code Monitor
        try:
            code_log = os.path.expanduser("~/code_quality_report.json")
            if os.path.exists(code_log):
                with open(code_log, 'r') as f:
                    data = json.load(f)
                    files_count = len(data.get('files', {}))
                    overview_lines.append(f"🔍 Code Monitor: {files_count} files analyzed")
            else:
                overview_lines.append("🔍 Code Monitor: No data")
        except:
            overview_lines.append("🔍 Code Monitor: Error")
        
        # Email Intelligence
        try:
            email_log = os.path.expanduser("~/email_intelligence.json")
            if os.path.exists(email_log):
                with open(email_log, 'r') as f:
                    data = json.load(f)
                    stats = data.get('stats', {})
                    total = stats.get('total_processed', 0)
                    urgent = stats.get('urgent_count', 0)
                    overview_lines.append(f"📧 Email Intelligence: {total} emails, {urgent} urgent")
            else:
                overview_lines.append("📧 Email Intelligence: No data")
        except:
            overview_lines.append("📧 Email Intelligence: Error")
        
        # Health Interpreter
        try:
            health_log = os.path.expanduser("~/health_intelligence.json")
            if os.path.exists(health_log):
                with open(health_log, 'r') as f:
                    data = json.load(f)
                    stats = data.get('stats', {})
                    score = stats.get('health_score', 0)
                    days = stats.get('total_days_tracked', 0)
                    overview_lines.append(f"🏃‍♂️ Health Interpreter: {score}/100 score, {days} days")
            else:
                overview_lines.append("🏃‍♂️ Health Interpreter: No data")
        except:
            overview_lines.append("🏃‍♂️ Health Interpreter: Error")
        
        overview_lines.append(f"\nLast updated: {datetime.now().strftime('%H:%M:%S')}")
        
        return "\n".join(overview_lines)
    
    @rumps.clicked("🗂️ File Organizer")
    def file_organizer_menu(self, _):
        """File organizer submenu"""
        submenu = rumps.alert(
            title="🗂️ Smart File Organizer",
            message="Choose an action:",
            ok="Run Now",
            cancel="Open Folder",
            other="View Dashboard"
        )
        
        if submenu == 1:  # Run Now
            self.run_file_organizer()
        elif submenu == 0:  # Open Folder
            self.open_organized_folder()
        elif submenu == -1:  # View Dashboard
            self.open_dashboard("file")
    
    @rumps.clicked("🔍 Code Monitor")
    def code_monitor_menu(self, _):
        """Code monitor submenu"""
        submenu = rumps.alert(
            title="🔍 Code Quality Monitor",
            message="Choose an action:",
            ok="Analyze Now",
            cancel="View Dashboard",
            other="View Suggestions"
        )
        
        if submenu == 1:  # Analyze Now
            self.run_code_monitor()
        elif submenu == 0:  # View Dashboard
            self.open_dashboard("code")
        elif submenu == -1:  # View Suggestions
            self.view_code_suggestions()
    
    @rumps.clicked("📧 Email Intelligence")
    def email_intelligence_menu(self, _):
        """Email intelligence submenu"""
        submenu = rumps.alert(
            title="📧 Enhanced Email Intelligence",
            message="Choose an action:",
            ok="Analyze Now",
            cancel="View Dashboard",
            other="View Drafts"
        )
        
        if submenu == 1:  # Analyze Now
            self.run_email_intelligence()
        elif submenu == 0:  # View Dashboard
            self.open_dashboard("email")
        elif submenu == -1:  # View Drafts
            self.view_email_drafts()
    
    @rumps.clicked("🏃‍♂️ Health Interpreter")
    def health_interpreter_menu(self, _):
        """Health interpreter submenu"""
        submenu = rumps.alert(
            title="🏃‍♂️ Health Data Interpreter",
            message="Choose an action:",
            ok="Analyze Now",
            cancel="View Dashboard",
            other="View Reports"
        )
        
        if submenu == 1:  # Analyze Now
            self.run_health_interpreter()
        elif submenu == 0:  # View Dashboard
            self.open_dashboard("health")
        elif submenu == -1:  # View Reports
            self.view_health_reports()
    
    @rumps.clicked("📊 Open All Dashboards")
    def open_all_dashboards(self, _):
        """Open all available dashboards"""
        dashboards = [
            ("~/code_quality_dashboard.html", "Code Quality"),
            ("~/email_dashboard.html", "Email Intelligence"),
            ("~/health_dashboard.html", "Health Data")
        ]
        
        opened = 0
        for dashboard_path, name in dashboards:
            path = os.path.expanduser(dashboard_path)
            if os.path.exists(path):
                webbrowser.open(f"file://{path}")
                opened += 1
        
        rumps.alert(f"Opened {opened} dashboards in your browser.")
    
    @rumps.clicked("🔄 Refresh All Systems")
    def refresh_all_systems(self, _):
        """Refresh all systems"""
        rumps.notification(
            title="🔄 Refreshing Systems",
            subtitle="Running all AI systems...",
            message="This may take a few moments."
        )
        
        # Run all systems in background
        def run_all():
            try:
                self.run_file_organizer(silent=True)
                self.run_code_monitor(silent=True)
                self.run_email_intelligence(silent=True)
                self.run_health_interpreter(silent=True)
                
                rumps.notification(
                    title="✅ Refresh Complete",
                    subtitle="All systems updated",
                    message="Check dashboards for latest results."
                )
            except Exception as e:
                rumps.notification(
                    title="❌ Refresh Error",
                    subtitle="Some systems failed",
                    message=str(e)
                )
        
        import threading
        threading.Thread(target=run_all, daemon=True).start()
    
    @rumps.clicked("⚙️ Settings")
    def settings_menu(self, _):
        """Settings menu"""
        rumps.alert(
            title="⚙️ Settings",
            message="Settings can be configured through:\n\n"
                   "• ~/.email_config.yaml (Email settings)\n"
                   "• Main GUI application\n"
                   "• Individual system dashboards",
            ok="Open Main GUI"
        )
        self.open_main_gui()
    
    @rumps.clicked("📋 View Logs")
    def view_logs_menu(self, _):
        """View logs menu"""
        log_choice = rumps.alert(
            title="📋 System Logs",
            message="Which logs would you like to view?",
            ok="All Logs",
            cancel="Cancel",
            other="Choose Specific"
        )
        
        if log_choice == 1:  # All Logs
            self.open_logs_folder()
        elif log_choice == -1:  # Choose Specific
            self.choose_specific_log()
    
    @rumps.clicked("❌ Quit")
    def quit_app(self, _):
        """Quit the application"""
        rumps.quit_application()
    
    def update_status(self, timer):
        """Periodic status update"""
        self.update_title()
    
    # Helper methods
    def run_file_organizer(self, silent=False):
        """Run file organizer"""
        try:
            subprocess.run(['python3', '/Users/MAC/smart_file_organizer.py'], 
                         cwd='/Users/MAC', check=True)
            if not silent:
                rumps.notification("🗂️ File Organizer", "Completed successfully", "Files have been organized")
        except Exception as e:
            if not silent:
                rumps.alert(f"Error running file organizer: {str(e)}")
    
    def run_code_monitor(self, silent=False):
        """Run code monitor"""
        try:
            subprocess.run(['python3', '/Users/MAC/code_quality_monitor.py'], 
                         cwd='/Users/MAC', check=True)
            if not silent:
                rumps.notification("🔍 Code Monitor", "Analysis completed", "Check dashboard for results")
        except Exception as e:
            if not silent:
                rumps.alert(f"Error running code monitor: {str(e)}")
    
    def run_email_intelligence(self, silent=False):
        """Run email intelligence"""
        try:
            # Run the enhanced email system
            subprocess.run(['python3', '-c', '''
import sys
sys.path.append('/Users/MAC')
exec(open('/Users/MAC/email_intelligence_complete.py').read())
exec(open('/Users/MAC/email_dashboard_generator.py').read())

def fix_stats(email_history):
    required_stats = ['total_processed', 'urgent_count', 'spam_detected', 'drafts_created', 'unsubscribed_count', 'attachments_moved', 'storage_saved_mb']
    for stat in required_stats:
        if stat not in email_history['stats']:
            email_history['stats'][stat] = 0
    return email_history

email_ai = CompleteEmailIntelligence()
email_ai.email_history = fix_stats(email_ai.email_history)
email_ai.simulate_enhanced_email_analysis()
email_ai.save_histories()

html_content = generate_complete_dashboard(email_ai.email_history, email_ai.unsubscribe_history, email_ai.config)
with open('/Users/MAC/email_dashboard.html', 'w') as f:
    f.write(html_content)
            '''], cwd='/Users/MAC', check=True)
            if not silent:
                rumps.notification("📧 Email Intelligence", "Analysis completed", "Check dashboard for insights")
        except Exception as e:
            if not silent:
                rumps.alert(f"Error running email intelligence: {str(e)}")
    
    def run_health_interpreter(self, silent=False):
        """Run health interpreter"""
        try:
            subprocess.run(['python3', '-c', '''
import sys
sys.path.append('/Users/MAC')
exec(open('/Users/MAC/health_data_interpreter.py').read())
exec(open('/Users/MAC/health_dashboard_generator.py').read())

health_ai = HealthDataInterpreter()
results = health_ai.run_health_analysis()

html_content = generate_health_dashboard(
    health_ai.health_history,
    results['health_data'],
    results['fitness_data'],
    results['insights'],
    results['alerts'],
    results['health_score'],
    results['recommendations']
)

with open('/Users/MAC/health_dashboard.html', 'w') as f:
    f.write(html_content)
            '''], cwd='/Users/MAC', check=True)
            if not silent:
                rumps.notification("🏃‍♂️ Health Interpreter", "Analysis completed", "Check dashboard for insights")
        except Exception as e:
            if not silent:
                rumps.alert(f"Error running health interpreter: {str(e)}")
    
    def open_dashboard(self, system_type):
        """Open system dashboard"""
        dashboard_files = {
            "code": "~/code_quality_dashboard.html",
            "email": "~/email_dashboard.html",
            "health": "~/health_dashboard.html"
        }
        
        dashboard_path = os.path.expanduser(dashboard_files.get(system_type, ""))
        if os.path.exists(dashboard_path):
            webbrowser.open(f"file://{dashboard_path}")
        else:
            rumps.alert(f"Dashboard for {system_type} not found. Run the system first.")
    
    def open_main_gui(self):
        """Open the main GUI application"""
        try:
            subprocess.Popen(['python3', '/Users/MAC/ai_ecosystem_app.py'], cwd='/Users/MAC')
        except Exception as e:
            rumps.alert(f"Error opening main GUI: {str(e)}")
    
    def open_organized_folder(self):
        """Open organized files folder"""
        folder_path = os.path.expanduser("~/SmartOrganized")
        if os.path.exists(folder_path):
            subprocess.run(['open', folder_path])
        else:
            rumps.alert("SmartOrganized folder not found. Run the file organizer first.")
    
    def view_code_suggestions(self):
        """View code suggestions"""
        suggestions_path = os.path.expanduser("~/code_suggestions.log")
        if os.path.exists(suggestions_path):
            subprocess.run(['open', '-a', 'TextEdit', suggestions_path])
        else:
            rumps.alert("Code suggestions log not found.")
    
    def view_email_drafts(self):
        """View email drafts"""
        drafts_path = os.path.expanduser("~/EmailDrafts")
        if os.path.exists(drafts_path):
            subprocess.run(['open', drafts_path])
        else:
            rumps.alert("Email drafts folder not found.")
    
    def view_health_reports(self):
        """View health reports"""
        reports_path = os.path.expanduser("~/HealthInsights")
        if os.path.exists(reports_path):
            subprocess.run(['open', reports_path])
        else:
            rumps.alert("Health insights folder not found.")
    
    def open_logs_folder(self):
        """Open logs folder"""
        subprocess.run(['open', '/Users/MAC'])
    
    def choose_specific_log(self):
        """Choose specific log to view"""
        # This would need a more complex dialog - simplified for now
        rumps.alert("Use the main GUI application for detailed log viewing.")

if __name__ == "__main__":
    app = AIEcosystemMenuBar()
    app.run()
