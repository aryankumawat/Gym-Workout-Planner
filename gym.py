#!/usr/bin/env python3
"""
Gym Workout Planner - Interactive Platform
Author: Aryan Kumawat
An interactive gym workout planning system with personalized training programs
"""

import math
import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class WorkoutDatabase:
    """Database of workout routines"""
    
    WORKOUT_LISTS = [
        """Gym workout for fat loss

Plate thrusters (15 reps x 3 sets)
Mountain climbers (20 reps x 3 sets)
Box jumps (10 reps x 3 sets)
Lunges (10 reps x 3 sets)
Renegade rows (10 reps x 3 sets)
Press ups (15 reps x 3 sets)
Treadmill (10 mins x 3 sets)
Supermans (10 reps x 3 sets)
Crunches (10 reps x 3 sets)""",
        
        """Gym workout for stretch and relax

Quad stretchs (2 mins x 3 sets)
Hamstring stretchs (2 mins x 3 sets)
Chest and shoulder stretchs (2 mins x 2 sets)
Upper back stretchs (3 mins x 2 sets)
Biceps stretchs (2 mins x 2 sets)
Triceps stretchs (2 mins x 3 sets)
Hip flexors (2 mins x 3 sets)
Calf stretchs (2 mins x 3 sets)
Lower back stretchs (2 mins x 3 sets)""",
        
        """Gym workout for high-intensity exercises

Jumping jacks (20 reps x 4 sets)
Sprints (20 reps x 3 sets)
Mountain climbers (20 reps x 4 sets)
Squat jumps (20 reps x 4 sets)
Lunges (20 reps x 3 sets)
Crunches (20 reps x 3 sets)
Treadmill (15 mins x 2 sets)
Side planks (15 reps x 3 sets)
Burpees (15 reps x 3 sets)""",
        
        """Gym workout for strong legs

Back squats (10 reps x 5 sets)
Hip thrusts (12 reps x 3 sets)
Overhead presses (10 reps x 5 sets)
Rack pulls (10 reps x 5 sets)
Squats (10 reps x 4 sets)
Dumbbell lunges (10 reps x 3 sets)
Leg curls (15 reps x 3 sets)
Standing calf raises (20 reps x 2 sets)""",
        
        """Gym workout for strong ABS

Cross crunchs (12 reps x 3 sets)
Knee ups (15 reps x 5 sets)
Hip thrusts (15 reps x 3 sets)
Mountain climbers (15 reps x 3 sets)
Vertical hip thrusts (12 reps x 3 sets)
Bicycles (15 mins x 2 sets)
Front planks (15 mins x 3 sets)
Dragon flags (12 reps x 4 sets)
Reverse crunches (10 reps x 3 sets)""",
        
        """Gym workout for strong shoulder and arms

Bench presses (10 reps x 5 sets)
Triceps dips (10 reps x 5 sets)
Incline dumbbell presses (12 reps x 3 sets)
Dumbbell flyes (15 reps x 3 sets)
Triceps extensions (15 reps x 3 sets)
Pull ups (10 reps x 5 sets)
Treadmill (15 mins x 2 sets)
Bent over rows (10 reps x 5 sets)
Chin ups (10 reps x 3 sets)""",
        
        """Gym workout for a male younger than 18 years old

High knees (20 reps x 3 sets)
Squats (10 reps x 3 sets)
Calf raises (10 reps x 3 sets)
Scissor jumps (12 reps x 3 sets)
Burpees (10 reps x 3 sets)
Treadmill (10 mins x 2 sets)""",
        
        """Gym workout for a female younger than 18 years old

Squats (10 reps x 3 sets)
Crunches (10 reps x 2 sets)
Jumping jacks (10 reps x 3 sets)
Push ups (10 reps x 2 sets)
Burpees (10 reps x 3 sets)
Treadmill (10 mins x 2 sets)""",
        
        """Gym workout for a male at least 18 years old

Standing biceps curls (20 reps x 3 sets)
Seated incline curls (18 reps x 3 sets)
Seated dumbbell presses (12 reps x 3 sets)
Leg presses (15 reps x 3 sets)
Bench presses (10 reps x 4 sets)
Tricep kickbacks (15 reps x 3 sets)
Hip thrusts (12 reps x 3 sets)
Seated rows (10 reps x 4 sets)""",
        
        """Gym workout for a female at least 18 years old

Lateral raises (15 reps x 3 sets)
Reverse flyes (12 reps x 3 sets)
Hip thrusts (12 reps x 3 sets)
Incline dumbbell presses (15 reps x 3 sets)
Squats (10 reps x 4 sets)
Dumbbell lunges (10 reps x 3 sets)
Leg presses (12 reps x 3 sets)
Dumbbell presses (10 reps x 4 sets)"""
    ]
    
    GOAL_NAMES = [
        "Losing Weight",
        "Staying Calm and Relax",
        "Increasing Heart Rate",
        "Stronger Legs",
        "Stronger ABS",
        "Stronger Shoulders and Arms"
    ]


