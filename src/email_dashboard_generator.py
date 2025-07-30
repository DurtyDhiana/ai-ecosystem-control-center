#!/usr/bin/env python3
"""
Complete Enhanced Email Dashboard Generator
"""
import json
import os
from datetime import datetime

def generate_complete_dashboard(email_history, unsubscribe_history, config):
    """Generate the complete enhanced HTML dashboard"""
    stats = email_history["stats"]
    
    # Calculate monthly unsubscribe stats
    current_month = datetime.now().strftime("%Y-%m")
    monthly_unsubscribes = len([
        u for u in unsubscribe_history.get('successful_unsubscribes', [])
        if u['timestamp'].startswith(current_month)
    ])
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Enhanced Email Intelligence Dashboard</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{ 
            max-width: 1400px; 
            margin: 0 auto; 
            background: rgba(255,255,255,0.95);
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }}
        
        .header {{ 
            background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%); 
            color: white; 
            padding: 40px; 
            text-align: center;
        }}
        
        .header h1 {{ 
            font-size: 3em; 
            margin-bottom: 10px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }}
        
        .header p {{ 
            opacity: 0.9; 
            font-size: 1.1em;
        }}
        
        .stats-grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
            gap: 25px; 
            padding: 40px;
            background: #f8fafc;
        }}
        
        .stat-card {{ 
            background: white; 
            padding: 30px; 
            border-radius: 15px; 
            box-shadow: 0 8px 25px rgba(0,0,0,0.08); 
            border-left: 5px solid #667eea;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.15);
        }}
        
        .stat-number {{ 
            font-size: 3em; 
            font-weight: 800; 
            color: #2d3748; 
            margin-bottom: 10px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .stat-label {{ 
            color: #718096; 
            font-size: 1em; 
            text-transform: uppercase; 
            letter-spacing: 1px;
            font-weight: 600;
        }}
        
        .stat-change {{ 
            font-size: 0.9em; 
            color: #38a169; 
            margin-top: 8px;
            font-weight: 500;
        }}
        
        .main-content {{ 
            display: grid; 
            grid-template-columns: 2fr 1fr; 
            gap: 40px; 
            padding: 40px;
        }}
        
        .email-list {{ 
            background: white; 
            padding: 30px; 
            border-radius: 15px; 
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        }}
        
        .email-list h2 {{
            color: #2d3748;
            margin-bottom: 25px;
            font-size: 1.8em;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .sidebar {{ 
            display: flex; 
            flex-direction: column; 
            gap: 25px; 
        }}
        
        .email-item {{ 
            border-bottom: 1px solid #e2e8f0; 
            padding: 25px 0; 
            transition: background-color 0.3s ease;
        }}
        
        .email-item:hover {{
            background-color: #f7fafc;
            margin: 0 -15px;
            padding: 25px 15px;
            border-radius: 10px;
        }}
        
        .email-item:last-child {{ border-bottom: none; }}
        
        .email-subject {{ 
            font-weight: 700; 
            color: #2d3748; 
            font-size: 1.2em; 
            margin-bottom: 12px;
            line-height: 1.4;
        }}
        
        .email-meta {{ 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            margin-bottom: 15px; 
        }}
        
        .email-sender {{ 
            color: #4a5568; 
            font-size: 1em;
            font-weight: 500;
        }}
        
        .email-time {{ 
            color: #a0aec0; 
            font-size: 0.9em; 
        }}
        
        .urgency-badge {{ 
            padding: 6px 15px; 
            border-radius: 25px; 
            color: white; 
            font-size: 0.8em; 
            font-weight: 700; 
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .urgency-high {{ background: linear-gradient(135deg, #e53e3e, #c53030); }}
        .urgency-medium {{ background: linear-gradient(135deg, #dd6b20, #c05621); }}
        .urgency-low {{ background: linear-gradient(135deg, #38a169, #2f855a); }}
        
        .category-badge {{ 
            padding: 4px 12px; 
            border-radius: 15px; 
            font-size: 0.75em; 
            margin-left: 10px;
            font-weight: 600;
        }}
        
        .category-work {{ background: #ebf8ff; color: #2b6cb0; }}
        .category-personal {{ background: #f0fff4; color: #276749; }}
        .category-promotional {{ background: #fef5e7; color: #b7791f; }}
        .category-spam {{ background: #fed7d7; color: #c53030; }}
        
        .features {{ 
            color: #4a5568; 
            font-size: 0.9em; 
            margin-top: 12px; 
        }}
        
        .feature-tag {{ 
            display: inline-block; 
            background: linear-gradient(135deg, #edf2f7, #e2e8f0); 
            color: #4a5568; 
            padding: 4px 10px; 
            border-radius: 8px; 
            margin-right: 8px; 
            font-size: 0.8em;
            margin-bottom: 5px;
        }}
        
        .sidebar-card {{ 
            background: white; 
            padding: 25px; 
            border-radius: 15px; 
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        }}
        
        .sidebar-card h3 {{ 
            margin: 0 0 20px 0; 
            color: #2d3748;
            font-size: 1.3em;
            border-bottom: 2px solid #667eea;
            padding-bottom: 8px;
        }}
        
        .unsubscribe-list {{ 
            max-height: 250px; 
            overflow-y: auto; 
        }}
        
        .unsubscribe-item {{ 
            padding: 12px 0; 
            border-bottom: 1px solid #e2e8f0; 
            font-size: 0.9em; 
        }}
        
        .unsubscribe-item:last-child {{ border-bottom: none; }}
        
        .attachment-stats {{ 
            display: flex; 
            justify-content: space-between; 
            margin-bottom: 15px;
            align-items: center;
        }}
        
        .storage-saved {{ 
            font-size: 1.4em; 
            font-weight: 700; 
            color: #38a169; 
        }}
        
        .quick-actions {{ 
            display: flex; 
            gap: 12px; 
            margin-top: 20px; 
        }}
        
        .action-btn {{ 
            padding: 10px 20px; 
            background: linear-gradient(135deg, #667eea, #764ba2); 
            color: white; 
            border: none; 
            border-radius: 8px; 
            cursor: pointer; 
            font-size: 0.9em;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        
        .action-btn:hover {{ 
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}
        
        .footer {{
            text-align: center;
            padding: 30px;
            background: #f8fafc;
            color: #a0aec0;
            font-size: 0.9em;
        }}
        
        .footer a {{
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
        }}
        
        @media (max-width: 768px) {{
            .main-content {{ grid-template-columns: 1fr; }}
            .stats-grid {{ grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); }}
            .header h1 {{ font-size: 2em; }}
            .container {{ margin: 10px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Enhanced Email Intelligence</h1>
            <p>AI-powered email analysis, auto-unsubscribe, and smart attachment management</p>
            <p>Last updated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{stats['total_processed']}</div>
                <div class="stat-label">Emails Processed</div>
                <div class="stat-change">📧 All time total</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{stats['urgent_count']}</div>
                <div class="stat-label">Urgent Emails</div>
                <div class="stat-change">🚨 Requires attention</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{monthly_unsubscribes}</div>
                <div class="stat-label">Unsubscribed This Month</div>
                <div class="stat-change">🚫 Auto-cleaned</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{stats['attachments_moved']}</div>
                <div class="stat-label">Attachments Moved</div>
                <div class="stat-change">☁️ {stats['storage_saved_mb']:.1f}MB saved</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{stats['drafts_created']}</div>
                <div class="stat-label">AI Drafts Created</div>
                <div class="stat-change">💬 Ready to send</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{stats['spam_detected']}</div>
                <div class="stat-label">Spam Blocked</div>
                <div class="stat-change">🛡️ Protected</div>
            </div>
        </div>
        
        <div class="main-content">
            <div class="email-list">
                <h2>📬 Recent Email Analysis</h2>
    """
    
    # Sort emails by urgency and recency
    sorted_emails = sorted(
        email_history["emails"].items(),
        key=lambda x: (
            {"HIGH": 3, "MEDIUM": 2, "LOW": 1}.get(x[1]["analysis"]["urgency_level"], 0),
            x[1]["received"]
        ),
        reverse=True
    )
    
    for email_id, email_data in sorted_emails:
        analysis = email_data["analysis"]
        urgency_class = f"urgency-{analysis['urgency_level'].lower()}"
        category_class = f"category-{analysis['category']}"
        
        category_emoji = {
            "work": "💼", "personal": "👤", 
            "promotional": "🛍️", "spam": "🗑️"
        }.get(analysis["category"], "📧")
        
        html_content += f"""
        <div class="email-item">
            <div class="email-subject">{email_data['subject']}</div>
            <div class="email-meta">
                <div class="email-sender">
                    {category_emoji} {email_data['sender']}
                    <span class="category-badge {category_class}">{analysis['category'].title()}</span>
                </div>
                <div>
                    <span class="urgency-badge {urgency_class}">{analysis['urgency_level']}</span>
                </div>
            </div>
            <div class="email-time">📅 {email_data['received'][:16]} | Urgency Score: {analysis['urgency_score']}/100</div>
        """
        
        # Features and enhancements
        features = []
        if analysis["keywords"]:
            features.append(f"🔍 {', '.join(analysis['keywords'][:3])}")
        if analysis["suggested_response"]:
            features.append("💬 AI Draft Available")
        if analysis.get("attachment_links"):
            features.append(f"📎 {len(analysis['attachment_links'])} attachments moved")
        if email_data.get("attachments"):
            total_size = sum(att['size_mb'] for att in email_data['attachments'])
            features.append(f"📊 {total_size:.1f}MB attachments")
        
        if features:
            html_content += f"<div class='features'>"
            for feature in features:
                html_content += f"<span class='feature-tag'>{feature}</span>"
            html_content += "</div>"
        
        html_content += "</div>"
    
    # Sidebar content
    html_content += f"""
            </div>
            
            <div class="sidebar">
                <div class="sidebar-card">
                    <h3>🚫 Auto-Unsubscribe</h3>
                    <div class="attachment-stats">
                        <span>This Month:</span>
                        <span class="storage-saved">{monthly_unsubscribes}</span>
                    </div>
                    <div class="unsubscribe-list">
    """
    
    # Recent unsubscribes
    recent_unsubscribes = unsubscribe_history.get('successful_unsubscribes', [])[-5:]
    for unsub in reversed(recent_unsubscribes):
        html_content += f"""
        <div class="unsubscribe-item">
            ✅ <strong>{unsub['sender']}</strong><br>
            <small style="color: #a0aec0;">{unsub['timestamp'][:16]}</small>
        </div>
        """
    
    if not recent_unsubscribes:
        html_content += "<div class='unsubscribe-item'>No recent unsubscribes</div>"
    
    html_content += f"""
                    </div>
                    <div class="quick-actions">
                        <button class="action-btn" onclick="location.reload()">🔄 Refresh</button>
                    </div>
                </div>
                
                <div class="sidebar-card">
                    <h3>☁️ Storage Management</h3>
                    <div class="attachment-stats">
                        <span>Space Saved:</span>
                        <span class="storage-saved">{stats['storage_saved_mb']:.1f} MB</span>
                    </div>
                    <div class="attachment-stats">
                        <span>Files Moved:</span>
                        <span><strong>{stats['attachments_moved']}</strong> attachments</span>
                    </div>
                    <div style="font-size: 0.85em; color: #718096; margin-top: 15px; line-height: 1.5;">
                        Large attachments are automatically moved to cloud storage and replaced with secure links.
                    </div>
                </div>
                
                <div class="sidebar-card">
                    <h3>📊 Category Breakdown</h3>
    """
    
    # Category breakdown
    for category, email_ids in email_history["categories"].items():
        if email_ids:
            category_emoji = {
                "work": "💼", "personal": "👤", 
                "promotional": "🛍️", "spam": "🗑️", "urgent": "🚨"
            }.get(category, "📧")
            
            html_content += f"""
            <div class="attachment-stats">
                <span>{category_emoji} {category.title()}:</span>
                <span><strong>{len(email_ids)}</strong> emails</span>
            </div>
            """
    
    html_content += f"""
                </div>
                
                <div class="sidebar-card">
                    <h3>⚙️ Configuration</h3>
                    <div style="font-size: 0.9em; color: #4a5568; line-height: 1.6;">
                        <div style="margin-bottom: 8px;">
                            <strong>Auto-unsubscribe:</strong> {'✅ Enabled' if config.get('auto_unsubscribe') else '❌ Disabled'}
                        </div>
                        <div style="margin-bottom: 8px;">
                            <strong>Attachment limit:</strong> {config.get('attachment_size_limit_mb', 3)} MB
                        </div>
                        <div style="margin-bottom: 8px;">
                            <strong>Cloud storage:</strong> {config.get('cloud_storage', 'icloud').title()}
                        </div>
                        <div>
                            <strong>Safelist domains:</strong> {len(config.get('safelist_domains', []))} domains
                        </div>
                    </div>
                    <div class="quick-actions">
                        <button class="action-btn" onclick="alert('Edit ~/.email_config.yaml to modify settings')">⚙️ Settings</button>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            Enhanced Email Intelligence Dashboard | Powered by AI | 
            <a href="file://{os.path.expanduser('~/email_intelligence.log')}">View Logs</a> | 
            <a href="file://{os.path.expanduser('~/EmailDrafts')}">View Drafts</a>
        </div>
    </div>
    
    <script>
        // Auto-refresh every 5 minutes
        setTimeout(() => location.reload(), 300000);
        
        // Add smooth scrolling
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({{
                    behavior: 'smooth'
                }});
            }});
        }});
        
        // Add click handlers for action buttons
        document.querySelectorAll('.action-btn').forEach(btn => {{
            btn.addEventListener('click', function(e) {{
                if (this.textContent.includes('Settings')) {{
                    alert('Settings panel coming soon! Edit ~/.email_config.yaml for now.');
                }}
            }});
        }});
        
        // Add loading animation
        window.addEventListener('load', function() {{
            document.querySelectorAll('.stat-card, .email-item, .sidebar-card').forEach((el, index) => {{
                el.style.opacity = '0';
                el.style.transform = 'translateY(20px)';
                setTimeout(() => {{
                    el.style.transition = 'all 0.6s ease';
                    el.style.opacity = '1';
                    el.style.transform = 'translateY(0)';
                }}, index * 100);
            }});
        }});
    </script>
</body>
</html>"""
    
    return html_content

if __name__ == "__main__":
    print("Enhanced dashboard generator ready!")
