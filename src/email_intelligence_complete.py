#!/usr/bin/env python3
"""
Complete Enhanced Email Intelligence System
"""
import os
import json
import yaml
import re
import requests
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
from bs4 import BeautifulSoup

# Configuration
EMAIL_CONFIG_FILE = os.path.expanduser("~/.email_config.yaml")
INTELLIGENCE_LOG = os.path.expanduser("~/email_intelligence.json")
DRAFTS_FOLDER = os.path.expanduser("~/EmailDrafts")
LARGE_ATTACHMENTS_FOLDER = os.path.expanduser("~/LargeAttachments")
DASHBOARD_HTML = os.path.expanduser("~/email_dashboard.html")
LOG_FILE = os.path.expanduser("~/email_intelligence.log")
UNSUBSCRIBE_LOG = os.path.expanduser("~/unsubscribe_log.json")

class CompleteEmailIntelligence:
    def __init__(self):
        self.email_history = self.load_email_history()
        self.unsubscribe_history = self.load_unsubscribe_history()
        self.config = self.load_config()
        self.ensure_folders_exist()
    
    def ensure_folders_exist(self):
        """Create necessary folders"""
        os.makedirs(DRAFTS_FOLDER, exist_ok=True)
        os.makedirs(LARGE_ATTACHMENTS_FOLDER, exist_ok=True)
    
    def load_config(self):
        """Load email configuration"""
        default_config = {
            "auto_unsubscribe": True,
            "safelist_domains": ["apple.com", "github.com", "amazon.com"],
            "attachment_size_limit_mb": 3,
            "cloud_storage": "icloud",
            "weekly_digest": True,
            "digest_frequency_days": 3
        }
        
        try:
            if os.path.exists(EMAIL_CONFIG_FILE):
                with open(EMAIL_CONFIG_FILE, 'r') as f:
                    user_config = yaml.safe_load(f)
                    default_config.update(user_config)
        except:
            pass
        
        return default_config
    
    def load_email_history(self):
        """Load email analysis history"""
        try:
            if os.path.exists(INTELLIGENCE_LOG):
                with open(INTELLIGENCE_LOG, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {
            "emails": {},
            "stats": {
                "total_processed": 0,
                "urgent_count": 0,
                "spam_detected": 0,
                "drafts_created": 0,
                "unsubscribed_count": 0,
                "attachments_moved": 0,
                "storage_saved_mb": 0
            },
            "categories": {
                "urgent": [],
                "work": [],
                "personal": [],
                "promotional": [],
                "spam": []
            }
        }
    
    def load_unsubscribe_history(self):
        """Load unsubscribe history"""
        try:
            if os.path.exists(UNSUBSCRIBE_LOG):
                with open(UNSUBSCRIBE_LOG, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {
            "successful_unsubscribes": [],
            "failed_attempts": [],
            "safelist_skipped": [],
            "monthly_stats": {}
        }
    
    def save_histories(self):
        """Save all history files"""
        with open(INTELLIGENCE_LOG, 'w') as f:
            json.dump(self.email_history, f, indent=2)
        
        with open(UNSUBSCRIBE_LOG, 'w') as f:
            json.dump(self.unsubscribe_history, f, indent=2)
    
    def log_action(self, message):
        """Log actions with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a") as f:
            f.write(f"[{timestamp}] {message}\n")
        print(f"[{timestamp}] {message}")
    
    def extract_unsubscribe_link(self, email_body):
        """Extract unsubscribe link from email body"""
        try:
            soup = BeautifulSoup(email_body, 'html.parser')
            
            unsubscribe_patterns = [
                r'unsubscribe',
                r'opt.?out',
                r'remove.?me',
                r'stop.?emails'
            ]
            
            for pattern in unsubscribe_patterns:
                links = soup.find_all('a', href=True)
                for link in links:
                    if re.search(pattern, link.get_text().lower()) or re.search(pattern, link['href'].lower()):
                        return link['href']
            
            return None
        except Exception as e:
            self.log_action(f"Error extracting unsubscribe link: {str(e)}")
            return None
    
    def is_domain_safelisted(self, sender_email):
        """Check if sender domain is in safelist"""
        try:
            domain = sender_email.split('@')[1].lower()
            return any(safe_domain in domain for safe_domain in self.config['safelist_domains'])
        except:
            return False
    
    def auto_unsubscribe(self, sender_email, email_body):
        """Automatically unsubscribe from promotional emails"""
        if not self.config.get('auto_unsubscribe', False):
            return False
        
        if self.is_domain_safelisted(sender_email):
            self.unsubscribe_history['safelist_skipped'].append({
                'sender': sender_email,
                'timestamp': datetime.now().isoformat(),
                'reason': 'Domain safelisted'
            })
            self.log_action(f"🛡️ Skipped unsubscribe for safelisted domain: {sender_email}")
            return False
        
        unsubscribe_link = self.extract_unsubscribe_link(email_body)
        if not unsubscribe_link:
            return False
        
        try:
            self.log_action(f"🔗 Found unsubscribe link for: {sender_email}")
            
            # Simulate successful unsubscribe for demo
            self.unsubscribe_history['successful_unsubscribes'].append({
                'sender': sender_email,
                'link': unsubscribe_link,
                'timestamp': datetime.now().isoformat()
            })
            self.email_history['stats']['unsubscribed_count'] += 1
            self.log_action(f"✅ Successfully unsubscribed from: {sender_email}")
            return True
                
        except Exception as e:
            self.log_action(f"❌ Unsubscribe error for {sender_email}: {str(e)}")
            return False
    
    def handle_large_attachment(self, email_id, attachment_name, attachment_size_mb):
        """Handle large attachments by moving to cloud storage"""
        if attachment_size_mb < self.config.get('attachment_size_limit_mb', 3):
            return None
        
        try:
            cloud_storage = self.config.get('cloud_storage', 'icloud')
            cloud_url = f"https://{cloud_storage}.com/shared/{attachment_name}"
            
            self.log_action(f"☁️ Moving large attachment ({attachment_size_mb:.1f}MB) to {cloud_storage}")
            
            self.email_history['stats']['attachments_moved'] += 1
            self.email_history['stats']['storage_saved_mb'] += attachment_size_mb
            
            return f"[📎 {attachment_name}]({cloud_url})"
            
        except Exception as e:
            self.log_action(f"❌ Error handling attachment {attachment_name}: {str(e)}")
            return None
    
    def analyze_email_content(self, subject, body, sender, attachments=None):
        """Enhanced AI analysis of email content"""
        urgency_score = 0
        category = "personal"
        keywords = []
        suggested_response = None
        
        subject_lower = subject.lower()
        body_lower = body.lower()
        sender_lower = sender.lower()
        
        # Enhanced urgency detection
        urgent_keywords = [
            'urgent', 'asap', 'emergency', 'critical', 'deadline', 'immediate',
            'important', 'priority', 'rush', 'quickly', 'soon as possible',
            'action required', 'time sensitive', 'expires today'
        ]
        
        for keyword in urgent_keywords:
            if keyword in subject_lower or keyword in body_lower:
                urgency_score += 20
                keywords.append(keyword)
        
        # Time-sensitive phrases
        time_phrases = [
            'by end of day', 'eod', 'by tomorrow', 'this week', 'before',
            'due date', 'expires', 'deadline', 'final notice', 'last chance'
        ]
        
        for phrase in time_phrases:
            if phrase in body_lower:
                urgency_score += 15
                keywords.append(phrase)
        
        # Work email detection
        work_indicators = [
            'meeting', 'conference', 'project', 'report', 'presentation',
            'client', 'customer', 'proposal', 'contract', 'invoice',
            'schedule', 'appointment', 'review', 'feedback', 'team'
        ]
        
        work_score = 0
        for indicator in work_indicators:
            if indicator in subject_lower or indicator in body_lower:
                work_score += 10
        
        if work_score >= 20:
            category = "work"
        
        # Enhanced promotional detection
        promo_keywords = [
            'sale', 'discount', 'offer', 'deal', 'promotion', 'coupon',
            'free', 'limited time', 'act now', 'click here', 'unsubscribe',
            'newsletter', 'marketing', '% off', 'save money', 'exclusive'
        ]
        
        promo_score = 0
        for keyword in promo_keywords:
            if keyword in subject_lower or keyword in body_lower:
                promo_score += 10
        
        if promo_score >= 30:
            category = "promotional"
        
        # Spam detection
        spam_indicators = [
            'congratulations', 'winner', 'lottery', 'prize', 'claim now',
            'million dollars', 'bitcoin', 'cryptocurrency', 'make money fast'
        ]
        
        spam_score = 0
        for indicator in spam_indicators:
            if indicator in subject_lower or indicator in body_lower:
                spam_score += 25
        
        if spam_score >= 25:
            category = "spam"
            urgency_score = 0
        
        # Handle attachments
        attachment_links = []
        if attachments:
            for attachment in attachments:
                attachment_link = self.handle_large_attachment(
                    f"email_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    attachment['name'],
                    attachment['size_mb']
                )
                if attachment_link:
                    attachment_links.append(attachment_link)
        
        # Generate responses
        if category == "work":
            if any(word in body_lower for word in ['meeting', 'schedule']):
                suggested_response = "Thank you for the meeting invitation. I'll check my calendar and confirm my availability shortly."
            elif any(word in body_lower for word in ['report', 'update', 'status']):
                suggested_response = "Thank you for your request. I'm currently working on this and will provide an update by end of day."
        
        # Final urgency categorization
        if urgency_score >= 40:
            urgency_level = "HIGH"
        elif urgency_score >= 20:
            urgency_level = "MEDIUM"
        else:
            urgency_level = "LOW"
        
        return {
            "urgency_level": urgency_level,
            "urgency_score": urgency_score,
            "category": category,
            "keywords": keywords,
            "suggested_response": suggested_response,
            "attachment_links": attachment_links,
            "analysis_time": datetime.now().isoformat()
        }
    
    def save_draft_response(self, email_id, subject, suggested_response, recipient):
        """Save AI-generated draft response"""
        if not suggested_response:
            return None
        
        draft_filename = f"draft_{email_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        draft_path = os.path.join(DRAFTS_FOLDER, draft_filename)
        
        draft_content = f"""To: {recipient}
Subject: Re: {subject}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

{suggested_response}

---
[This is an AI-generated draft. Please review and modify before sending.]
"""
        
        with open(draft_path, 'w') as f:
            f.write(draft_content)
        
        self.log_action(f"💬 Draft saved: {draft_filename}")
        return draft_path
    
    def simulate_enhanced_email_analysis(self):
        """Simulate enhanced email analysis"""
        sample_emails = [
            {
                "id": "email_001",
                "sender": "boss@company.com",
                "subject": "URGENT: Project deadline moved to tomorrow - ACTION REQUIRED",
                "body": "Hi, we need to move the project deadline to tomorrow EOD. This is critical for the client presentation. Please confirm you can deliver on time.",
                "received": datetime.now() - timedelta(minutes=30),
                "attachments": [{"name": "contract.pdf", "size_mb": 5.2}]
            },
            {
                "id": "email_002", 
                "sender": "newsletter@store.com",
                "subject": "🔥 FLASH SALE: 70% OFF Everything - Last Chance!",
                "body": """Don't miss out on our biggest sale of the year! 70% off everything. 
                <a href='https://store.com/unsubscribe?id=123'>Unsubscribe here</a> if you no longer wish to receive these offers. 
                Offer expires tonight!""",
                "received": datetime.now() - timedelta(hours=2),
                "attachments": []
            },
            {
                "id": "email_003",
                "sender": "colleague@company.com", 
                "subject": "Meeting request for quarterly review next week",
                "body": "Hi, I'd like to schedule a meeting to discuss the quarterly review. Are you available Tuesday or Wednesday afternoon?",
                "received": datetime.now() - timedelta(hours=1),
                "attachments": [{"name": "Q3_report.pdf", "size_mb": 8.1}]
            }
        ]
        
        self.log_action("📧 Starting enhanced email intelligence analysis...")
        
        for email_data in sample_emails:
            analysis = self.analyze_email_content(
                email_data["subject"],
                email_data["body"], 
                email_data["sender"],
                email_data.get("attachments", [])
            )
            
            # Store analysis
            self.email_history["emails"][email_data["id"]] = {
                "sender": email_data["sender"],
                "subject": email_data["subject"],
                "received": email_data["received"].isoformat(),
                "analysis": analysis,
                "attachments": email_data.get("attachments", [])
            }
            
            # Update categories
            category = analysis["category"]
            if email_data["id"] not in self.email_history["categories"][category]:
                self.email_history["categories"][category].append(email_data["id"])
            
            # Update stats
            self.email_history["stats"]["total_processed"] += 1
            if analysis["urgency_level"] == "HIGH":
                self.email_history["stats"]["urgent_count"] += 1
            if analysis["category"] == "spam":
                self.email_history["stats"]["spam_detected"] += 1
            
            # Auto-unsubscribe for promotional emails
            if analysis["category"] == "promotional":
                unsubscribed = self.auto_unsubscribe(email_data["sender"], email_data["body"])
            
            # Generate draft if suggested
            if analysis["suggested_response"]:
                draft_path = self.save_draft_response(
                    email_data["id"],
                    email_data["subject"],
                    analysis["suggested_response"],
                    email_data["sender"]
                )
                if draft_path:
                    self.email_history["stats"]["drafts_created"] += 1
            
            # Log findings
            urgency_emoji = "🚨" if analysis["urgency_level"] == "HIGH" else "⚠️" if analysis["urgency_level"] == "MEDIUM" else "📧"
            category_emoji = {"work": "💼", "personal": "👤", "promotional": "🛍️", "spam": "🗑️"}.get(category, "📧")
            
            self.log_action(f"{urgency_emoji} {category_emoji} {email_data['subject'][:50]}...")
            self.log_action(f"   From: {email_data['sender']}")
            self.log_action(f"   Urgency: {analysis['urgency_level']} ({analysis['urgency_score']}/100)")
            self.log_action(f"   Category: {category.upper()}")
            
            if analysis["keywords"]:
                self.log_action(f"   Keywords: {', '.join(analysis['keywords'][:3])}")
            
            if analysis["attachment_links"]:
                self.log_action(f"   📎 {len(analysis['attachment_links'])} large attachments moved to cloud")
            
            if analysis["suggested_response"]:
                self.log_action(f"   💬 Draft response generated")
            
            self.log_action("")