class User:
    """Represents a user profile"""
    
    def __init__(self, name: str = "", age: int = 0, gender: str = "", 
                 goal: int = 0, training_days: int = 0):
        self.name = name
        self.age = age
        self.gender = gender
        self.goal = goal
        self.training_days = training_days
        self.progress_log = []
    
    def to_dict(self) -> Dict:
        """Convert user to dictionary for JSON serialization"""
        return {
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'goal': self.goal,
            'training_days': self.training_days,
            'progress_log': self.progress_log
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        """Create user from dictionary"""
        user = cls(
            name=data.get('name', ''),
            age=data.get('age', 0),
            gender=data.get('gender', ''),
            goal=data.get('goal', 0),
            training_days=data.get('training_days', 0)
        )
        user.progress_log = data.get('progress_log', [])
        return user


class WorkoutCalculator:
    """Handles workout calculations and adjustments"""
    
    @staticmethod
    def get_exercise_index(gender: str, age: int) -> int:
        """Get the exercise index based on gender and age"""
        if gender == "male" and age >= 18:
            return 9
        elif gender == "male" and age < 18:
            return 7
        elif gender == "female" and age >= 18:
            return 10
        return 8
    
    @staticmethod
    def calculate_age_reduction(age: int) -> int:
        """Calculate workout reduction percentage based on age"""
        if age > 80:
            reduction = 40 + ((age - 80) * 4)
            return min(reduction, 80)
        if age > 75:
            return 25 + ((age - 75) * 3)
        if age > 65:
            return 5 + ((age - 65) * 2)
        if age > 60:
            return (age - 60) * 1
        return 0
    
    @staticmethod
    def adjust_workout_line(line: str, reduction: int, goal: int) -> str:
        """Adjust a single workout line based on age reduction"""
        subtract = 1 if goal == 2 else 2
        
        # Find reps or mins
        val = line.find(" reps")
        if val == -1:
            val = line.find(" mins")
        
        if val == -1:
            return line
        
        try:
            exercise_val = int(line[val - subtract:val])
            adjusted_val = math.ceil(exercise_val - ((exercise_val * reduction) / 100))
            return line[:val - subtract] + str(adjusted_val) + line[val:]
        except (ValueError, IndexError):
            return line
    
    @classmethod
    def generate_workout_plan(cls, user: User) -> List[str]:
        """Generate a complete workout plan for the user"""
        reduction = cls.calculate_age_reduction(user.age)
        ex_index = cls.get_exercise_index(user.gender, user.age)
        workout_plan = []
        
        for day in range(1, user.training_days + 1):
            # Alternate between goal workout and age/gender workout
            if user.training_days % 2 == 1:
                workout_index = user.goal - 1 if day % 2 == 1 else ex_index - 1
            else:
                workout_index = user.goal - 1 if day % 2 == 0 else ex_index - 1
            
            workout = WorkoutDatabase.WORKOUT_LISTS[workout_index]
            adjusted_lines = []
            
            for line in workout.split("\n"):
                adjusted_lines.append(cls.adjust_workout_line(line, reduction, user.goal))
            
            workout_plan.append({
                'day': day,
                'workout': '\n'.join(adjusted_lines)
            })
        
        return workout_plan


class GymWorkoutPlanner:
    """Main application class"""
    
    def __init__(self):
        self.user: Optional[User] = None
        self.workout_plan: List[str] = []
        self.data_file = "user_data.json"
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def print_header(self, text: str):
        """Print a styled header"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.END}")
        print(f"{Colors.HEADER}{Colors.BOLD}{text.center(80)}{Colors.END}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.END}\n")
    
    def print_section(self, text: str):
        """Print a styled section"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}{text}{Colors.END}")
        print(f"{Colors.CYAN}{'-' * 80}{Colors.END}")
    
    def validate_name(self, name: str) -> bool:
        """Validate user name input"""
        name_cleaned = name.replace(" ", "")
        return bool(name and not name.isspace() and name_cleaned.isalpha())
    
    def get_user_input(self):
        """Get user information through interactive prompts"""
        self.print_header("WELCOME TO GYM WORKOUT PLANNER")
        
        # Get name
        while True:
            name = input(f"{Colors.BOLD}Please enter your name: {Colors.END}").strip()
            if self.validate_name(name):
                break
            print(f"{Colors.RED}Error: Only alphabetical characters and spaces allowed{Colors.END}")
        
        # Get age
        while True:
            try:
                age = int(input(f"{Colors.BOLD}Please enter your age: {Colors.END}"))
                if 0 < age <= 110:
                    break
                print(f"{Colors.RED}Error: Age must be between 1 and 110{Colors.END}")
            except ValueError:
                print(f"{Colors.RED}Error: Please enter a valid number{Colors.END}")
        
        # Get gender
        while True:
            gender = input(f"{Colors.BOLD}Please enter your biological sex (female/male): {Colors.END}").strip().lower()
            if gender in ["female", "male"]:
                break
            print(f"{Colors.RED}Error: Please enter 'female' or 'male'{Colors.END}")
        
        # Get training goal
        self.print_section("Training Goals")
        print(f"{Colors.GREEN}1.{Colors.END} Losing weight")
        print(f"{Colors.GREEN}2.{Colors.END} Staying calm and relax")
        print(f"{Colors.GREEN}3.{Colors.END} Increasing your heart rate")
        print(f"{Colors.GREEN}4.{Colors.END} Having stronger legs")
        print(f"{Colors.GREEN}5.{Colors.END} Having stronger ABS")
        print(f"{Colors.GREEN}6.{Colors.END} Having stronger shoulders and arms")
        
        while True:
            try:
                goal = int(input(f"\n{Colors.BOLD}Choose your goal (1-6): {Colors.END}"))
                if 1 <= goal <= 6:
                    break
                print(f"{Colors.RED}Error: Please choose a number between 1 and 6{Colors.END}")
            except ValueError:
                print(f"{Colors.RED}Error: Please enter a valid number{Colors.END}")
        
        # Get training days
        while True:
            try:
                training_days = int(input(f"{Colors.BOLD}How many days per week can you train? (1-7): {Colors.END}"))
                if 1 <= training_days <= 7:
                    break
                print(f"{Colors.RED}Error: Please choose a number between 1 and 7{Colors.END}")
            except ValueError:
                print(f"{Colors.RED}Error: Please enter a valid number{Colors.END}")
        
        self.user = User(name, age, gender, goal, training_days)
        self.workout_plan = WorkoutCalculator.generate_workout_plan(self.user)
        self.save_user_data()
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Profile created successfully!{Colors.END}")
        input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
    
    def display_workout_plan(self):
        """Display the complete workout plan"""
        if not self.user or not self.workout_plan:
            print(f"\n{Colors.RED}No workout plan available. Please create a profile first.{Colors.END}")
            input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
            return
        
        self.clear_screen()
        self.print_header(f"{self.user.name.upper()}'S WORKOUT PLAN")
        
        print(f"{Colors.BOLD}Profile:{Colors.END}")
        print(f"  Age: {self.user.age} years")
        print(f"  Gender: {self.user.gender.capitalize()}")
        print(f"  Goal: {WorkoutDatabase.GOAL_NAMES[self.user.goal - 1]}")
        print(f"  Training Days: {self.user.training_days} days per week")
        
        age_reduction = WorkoutCalculator.calculate_age_reduction(self.user.age)
        if age_reduction > 0:
            print(f"\n{Colors.YELLOW}Note: Workouts adjusted by {age_reduction}% for age{Colors.END}")
        
        for day_plan in self.workout_plan:
            self.print_section(f"Day {day_plan['day']}")
            print(day_plan['workout'])
        
        print(f"\n{Colors.BOLD}{'=' * 80}{Colors.END}")
        input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
    
    def export_workout_plan(self):
        """Export workout plan to a text file"""
        if not self.user or not self.workout_plan:
            print(f"\n{Colors.RED}No workout plan available. Please create a profile first.{Colors.END}")
            input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"workout_plan_{self.user.name.replace(' ', '_')}_{timestamp}.txt"
        
        try:
            with open(filename, 'w') as f:
                f.write("=" * 80 + "\n")
                f.write(f"{self.user.name.upper()}'S PERSONALIZED WORKOUT PLAN\n")
                f.write("=" * 80 + "\n\n")
                
                f.write(f"Profile Information:\n")
                f.write(f"  Name: {self.user.name}\n")
                f.write(f"  Age: {self.user.age} years\n")
                f.write(f"  Gender: {self.user.gender.capitalize()}\n")
                f.write(f"  Goal: {WorkoutDatabase.GOAL_NAMES[self.user.goal - 1]}\n")
                f.write(f"  Training Days: {self.user.training_days} days per week\n")
                f.write(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                age_reduction = WorkoutCalculator.calculate_age_reduction(self.user.age)
                if age_reduction > 0:
                    f.write(f"Note: Workouts adjusted by {age_reduction}% for age\n\n")
                
                for day_plan in self.workout_plan:
                    f.write("-" * 80 + "\n")
                    f.write(f"DAY {day_plan['day']}\n")
                    f.write("-" * 80 + "\n")
                    f.write(day_plan['workout'] + "\n\n")
                
                f.write("=" * 80 + "\n")
                f.write("Keep up the great work! Stay consistent and track your progress.\n")
                f.write("=" * 80 + "\n")
            
            print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Workout plan exported successfully!{Colors.END}")
            print(f"{Colors.CYAN}File saved as: {filename}{Colors.END}")
        except Exception as e:
            print(f"\n{Colors.RED}Error exporting workout plan: {e}{Colors.END}")
        
        input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
    
    def log_workout(self):
        """Log a completed workout"""
        if not self.user:
            print(f"\n{Colors.RED}Please create a profile first.{Colors.END}")
            input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
            return
        
        self.clear_screen()
        self.print_header("LOG WORKOUT")
        
        print(f"{Colors.BOLD}Which day did you complete?{Colors.END}")
        for i in range(1, self.user.training_days + 1):
            print(f"  {i}. Day {i}")
        
        try:
            day = int(input(f"\n{Colors.BOLD}Enter day number: {Colors.END}"))
            if 1 <= day <= self.user.training_days:
                notes = input(f"{Colors.BOLD}Add notes (optional): {Colors.END}")
                
                log_entry = {
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'day': day,
                    'notes': notes
                }
                self.user.progress_log.append(log_entry)
                self.save_user_data()
                
                print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Workout logged successfully!{Colors.END}")
                print(f"{Colors.CYAN}Great job completing Day {day}!{Colors.END}")
            else:
                print(f"\n{Colors.RED}Invalid day number{Colors.END}")
        except ValueError:
            print(f"\n{Colors.RED}Invalid input{Colors.END}")
        
        input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
    
    def view_progress(self):
        """View workout progress history"""
        if not self.user or not self.user.progress_log:
            print(f"\n{Colors.YELLOW}No workout history available yet.{Colors.END}")
            input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
            return
        
        self.clear_screen()
        self.print_header("WORKOUT PROGRESS")
        
        print(f"{Colors.BOLD}Total workouts completed: {len(self.user.progress_log)}{Colors.END}\n")
        
        for i, entry in enumerate(self.user.progress_log, 1):
            print(f"{Colors.GREEN}{i}.{Colors.END} {entry['date']} - Day {entry['day']}")
            if entry['notes']:
                print(f"   {Colors.CYAN}Notes: {entry['notes']}{Colors.END}")
        
        input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
    
    def save_user_data(self):
        """Save user data to JSON file"""
        if self.user:
            try:
                with open(self.data_file, 'w') as f:
                    json.dump(self.user.to_dict(), f, indent=2)
            except Exception as e:
                print(f"{Colors.RED}Error saving user data: {e}{Colors.END}")
    
    def load_user_data(self) -> bool:
        """Load user data from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.user = User.from_dict(data)
                    self.workout_plan = WorkoutCalculator.generate_workout_plan(self.user)
                    return True
        except Exception as e:
            print(f"{Colors.RED}Error loading user data: {e}{Colors.END}")
        return False
    
    def show_main_menu(self):
        """Display and handle main menu"""
        while True:
            self.clear_screen()
            self.print_header("GYM WORKOUT PLANNER")
            
            if self.user:
                print(f"{Colors.GREEN}Welcome back, {self.user.name}!{Colors.END}\n")
            
            print(f"{Colors.BOLD}Main Menu:{Colors.END}")
            print(f"  {Colors.GREEN}1.{Colors.END} {'Update' if self.user else 'Create'} Profile")
            print(f"  {Colors.GREEN}2.{Colors.END} View Workout Plan")
            print(f"  {Colors.GREEN}3.{Colors.END} Export Workout Plan")
            print(f"  {Colors.GREEN}4.{Colors.END} Log Completed Workout")
            print(f"  {Colors.GREEN}5.{Colors.END} View Progress History")
            print(f"  {Colors.GREEN}6.{Colors.END} About")
            print(f"  {Colors.RED}0.{Colors.END} Exit")
            
            try:
                choice = input(f"\n{Colors.BOLD}Enter your choice: {Colors.END}").strip()
                
                if choice == '1':
                    self.get_user_input()
                elif choice == '2':
                    self.display_workout_plan()
                elif choice == '3':
                    self.export_workout_plan()
                elif choice == '4':
                    self.log_workout()
                elif choice == '5':
                    self.view_progress()
                elif choice == '6':
                    self.show_about()
                elif choice == '0':
                    self.clear_screen()
                    print(f"\n{Colors.GREEN}{Colors.BOLD}Thank you for using Gym Workout Planner!{Colors.END}")
                    if self.user:
                        print(f"{Colors.CYAN}Keep up the great work, {self.user.name}!{Colors.END}\n")
                    break
                else:
                    print(f"\n{Colors.RED}Invalid choice. Please try again.{Colors.END}")
                    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
            except KeyboardInterrupt:
                print(f"\n\n{Colors.YELLOW}Exiting...{Colors.END}\n")
                break
    
    def show_about(self):
        """Show about information"""
        self.clear_screen()
        self.print_header("ABOUT")
        
        print(f"{Colors.BOLD}Gym Workout Planner v2.0{Colors.END}")
        print(f"{Colors.CYAN}Author: Aryan Kumawat{Colors.END}\n")
        
        print("This interactive platform helps you create personalized workout plans")
        print("based on your age, gender, fitness goals, and training schedule.\n")
        
        print(f"{Colors.BOLD}Features:{Colors.END}")
        print("  • Personalized workout routines")
        print("  • Age-adjusted exercise intensity")
        print("  • Multiple fitness goals")
        print("  • Progress tracking")
        print("  • Export workout plans")
        print("  • Save and load user profiles")
        
        input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
    
    def run(self):
        """Run the application"""
        self.load_user_data()
        self.show_main_menu()


if __name__ == "__main__":
    app = GymWorkoutPlanner()
    app.run()

