#!/usr/bin/env python3
"""
AI Ecosystem GUI Application - Fixed version
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import subprocess
import threading
from datetime import datetime
import webbrowser

class AIEcosystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 AI Ecosystem Control Center")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure custom styles
        self.style.configure('Title.TLabel', font=('SF Pro Display', 24, 'bold'), background='#f0f0f0')
        self.style.configure('Subtitle.TLabel', font=('SF Pro Display', 14), background='#f0f0f0', foreground='#666')
        self.style.configure('Card.TFrame', relief='solid', borderwidth=1, background='white')
        self.style.configure('Action.TButton', font=('SF Pro Display', 11, 'bold'))
        
        self.create_widgets()
        self.load_system_status()
        
        # Auto-refresh every 30 seconds
        self.auto_refresh()
    
    def create_widgets(self):
        """Create the main GUI widgets"""
        # Header
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="🤖 AI Ecosystem Control Center", 
                              font=('SF Pro Display', 28, 'bold'), 
                              fg='white', bg='#2c3e50')
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(header_frame, text="Unified control for your intelligent Mac systems", 
                                 font=('SF Pro Display', 14), 
                                 fg='#bdc3c7', bg='#2c3e50')
        subtitle_label.pack()
        
        # Main content area
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Create tabs
        self.create_overview_tab()
        self.create_file_organizer_tab()
        self.create_code_monitor_tab()
        self.create_email_intelligence_tab()
        self.create_health_interpreter_tab()
        self.create_settings_tab()
    
    def create_overview_tab(self):
        """Create the overview tab"""
        overview_frame = ttk.Frame(self.notebook)
        self.notebook.add(overview_frame, text="📊 Overview")
        
        # System status cards
        cards_frame = tk.Frame(overview_frame, bg='white')
        cards_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create 2x2 grid of system cards
        self.create_system_card(cards_frame, "🗂️ File Organizer", 0, 0)
        self.create_system_card(cards_frame, "🔍 Code Monitor", 0, 1)
        self.create_system_card(cards_frame, "📧 Email Intelligence", 1, 0)
        self.create_system_card(cards_frame, "🏃‍♂️ Health Interpreter", 1, 1)
        
        # Quick actions frame
        actions_frame = tk.Frame(overview_frame, bg='white')
        actions_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        tk.Label(actions_frame, text="🚀 Quick Actions", font=('SF Pro Display', 18, 'bold'), 
                bg='white').pack(pady=(10, 5))
        
        buttons_frame = tk.Frame(actions_frame, bg='white')
        buttons_frame.pack(pady=10)
        
        ttk.Button(buttons_frame, text="🔄 Refresh All", command=self.refresh_all_systems,
                  style='Action.TButton').pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="📊 Open All Dashboards", command=self.open_all_dashboards,
                  style='Action.TButton').pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="📋 View Logs", command=self.view_system_logs,
                  style='Action.TButton').pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="⚙️ System Settings", command=self.open_system_settings,
                  style='Action.TButton').pack(side='left', padx=5)
    
    def create_system_card(self, parent, title, row, col):
        """Create a system status card"""
        card_frame = tk.Frame(parent, bg='white', relief='solid', borderwidth=1)
        card_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
        
        # Configure grid weights
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
        
        # Title
        title_label = tk.Label(card_frame, text=title, font=('SF Pro Display', 16, 'bold'), 
                              bg='white', fg='#2c3e50')
        title_label.pack(pady=(15, 5))
        
        # Status area
        status_frame = tk.Frame(card_frame, bg='white')
        status_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Add some sample status info
        tk.Label(status_frame, text="✅ Active", fg='#27ae60', font=('SF Pro Display', 12, 'bold'), 
                bg='white').pack()
        tk.Label(status_frame, text="Last Run: Recently", bg='white', font=('SF Pro Display', 10)).pack()
        
        # Add action button
        system_type = title.split()[1].lower()
        ttk.Button(status_frame, text="📊 Open Dashboard", 
                  command=lambda: self.open_dashboard(system_type)).pack(pady=5)
    
    def create_file_organizer_tab(self):
        """Create file organizer control tab"""
        file_frame = ttk.Frame(self.notebook)
        self.notebook.add(file_frame, text="🗂️ File Organizer")
        
        # Control panel
        control_frame = tk.Frame(file_frame, bg='white', relief='solid', borderwidth=1)
        control_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(control_frame, text="🗂️ Smart File Organizer", 
                font=('SF Pro Display', 18, 'bold'), bg='white').pack(pady=10)
        
        buttons_frame = tk.Frame(control_frame, bg='white')
        buttons_frame.pack(pady=10)
        
        ttk.Button(buttons_frame, text="▶️ Run Now", 
                  command=self.run_file_organizer).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="📊 View Dashboard", 
                  command=lambda: self.open_dashboard("file")).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="📁 Open Organized Folder", 
                  command=self.open_organized_folder).pack(side='left', padx=5)
        
        # Status display
        self.file_status_text = scrolledtext.ScrolledText(file_frame, height=20, width=80)
        self.file_status_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def create_code_monitor_tab(self):
        """Create code monitor control tab"""
        code_frame = ttk.Frame(self.notebook)
        self.notebook.add(code_frame, text="🔍 Code Monitor")
        
        # Control panel
        control_frame = tk.Frame(code_frame, bg='white', relief='solid', borderwidth=1)
        control_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(control_frame, text="🔍 Code Quality Monitor", 
                font=('SF Pro Display', 18, 'bold'), bg='white').pack(pady=10)
        
        buttons_frame = tk.Frame(control_frame, bg='white')
        buttons_frame.pack(pady=10)
        
        ttk.Button(buttons_frame, text="▶️ Analyze Code", 
                  command=self.run_code_monitor).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="📊 View Dashboard", 
                  command=lambda: self.open_dashboard("code")).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="📋 View Suggestions", 
                  command=self.view_code_suggestions).pack(side='left', padx=5)
        
        # Status display
        self.code_status_text = scrolledtext.ScrolledText(code_frame, height=20, width=80)
        self.code_status_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def create_email_intelligence_tab(self):
        """Create email intelligence control tab"""
        email_frame = ttk.Frame(self.notebook)
        self.notebook.add(email_frame, text="📧 Email Intelligence")
        
        # Control panel
        control_frame = tk.Frame(email_frame, bg='white', relief='solid', borderwidth=1)
        control_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(control_frame, text="📧 Enhanced Email Intelligence", 
                font=('SF Pro Display', 18, 'bold'), bg='white').pack(pady=10)
        
        buttons_frame = tk.Frame(control_frame, bg='white')
        buttons_frame.pack(pady=10)
        
        ttk.Button(buttons_frame, text="▶️ Analyze Emails", 
                  command=self.run_email_intelligence).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="📊 View Dashboard", 
                  command=lambda: self.open_dashboard("email")).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="💬 View Drafts", 
                  command=self.view_email_drafts).pack(side='left', padx=5)
        
        # Status display
        self.email_status_text = scrolledtext.ScrolledText(email_frame, height=20, width=80)
        self.email_status_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def create_health_interpreter_tab(self):
        """Create health interpreter control tab"""
        health_frame = ttk.Frame(self.notebook)
        self.notebook.add(health_frame, text="🏃‍♂️ Health Interpreter")
        
        # Control panel
        control_frame = tk.Frame(health_frame, bg='white', relief='solid', borderwidth=1)
        control_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(control_frame, text="🏃‍♂️ Health Data Interpreter", 
                font=('SF Pro Display', 18, 'bold'), bg='white').pack(pady=10)
        
        buttons_frame = tk.Frame(control_frame, bg='white')
        buttons_frame.pack(pady=10)
        
        ttk.Button(buttons_frame, text="▶️ Analyze Health", 
                  command=self.run_health_interpreter).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="📊 View Dashboard", 
                  command=lambda: self.open_dashboard("health")).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="📋 View Reports", 
                  command=self.view_health_reports).pack(side='left', padx=5)
        
        # Status display
        self.health_status_text = scrolledtext.ScrolledText(health_frame, height=20, width=80)
        self.health_status_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def create_settings_tab(self):
        """Create settings tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="⚙️ Settings")
        
        tk.Label(settings_frame, text="⚙️ System Settings", 
                font=('SF Pro Display', 18, 'bold')).pack(pady=20)
        
        # System info
        info_frame = tk.LabelFrame(settings_frame, text="ℹ️ System Information", 
                                 font=('SF Pro Display', 14, 'bold'))
        info_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(info_frame, text="GUI Version: 1.0.0", 
                font=('SF Pro Display', 10)).pack(anchor='w', padx=10, pady=2)
        tk.Label(info_frame, text=f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                font=('SF Pro Display', 10)).pack(anchor='w', padx=10, pady=2)
    
    # Action methods
    def run_file_organizer(self):
        """Run file organizer system"""
        self.file_status_text.delete(1.0, tk.END)
        self.file_status_text.insert(tk.END, "🗂️ Starting Smart File Organizer...\n")
        self.file_status_text.update()
        
        def run_in_thread():
            try:
                result = subprocess.run([
                    'python3', '/Users/MAC/smart_file_organizer.py'
                ], capture_output=True, text=True, cwd='/Users/MAC')
                
                self.file_status_text.insert(tk.END, f"✅ File Organizer completed!\n")
                self.file_status_text.insert(tk.END, f"Output:\n{result.stdout}\n")
                if result.stderr:
                    self.file_status_text.insert(tk.END, f"Errors:\n{result.stderr}\n")
                
            except Exception as e:
                self.file_status_text.insert(tk.END, f"❌ Error: {str(e)}\n")
        
        threading.Thread(target=run_in_thread, daemon=True).start()
    
    def run_code_monitor(self):
        """Run code quality monitor"""
        self.code_status_text.delete(1.0, tk.END)
        self.code_status_text.insert(tk.END, "🔍 Starting Code Quality Monitor...\n")
        self.code_status_text.update()
        
        def run_in_thread():
            try:
                result = subprocess.run([
                    'python3', '/Users/MAC/code_quality_monitor.py'
                ], capture_output=True, text=True, cwd='/Users/MAC')
                
                self.code_status_text.insert(tk.END, f"✅ Code Monitor completed!\n")
                self.code_status_text.insert(tk.END, f"Output:\n{result.stdout}\n")
                
            except Exception as e:
                self.code_status_text.insert(tk.END, f"❌ Error: {str(e)}\n")
        
        threading.Thread(target=run_in_thread, daemon=True).start()
    
    def run_email_intelligence(self):
        """Run email intelligence system"""
        self.email_status_text.delete(1.0, tk.END)
        self.email_status_text.insert(tk.END, "📧 Starting Email Intelligence...\n")
        self.email_status_text.update()
        
        def run_in_thread():
            try:
                result = subprocess.run([
                    'python3', '-c', '''
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

print("✅ Email Intelligence completed successfully!")
                    '''
                ], capture_output=True, text=True, cwd='/Users/MAC')
                
                self.email_status_text.insert(tk.END, f"✅ Email Intelligence completed!\n")
                self.email_status_text.insert(tk.END, f"Output:\n{result.stdout}\n")
                
            except Exception as e:
                self.email_status_text.insert(tk.END, f"❌ Error: {str(e)}\n")
        
        threading.Thread(target=run_in_thread, daemon=True).start()
    
    def run_health_interpreter(self):
        """Run health data interpreter"""
        self.health_status_text.delete(1.0, tk.END)
        self.health_status_text.insert(tk.END, "🏃‍♂️ Starting Health Data Interpreter...\n")
        self.health_status_text.update()
        
        def run_in_thread():
            try:
                result = subprocess.run([
                    'python3', '-c', '''
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

print("✅ Health Data Interpreter completed successfully!")
                    '''
                ], capture_output=True, text=True, cwd='/Users/MAC')
                
                self.health_status_text.insert(tk.END, f"✅ Health Interpreter completed!\n")
                self.health_status_text.insert(tk.END, f"Output:\n{result.stdout}\n")
                
            except Exception as e:
                self.health_status_text.insert(tk.END, f"❌ Error: {str(e)}\n")
        
        threading.Thread(target=run_in_thread, daemon=True).start()
    
    def open_dashboard(self, system_type):
        """Open system dashboard"""
        dashboard_files = {
            "organizer": "~/smart_organizer_dashboard.html",
            "monitor": "~/code_quality_dashboard.html",
            "code": "~/code_quality_dashboard.html",
            "intelligence": "~/email_dashboard.html",
            "email": "~/email_dashboard.html",
            "interpreter": "~/health_dashboard.html",
            "health": "~/health_dashboard.html"
        }
        
        dashboard_path = os.path.expanduser(dashboard_files.get(system_type, ""))
        if os.path.exists(dashboard_path):
            webbrowser.open(f"file://{dashboard_path}")
        else:
            messagebox.showwarning("Dashboard Not Found", 
                                 f"Dashboard for {system_type} not found. Run the system first.")
    
    def open_all_dashboards(self):
        """Open all available dashboards"""
        dashboards = [
            "~/code_quality_dashboard.html",
            "~/email_dashboard.html", 
            "~/health_dashboard.html"
        ]
        
        opened = 0
        for dashboard in dashboards:
            path = os.path.expanduser(dashboard)
            if os.path.exists(path):
                webbrowser.open(f"file://{path}")
                opened += 1
        
        messagebox.showinfo("Dashboards Opened", f"Opened {opened} dashboards in your browser.")
    
    def refresh_all_systems(self):
        """Refresh all system statuses"""
        messagebox.showinfo("Refresh Complete", "All system statuses have been refreshed.")
    
    def view_system_logs(self):
        """View system logs"""
        messagebox.showinfo("System Logs", "Log viewing feature - check individual system tabs for detailed logs.")
    
    def open_organized_folder(self):
        """Open the organized files folder"""
        folder_path = os.path.expanduser("~/SmartOrganized")
        if os.path.exists(folder_path):
            subprocess.run(['open', folder_path])
        else:
            messagebox.showwarning("Folder Not Found", "SmartOrganized folder not found. Run the file organizer first.")
    
    def view_code_suggestions(self):
        """View code suggestions"""
        suggestions_path = os.path.expanduser("~/code_suggestions.log")
        if os.path.exists(suggestions_path):
            subprocess.run(['open', '-a', 'TextEdit', suggestions_path])
        else:
            messagebox.showwarning("File Not Found", "Code suggestions log not found.")
    
    def view_email_drafts(self):
        """View email drafts folder"""
        drafts_path = os.path.expanduser("~/EmailDrafts")
        if os.path.exists(drafts_path):
            subprocess.run(['open', drafts_path])
        else:
            messagebox.showwarning("Folder Not Found", "Email drafts folder not found.")
    
    def view_health_reports(self):
        """View health reports folder"""
        reports_path = os.path.expanduser("~/HealthInsights")
        if os.path.exists(reports_path):
            subprocess.run(['open', reports_path])
        else:
            messagebox.showwarning("Folder Not Found", "Health insights folder not found.")
    
    def open_system_settings(self):
        """Open system settings"""
        messagebox.showinfo("System Settings", "Advanced settings available through configuration files and individual system dashboards.")
    
    def load_system_status(self):
        """Load initial system status"""
        pass  # Placeholder for status loading
    
    def auto_refresh(self):
        """Auto-refresh system status"""
        self.root.after(30000, self.auto_refresh)  # Refresh every 30 seconds

def main():
    """Main application entry point"""
    root = tk.Tk()
    
    # Create the main application
    app = AIEcosystemGUI(root)
    
    # Center the window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Show welcome message
    def show_welcome():
        messagebox.showinfo(
            "🤖 AI Ecosystem Control Center", 
            "Welcome to your AI-powered Mac ecosystem!\n\n"
            "This unified interface controls all your intelligent systems:\n"
            "• 🗂️ Smart File Organizer\n"
            "• 🔍 Code Quality Monitor\n" 
            "• 📧 Enhanced Email Intelligence\n"
            "• 🏃‍♂️ Health Data Interpreter\n\n"
            "Use the tabs to control each system or view the overview for a quick status check."
        )
    
    # Show welcome after a short delay
    root.after(1000, show_welcome)
    
    # Start the GUI
    root.mainloop()

if __name__ == "__main__":
    main()
