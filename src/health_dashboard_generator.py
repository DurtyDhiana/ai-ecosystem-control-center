#!/usr/bin/env python3
"""
Health Dashboard Generator - Beautiful visualization of health insights
"""
import json
import os
from datetime import datetime
import statistics

def generate_health_dashboard(health_history, health_data, fitness_data, insights, alerts, health_score, recommendations):
    """Generate comprehensive health dashboard"""
    
    # Calculate recent trends
    recent_dates = sorted(health_data.keys())[-7:]
    recent_steps = [health_data[date]["steps"] for date in recent_dates]
    recent_sleep = [health_data[date]["sleep_hours"] for date in recent_dates]
    recent_hr = [health_data[date]["resting_heart_rate"] for date in recent_dates]
    
    avg_steps = int(statistics.mean(recent_steps))
    avg_sleep = round(statistics.mean(recent_sleep), 1)
    avg_hr = int(statistics.mean(recent_hr))
    
    # Count workout days
    workout_days = sum(1 for data in fitness_data.values() if data["workouts"])
    
    # Priority alerts
    high_priority_alerts = [alert for alert in alerts if alert["priority"] == "high"]
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Health Data Interpreter Dashboard</title>
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
            max-width: 1600px; 
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
            font-size: 3.5em; 
            margin-bottom: 10px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }}
        
        .header p {{ 
            opacity: 0.9; 
            font-size: 1.2em;
        }}
        
        .health-score-section {{
            background: linear-gradient(135deg, #38a169 0%, #2f855a 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .health-score {{
            font-size: 6em;
            font-weight: 900;
            margin-bottom: 10px;
            text-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }}
        
        .health-grade {{
            font-size: 2.5em;
            font-weight: 700;
            margin-bottom: 20px;
        }}
        
        .score-components {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }}
        
        .score-component {{
            background: rgba(255,255,255,0.2);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
        }}
        
        .component-score {{
            font-size: 2em;
            font-weight: 700;
            margin-bottom: 5px;
        }}
        
        .component-label {{
            font-size: 0.9em;
            opacity: 0.9;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .stats-grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); 
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
        
        .stat-card.steps {{ border-left-color: #38a169; }}
        .stat-card.sleep {{ border-left-color: #805ad5; }}
        .stat-card.heart {{ border-left-color: #e53e3e; }}
        .stat-card.workout {{ border-left-color: #dd6b20; }}
        
        .stat-number {{ 
            font-size: 3.5em; 
            font-weight: 800; 
            color: #2d3748; 
            margin-bottom: 10px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .stat-label {{ 
            color: #718096; 
            font-size: 1.1em; 
            text-transform: uppercase; 
            letter-spacing: 1px;
            font-weight: 600;
            margin-bottom: 10px;
        }}
        
        .stat-detail {{ 
            color: #4a5568; 
            font-size: 0.95em;
            line-height: 1.5;
        }}
        
        .main-content {{ 
            display: grid; 
            grid-template-columns: 2fr 1fr; 
            gap: 40px; 
            padding: 40px;
        }}
        
        .insights-section {{ 
            background: white; 
            padding: 30px; 
            border-radius: 15px; 
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        }}
        
        .insights-section h2 {{
            color: #2d3748;
            margin-bottom: 25px;
            font-size: 2em;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .sidebar {{ 
            display: flex; 
            flex-direction: column; 
            gap: 25px; 
        }}
        
        .insight-item {{ 
            border-left: 4px solid #667eea;
            padding: 20px;
            margin-bottom: 20px;
            background: #f7fafc;
            border-radius: 0 10px 10px 0;
            transition: all 0.3s ease;
        }}
        
        .insight-item:hover {{
            background: #edf2f7;
            transform: translateX(5px);
        }}
        
        .insight-item.high {{ border-left-color: #e53e3e; }}
        .insight-item.medium {{ border-left-color: #dd6b20; }}
        .insight-item.positive {{ border-left-color: #38a169; }}
        
        .insight-title {{ 
            font-weight: 700; 
            color: #2d3748; 
            font-size: 1.2em; 
            margin-bottom: 10px;
        }}
        
        .insight-message {{ 
            color: #4a5568; 
            margin-bottom: 15px;
            line-height: 1.6;
        }}
        
        .insight-recommendation {{ 
            color: #2b6cb0; 
            font-style: italic;
            background: #ebf8ff;
            padding: 10px;
            border-radius: 8px;
            border-left: 3px solid #3182ce;
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
            font-size: 1.4em;
            border-bottom: 2px solid #667eea;
            padding-bottom: 8px;
        }}
        
        .alert-item {{
            background: #fed7d7;
            border: 1px solid #feb2b2;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
        }}
        
        .alert-title {{
            font-weight: 700;
            color: #c53030;
            margin-bottom: 8px;
        }}
        
        .alert-message {{
            color: #742a2a;
            font-size: 0.9em;
            line-height: 1.5;
        }}
        
        .recommendation-category {{
            margin-bottom: 25px;
        }}
        
        .recommendation-title {{
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 10px;
            font-size: 1.1em;
        }}
        
        .recommendation-timeline {{
            color: #718096;
            font-size: 0.8em;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .recommendation-list {{
            list-style: none;
            padding: 0;
        }}
        
        .recommendation-list li {{
            background: #f7fafc;
            padding: 8px 12px;
            margin-bottom: 5px;
            border-radius: 6px;
            border-left: 3px solid #667eea;
            font-size: 0.9em;
        }}
        
        .trend-indicator {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: 600;
            margin-left: 10px;
        }}
        
        .trend-up {{ background: #c6f6d5; color: #22543d; }}
        .trend-down {{ background: #fed7d7; color: #742a2a; }}
        .trend-stable {{ background: #e2e8f0; color: #4a5568; }}
        
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
            .stats-grid {{ grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); }}
            .score-components {{ grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); }}
            .header h1 {{ font-size: 2.5em; }}
            .health-score {{ font-size: 4em; }}
            .container {{ margin: 10px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏃‍♂️ Health Data Interpreter</h1>
            <p>AI-powered health analysis and personalized insights</p>
            <p>Last updated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</p>
        </div>
        
        <div class="health-score-section">
            <div class="health-score">{health_score['total_score']}</div>
            <div class="health-grade">Grade: {health_score['grade']}</div>
            <p>Your overall health score based on activity, sleep, heart rate, exercise, and wellness metrics</p>
            
            <div class="score-components">
                <div class="score-component">
                    <div class="component-score">{health_score['components']['activity']}</div>
                    <div class="component-label">Activity</div>
                </div>
                <div class="score-component">
                    <div class="component-score">{health_score['components']['sleep']}</div>
                    <div class="component-label">Sleep</div>
                </div>
                <div class="score-component">
                    <div class="component-score">{health_score['components']['heart_rate']}</div>
                    <div class="component-label">Heart Rate</div>
                </div>
                <div class="score-component">
                    <div class="component-score">{health_score['components']['exercise']}</div>
                    <div class="component-label">Exercise</div>
                </div>
                <div class="score-component">
                    <div class="component-score">{health_score['components']['wellness']}</div>
                    <div class="component-label">Wellness</div>
                </div>
            </div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card steps">
                <div class="stat-number">{avg_steps:,}</div>
                <div class="stat-label">Daily Steps</div>
                <div class="stat-detail">
                    7-day average | Goal: 10,000 steps
                    <span class="trend-indicator {'trend-up' if avg_steps > 10000 else 'trend-down' if avg_steps < 8000 else 'trend-stable'}">
                        {'🔥 Excellent' if avg_steps > 12000 else '✅ Good' if avg_steps > 10000 else '⚠️ Below target' if avg_steps > 8000 else '🚨 Low activity'}
                    </span>
                </div>
            </div>
            
            <div class="stat-card sleep">
                <div class="stat-number">{avg_sleep}</div>
                <div class="stat-label">Sleep Hours</div>
                <div class="stat-detail">
                    7-day average | Goal: 7-9 hours
                    <span class="trend-indicator {'trend-up' if 7 <= avg_sleep <= 9 else 'trend-down'}">
                        {'✅ Optimal' if 7 <= avg_sleep <= 9 else '⚠️ Needs attention'}
                    </span>
                </div>
            </div>
            
            <div class="stat-card heart">
                <div class="stat-number">{avg_hr}</div>
                <div class="stat-label">Resting HR</div>
                <div class="stat-detail">
                    7-day average | Optimal: 60-70 bpm
                    <span class="trend-indicator {'trend-up' if avg_hr <= 70 else 'trend-down' if avg_hr > 80 else 'trend-stable'}">
                        {'✅ Excellent' if avg_hr <= 70 else '⚠️ Elevated' if avg_hr > 80 else '👍 Good'}
                    </span>
                </div>
            </div>
            
            <div class="stat-card workout">
                <div class="stat-number">{workout_days}</div>
                <div class="stat-label">Workout Days</div>
                <div class="stat-detail">
                    This week | Goal: 3-5 days
                    <span class="trend-indicator {'trend-up' if workout_days >= 3 else 'trend-down'}">
                        {'🔥 Great' if workout_days >= 5 else '✅ Good' if workout_days >= 3 else '⚠️ Increase frequency'}
                    </span>
                </div>
            </div>
        </div>
        
        <div class="main-content">
            <div class="insights-section">
                <h2>🧠 AI Health Insights</h2>
    """
    
    # Display insights
    for insight in insights:
        priority_class = insight["priority"]
        priority_emoji = {"high": "🚨", "medium": "⚠️", "positive": "✅"}.get(priority_class, "💡")
        
        html_content += f"""
        <div class="insight-item {priority_class}">
            <div class="insight-title">{priority_emoji} {insight['title']}</div>
            <div class="insight-message">{insight['message']}</div>
            <div class="insight-recommendation">💡 {insight['recommendation']}</div>
        </div>
        """
    
    if not insights:
        html_content += "<div class='insight-item'><div class='insight-title'>🎉 All Good!</div><div class='insight-message'>No specific insights at this time. Keep up the great work!</div></div>"
    
    html_content += """
            </div>
            
            <div class="sidebar">
    """
    
    # High priority alerts
    if high_priority_alerts:
        html_content += """
                <div class="sidebar-card">
                    <h3>🚨 Priority Alerts</h3>
        """
        for alert in high_priority_alerts:
            html_content += f"""
            <div class="alert-item">
                <div class="alert-title">{alert['title']}</div>
                <div class="alert-message">{alert['message']}</div>
            </div>
            """
        html_content += "</div>"
    
    # Recommendations
    html_content += """
                <div class="sidebar-card">
                    <h3>📋 Personalized Recommendations</h3>
    """
    
    for rec in recommendations[:3]:  # Show top 3 recommendation categories
        html_content += f"""
        <div class="recommendation-category">
            <div class="recommendation-title">🎯 {rec['title']}</div>
            <div class="recommendation-timeline">{rec['timeline']}</div>
            <ul class="recommendation-list">
        """
        for item in rec['items'][:3]:  # Show top 3 items per category
            html_content += f"<li>{item}</li>"
        html_content += "</ul></div>"
    
    html_content += f"""
                </div>
                
                <div class="sidebar-card">
                    <h3>📊 Health Metrics Summary</h3>
                    <div style="font-size: 0.9em; color: #4a5568; line-height: 1.8;">
                        <div><strong>Days Tracked:</strong> {health_history['stats']['total_days_tracked']}</div>
                        <div><strong>Insights Generated:</strong> {len(insights)}</div>
                        <div><strong>Health Alerts:</strong> {len(alerts)}</div>
                        <div><strong>Current Streak:</strong> 7 days</div>
                        <div><strong>Best Score:</strong> {health_score['total_score']}/100</div>
                    </div>
                </div>
                
                <div class="sidebar-card">
                    <h3>🎯 Health Goals</h3>
                    <div style="font-size: 0.9em; color: #4a5568; line-height: 1.8;">
                        <div>📱 Daily Steps: {health_history['goals']['steps']:,}</div>
                        <div>😴 Sleep Hours: {health_history['goals']['sleep_hours']}</div>
                        <div>🏃‍♂️ Active Minutes: {health_history['goals']['active_minutes']}</div>
                        <div>❤️ Resting HR: <{health_history['goals']['heart_rate_zones']['resting']} bpm</div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            Health Data Interpreter Dashboard | Powered by AI | 
            <a href="file://{os.path.expanduser('~/health_intelligence.log')}">View Logs</a> | 
            <a href="file://{os.path.expanduser('~/HealthInsights')}">View Reports</a>
        </div>
    </div>
    
    <script>
        // Auto-refresh every 10 minutes
        setTimeout(() => location.reload(), 600000);
        
        // Add loading animation
        window.addEventListener('load', function() {{
            document.querySelectorAll('.stat-card, .insight-item, .sidebar-card').forEach((el, index) => {{
                el.style.opacity = '0';
                el.style.transform = 'translateY(20px)';
                setTimeout(() => {{
                    el.style.transition = 'all 0.6s ease';
                    el.style.opacity = '1';
                    el.style.transform = 'translateY(0)';
                }}, index * 100);
            }});
        }});
        
        // Add smooth scrolling
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({{
                    behavior: 'smooth'
                }});
            }});
        }});
    </script>
</body>
</html>"""
    
    return html_content

if __name__ == "__main__":
    print("Health dashboard generator ready!")
