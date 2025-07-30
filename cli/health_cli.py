#!/usr/bin/env python3
"""
Health CLI - Quick command-line actions for health data
"""
import click
import json
import os
from datetime import datetime

HEALTH_DATA_LOG = os.path.expanduser("~/health_intelligence.json")
INSIGHTS_FOLDER = os.path.expanduser("~/HealthInsights")

class HealthCLI:
    def __init__(self):
        self.health_history = self.load_health_history()
    
    def load_health_history(self):
        """Load health analysis history"""
        try:
            if os.path.exists(HEALTH_DATA_LOG):
                with open(HEALTH_DATA_LOG, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {"daily_metrics": {}, "insights": [], "alerts": [], "stats": {}}

@click.group()
def health():
    """Health Intelligence CLI - Quick actions for health data"""
    pass

@health.command()
def score():
    """Show current health score"""
    cli = HealthCLI()
    stats = cli.health_history.get("stats", {})
    
    if not stats:
        click.echo("📊 No health data available. Run the health intelligence analyzer first.")
        return
    
    health_score = stats.get("health_score", 0)
    
    # Determine grade
    if health_score >= 90:
        grade = "A+"
        emoji = "🏆"
    elif health_score >= 85:
        grade = "A"
        emoji = "🥇"
    elif health_score >= 80:
        grade = "A-"
        emoji = "✨"
    elif health_score >= 75:
        grade = "B+"
        emoji = "👍"
    elif health_score >= 70:
        grade = "B"
        emoji = "👌"
    else:
        grade = "C"
        emoji = "⚠️"
    
    click.echo(f"\n{emoji} Your Health Score")
    click.echo("=" * 30)
    click.echo(f"Score: {health_score}/100")
    click.echo(f"Grade: {grade}")
    click.echo(f"Days Tracked: {stats.get('total_days_tracked', 0)}")
    click.echo(f"Insights Generated: {stats.get('insights_generated', 0)}")

@health.command()
@click.option('--priority', type=click.Choice(['high', 'medium', 'positive']), help='Filter by priority')
@click.option('--type', type=click.Choice(['activity', 'sleep', 'heart_rate', 'exercise', 'wellness']), help='Filter by type')
@click.option('--limit', default=5, help='Number of insights to show')
def insights(priority, type, limit):
    """Show health insights"""
    cli = HealthCLI()
    all_insights = cli.health_history.get("insights", [])
    
    if not all_insights:
        click.echo("💡 No insights available. Run the health intelligence analyzer first.")
        return
    
    # Filter insights
    filtered_insights = all_insights
    if priority:
        filtered_insights = [i for i in filtered_insights if i.get("priority") == priority]
    if type:
        filtered_insights = [i for i in filtered_insights if i.get("type") == type]
    
    # Sort by timestamp (most recent first)
    filtered_insights.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    
    if not filtered_insights:
        click.echo("💡 No insights match your filters.")
        return
    
    click.echo(f"\n💡 Health Insights ({len(filtered_insights)} found)")
    click.echo("=" * 60)
    
    for i, insight in enumerate(filtered_insights[:limit]):
        priority_emoji = {"high": "🚨", "medium": "⚠️", "positive": "✅"}.get(insight.get("priority"), "💡")
        type_emoji = {
            "activity": "🏃‍♂️", "sleep": "😴", "heart_rate": "❤️", 
            "exercise": "💪", "wellness": "🧘‍♂️"
        }.get(insight.get("type"), "📊")
        
        click.echo(f"\n{i+1}. {priority_emoji} {type_emoji} {insight.get('title', 'Unknown')}")
        click.echo(f"   {insight.get('message', 'No message')}")
        if insight.get('recommendation'):
            click.echo(f"   💡 {insight['recommendation']}")
        
        timestamp = insight.get('timestamp', '')
        if timestamp:
            click.echo(f"   📅 {timestamp[:16]}")

@health.command()
def alerts():
    """Show health alerts"""
    cli = HealthCLI()
    all_alerts = cli.health_history.get("alerts", [])
    
    if not all_alerts:
        click.echo("🎉 No health alerts! You're doing great!")
        return
    
    # Sort by priority and timestamp
    high_priority = [a for a in all_alerts if a.get("priority") == "high"]
    medium_priority = [a for a in all_alerts if a.get("priority") == "medium"]
    
    click.echo(f"\n🚨 Health Alerts ({len(all_alerts)} total)")
    click.echo("=" * 50)
    
    if high_priority:
        click.echo("\n🚨 HIGH PRIORITY:")
        for alert in high_priority:
            click.echo(f"   • {alert.get('title', 'Unknown')}")
            click.echo(f"     {alert.get('message', 'No message')}")
            if alert.get('recommendation'):
                click.echo(f"     💡 {alert['recommendation']}")
    
    if medium_priority:
        click.echo("\n⚠️ MEDIUM PRIORITY:")
        for alert in medium_priority:
            click.echo(f"   • {alert.get('title', 'Unknown')}")
            click.echo(f"     {alert.get('message', 'No message')}")

@health.command()
def dashboard():
    """Open health dashboard in browser"""
    dashboard_path = os.path.expanduser("~/health_dashboard.html")
    
    if os.path.exists(dashboard_path):
        os.system(f"open {dashboard_path}")
        click.echo("🌐 Opening health dashboard in browser...")
    else:
        click.echo("❌ Dashboard not found. Run the health intelligence analyzer first.")

@health.command()
def reports():
    """List available health reports"""
    if not os.path.exists(INSIGHTS_FOLDER):
        click.echo("📭 No reports folder found.")
        return
    
    import glob
    report_files = glob.glob(os.path.join(INSIGHTS_FOLDER, "health_insights_*.json"))
    
    if not report_files:
        click.echo("📭 No health reports available.")
        return
    
    click.echo(f"\n📊 Found {len(report_files)} health reports:")
    click.echo("=" * 60)
    
    # Sort by modification time (newest first)
    report_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    
    for i, report_file in enumerate(report_files[:10]):  # Show last 10
        filename = os.path.basename(report_file)
        modified_time = datetime.fromtimestamp(os.path.getmtime(report_file))
        
        # Try to read basic info from report
        try:
            with open(report_file, 'r') as f:
                report_data = json.load(f)
                health_score = report_data.get('health_score', {}).get('total_score', 'N/A')
                insights_count = len(report_data.get('insights', []))
                alerts_count = len(report_data.get('alerts', []))
        except:
            health_score = 'N/A'
            insights_count = 0
            alerts_count = 0
        
        click.echo(f"{i+1:2d}. {filename}")
        click.echo(f"    📅 {modified_time.strftime('%Y-%m-%d %H:%M:%S')}")
        click.echo(f"    🎯 Score: {health_score}/100 | 💡 {insights_count} insights | 🚨 {alerts_count} alerts")

@health.command()
@click.argument('report_name')
def show_report(report_name):
    """Show content of specific health report"""
    # Try to find the report file
    report_path = os.path.join(INSIGHTS_FOLDER, report_name)
    if not os.path.exists(report_path):
        # Try partial match
        import glob
        matches = glob.glob(os.path.join(INSIGHTS_FOLDER, f"*{report_name}*"))
        if matches:
            report_path = matches[0]
        else:
            click.echo(f"❌ Report '{report_name}' not found.")
            return
    
    try:
        with open(report_path, 'r') as f:
            report_data = json.load(f)
        
        click.echo(f"\n📊 Health Report: {os.path.basename(report_path)}")
        click.echo("=" * 80)
        
        # Health score
        health_score = report_data.get('health_score', {})
        click.echo(f"🎯 Health Score: {health_score.get('total_score', 'N/A')}/100 (Grade: {health_score.get('grade', 'N/A')})")
        
        # Components
        components = health_score.get('components', {})
        if components:
            click.echo("\n📈 Score Components:")
            for component, score in components.items():
                click.echo(f"   {component.title()}: {score}/25" if component in ['activity', 'sleep'] else f"   {component.title()}: {score}")
        
        # Summary
        summary = report_data.get('summary', {})
        if summary:
            click.echo(f"\n📋 Summary:")
            click.echo(f"   Total Insights: {summary.get('total_insights', 0)}")
            click.echo(f"   High Priority Alerts: {summary.get('high_priority_alerts', 0)}")
            click.echo(f"   Focus Areas: {', '.join(summary.get('key_focus_areas', []))}")
        
        # Recent insights
        insights = report_data.get('insights', [])[:3]
        if insights:
            click.echo(f"\n💡 Key Insights:")
            for insight in insights:
                priority_emoji = {"high": "🚨", "medium": "⚠️", "positive": "✅"}.get(insight.get("priority"), "💡")
                click.echo(f"   {priority_emoji} {insight.get('title', 'Unknown')}")
                click.echo(f"      {insight.get('message', 'No message')}")
        
    except Exception as e:
        click.echo(f"❌ Error reading report: {str(e)}")

@health.command()
def goals():
    """Show health goals and progress"""
    cli = HealthCLI()
    goals = cli.health_history.get("goals", {})
    
    if not goals:
        click.echo("🎯 No health goals set.")
        return
    
    click.echo("\n🎯 Your Health Goals")
    click.echo("=" * 30)
    click.echo(f"📱 Daily Steps: {goals.get('steps', 10000):,}")
    click.echo(f"😴 Sleep Hours: {goals.get('sleep_hours', 8)}")
    click.echo(f"🏃‍♂️ Active Minutes: {goals.get('active_minutes', 30)}")
    
    hr_zones = goals.get('heart_rate_zones', {})
    if hr_zones:
        click.echo(f"❤️ Resting HR Goal: <{hr_zones.get('resting', 60)} bpm")

if __name__ == '__main__':
    health()
