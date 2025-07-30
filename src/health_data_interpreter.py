#!/usr/bin/env python3
"""
Health Data Interpreter - AI-powered health analysis and personalized insights
"""
import os
import json
import sqlite3
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import statistics
import re

# Configuration
HEALTH_DATA_LOG = os.path.expanduser("~/health_intelligence.json")
HEALTH_DASHBOARD_HTML = os.path.expanduser("~/health_dashboard.html")
HEALTH_LOG_FILE = os.path.expanduser("~/health_intelligence.log")
INSIGHTS_FOLDER = os.path.expanduser("~/HealthInsights")
HEALTH_EXPORT_PATH = os.path.expanduser("~/Desktop/export.xml")  # Apple Health export location

class HealthDataInterpreter:
    def __init__(self):
        self.health_history = self.load_health_history()
        self.ensure_folders_exist()
    
    def ensure_folders_exist(self):
        """Create necessary folders"""
        os.makedirs(INSIGHTS_FOLDER, exist_ok=True)
    
    def load_health_history(self):
        """Load health analysis history"""
        try:
            if os.path.exists(HEALTH_DATA_LOG):
                with open(HEALTH_DATA_LOG, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {
            "daily_metrics": {},
            "weekly_trends": {},
            "insights": [],
            "alerts": [],
            "goals": {
                "steps": 10000,
                "sleep_hours": 8,
                "active_minutes": 30,
                "heart_rate_zones": {"resting": 60, "max": 180}
            },
            "stats": {
                "total_days_tracked": 0,
                "insights_generated": 0,
                "goals_achieved": 0,
                "health_score": 0
            }
        }
    
    def save_health_history(self):
        """Save health analysis to file"""
        with open(HEALTH_DATA_LOG, 'w') as f:
            json.dump(self.health_history, f, indent=2)
    
    def log_action(self, message):
        """Log actions with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(HEALTH_LOG_FILE, "a") as f:
            f.write(f"[{timestamp}] {message}\n")
        print(f"[{timestamp}] {message}")
    
    def get_apple_health_data(self):
        """Extract data from Apple Health (simulated for demo)"""
        # In a real implementation, this would parse the Apple Health export XML
        # For now, we'll simulate realistic health data
        
        current_date = datetime.now()
        simulated_data = {}
        
        # Generate 30 days of simulated health data
        for i in range(30):
            date = (current_date - timedelta(days=i)).strftime("%Y-%m-%d")
            
            # Simulate realistic patterns
            day_of_week = (current_date - timedelta(days=i)).weekday()
            is_weekend = day_of_week >= 5
            
            # Steps (lower on weekends, higher on weekdays)
            base_steps = 8000 if is_weekend else 12000
            steps = base_steps + (i * 100) + ((-1) ** i * 1500)  # Add some variation
            
            # Sleep (slightly less on weekends due to later nights)
            base_sleep = 7.5 if is_weekend else 7.8
            sleep_hours = base_sleep + ((-1) ** i * 0.5)
            
            # Heart rate (varies with activity and stress)
            resting_hr = 65 + (i % 10)  # Slight variation
            max_hr = 150 + (i % 20)
            
            # Active minutes (lower on weekends)
            base_active = 25 if is_weekend else 45
            active_minutes = base_active + (i % 15)
            
            # Weight (slight fluctuation)
            weight = 70 + (i * 0.1) + ((-1) ** i * 0.3)
            
            simulated_data[date] = {
                "steps": max(0, int(steps)),
                "sleep_hours": max(4, min(12, sleep_hours)),
                "resting_heart_rate": max(50, min(100, int(resting_hr))),
                "max_heart_rate": max(120, min(200, int(max_hr))),
                "active_minutes": max(0, int(active_minutes)),
                "weight_kg": round(weight, 1),
                "calories_burned": int(steps * 0.04 + active_minutes * 8),
                "day_of_week": day_of_week,
                "is_weekend": is_weekend
            }
        
        return simulated_data
    
    def get_fitness_app_data(self):
        """Get data from fitness tracking apps (simulated)"""
        # This would integrate with apps like Strava, MyFitnessPal, etc.
        # For now, we'll simulate some additional metrics
        
        current_date = datetime.now()
        fitness_data = {}
        
        for i in range(7):  # Last 7 days
            date = (current_date - timedelta(days=i)).strftime("%Y-%m-%d")
            
            fitness_data[date] = {
                "workouts": [
                    {
                        "type": "Running" if i % 3 == 0 else "Walking" if i % 2 == 0 else "Cycling",
                        "duration_minutes": 30 + (i * 5),
                        "calories": 200 + (i * 25),
                        "intensity": "Moderate" if i % 2 == 0 else "High"
                    }
                ] if i < 5 else [],  # No workouts on some days
                "water_intake_liters": 2.0 + (i * 0.2),
                "mood_score": 7 + (i % 3),  # 1-10 scale
                "stress_level": 3 + (i % 4),  # 1-10 scale
                "energy_level": 8 - (i % 3)  # 1-10 scale
            }
        
        return fitness_data
    
    def analyze_health_patterns(self, health_data, fitness_data):
        """AI analysis of health patterns and trends"""
        insights = []
        alerts = []
        
        # Analyze step patterns
        recent_steps = [health_data[date]["steps"] for date in sorted(health_data.keys())[-7:]]
        avg_steps = statistics.mean(recent_steps)
        step_trend = "increasing" if recent_steps[-1] > recent_steps[0] else "decreasing"
        
        if avg_steps < 8000:
            insights.append({
                "type": "activity",
                "priority": "medium",
                "title": "Low Daily Activity Detected",
                "message": f"Your average daily steps ({int(avg_steps):,}) are below the recommended 10,000. Consider taking short walks throughout the day.",
                "recommendation": "Set hourly reminders to take a 5-minute walk. Park further away or take stairs when possible.",
                "timestamp": datetime.now().isoformat()
            })
        elif avg_steps > 12000:
            insights.append({
                "type": "activity",
                "priority": "positive",
                "title": "Excellent Activity Level!",
                "message": f"Great job! You're averaging {int(avg_steps):,} steps daily, well above the recommended target.",
                "recommendation": "Keep up the excellent work! Consider setting a new challenge like increasing intensity or trying new activities.",
                "timestamp": datetime.now().isoformat()
            })
        
        # Analyze sleep patterns
        recent_sleep = [health_data[date]["sleep_hours"] for date in sorted(health_data.keys())[-7:]]
        avg_sleep = statistics.mean(recent_sleep)
        sleep_consistency = statistics.stdev(recent_sleep)
        
        if avg_sleep < 7:
            alerts.append({
                "type": "sleep",
                "priority": "high",
                "title": "Insufficient Sleep Detected",
                "message": f"You're averaging only {avg_sleep:.1f} hours of sleep. This can impact your health, mood, and performance.",
                "recommendation": "Aim for 7-9 hours nightly. Try setting a consistent bedtime and avoiding screens 1 hour before sleep.",
                "timestamp": datetime.now().isoformat()
            })
        
        if sleep_consistency > 1.5:
            insights.append({
                "type": "sleep",
                "priority": "medium",
                "title": "Inconsistent Sleep Schedule",
                "message": f"Your sleep duration varies significantly (±{sleep_consistency:.1f} hours). Consistency is key for quality rest.",
                "recommendation": "Try to go to bed and wake up at the same time daily, even on weekends.",
                "timestamp": datetime.now().isoformat()
            })
        
        # Analyze heart rate patterns
        recent_resting_hr = [health_data[date]["resting_heart_rate"] for date in sorted(health_data.keys())[-7:]]
        avg_resting_hr = statistics.mean(recent_resting_hr)
        hr_trend = recent_resting_hr[-1] - recent_resting_hr[0]
        
        if avg_resting_hr > 80:
            alerts.append({
                "type": "heart_rate",
                "priority": "medium",
                "title": "Elevated Resting Heart Rate",
                "message": f"Your resting heart rate ({int(avg_resting_hr)} bpm) is higher than optimal (60-70 bpm).",
                "recommendation": "Consider stress management techniques, regular cardio exercise, and adequate hydration. Consult a healthcare provider if persistent.",
                "timestamp": datetime.now().isoformat()
            })
        
        if hr_trend < -5:
            insights.append({
                "type": "heart_rate",
                "priority": "positive",
                "title": "Improving Cardiovascular Fitness",
                "message": f"Your resting heart rate has decreased by {abs(int(hr_trend))} bpm this week - a sign of improving fitness!",
                "recommendation": "Keep up your current exercise routine. This indicates your cardiovascular health is improving.",
                "timestamp": datetime.now().isoformat()
            })
        
        # Analyze weekend vs weekday patterns
        weekday_steps = []
        weekend_steps = []
        
        for date, data in health_data.items():
            if data["is_weekend"]:
                weekend_steps.append(data["steps"])
            else:
                weekday_steps.append(data["steps"])
        
        if weekday_steps and weekend_steps:
            weekday_avg = statistics.mean(weekday_steps)
            weekend_avg = statistics.mean(weekend_steps)
            
            if weekend_avg < weekday_avg * 0.7:
                insights.append({
                    "type": "lifestyle",
                    "priority": "medium",
                    "title": "Weekend Activity Drop",
                    "message": f"Your weekend activity ({int(weekend_avg):,} steps) is significantly lower than weekdays ({int(weekday_avg):,} steps).",
                    "recommendation": "Plan active weekend activities like hiking, sports, or exploring new neighborhoods to maintain consistency.",
                    "timestamp": datetime.now().isoformat()
                })
        
        # Analyze workout consistency from fitness data
        workout_days = 0
        total_workout_time = 0
        
        for date, data in fitness_data.items():
            if data["workouts"]:
                workout_days += 1
                total_workout_time += sum(w["duration_minutes"] for w in data["workouts"])
        
        if workout_days < 3:
            insights.append({
                "type": "exercise",
                "priority": "medium",
                "title": "Low Workout Frequency",
                "message": f"You've only had {workout_days} workout days this week. Regular exercise is crucial for health.",
                "recommendation": "Aim for at least 3-4 workout sessions per week. Start with 20-30 minute sessions and gradually increase.",
                "timestamp": datetime.now().isoformat()
            })
        
        # Analyze mood and energy correlation
        mood_scores = [fitness_data[date]["mood_score"] for date in fitness_data.keys()]
        energy_scores = [fitness_data[date]["energy_level"] for date in fitness_data.keys()]
        
        if statistics.mean(mood_scores) < 6:
            insights.append({
                "type": "wellness",
                "priority": "medium",
                "title": "Low Mood Patterns Detected",
                "message": f"Your average mood score ({statistics.mean(mood_scores):.1f}/10) suggests you might be feeling down lately.",
                "recommendation": "Consider activities that boost mood: exercise, sunlight exposure, social connections, or speaking with a healthcare provider.",
                "timestamp": datetime.now().isoformat()
            })
        
        return insights, alerts
    
    def calculate_health_score(self, health_data, fitness_data):
        """Calculate overall health score based on multiple factors"""
        score_components = {}
        
        # Activity score (0-25 points)
        recent_steps = [health_data[date]["steps"] for date in sorted(health_data.keys())[-7:]]
        avg_steps = statistics.mean(recent_steps)
        activity_score = min(25, (avg_steps / 10000) * 25)
        score_components["activity"] = activity_score
        
        # Sleep score (0-25 points)
        recent_sleep = [health_data[date]["sleep_hours"] for date in sorted(health_data.keys())[-7:]]
        avg_sleep = statistics.mean(recent_sleep)
        sleep_score = max(0, min(25, (avg_sleep / 8) * 25))
        if avg_sleep > 9:  # Too much sleep can also be concerning
            sleep_score = max(0, sleep_score - 5)
        score_components["sleep"] = sleep_score
        
        # Heart rate score (0-20 points)
        recent_resting_hr = [health_data[date]["resting_heart_rate"] for date in sorted(health_data.keys())[-7:]]
        avg_resting_hr = statistics.mean(recent_resting_hr)
        if avg_resting_hr <= 70:
            hr_score = 20
        elif avg_resting_hr <= 80:
            hr_score = 15
        elif avg_resting_hr <= 90:
            hr_score = 10
        else:
            hr_score = 5
        score_components["heart_rate"] = hr_score
        
        # Exercise consistency score (0-15 points)
        workout_days = sum(1 for data in fitness_data.values() if data["workouts"])
        exercise_score = min(15, (workout_days / 5) * 15)  # 5 days = perfect score
        score_components["exercise"] = exercise_score
        
        # Wellness score (0-15 points)
        mood_scores = [fitness_data[date]["mood_score"] for date in fitness_data.keys()]
        energy_scores = [fitness_data[date]["energy_level"] for date in fitness_data.keys()]
        wellness_score = ((statistics.mean(mood_scores) + statistics.mean(energy_scores)) / 20) * 15
        score_components["wellness"] = wellness_score
        
        total_score = sum(score_components.values())
        
        return {
            "total_score": round(total_score, 1),
            "components": {k: round(v, 1) for k, v in score_components.items()},
            "grade": self.get_health_grade(total_score),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_health_grade(self, score):
        """Convert health score to letter grade"""
        if score >= 90:
            return "A+"
        elif score >= 85:
            return "A"
        elif score >= 80:
            return "A-"
        elif score >= 75:
            return "B+"
        elif score >= 70:
            return "B"
        elif score >= 65:
            return "B-"
        elif score >= 60:
            return "C+"
        elif score >= 55:
            return "C"
        elif score >= 50:
            return "C-"
        else:
            return "D"
    
    def generate_personalized_recommendations(self, insights, alerts, health_score):
        """Generate personalized health recommendations"""
        recommendations = []
        
        # Priority recommendations based on alerts
        high_priority_alerts = [alert for alert in alerts if alert["priority"] == "high"]
        if high_priority_alerts:
            recommendations.append({
                "category": "urgent",
                "title": "Immediate Health Concerns",
                "items": [alert["recommendation"] for alert in high_priority_alerts],
                "timeline": "This week"
            })
        
        # Activity recommendations
        activity_insights = [insight for insight in insights if insight["type"] == "activity"]
        if activity_insights:
            recommendations.append({
                "category": "activity",
                "title": "Activity & Movement",
                "items": [
                    "Take a 10-minute walk after each meal",
                    "Use a standing desk for 2-3 hours daily",
                    "Park further away or take stairs when possible",
                    "Set hourly movement reminders"
                ],
                "timeline": "Daily habits"
            })
        
        # Sleep recommendations
        sleep_insights = [insight for insight in insights if insight["type"] == "sleep"]
        if sleep_insights:
            recommendations.append({
                "category": "sleep",
                "title": "Sleep Optimization",
                "items": [
                    "Maintain consistent bedtime and wake time",
                    "Create a relaxing bedtime routine",
                    "Avoid screens 1 hour before sleep",
                    "Keep bedroom cool (65-68°F) and dark"
                ],
                "timeline": "Evening routine"
            })
        
        # Fitness recommendations based on health score
        if health_score["total_score"] < 70:
            recommendations.append({
                "category": "fitness",
                "title": "Fitness Improvement Plan",
                "items": [
                    "Start with 20-minute walks 3x per week",
                    "Add 2 strength training sessions weekly",
                    "Try yoga or stretching for flexibility",
                    "Gradually increase workout intensity"
                ],
                "timeline": "4-week plan"
            })
        
        # Wellness recommendations
        wellness_insights = [insight for insight in insights if insight["type"] == "wellness"]
        if wellness_insights:
            recommendations.append({
                "category": "wellness",
                "title": "Mental & Emotional Health",
                "items": [
                    "Practice 10 minutes of meditation daily",
                    "Spend time in nature or sunlight",
                    "Connect with friends and family regularly",
                    "Consider journaling or gratitude practice"
                ],
                "timeline": "Daily practice"
            })
        
        return recommendations
    
    def save_insight_report(self, insights, alerts, health_score, recommendations):
        """Save detailed insight report"""
        report_filename = f"health_insights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path = os.path.join(INSIGHTS_FOLDER, report_filename)
        
        report_data = {
            "generated_at": datetime.now().isoformat(),
            "health_score": health_score,
            "insights": insights,
            "alerts": alerts,
            "recommendations": recommendations,
            "summary": {
                "total_insights": len(insights),
                "high_priority_alerts": len([a for a in alerts if a["priority"] == "high"]),
                "health_grade": health_score["grade"],
                "key_focus_areas": list(set([i["type"] for i in insights]))
            }
        }
        
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        self.log_action(f"📊 Health insight report saved: {report_filename}")
        return report_path
    
    def run_health_analysis(self):
        """Main function to run health data analysis"""
        self.log_action("🏃‍♂️ Starting health data analysis...")
        
        # Get health data from various sources
        health_data = self.get_apple_health_data()
        fitness_data = self.get_fitness_app_data()
        
        self.log_action(f"📱 Analyzed {len(health_data)} days of health data")
        self.log_action(f"💪 Processed {len(fitness_data)} days of fitness data")
        
        # Analyze patterns and generate insights
        insights, alerts = self.analyze_health_patterns(health_data, fitness_data)
        health_score = self.calculate_health_score(health_data, fitness_data)
        recommendations = self.generate_personalized_recommendations(insights, alerts, health_score)
        
        # Update health history
        self.health_history["daily_metrics"].update(health_data)
        self.health_history["insights"].extend(insights)
        self.health_history["alerts"].extend(alerts)
        self.health_history["stats"]["total_days_tracked"] = len(health_data)
        self.health_history["stats"]["insights_generated"] = len(insights)
        self.health_history["stats"]["health_score"] = health_score["total_score"]
        
        # Save data and generate reports
        self.save_health_history()
        report_path = self.save_insight_report(insights, alerts, health_score, recommendations)
        
        # Log findings
        self.log_action(f"🎯 Health Score: {health_score['total_score']}/100 (Grade: {health_score['grade']})")
        self.log_action(f"💡 Generated {len(insights)} insights and {len(alerts)} alerts")
        
        if alerts:
            high_priority = [a for a in alerts if a["priority"] == "high"]
            if high_priority:
                self.log_action(f"🚨 {len(high_priority)} high-priority health alerts require attention")
        
        # Log key insights
        for insight in insights[:3]:  # Top 3 insights
            priority_emoji = {"high": "🚨", "medium": "⚠️", "positive": "✅"}.get(insight["priority"], "💡")
            self.log_action(f"{priority_emoji} {insight['title']}")
        
        self.log_action("")
        
        return {
            "health_data": health_data,
            "fitness_data": fitness_data,
            "insights": insights,
            "alerts": alerts,
            "health_score": health_score,
            "recommendations": recommendations,
            "report_path": report_path
        }

if __name__ == "__main__":
    health_ai = HealthDataInterpreter()
    results = health_ai.run_health_analysis()
    
    # Send notification
    health_score = results["health_score"]
    notification_text = f"Health Score: {health_score['total_score']}/100 ({health_score['grade']}) | {len(results['insights'])} insights generated"
    
    try:
        subprocess.run([
            'osascript', '-e', 
            f'display notification "{notification_text}" with title "Health Data Interpreter"'
        ])
    except:
        pass
    
    health_ai.log_action("✅ Health data analysis complete!")
