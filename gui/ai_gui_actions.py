#!/usr/bin/env python3
"""
AI GUI Actions - Methods for the GUI application
"""

def add_gui_actions(gui_class):
    """Add action methods to the GUI class"""
    
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
                
                # Refresh status
                self.file_organizer_status(self.organizer_status_frame)
                
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
                
                # Refresh status
                self.code_monitor_status(self.monitor_status_frame)
                
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
                # Run the enhanced email intelligence
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

email_ai.log_action('📊 Enhanced dashboard updated successfully!')
email_ai.log_action('✅ Complete enhanced email intelligence analysis finished!')
                    '''
                ], capture_output=True, text=True, cwd='/Users/MAC')
                
                self.email_status_text.insert(tk.END, f"✅ Email Intelligence completed!\n")
                self.email_status_text.insert(tk.END, f"Output:\n{result.stdout}\n")
                
                # Refresh status
                self.email_intelligence_status(self.intelligence_status_frame)
                
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

health_ai.log_action('📊 Health dashboard updated successfully!')
health_ai.log_action('✅ Complete health intelligence analysis finished!')
                    '''
                ], capture_output=True, text=True, cwd='/Users/MAC')
                
                self.health_status_text.insert(tk.END, f"✅ Health Interpreter completed!\n")
                self.health_status_text.insert(tk.END, f"Output:\n{result.stdout}\n")
                
                # Refresh status
                self.health_interpreter_status(self.interpreter_status_frame)
                
            except Exception as e:
                self.health_status_text.insert(tk.END, f"❌ Error: {str(e)}\n")
        
        threading.Thread(target=run_in_thread, daemon=True).start()
    
    def open_dashboard(self, system_type):
        """Open system dashboard"""
        dashboard_files = {
            "file": "~/smart_organizer_dashboard.html",  # Would need to create this
            "code": "~/code_quality_dashboard.html",
            "email": "~/email_dashboard.html",
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
        self.load_system_status()
        messagebox.showinfo("Refresh Complete", "All system statuses have been refreshed.")
    
    def view_system_logs(self):
        """View system logs"""
        log_window = tk.Toplevel(self.root)
        log_window.title("📋 System Logs")
        log_window.geometry("800x600")
        
        notebook = ttk.Notebook(log_window)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Add log tabs
        log_files = {
            "File Organizer": "~/smart_organizer.log",
            "Code Monitor": "~/code_suggestions.log", 
            "Email Intelligence": "~/email_intelligence.log",
            "Health Interpreter": "~/health_intelligence.log"
        }
        
        for name, log_file in log_files.items():
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=name)
            
            text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD)
            text_widget.pack(fill='both', expand=True)
            
            # Load log content
            log_path = os.path.expanduser(log_file)
            if os.path.exists(log_path):
                try:
                    with open(log_path, 'r') as f:
                        content = f.read()
                        # Show last 100 lines
                        lines = content.split('\n')
                        text_widget.insert(tk.END, '\n'.join(lines[-100:]))
                except Exception as e:
                    text_widget.insert(tk.END, f"Error reading log: {str(e)}")
            else:
                text_widget.insert(tk.END, "Log file not found.")
    
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
    
    def control_agent(self, agent_name, action):
        """Control LaunchAgent"""
        try:
            if action == "load":
                result = subprocess.run([
                    'launchctl', 'load', f'{os.path.expanduser("~/Library/LaunchAgents")}/{agent_name}.plist'
                ], capture_output=True, text=True)
                if result.returncode == 0:
                    messagebox.showinfo("Success", f"{agent_name} started successfully.")
                else:
                    messagebox.showerror("Error", f"Failed to start {agent_name}: {result.stderr}")
            
            elif action == "unload":
                result = subprocess.run([
                    'launchctl', 'unload', f'{os.path.expanduser("~/Library/LaunchAgents")}/{agent_name}.plist'
                ], capture_output=True, text=True)
                if result.returncode == 0:
                    messagebox.showinfo("Success", f"{agent_name} stopped successfully.")
                else:
                    messagebox.showerror("Error", f"Failed to stop {agent_name}: {result.stderr}")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error controlling {agent_name}: {str(e)}")
    
    def check_agent_status(self, agent_name):
        """Check LaunchAgent status"""
        try:
            result = subprocess.run([
                'launchctl', 'list', agent_name
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                messagebox.showinfo("Agent Status", f"{agent_name} is running.")
            else:
                messagebox.showinfo("Agent Status", f"{agent_name} is not running.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error checking {agent_name}: {str(e)}")
    
    def open_system_settings(self):
        """Open system settings"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("⚙️ Advanced Settings")
        settings_window.geometry("600x400")
        
        tk.Label(settings_window, text="⚙️ Advanced System Settings", 
                font=('SF Pro Display', 18, 'bold')).pack(pady=20)
        
        # Configuration files
        config_frame = tk.LabelFrame(settings_window, text="📝 Configuration Files", 
                                   font=('SF Pro Display', 14, 'bold'))
        config_frame.pack(fill='x', padx=20, pady=10)
        
        configs = [
            ("Email Config", "~/.email_config.yaml"),
            ("Health Goals", "~/health_intelligence.json"),
            ("System Aliases", "~/.email_aliases")
        ]
        
        for name, path in configs:
            frame = tk.Frame(config_frame)
            frame.pack(fill='x', padx=10, pady=5)
            
            tk.Label(frame, text=name, font=('SF Pro Display', 12)).pack(side='left')
            ttk.Button(frame, text="Edit", 
                      command=lambda p=path: subprocess.run(['open', '-a', 'TextEdit', os.path.expanduser(p)])).pack(side='right')
    
    # Add all methods to the class
    gui_class.run_file_organizer = run_file_organizer
    gui_class.run_code_monitor = run_code_monitor
    gui_class.run_email_intelligence = run_email_intelligence
    gui_class.run_health_interpreter = run_health_interpreter
    gui_class.open_dashboard = open_dashboard
    gui_class.open_all_dashboards = open_all_dashboards
    gui_class.refresh_all_systems = refresh_all_systems
    gui_class.view_system_logs = view_system_logs
    gui_class.open_organized_folder = open_organized_folder
    gui_class.view_code_suggestions = view_code_suggestions
    gui_class.view_email_drafts = view_email_drafts
    gui_class.view_health_reports = view_health_reports
    gui_class.control_agent = control_agent
    gui_class.check_agent_status = check_agent_status
    gui_class.open_system_settings = open_system_settings

if __name__ == "__main__":
    print("GUI actions module ready!")
