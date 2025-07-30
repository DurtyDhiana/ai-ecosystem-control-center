#!/usr/bin/env python3
"""
AI Code Quality Monitor - Real-time code analysis and improvement suggestions
"""
import os
import json
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime
import time
import re

# Configuration
CODE_FOLDERS = [
    os.path.expanduser("~/code"),
    os.path.expanduser("~/Documents/Code"),
    os.path.expanduser("~/SmartOrganized/Documents/Code"),
    os.path.expanduser("~/Desktop"),  # For quick scripts
]

QUALITY_LOG = os.path.expanduser("~/code_quality_report.json")
SUGGESTIONS_LOG = os.path.expanduser("~/code_suggestions.log")
DASHBOARD_HTML = os.path.expanduser("~/code_quality_dashboard.html")

# File extensions to monitor
CODE_EXTENSIONS = {'.py', '.js', '.html', '.css', '.json', '.md', '.txt', '.sh', '.yml', '.yaml'}

class CodeQualityAnalyzer:
    def __init__(self):
        self.file_hashes = {}
        self.quality_history = self.load_quality_history()
    
    def load_quality_history(self):
        """Load previous quality analysis history"""
        try:
            if os.path.exists(QUALITY_LOG):
                with open(QUALITY_LOG, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {"files": {}, "summary": {"total_files": 0, "issues_found": 0, "suggestions_made": 0}}
    
    def save_quality_history(self):
        """Save quality analysis to file"""
        with open(QUALITY_LOG, 'w') as f:
            json.dump(self.quality_history, f, indent=2)
    
    def log_suggestion(self, message):
        """Log suggestions with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(SUGGESTIONS_LOG, "a") as f:
            f.write(f"[{timestamp}] {message}\n")
        print(f"[{timestamp}] {message}")
    
    def get_file_hash(self, file_path):
        """Get MD5 hash of file content"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None
    
    def analyze_python_code(self, file_path, content):
        """AI analysis for Python files"""
        issues = []
        suggestions = []
        
        lines = content.split('\n')
        
        # Check for common issues
        for i, line in enumerate(lines, 1):
            line_stripped = line.strip()
            
            # Long lines
            if len(line) > 100:
                issues.append(f"Line {i}: Line too long ({len(line)} chars)")
                suggestions.append(f"Consider breaking line {i} into multiple lines")
            
            # Unused imports (simple detection)
            if line_stripped.startswith('import ') or line_stripped.startswith('from '):
                import_name = line_stripped.split()[1].split('.')[0]
                if content.count(import_name) == 1:  # Only appears in import line
                    issues.append(f"Line {i}: Potentially unused import '{import_name}'")
                    suggestions.append(f"Consider removing unused import '{import_name}' on line {i}")
            
            # TODO comments
            if 'TODO' in line_stripped or 'FIXME' in line_stripped:
                issues.append(f"Line {i}: TODO/FIXME comment found")
                suggestions.append(f"Address TODO/FIXME comment on line {i}")
            
            # Print statements (should use logging)
            if 'print(' in line_stripped and not line_stripped.startswith('#'):
                suggestions.append(f"Line {i}: Consider using logging instead of print()")
            
            # No docstrings for functions
            if line_stripped.startswith('def ') and i < len(lines) - 1:
                next_line = lines[i].strip() if i < len(lines) else ""
                if not next_line.startswith('"""') and not next_line.startswith("'''"):
                    func_name = line_stripped.split('(')[0].replace('def ', '')
                    suggestions.append(f"Function '{func_name}' on line {i} missing docstring")
        
        # Check for complexity
        function_count = content.count('def ')
        class_count = content.count('class ')
        
        if function_count > 10:
            suggestions.append(f"File has {function_count} functions - consider splitting into modules")
        
        if len(lines) > 200:
            suggestions.append(f"File is {len(lines)} lines long - consider refactoring")
        
        return issues, suggestions
    
    def analyze_javascript_code(self, file_path, content):
        """AI analysis for JavaScript files"""
        issues = []
        suggestions = []
        
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            line_stripped = line.strip()
            
            # Console.log statements
            if 'console.log(' in line_stripped:
                suggestions.append(f"Line {i}: Consider removing console.log() for production")
            
            # Var instead of let/const
            if line_stripped.startswith('var '):
                suggestions.append(f"Line {i}: Consider using 'let' or 'const' instead of 'var'")
            
            # Missing semicolons
            if line_stripped and not line_stripped.endswith((';', '{', '}', ')', ']')) and not line_stripped.startswith('//'):
                if any(keyword in line_stripped for keyword in ['=', 'return', 'const', 'let']):
                    issues.append(f"Line {i}: Missing semicolon")
            
            # Long lines
            if len(line) > 120:
                issues.append(f"Line {i}: Line too long ({len(line)} chars)")
        
        return issues, suggestions
    
    def analyze_general_code(self, file_path, content):
        """General analysis for any code file"""
        issues = []
        suggestions = []
        
        lines = content.split('\n')
        
        # Check for common patterns
        for i, line in enumerate(lines, 1):
            line_stripped = line.strip()
            
            # Hardcoded passwords/keys (simple detection)
            if any(keyword in line_stripped.lower() for keyword in ['password=', 'api_key=', 'secret=', 'token=']):
                if not line_stripped.startswith('#'):
                    issues.append(f"Line {i}: Potential hardcoded credential")
                    suggestions.append(f"Line {i}: Move credentials to environment variables")
            
            # Very long lines
            if len(line) > 150:
                issues.append(f"Line {i}: Extremely long line ({len(line)} chars)")
            
            # Trailing whitespace
            if line.endswith(' ') or line.endswith('\t'):
                issues.append(f"Line {i}: Trailing whitespace")
        
        # File-level checks
        if len(lines) > 500:
            suggestions.append(f"File is very large ({len(lines)} lines) - consider splitting")
        
        if content.count('\t') > 0 and content.count('    ') > 0:
            issues.append("Mixed indentation (tabs and spaces)")
            suggestions.append("Use consistent indentation (prefer spaces)")
        
        return issues, suggestions
    
    def analyze_file(self, file_path):
        """Analyze a single code file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            if not content.strip():
                return
            
            file_ext = Path(file_path).suffix.lower()
            filename = Path(file_path).name
            
            # Get file-specific analysis
            if file_ext == '.py':
                issues, suggestions = self.analyze_python_code(file_path, content)
            elif file_ext == '.js':
                issues, suggestions = self.analyze_javascript_code(file_path, content)
            else:
                issues, suggestions = self.analyze_general_code(file_path, content)
            
            # Calculate quality score
            total_lines = len(content.split('\n'))
            issue_ratio = len(issues) / max(total_lines, 1)
            quality_score = max(0, 100 - (issue_ratio * 100))
            
            # Update history
            file_key = str(file_path)
            self.quality_history["files"][file_key] = {
                "last_analyzed": datetime.now().isoformat(),
                "quality_score": round(quality_score, 2),
                "issues_count": len(issues),
                "suggestions_count": len(suggestions),
                "file_size": len(content),
                "line_count": total_lines,
                "issues": issues[:5],  # Store top 5 issues
                "suggestions": suggestions[:5]  # Store top 5 suggestions
            }
            
            # Log findings
            if issues or suggestions:
                self.log_suggestion(f"📁 Analyzed {filename}")
                
                if issues:
                    self.log_suggestion(f"  🚨 Found {len(issues)} issues:")
                    for issue in issues[:3]:  # Show top 3
                        self.log_suggestion(f"    • {issue}")
                
                if suggestions:
                    self.log_suggestion(f"  💡 {len(suggestions)} suggestions:")
                    for suggestion in suggestions[:3]:  # Show top 3
                        self.log_suggestion(f"    • {suggestion}")
                
                self.log_suggestion(f"  📊 Quality Score: {quality_score:.1f}/100")
                self.log_suggestion("")
            
        except Exception as e:
            self.log_suggestion(f"Error analyzing {file_path}: {str(e)}")
    
    def generate_dashboard(self):
        """Generate HTML dashboard"""
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Code Quality Dashboard</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px; }}
        .stat-card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .stat-number {{ font-size: 2em; font-weight: bold; color: #3498db; }}
        .file-list {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .file-item {{ border-bottom: 1px solid #eee; padding: 15px 0; }}
        .file-name {{ font-weight: bold; color: #2c3e50; }}
        .quality-score {{ float: right; padding: 5px 10px; border-radius: 20px; color: white; }}
        .score-high {{ background: #27ae60; }}
        .score-medium {{ background: #f39c12; }}
        .score-low {{ background: #e74c3c; }}
        .issues {{ color: #e74c3c; margin-top: 5px; }}
        .suggestions {{ color: #3498db; margin-top: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Code Quality Dashboard</h1>
            <p>Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{len(self.quality_history['files'])}</div>
                <div>Files Monitored</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{sum(f.get('issues_count', 0) for f in self.quality_history['files'].values())}</div>
                <div>Total Issues</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{sum(f.get('suggestions_count', 0) for f in self.quality_history['files'].values())}</div>
                <div>Suggestions Made</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{round(sum(f.get('quality_score', 0) for f in self.quality_history['files'].values()) / max(len(self.quality_history['files']), 1), 1)}</div>
                <div>Average Quality</div>
            </div>
        </div>
        
        <div class="file-list">
            <h2>📂 File Analysis Results</h2>
        """
        
        # Sort files by quality score
        sorted_files = sorted(
            self.quality_history['files'].items(),
            key=lambda x: x[1].get('quality_score', 0),
            reverse=True
        )
        
        for file_path, data in sorted_files:
            filename = Path(file_path).name
            score = data.get('quality_score', 0)
            
            score_class = 'score-high' if score >= 80 else 'score-medium' if score >= 60 else 'score-low'
            
            html_content += f"""
            <div class="file-item">
                <div class="file-name">{filename}</div>
                <div class="quality-score {score_class}">{score}/100</div>
                <div style="clear: both;"></div>
                <small>📏 {data.get('line_count', 0)} lines | 📅 {data.get('last_analyzed', '')[:16]}</small>
            """
            
            if data.get('issues'):
                html_content += f"<div class='issues'>🚨 Issues: {', '.join(data['issues'][:2])}</div>"
            
            if data.get('suggestions'):
                html_content += f"<div class='suggestions'>💡 Suggestions: {', '.join(data['suggestions'][:2])}</div>"
            
            html_content += "</div>"
        
        html_content += """
        </div>
    </div>
</body>
</html>
        """
        
        with open(DASHBOARD_HTML, 'w') as f:
            f.write(html_content)
        
        self.log_suggestion(f"📊 Dashboard updated: {DASHBOARD_HTML}")
    
    def scan_and_analyze(self):
        """Main function to scan folders and analyze code"""
        self.log_suggestion("🔍 Starting code quality analysis...")
        
        files_analyzed = 0
        
        for folder in CODE_FOLDERS:
            if not os.path.exists(folder):
                continue
            
            self.log_suggestion(f"📁 Scanning {folder}...")
            
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_ext = Path(file_path).suffix.lower()
                    
                    if file_ext in CODE_EXTENSIONS:
                        # Check if file changed
                        current_hash = self.get_file_hash(file_path)
                        if current_hash and current_hash != self.file_hashes.get(file_path):
                            self.analyze_file(file_path)
                            self.file_hashes[file_path] = current_hash
                            files_analyzed += 1
        
        if files_analyzed > 0:
            self.save_quality_history()
            self.generate_dashboard()
            
            # Send notification
            try:
                subprocess.run([
                    'osascript', '-e', 
                    f'display notification "Analyzed {files_analyzed} code files!" with title "Code Quality Monitor"'
                ])
            except:
                pass
        
        self.log_suggestion(f"✅ Analysis complete! Processed {files_analyzed} files.")

if __name__ == "__main__":
    analyzer = CodeQualityAnalyzer()
    analyzer.scan_and_analyze()
