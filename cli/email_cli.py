#!/usr/bin/env python3
"""
Email CLI - Quick command-line actions for email management
"""
import click
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

INTELLIGENCE_LOG = os.path.expanduser("~/email_intelligence.json")
DRAFTS_FOLDER = os.path.expanduser("~/EmailDrafts")

class EmailCLI:
    def __init__(self):
        self.email_history = self.load_email_history()
    
    def load_email_history(self):
        """Load email analysis history"""
        try:
            if os.path.exists(INTELLIGENCE_LOG):
                with open(INTELLIGENCE_LOG, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {"emails": {}, "stats": {}, "categories": {}}

@click.group()
def email():
    """Email Intelligence CLI - Quick actions for email management"""
    pass

@email.command()
@click.option('--urgent', is_flag=True, help='Show only urgent emails')
@click.option('--category', type=click.Choice(['work', 'personal', 'promotional', 'spam']), help='Filter by category')
@click.option('--limit', default=10, help='Number of emails to show')
def ls(urgent, category, limit):
    """List emails with optional filters"""
    cli = EmailCLI()
    emails = cli.email_history.get("emails", {})
    
    if not emails:
        click.echo("📭 No emails found. Run the email intelligence analyzer first.")
        return
    
    # Filter emails
    filtered_emails = []
    for email_id, email_data in emails.items():
        analysis = email_data.get("analysis", {})
        
        # Apply filters
        if urgent and analysis.get("urgency_level") != "HIGH":
            continue
        if category and analysis.get("category") != category:
            continue
        
        filtered_emails.append((email_id, email_data))
    
    # Sort by urgency and date
    filtered_emails.sort(
        key=lambda x: (
            {"HIGH": 3, "MEDIUM": 2, "LOW": 1}.get(x[1]["analysis"]["urgency_level"], 0),
            x[1]["received"]
        ),
        reverse=True
    )
    
    # Display results
    if not filtered_emails:
        click.echo("📭 No emails match your filters.")
        return
    
    click.echo(f"\n📧 Found {len(filtered_emails)} emails:")
    click.echo("=" * 80)
    
    for i, (email_id, email_data) in enumerate(filtered_emails[:limit]):
        analysis = email_data["analysis"]
        
        # Urgency indicator
        urgency_emoji = {"HIGH": "🚨", "MEDIUM": "⚠️", "LOW": "📧"}.get(analysis["urgency_level"], "📧")
        category_emoji = {"work": "💼", "personal": "👤", "promotional": "🛍️", "spam": "🗑️"}.get(analysis["category"], "📧")
        
        click.echo(f"\n{i+1:2d}. {urgency_emoji} {category_emoji} {email_data['subject'][:60]}")
        click.echo(f"    From: {email_data['sender']}")
        click.echo(f"    Date: {email_data['received'][:16]} | Urgency: {analysis['urgency_level']} ({analysis['urgency_score']}/100)")
        
        if analysis.get("keywords"):
            click.echo(f"    Keywords: {', '.join(analysis['keywords'][:3])}")
        
        if analysis.get("suggested_response"):
            click.echo(f"    💬 AI draft available")

@email.command()
@click.argument('email_id')
@click.option('--template', type=click.Choice(['thanks', 'meeting', 'status', 'decline']), help='Use response template')
def reply(email_id, template):
    """Generate or show reply for specific email"""
    cli = EmailCLI()
    emails = cli.email_history.get("emails", {})
    
    if email_id not in emails:
        click.echo(f"❌ Email ID '{email_id}' not found.")
        return
    
    email_data = emails[email_id]
    analysis = email_data["analysis"]
    
    click.echo(f"\n📧 Reply to: {email_data['subject']}")
    click.echo(f"From: {email_data['sender']}")
    click.echo("=" * 60)
    
    # Generate response based on template or existing suggestion
    if template:
        response = generate_template_response(template, email_data)
    elif analysis.get("suggested_response"):
        response = analysis["suggested_response"]
    else:
        response = "Thank you for your email. I'll review this and get back to you shortly."
    
    click.echo(f"\n💬 Suggested Response:\n")
    click.echo(response)
    click.echo("\n" + "=" * 60)
    
    # Save as draft
    if click.confirm("Save this as a draft?"):
        draft_filename = f"cli_draft_{email_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        draft_path = os.path.join(DRAFTS_FOLDER, draft_filename)
        
        os.makedirs(DRAFTS_FOLDER, exist_ok=True)
        
        draft_content = f"""To: {email_data['sender']}
Subject: Re: {email_data['subject']}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (CLI)

---

{response}

---
[This is an AI-generated draft. Please review and modify before sending.]
"""
        
        with open(draft_path, 'w') as f:
            f.write(draft_content)
        
        click.echo(f"✅ Draft saved: {draft_path}")

def generate_template_response(template, email_data):
    """Generate response based on template"""
    templates = {
        'thanks': "Thank you for your email. I appreciate you reaching out and will review this carefully.",
        'meeting': "Thank you for the meeting invitation. I'll check my calendar and confirm my availability shortly.",
        'status': "Thank you for your inquiry. I'm currently working on this and will provide an update by end of day.",
        'decline': "Thank you for your invitation. Unfortunately, I won't be able to participate at this time."
    }
    
    return templates.get(template, templates['thanks'])

@email.command()
@click.argument('email_id')
@click.option('--until', help='Snooze until time (e.g., "9am", "tomorrow", "next week")')
def snooze(email_id, until):
    """Snooze email until specified time"""
    cli = EmailCLI()
    emails = cli.email_history.get("emails", {})
    
    if email_id not in emails:
        click.echo(f"❌ Email ID '{email_id}' not found.")
        return
    
    email_data = emails[email_id]
    
    # Parse snooze time (simplified)
    snooze_time = parse_snooze_time(until)
    
    click.echo(f"⏰ Snoozed: {email_data['subject'][:50]}...")
    click.echo(f"Until: {snooze_time}")
    click.echo("(Note: This is a simulation - actual snoozing would require email client integration)")

def parse_snooze_time(until_str):
    """Parse snooze time string"""
    if not until_str:
        return "1 hour from now"
    
    until_lower = until_str.lower()
    
    if "9am" in until_lower or "morning" in until_lower:
        return "Tomorrow at 9:00 AM"
    elif "tomorrow" in until_lower:
        return "Tomorrow at 9:00 AM"
    elif "next week" in until_lower:
        return "Next Monday at 9:00 AM"
    else:
        return f"Parsed: {until_str}"

@email.command()
def stats():
    """Show email intelligence statistics"""
    cli = EmailCLI()
    stats = cli.email_history.get("stats", {})
    categories = cli.email_history.get("categories", {})
    
    if not stats:
        click.echo("📊 No statistics available. Run the email intelligence analyzer first.")
        return
    
    click.echo("\n📊 Email Intelligence Statistics")
    click.echo("=" * 50)
    
    click.echo(f"📧 Total Processed: {stats.get('total_processed', 0)}")
    click.echo(f"🚨 Urgent Emails: {stats.get('urgent_count', 0)}")
    click.echo(f"🗑️ Spam Detected: {stats.get('spam_detected', 0)}")
    click.echo(f"💬 Drafts Created: {stats.get('drafts_created', 0)}")
    click.echo(f"🚫 Unsubscribed: {stats.get('unsubscribed_count', 0)}")
    click.echo(f"📎 Attachments Moved: {stats.get('attachments_moved', 0)}")
    click.echo(f"💾 Storage Saved: {stats.get('storage_saved_mb', 0):.1f} MB")
    
    click.echo("\n📂 Category Breakdown:")
    for category, email_ids in categories.items():
        if email_ids:
            emoji = {"work": "💼", "personal": "👤", "promotional": "🛍️", "spam": "🗑️"}.get(category, "📧")
            click.echo(f"  {emoji} {category.title()}: {len(email_ids)} emails")

@email.command()
def dashboard():
    """Open email dashboard in browser"""
    dashboard_path = os.path.expanduser("~/email_dashboard.html")
    
    if os.path.exists(dashboard_path):
        os.system(f"open {dashboard_path}")
        click.echo("🌐 Opening email dashboard in browser...")
    else:
        click.echo("❌ Dashboard not found. Run the email intelligence analyzer first.")

@email.command()
def drafts():
    """List available email drafts"""
    if not os.path.exists(DRAFTS_FOLDER):
        click.echo("📭 No drafts folder found.")
        return
    
    draft_files = list(Path(DRAFTS_FOLDER).glob("*.txt"))
    
    if not draft_files:
        click.echo("📭 No drafts available.")
        return
    
    click.echo(f"\n💬 Found {len(draft_files)} drafts:")
    click.echo("=" * 60)
    
    for i, draft_file in enumerate(sorted(draft_files, key=lambda x: x.stat().st_mtime, reverse=True)):
        # Read first few lines to get subject
        try:
            with open(draft_file, 'r') as f:
                lines = f.readlines()
                subject_line = next((line for line in lines if line.startswith("Subject:")), "Subject: Unknown")
                subject = subject_line.replace("Subject: Re: ", "").strip()
        except:
            subject = "Unknown"
        
        modified_time = datetime.fromtimestamp(draft_file.stat().st_mtime)
        click.echo(f"{i+1:2d}. {subject[:50]}")
        click.echo(f"    File: {draft_file.name}")
        click.echo(f"    Modified: {modified_time.strftime('%Y-%m-%d %H:%M:%S')}")

@email.command()
@click.argument('draft_name')
def show_draft(draft_name):
    """Show content of specific draft"""
    draft_path = os.path.join(DRAFTS_FOLDER, draft_name)
    
    if not os.path.exists(draft_path):
        # Try to find partial match
        draft_files = list(Path(DRAFTS_FOLDER).glob(f"*{draft_name}*"))
        if draft_files:
            draft_path = str(draft_files[0])
        else:
            click.echo(f"❌ Draft '{draft_name}' not found.")
            return
    
    try:
        with open(draft_path, 'r') as f:
            content = f.read()
        
        click.echo(f"\n💬 Draft Content:")
        click.echo("=" * 60)
        click.echo(content)
        click.echo("=" * 60)
        
    except Exception as e:
        click.echo(f"❌ Error reading draft: {str(e)}")

if __name__ == '__main__':
    email()
