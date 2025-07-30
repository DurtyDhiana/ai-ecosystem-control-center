#!/usr/bin/env python3
"""
AI Ecosystem GUI Application - Complete unified interface
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import subprocess
import threading
from datetime import datetime
import webbrowser

# Import the main GUI class
exec(open('/Users/MAC/ai_ecosystem_gui.py').read())

# Import and add the action methods
exec(open('/Users/MAC/ai_gui_actions.py').read())

def main():
    """Main application entry point"""
    root = tk.Tk()
    
    # Set app icon and properties
    root.title("🤖 AI Ecosystem Control Center")
    
    # Try to set a nice icon (optional)
    try:
        # You could add an icon file here
        pass
    except:
        pass
    
    # Create the main application
    app = AIEcosystemGUI(root)
    
    # Add action methods to the app
    add_gui_actions(AIEcosystemGUI)
    
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
