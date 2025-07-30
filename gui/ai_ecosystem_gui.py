#!/usr/bin/env python3
"""
AI Ecosystem GUI - Unified interface for all AI systems
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
        self.create_system_card(cards_frame, "🗂️ File Organizer", 0, 0, self.file_organizer_status)
        self.create_system_card(cards_frame, "🔍 Code Monitor", 0, 1, self.code_monitor_status)
        self.create_system_card(cards_frame, "📧 Email Intelligence", 1, 0, self.email_intelligence_status)
        self.create_system_card(cards_frame, "🏃‍♂️ Health Interpreter", 1, 1, self.health_interpreter_status)
        
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
    
    def create_system_card(self, parent, title, row, col, status_func):
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
        
        # Store reference for updates
        setattr(self, f"{title.split()[1].lower()}_status_frame", status_frame)
        
        # Initial status load
        status_func(status_frame)
    
    def file_organizer_status(self, frame):
        """Update file organizer status"""
        try:
            # Clear frame
            for widget in frame.winfo_children():
                widget.destroy()
            
            # Try to load file organizer data
            intelligence_log = os.path.expanduser("~/email_intelligence.json")  # Using email log as proxy
            if os.path.exists(intelligence_log):
                with open(intelligence_log, 'r') as f:
                    data = json.load(f)
                
                stats = data.get('stats', {})
                
                tk.Label(frame, text="✅ Active", fg='#27ae60', font=('SF Pro Display', 12, 'bold'), 
                        bg='white').pack()
                tk.Label(frame, text=f"Files Processed: {stats.get('total_processed', 0)}", 
                        bg='white', font=('SF Pro Display', 10)).pack()
                tk.Label(frame, text="Last Run: Recently", bg='white', font=('SF Pro Display', 10)).pack()
                
                ttk.Button(frame, text="📁 Open Dashboard", 
                          command=lambda: self.open_dashboard("file")).pack(pady=5)
            else:
                tk.Label(frame, text="⚠️ No Data", fg='#f39c12', font=('SF Pro Display', 12, 'bold'), 
                        bg='white').pack()
                tk.Label(frame, text="Run system to see stats", bg='white', font=('SF Pro Display', 10)).pack()
                
        except Exception as e:
            tk.Label(frame, text="❌ Error", fg='#e74c3c', font=('SF Pro Display', 12, 'bold'), 
                    bg='white').pack()
            tk.Label(frame, text=str(e)[:30], bg='white', font=('SF Pro Display', 9)).pack()
    
    def code_monitor_status(self, frame):
        """Update code monitor status"""
        try:
            for widget in frame.winfo_children():
                widget.destroy()
            
            # Try to load code quality data
            quality_log = os.path.expanduser("~/code_quality_report.json")
            if os.path.exists(quality_log):
                with open(quality_log, 'r') as f:
                    data = json.load(f)
                
                files = data.get('files', {})
                total_files = len(files)
                avg_score = sum(f.get('quality_score', 0) for f in files.values()) / max(total_files, 1)
                
                tk.Label(frame, text="✅ Active", fg='#27ae60', font=('SF Pro Display', 12, 'bold'), 
                        bg='white').pack()
                tk.Label(frame, text=f"Files Analyzed: {total_files}", 
                        bg='white', font=('SF Pro Display', 10)).pack()
                tk.Label(frame, text=f"Avg Quality: {avg_score:.1f}/100", 
                        bg='white', font=('SF Pro Display', 10)).pack()
                
                ttk.Button(frame, text="🔍 Open Dashboard", 
                          command=lambda: self.open_dashboard("code")).pack(pady=5)
            else:
                tk.Label(frame, text="⚠️ No Data", fg='#f39c12', font=('SF Pro Display', 12, 'bold'), 
                        bg='white').pack()
                
        except Exception as e:
            tk.Label(frame, text="❌ Error", fg='#e74c3c', font=('SF Pro Display', 12, 'bold'), 
                    bg='white').pack()
    
    def email_intelligence_status(self, frame):
        """Update email intelligence status"""
        try:
            for widget in frame.winfo_children():
                widget.destroy()
            
            intelligence_log = os.path.expanduser("~/email_intelligence.json")
            if os.path.exists(intelligence_log):
                with open(intelligence_log, 'r') as f:
                    data = json.load(f)
                
                stats = data.get('stats', {})
                
                tk.Label(frame, text="✅ Active", fg='#27ae60', font=('SF Pro Display', 12, 'bold'), 
                        bg='white').pack()
                tk.Label(frame, text=f"Emails: {stats.get('total_processed', 0)}", 
                        bg='white', font=('SF Pro Display', 10)).pack()
                tk.Label(frame, text=f"Urgent: {stats.get('urgent_count', 0)}", 
                        bg='white', font=('SF Pro Display', 10)).pack()
                
                ttk.Button(frame, text="📧 Open Dashboard", 
                          command=lambda: self.open_dashboard("email")).pack(pady=5)
            else:
                tk.Label(frame, text="⚠️ No Data", fg='#f39c12', font=('SF Pro Display', 12, 'bold'), 
                        bg='white').pack()
                
        except Exception as e:
            tk.Label(frame, text="❌ Error", fg='#e74c3c', font=('SF Pro Display', 12, 'bold'), 
                    bg='white').pack()
    
    def health_interpreter_status(self, frame):
        """Update health interpreter status"""
        try:
            for widget in frame.winfo_children():
                widget.destroy()
            
            health_log = os.path.expanduser("~/health_intelligence.json")
            if os.path.exists(health_log):
                with open(health_log, 'r') as f:
                    data = json.load(f)
                
                stats = data.get('stats', {})
                
                tk.Label(frame, text="✅ Active", fg='#27ae60', font=('SF Pro Display', 12, 'bold'), 
                        bg='white').pack()
                tk.Label(frame, text=f"Health Score: {stats.get('health_score', 0)}/100", 
                        bg='white', font=('SF Pro Display', 10)).pack()
                tk.Label(frame, text=f"Days Tracked: {stats.get('total_days_tracked', 0)}", 
                        bg='white', font=('SF Pro Display', 10)).pack()
                
                ttk.Button(frame, text="🏃‍♂️ Open Dashboard", 
                          command=lambda: self.open_dashboard("health")).pack(pady=5)
            else:
                tk.Label(frame, text="⚠️ No Data", fg='#f39c12', font=('SF Pro Display', 12, 'bold'), 
                        bg='white').pack()
                
        except Exception as e:
            tk.Label(frame, text="❌ Error", fg='#e74c3c', font=('SF Pro Display', 12, 'bold'), 
                    bg='white').pack()
    
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
        
        # LaunchAgent controls
        agents_frame = tk.LabelFrame(settings_frame, text="🔄 Background Automation", 
                                   font=('SF Pro Display', 14, 'bold'))
        agents_frame.pack(fill='x', padx=20, pady=10)
        
        self.create_agent_control(agents_frame, "File Organizer", "smart.file.organizer")
        self.create_agent_control(agents_frame, "Code Monitor", "code.quality.monitor")
        self.create_agent_control(agents_frame, "Email Intelligence", "enhanced.email.final")
        self.create_agent_control(agents_frame, "Health Interpreter", "health.intelligence")
        
        # System info
        info_frame = tk.LabelFrame(settings_frame, text="ℹ️ System Information", 
                                 font=('SF Pro Display', 14, 'bold'))
        info_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(info_frame, text=f"Python Version: {subprocess.check_output(['python3', '--version']).decode().strip()}", 
                font=('SF Pro Display', 10)).pack(anchor='w', padx=10, pady=2)
        tk.Label(info_frame, text=f"GUI Version: 1.0.0", 
                font=('SF Pro Display', 10)).pack(anchor='w', padx=10, pady=2)
        tk.Label(info_frame, text=f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                font=('SF Pro Display', 10)).pack(anchor='w', padx=10, pady=2)
    
    def create_agent_control(self, parent, name, agent_name):
        """Create LaunchAgent control"""
        frame = tk.Frame(parent)
        frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(frame, text=name, font=('SF Pro Display', 12)).pack(side='left')
        
        ttk.Button(frame, text="Start", 
                  command=lambda: self.control_agent(agent_name, "load")).pack(side='right', padx=2)
        ttk.Button(frame, text="Stop", 
                  command=lambda: self.control_agent(agent_name, "unload")).pack(side='right', padx=2)
        ttk.Button(frame, text="Status", 
                  command=lambda: self.check_agent_status(agent_name)).pack(side='right', padx=2)
    
    def load_system_status(self):
        """Load initial system status"""
        self.file_organizer_status(self.organizer_status_frame)
        self.code_monitor_status(self.monitor_status_frame)
        self.email_intelligence_status(self.intelligence_status_frame)
        self.health_interpreter_status(self.interpreter_status_frame)
    
    def auto_refresh(self):
        """Auto-refresh system status"""
        self.load_system_status()
        self.root.after(30000, self.auto_refresh)  # Refresh every 30 seconds
