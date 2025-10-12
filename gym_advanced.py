#!/usr/bin/env python3
"""
Gym Workout Planner - Advanced Version with Enhanced Features
Author: Aryan Kumawat
Includes: Custom workouts, Rest day recommendations, Weight tracking, Statistics, Calendar
"""

import math
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from gym import Colors, WorkoutDatabase, WorkoutCalculator


class AdvancedUser:
    """Enhanced user profile with advanced features"""
    
    def __init__(self, name: str = "", age: int = 0, gender: str = "", 
                 goal: int = 0, training_days: int = 0):
        self.name = name
        self.age = age
        self.gender = gender
        self.goal = goal
        self.training_days = training_days
        self.progress_log = []
        self.custom_workouts = []  # NEW: Custom workouts
        self.weight_log = []  # NEW: Weight tracking
        self.rest_days = []  # NEW: Rest day tracking
        self.workout_calendar = {}  # NEW: Calendar mapping
    
    def to_dict(self) -> Dict:
        """Convert user to dictionary for JSON serialization"""
        return {
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'goal': self.goal,
            'training_days': self.training_days,
            'progress_log': self.progress_log,
            'custom_workouts': self.custom_workouts,
            'weight_log': self.weight_log,
            'rest_days': self.rest_days,
            'workout_calendar': self.workout_calendar
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'AdvancedUser':
        """Create user from dictionary"""
        user = cls(
            name=data.get('name', ''),
            age=data.get('age', 0),
            gender=data.get('gender', ''),
            goal=data.get('goal', 0),
            training_days=data.get('training_days', 0)
        )
        user.progress_log = data.get('progress_log', [])
        user.custom_workouts = data.get('custom_workouts', [])
        user.weight_log = data.get('weight_log', [])
        user.rest_days = data.get('rest_days', [])
        user.workout_calendar = data.get('workout_calendar', {})
        return user


class CustomWorkoutManager:
    """Manages custom workout creation and editing"""
    
    @staticmethod
    def create_custom_workout(name: str, exercises: List[Dict]) -> Dict:
        """Create a custom workout with exercises"""
        return {
            'id': datetime.now().strftime('%Y%m%d%H%M%S'),
            'name': name,
            'exercises': exercises,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
    
    @staticmethod
    def format_custom_workout(workout: Dict) -> str:
        """Format custom workout for display"""
        lines = [f"Custom workout: {workout['name']}\n"]
        for exercise in workout['exercises']:
            if exercise['type'] == 'reps':
                lines.append(f"{exercise['name']} ({exercise['value']} reps x {exercise['sets']} sets)")
            else:
                lines.append(f"{exercise['name']} ({exercise['value']} mins x {exercise['sets']} sets)")
        return '\n'.join(lines)


class RestDayRecommender:
    """Provides intelligent rest day recommendations"""
    
    @staticmethod
    def calculate_rest_days_needed(training_days: int, age: int, intensity: str = 'medium') -> int:
        """Calculate recommended rest days per week"""
        base_rest = 7 - training_days
        
        # Adjust for age
        if age > 60:
            base_rest = max(base_rest, 3)
        elif age > 50:
            base_rest = max(base_rest, 2)
        
        # Adjust for intensity
        intensity_factor = {
            'low': 0,
            'medium': 0,
            'high': 1
        }
        base_rest += intensity_factor.get(intensity, 0)
        
        return min(base_rest, 4)  # Cap at 4 rest days
    
    @staticmethod
    def should_rest_today(user: 'AdvancedUser') -> tuple:
        """Determine if user should rest today based on recent activity"""
        if not user.progress_log:
            return False, "No workout history available"
        
        # Check last 7 days
        recent_workouts = []
        today = datetime.now()
        
        for log in user.progress_log:
            try:
                log_date = datetime.strptime(log['date'], '%Y-%m-%d %H:%M')
                days_ago = (today - log_date).days
                if days_ago <= 7:
                    recent_workouts.append(days_ago)
            except:
                continue
        
        # Recommendations
        if not recent_workouts:
            return False, "No recent workouts - you're good to train!"
        
        if 0 in recent_workouts or 1 in recent_workouts:
            consecutive = sum(1 for d in recent_workouts if d <= 2)
            if consecutive >= 3:
                return True, "You've worked out 3+ times in the last 2 days. Consider resting."
        
        workouts_this_week = len(recent_workouts)
        if workouts_this_week >= user.training_days:
            return True, f"You've completed your weekly goal ({workouts_this_week} workouts). Rest or do light activity."
        
        return False, f"You have {user.training_days - workouts_this_week} workouts left this week."


class WeightTracker:
    """Tracks and analyzes body weight progress"""
    
    @staticmethod
    def add_weight_entry(user: 'AdvancedUser', weight: float, unit: str = 'kg'):
        """Add a weight measurement"""
        entry = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'weight': weight,
            'unit': unit
        }
        user.weight_log.append(entry)
    
    @staticmethod
    def get_weight_statistics(user: 'AdvancedUser') -> Dict:
        """Calculate weight statistics"""
        if not user.weight_log:
            return {'error': 'No weight data available'}
        
        weights = [entry['weight'] for entry in user.weight_log]
        
        stats = {
            'current': weights[-1] if weights else 0,
            'starting': weights[0] if weights else 0,
            'highest': max(weights) if weights else 0,
            'lowest': min(weights) if weights else 0,
            'average': sum(weights) / len(weights) if weights else 0,
            'total_change': weights[-1] - weights[0] if len(weights) > 1 else 0,
            'entries': len(weights)
        }
        
        return stats
    
    @staticmethod
    def get_weight_trend(user: 'AdvancedUser', days: int = 30) -> str:
        """Analyze weight trend over specified days"""
        if len(user.weight_log) < 2:
            return "Insufficient data"
        
        try:
            recent_entries = user.weight_log[-min(len(user.weight_log), 5):]
            weights = [e['weight'] for e in recent_entries]
            
            if len(weights) < 2:
                return "Stable"
            
            change = weights[-1] - weights[0]
            if abs(change) < 0.5:
                return "Stable"
            elif change > 0:
                return f"Increasing (+{change:.1f} {user.weight_log[-1]['unit']})"
            else:
                return f"Decreasing ({change:.1f} {user.weight_log[-1]['unit']})"
        except:
            return "Unable to determine"


class WorkoutStatistics:
    """Calculates workout statistics and analytics"""
    
    @staticmethod
    def get_statistics(user: 'AdvancedUser') -> Dict:
        """Get comprehensive workout statistics"""
        if not user.progress_log:
            return {'error': 'No workout data available'}
        
        total_workouts = len(user.progress_log)
        
        # Calculate streaks
        current_streak = WorkoutStatistics._calculate_current_streak(user)
        longest_streak = WorkoutStatistics._calculate_longest_streak(user)
        
        # Calculate weekly average
        weekly_avg = WorkoutStatistics._calculate_weekly_average(user)
        
        # Most active day
        days_count = {}
        for log in user.progress_log:
            day = log.get('day', 0)
            days_count[day] = days_count.get(day, 0) + 1
        
        most_active_day = max(days_count.items(), key=lambda x: x[1])[0] if days_count else 0
        
        return {
            'total_workouts': total_workouts,
            'current_streak': current_streak,
            'longest_streak': longest_streak,
            'weekly_average': weekly_avg,
            'most_active_day': most_active_day,
            'days_trained': len(set(log.get('day', 0) for log in user.progress_log))
        }
    
    @staticmethod
    def _calculate_current_streak(user: 'AdvancedUser') -> int:
        """Calculate current consecutive workout streak"""
        if not user.progress_log:
            return 0
        
        streak = 0
        today = datetime.now().date()
        
        # Sort by date
        sorted_logs = sorted(user.progress_log, key=lambda x: x['date'], reverse=True)
        
        for log in sorted_logs:
            try:
                log_date = datetime.strptime(log['date'], '%Y-%m-%d %H:%M').date()
                days_diff = (today - log_date).days
                
                if days_diff <= 1:
                    streak += 1
                    today = log_date
                else:
                    break
            except:
                continue
        
        return streak
    
    @staticmethod
    def _calculate_longest_streak(user: 'AdvancedUser') -> int:
        """Calculate longest workout streak"""
        if not user.progress_log:
            return 0
        
        # Implementation simplified - returns current streak for now
        return WorkoutStatistics._calculate_current_streak(user)
    
    @staticmethod
    def _calculate_weekly_average(user: 'AdvancedUser') -> float:
        """Calculate average workouts per week"""
        if not user.progress_log:
            return 0.0
        
        try:
            first_date = datetime.strptime(user.progress_log[0]['date'], '%Y-%m-%d %H:%M')
            last_date = datetime.strptime(user.progress_log[-1]['date'], '%Y-%m-%d %H:%M')
            weeks = max((last_date - first_date).days / 7, 1)
            return len(user.progress_log) / weeks
        except:
            return 0.0


class WorkoutCalendar:
    """Manages workout calendar and scheduling"""
    
    @staticmethod
    def generate_calendar(user: 'AdvancedUser', weeks: int = 4) -> Dict:
        """Generate a workout calendar for specified weeks"""
        calendar = {}
        start_date = datetime.now()
        
        plan = WorkoutCalculator.generate_workout_plan(user)
        
        for week in range(weeks):
            for day in range(7):
                date = start_date + timedelta(days=week * 7 + day)
                date_str = date.strftime('%Y-%m-%d')
                
                # Determine if it's a workout day or rest day
                if day < len(plan) and week == 0:
                    calendar[date_str] = {
                        'type': 'workout',
                        'day': plan[day]['day'],
                        'workout': plan[day]['workout'][:100] + '...'  # Preview
                    }
                else:
                    calendar[date_str] = {'type': 'rest'}
        
        return calendar
    
    @staticmethod
    def get_today_workout(user: 'AdvancedUser') -> Optional[Dict]:
        """Get today's scheduled workout"""
        if not user.workout_calendar:
            return None
        
        today = datetime.now().strftime('%Y-%m-%d')
        return user.workout_calendar.get(today)


class AdvancedGymWorkoutPlanner:
    """Advanced gym workout planner with enhanced features"""
    
    def __init__(self):
        self.user: Optional[AdvancedUser] = None
        self.workout_plan: List[Dict] = []
        self.data_file = "user_data_advanced.json"
    
    def load_user_data(self) -> bool:
        """Load user data from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.user = AdvancedUser.from_dict(data)
                    self.workout_plan = WorkoutCalculator.generate_workout_plan(self.user)
                    return True
        except Exception as e:
            print(f"{Colors.RED}Error loading user data: {e}{Colors.END}")
        return False
    
    def save_user_data(self):
        """Save user data to JSON file"""
        if self.user:
            try:
                with open(self.data_file, 'w') as f:
                    json.dump(self.user.to_dict(), f, indent=2)
            except Exception as e:
                print(f"{Colors.RED}Error saving user data: {e}{Colors.END}")
    
    def show_statistics(self):
        """Display workout statistics"""
        if not self.user:
            print(f"\n{Colors.RED}Please create a profile first.{Colors.END}")
            return
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}{Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}WORKOUT STATISTICS{Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}{'='*80}{Colors.END}\n")
        
        stats = WorkoutStatistics.get_statistics(self.user)
        
        if 'error' in stats:
            print(f"{Colors.YELLOW}{stats['error']}{Colors.END}")
        else:
            print(f"{Colors.GREEN}Total Workouts:{Colors.END} {stats['total_workouts']}")
            print(f"{Colors.GREEN}Current Streak:{Colors.END} {stats['current_streak']} days")
            print(f"{Colors.GREEN}Longest Streak:{Colors.END} {stats['longest_streak']} days")
            print(f"{Colors.GREEN}Weekly Average:{Colors.END} {stats['weekly_average']:.1f} workouts/week")
            print(f"{Colors.GREEN}Most Active Day:{Colors.END} Day {stats['most_active_day']}")
        
        # Weight statistics
        if self.user.weight_log:
            print(f"\n{Colors.CYAN}WEIGHT TRACKING{Colors.END}")
            weight_stats = WeightTracker.get_weight_statistics(self.user)
            print(f"{Colors.GREEN}Current Weight:{Colors.END} {weight_stats['current']:.1f} {self.user.weight_log[-1]['unit']}")
            print(f"{Colors.GREEN}Starting Weight:{Colors.END} {weight_stats['starting']:.1f} {self.user.weight_log[0]['unit']}")
            print(f"{Colors.GREEN}Total Change:{Colors.END} {weight_stats['total_change']:+.1f} {self.user.weight_log[-1]['unit']}")
            print(f"{Colors.GREEN}Trend:{Colors.END} {WeightTracker.get_weight_trend(self.user)}")
        
        input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
    
    def manage_weight(self):
        """Weight tracking menu"""
        if not self.user:
            print(f"\n{Colors.RED}Please create a profile first.{Colors.END}")
            return
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}WEIGHT TRACKING{Colors.END}")
        print(f"{Colors.CYAN}{'='*80}{Colors.END}\n")
        
        print("1. Add weight entry")
        print("2. View weight history")
        print("3. View weight statistics")
        print("0. Back")
        
        choice = input(f"\n{Colors.BOLD}Choose an option: {Colors.END}")
        
        if choice == '1':
            try:
                weight = float(input("Enter your weight: "))
                unit = input("Unit (kg/lbs) [kg]: ").lower() or 'kg'
                WeightTracker.add_weight_entry(self.user, weight, unit)
                self.save_user_data()
                print(f"\n{Colors.GREEN}Weight entry added!{Colors.END}")
            except ValueError:
                print(f"\n{Colors.RED}Invalid weight value{Colors.END}")
        
        elif choice == '2':
            if not self.user.weight_log:
                print(f"\n{Colors.YELLOW}No weight entries yet{Colors.END}")
            else:
                print(f"\n{Colors.CYAN}WEIGHT HISTORY{Colors.END}")
                for i, entry in enumerate(self.user.weight_log, 1):
                    print(f"{i}. {entry['date']}: {entry['weight']} {entry['unit']}")
        
        elif choice == '3':
            stats = WeightTracker.get_weight_statistics(self.user)
            if 'error' not in stats:
                print(f"\n{Colors.GREEN}Current:{Colors.END} {stats['current']:.1f}")
                print(f"{Colors.GREEN}Average:{Colors.END} {stats['average']:.1f}")
                print(f"{Colors.GREEN}Change:{Colors.END} {stats['total_change']:+.1f}")
        
        input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
    
    def check_rest_recommendation(self):
        """Check if user should rest today"""
        if not self.user:
            print(f"\n{Colors.RED}Please create a profile first.{Colors.END}")
            return
        
        should_rest, message = RestDayRecommender.should_rest_today(self.user)
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}REST DAY RECOMMENDATION{Colors.END}")
        print(f"{Colors.CYAN}{'='*80}{Colors.END}\n")
        
        if should_rest:
            print(f"{Colors.YELLOW}{message}{Colors.END}")
        else:
            print(f"{Colors.GREEN}{message}{Colors.END}")
        
        input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
    
    def run(self):
        """Run the advanced application"""
        self.load_user_data()
        
        while True:
            os.system('clear' if os.name != 'nt' else 'cls')
            
            print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.END}")
            print(f"{Colors.HEADER}{Colors.BOLD}GYM WORKOUT PLANNER - ADVANCED EDITION{Colors.END}")
            print(f"{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.END}\n")
            
            if self.user:
                print(f"{Colors.GREEN}Welcome back, {self.user.name}!{Colors.END}\n")
            
            print(f"{Colors.BOLD}Main Menu:{Colors.END}")
            print(f"  {Colors.GREEN}1.{Colors.END} Profile & Settings")
            print(f"  {Colors.GREEN}2.{Colors.END} View Workout Plan")
            print(f"  {Colors.GREEN}3.{Colors.END} Log Workout")
            print(f"  {Colors.GREEN}4.{Colors.END} Statistics & Analytics")
            print(f"  {Colors.GREEN}5.{Colors.END} Weight Tracking")
            print(f"  {Colors.GREEN}6.{Colors.END} Rest Day Check")
            print(f"  {Colors.GREEN}7.{Colors.END} Custom Workouts (Coming Soon)")
            print(f"  {Colors.RED}0.{Colors.END} Exit")
            
            try:
                choice = input(f"\n{Colors.BOLD}Enter your choice: {Colors.END}").strip()
                
                if choice == '1':
                    print("\nProfile management - Use main gym.py for now")
                elif choice == '2':
                    print("\nView workout plan - Use main gym.py for now")
                elif choice == '3':
                    print("\nLog workout - Use main gym.py for now")
                elif choice == '4':
                    self.show_statistics()
                elif choice == '5':
                    self.manage_weight()
                elif choice == '6':
                    self.check_rest_recommendation()
                elif choice == '7':
                    print(f"\n{Colors.YELLOW}Custom workouts feature coming soon!{Colors.END}")
                    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
                elif choice == '0':
                    os.system('clear' if os.name != 'nt' else 'cls')
                    print(f"\n{Colors.GREEN}{Colors.BOLD}Thank you for using Advanced Gym Workout Planner!{Colors.END}")
                    if self.user:
                        print(f"{Colors.CYAN}Keep pushing towards your goals, {self.user.name}!{Colors.END}\n")
                    break
                else:
                    print(f"\n{Colors.RED}Invalid choice. Please try again.{Colors.END}")
                    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
            except KeyboardInterrupt:
                print(f"\n\n{Colors.YELLOW}Exiting...{Colors.END}\n")
                break


if __name__ == "__main__":
    app = AdvancedGymWorkoutPlanner()
    app.run()

