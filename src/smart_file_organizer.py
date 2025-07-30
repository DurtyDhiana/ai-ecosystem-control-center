#!/usr/bin/env python3
"""
Smart File Organizer - AI-powered file categorization and organization
"""
import os
import shutil
import json
import mimetypes
from pathlib import Path
from datetime import datetime
import subprocess
import hashlib
import sqlite3

# Configuration
WATCH_FOLDERS = [
    os.path.expanduser("~/Downloads"),
    os.path.expanduser("~/Desktop")
]

ORGANIZED_BASE = os.path.expanduser("~/SmartOrganized")
DUPLICATES_FOLDER = os.path.join(ORGANIZED_BASE, "Duplicates")
LOG_FILE = os.path.expanduser("~/smart_organizer.log")
HASH_DB_PATH = os.path.join(ORGANIZED_BASE, "file_hashes.db")

# Smart folder categories based on AI analysis
SMART_CATEGORIES = {
    "code": ["Documents/Code", [".py", ".js", ".html", ".css", ".json", ".md", ".txt"]],
    "images": ["Media/Images", [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"]],
    "documents": ["Documents/Papers", [".pdf", ".doc", ".docx", ".txt", ".rtf"]],
    "media": ["Media/Videos", [".mp4", ".mov", ".avi", ".mkv", ".mp3", ".wav"]],
    "archives": ["Archives", [".zip", ".rar", ".tar", ".gz", ".7z"]],
    "apps": ["Applications", [".dmg", ".pkg", ".app"]],
    "data": ["Data", [".csv", ".xlsx", ".json", ".xml", ".sql"]]
}

def log_action(message):
    """Log actions with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")

def analyze_file_with_ai(file_path):
    """Use AI to analyze file content and suggest category"""
    try:
        # Get basic file info
        file_ext = Path(file_path).suffix.lower()
        file_size = os.path.getsize(file_path)
        
        # Try to read file content for text files
        content_preview = ""
        if file_ext in ['.txt', '.md', '.py', '.js', '.html', '.css', '.json']:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content_preview = f.read(500)  # First 500 chars
            except:
                pass
        
        # Simple AI-like categorization based on content analysis
        filename = Path(file_path).name.lower()
        
        # Code detection
        if any(keyword in content_preview.lower() for keyword in ['import', 'function', 'class', 'def ', 'var ', 'const ']):
            return "code", f"Detected programming content in {filename}"
        
        # Document detection
        if any(keyword in filename for keyword in ['resume', 'cv', 'report', 'document', 'letter']):
            return "documents", f"Detected document: {filename}"
        
        # Project detection
        if any(keyword in filename for keyword in ['project', 'assignment', 'homework', 'work']):
            return "documents", f"Detected work-related file: {filename}"
        
        # Screenshot detection
        if any(keyword in filename for keyword in ['screenshot', 'screen shot', 'capture']):
            return "images", f"Detected screenshot: {filename}"
        
        # Default to extension-based categorization
        for category, (folder, extensions) in SMART_CATEGORIES.items():
            if file_ext in extensions:
                return category, f"Categorized by extension: {filename}"
        
        return "misc", f"Uncategorized file: {filename}"
        
    except Exception as e:
        log_action(f"Error analyzing {file_path}: {str(e)}")
        return "misc", f"Error analyzing file"

def calculate_file_hash(file_path):
    """Calculate SHA-256 hash of a file"""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            # Read file in chunks to handle large files efficiently
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
    except Exception as e:
        log_action(f"Error calculating hash for {file_path}: {str(e)}")
        return None

def init_hash_database():
    """Initialize the SQLite database for storing file hashes"""
    try:
        os.makedirs(os.path.dirname(HASH_DB_PATH), exist_ok=True)
        conn = sqlite3.connect(HASH_DB_PATH)
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_hashes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_hash TEXT UNIQUE NOT NULL,
                original_path TEXT NOT NULL,
                filename TEXT NOT NULL,
                organized_date TEXT NOT NULL,
                file_size INTEGER
            )
        ''')
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        log_action(f"Error initializing hash database: {str(e)}")
        return False

def check_duplicate(file_path, file_hash):
    """Check if file hash exists in database and return original location if found"""
    try:
        conn = sqlite3.connect(HASH_DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT original_path, filename, organized_date FROM file_hashes WHERE file_hash = ?', (file_hash,))
        result = cursor.fetchone()
        
        conn.close()
        return result  # Returns (original_path, filename, organized_date) or None
    except Exception as e:
        log_action(f"Error checking duplicate for {file_path}: {str(e)}")
        return None

def store_file_hash(file_path, file_hash, organized_path):
    """Store file hash in database"""
    try:
        conn = sqlite3.connect(HASH_DB_PATH)
        cursor = conn.cursor()
        
        filename = Path(file_path).name
        file_size = os.path.getsize(file_path)
        organized_date = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT OR REPLACE INTO file_hashes 
            (file_hash, original_path, filename, organized_date, file_size)
            VALUES (?, ?, ?, ?, ?)
        ''', (file_hash, organized_path, filename, organized_date, file_size))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        log_action(f"Error storing hash for {file_path}: {str(e)}")
        return False

def handle_duplicate_file(file_path, original_info):
    """Move duplicate file to Duplicates folder with timestamp suffix"""
    try:
        # Create duplicates folder
        os.makedirs(DUPLICATES_FOLDER, exist_ok=True)
        
        filename = Path(file_path).name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name, ext = os.path.splitext(filename)
        duplicate_filename = f"{name}_duplicate_{timestamp}{ext}"
        
        duplicate_path = os.path.join(DUPLICATES_FOLDER, duplicate_filename)
        
        # Move to duplicates folder
        shutil.move(file_path, duplicate_path)
        
        original_path, original_filename, organized_date = original_info
        log_action(f"DUPLICATE DETECTED: {filename} -> moved to Duplicates/{duplicate_filename}")
        log_action(f"Original file: {original_filename} organized on {organized_date} at {original_path}")
        
        return True
    except Exception as e:
        log_action(f"Error handling duplicate {file_path}: {str(e)}")
        return False

def create_smart_folders():
    """Create organized folder structure"""
    for category, (folder_path, _) in SMART_CATEGORIES.items():
        full_path = os.path.join(ORGANIZED_BASE, folder_path)
        os.makedirs(full_path, exist_ok=True)
    
    # Create misc and duplicates folders
    os.makedirs(os.path.join(ORGANIZED_BASE, "Miscellaneous"), exist_ok=True)
    os.makedirs(DUPLICATES_FOLDER, exist_ok=True)
    
    # Initialize hash database
    init_hash_database()

def organize_file(file_path):
    """Organize a single file using AI analysis and duplicate detection"""
    try:
        if not os.path.isfile(file_path):
            return
        
        filename = Path(file_path).name
        
        # Skip system files and already organized files
        if filename.startswith('.') or 'SmartOrganized' in file_path:
            return
        
        # Calculate file hash for duplicate detection
        file_hash = calculate_file_hash(file_path)
        if not file_hash:
            log_action(f"Skipping {filename} - could not calculate hash")
            return
        
        # Check for duplicates
        duplicate_info = check_duplicate(file_path, file_hash)
        if duplicate_info:
            handle_duplicate_file(file_path, duplicate_info)
            return
        
        # AI analysis for new files
        category, reason = analyze_file_with_ai(file_path)
        
        # Determine destination
        if category in SMART_CATEGORIES:
            dest_folder = os.path.join(ORGANIZED_BASE, SMART_CATEGORIES[category][0])
        else:
            dest_folder = os.path.join(ORGANIZED_BASE, "Miscellaneous")
        
        # Create destination if it doesn't exist
        os.makedirs(dest_folder, exist_ok=True)
        
        # Move file
        dest_path = os.path.join(dest_folder, filename)
        
        # Handle filename conflicts (different from content duplicates)
        counter = 1
        original_dest = dest_path
        while os.path.exists(dest_path):
            name, ext = os.path.splitext(original_dest)
            dest_path = f"{name}_{counter}{ext}"
            counter += 1
        
        shutil.move(file_path, dest_path)
        
        # Store hash in database for future duplicate detection
        store_file_hash(file_path, file_hash, dest_path)
        
        log_action(f"Moved {filename} to {category} folder - {reason}")
        
    except Exception as e:
        log_action(f"Error organizing {file_path}: {str(e)}")

def scan_and_organize():
    """Main function to scan folders and organize files"""
    log_action("Starting smart file organization scan...")
    
    create_smart_folders()
    files_processed = 0
    duplicates_found = 0
    
    for folder in WATCH_FOLDERS:
        if not os.path.exists(folder):
            continue
            
        log_action(f"Scanning {folder}...")
        
        for item in os.listdir(folder):
            item_path = os.path.join(folder, item)
            if os.path.isfile(item_path):
                # Check if it's a duplicate before organizing
                file_hash = calculate_file_hash(item_path)
                if file_hash and check_duplicate(item_path, file_hash):
                    duplicates_found += 1
                
                organize_file(item_path)
                files_processed += 1
    
    log_action(f"Organization complete! Processed {files_processed} files, found {duplicates_found} duplicates.")
    
    # Send notification
    try:
        notification_text = f"Organized {files_processed} files!"
        if duplicates_found > 0:
            notification_text += f" Found {duplicates_found} duplicates."
        
        subprocess.run([
            'osascript', '-e', 
            f'display notification "{notification_text}" with title "Smart File Organizer"'
        ])
    except:
        pass

if __name__ == "__main__":
    scan_and_organize()
