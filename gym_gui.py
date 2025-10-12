#!/usr/bin/env python3
"""
Gym Workout Planner - GUI Version
Author: Aryan Kumawat
A beautiful graphical interface for the gym workout planning system
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import json
import os
import math
from datetime import datetime
from typing import Dict, List, Optional


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
    def generate_workout_plan(cls, user: User) -> List[Dict]:
        """Generate a complete workout plan for the user"""
        reduction = cls.calculate_age_reduction(user.age)
        ex_index = cls.get_exercise_index(user.gender, user.age)
        workout_plan = []
        
        for day in range(1, user.training_days + 1):
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


class GymWorkoutPlannerGUI:
    """Main GUI application class"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Gym Workout Planner")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Color scheme
        self.bg_color = "#f0f0f0"
        self.primary_color = "#4CAF50"
        self.secondary_color = "#2196F3"
        self.accent_color = "#FF9800"
        self.text_color = "#333333"
        
        self.user: Optional[User] = None
        self.workout_plan: List[Dict] = []
        self.data_file = "user_data.json"
        
        # Load user data
        self.load_user_data()
        
        # Setup GUI
        self.setup_styles()
        self.create_main_window()
        
    def setup_styles(self):
        """Setup ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles
        style.configure('Primary.TButton',
                       background=self.primary_color,
                       foreground='white',
                       font=('Helvetica', 11, 'bold'),
                       padding=10)
        style.map('Primary.TButton',
                 background=[('active', '#45a049')])
        
        style.configure('Secondary.TButton',
                       background=self.secondary_color,
                       foreground='white',
                       font=('Helvetica', 10),
                       padding=8)
        style.map('Secondary.TButton',
                 background=[('active', '#1976D2')])
        
        # Configure label styles
        style.configure('Title.TLabel',
                       font=('Helvetica', 24, 'bold'),
                       foreground=self.primary_color)
        
        style.configure('Subtitle.TLabel',
                       font=('Helvetica', 12),
                       foreground=self.text_color)
        
        style.configure('Header.TLabel',
                       font=('Helvetica', 14, 'bold'),
                       foreground=self.primary_color)
    
    def create_main_window(self):
        """Create the main application window"""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container with padding
        main_container = ttk.Frame(self.root, padding="20")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text="Gym Workout Planner", style='Title.TLabel')
        title_label.pack()
        
        if self.user:
            subtitle_label = ttk.Label(header_frame, 
                                      text=f"Welcome back, {self.user.name}!",
                                      style='Subtitle.TLabel')
            subtitle_label.pack()
        else:
            subtitle_label = ttk.Label(header_frame,
                                      text="Create your personalized workout plan",
                                      style='Subtitle.TLabel')
            subtitle_label.pack()
        
        # Button container
        button_container = ttk.Frame(main_container)
        button_container.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Configure grid
        for i in range(3):
            button_container.columnconfigure(i, weight=1)
        
        # Create buttons in a grid layout
        buttons = [
            ("Create/Update Profile", self.show_profile_form, 0, 0),
            ("View Workout Plan", self.show_workout_plan, 0, 1),
            ("Export Workout Plan", self.export_workout_plan, 0, 2),
            ("Log Workout", self.show_log_workout, 1, 0),
            ("View Progress", self.show_progress, 1, 1),
            ("About", self.show_about, 1, 2),
        ]
        
        for text, command, row, col in buttons:
            btn = ttk.Button(button_container, text=text, command=command,
                           style='Primary.TButton', width=20)
            btn.grid(row=row, column=col, padx=10, pady=10, sticky='ew')
        
        # Exit button
        exit_btn = ttk.Button(main_container, text="Exit", command=self.root.quit,
                            style='Secondary.TButton')
        exit_btn.pack(pady=10)
        
        # Footer
        footer_label = ttk.Label(main_container,
                                text="Built with Python & Tkinter | Author: Aryan Kumawat",
                                font=('Helvetica', 9),
                                foreground='gray')
        footer_label.pack(side=tk.BOTTOM, pady=10)
    
    def show_profile_form(self):
        """Show profile creation/editing form"""
        # Create new window
        profile_window = tk.Toplevel(self.root)
        profile_window.title("Create/Update Profile")
        profile_window.geometry("500x550")
        profile_window.transient(self.root)
        profile_window.grab_set()
        
        # Main frame
        main_frame = ttk.Frame(profile_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(main_frame, text="Your Profile", style='Header.TLabel')
        title.pack(pady=(0, 20))
        
        # Form fields
        fields_frame = ttk.Frame(main_frame)
        fields_frame.pack(fill=tk.X, pady=10)
        
        # Name
        ttk.Label(fields_frame, text="Name:", font=('Helvetica', 10, 'bold')).grid(
            row=0, column=0, sticky='w', pady=5)
        name_entry = ttk.Entry(fields_frame, width=30, font=('Helvetica', 10))
        name_entry.grid(row=0, column=1, pady=5, padx=10)
        if self.user:
            name_entry.insert(0, self.user.name)
        
        # Age
        ttk.Label(fields_frame, text="Age:", font=('Helvetica', 10, 'bold')).grid(
            row=1, column=0, sticky='w', pady=5)
        age_spinbox = ttk.Spinbox(fields_frame, from_=1, to=110, width=28, font=('Helvetica', 10))
        age_spinbox.grid(row=1, column=1, pady=5, padx=10)
        if self.user:
            age_spinbox.set(self.user.age)
        
        # Gender
        ttk.Label(fields_frame, text="Gender:", font=('Helvetica', 10, 'bold')).grid(
            row=2, column=0, sticky='w', pady=5)
        gender_var = tk.StringVar(value=self.user.gender if self.user else "male")
        gender_frame = ttk.Frame(fields_frame)
        gender_frame.grid(row=2, column=1, pady=5, padx=10, sticky='w')
        ttk.Radiobutton(gender_frame, text="Male", variable=gender_var, value="male").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(gender_frame, text="Female", variable=gender_var, value="female").pack(side=tk.LEFT, padx=5)
        
        # Goal
        ttk.Label(fields_frame, text="Fitness Goal:", font=('Helvetica', 10, 'bold')).grid(
            row=3, column=0, sticky='w', pady=5)
        goal_var = tk.IntVar(value=self.user.goal if self.user else 1)
        goal_combo = ttk.Combobox(fields_frame, width=28, font=('Helvetica', 10), state='readonly')
        goal_combo['values'] = [f"{i+1}. {name}" for i, name in enumerate(WorkoutDatabase.GOAL_NAMES)]
        goal_combo.current((self.user.goal - 1) if self.user else 0)
        goal_combo.grid(row=3, column=1, pady=5, padx=10)
        
        # Training days
        ttk.Label(fields_frame, text="Training Days/Week:", font=('Helvetica', 10, 'bold')).grid(
            row=4, column=0, sticky='w', pady=5)
        days_spinbox = ttk.Spinbox(fields_frame, from_=1, to=7, width=28, font=('Helvetica', 10))
        days_spinbox.grid(row=4, column=1, pady=5, padx=10)
        if self.user:
            days_spinbox.set(self.user.training_days)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        def save_profile():
            try:
                name = name_entry.get().strip()
                age = int(age_spinbox.get())
                gender = gender_var.get()
                goal = goal_combo.current() + 1
                training_days = int(days_spinbox.get())
                
                # Validation
                if not name or not name.replace(" ", "").isalpha():
                    messagebox.showerror("Error", "Please enter a valid name (letters only)")
                    return
                
                if not (1 <= age <= 110):
                    messagebox.showerror("Error", "Age must be between 1 and 110")
                    return
                
                if not (1 <= training_days <= 7):
                    messagebox.showerror("Error", "Training days must be between 1 and 7")
                    return
                
                # Save user
                self.user = User(name, age, gender, goal, training_days)
                if hasattr(self, 'user') and self.user.progress_log:
                    self.user.progress_log = self.user.progress_log
                self.workout_plan = WorkoutCalculator.generate_workout_plan(self.user)
                self.save_user_data()
                
                messagebox.showinfo("Success", "Profile saved successfully!")
                profile_window.destroy()
                self.create_main_window()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for age and training days")
        
        save_btn = ttk.Button(button_frame, text="Save Profile", command=save_profile,
                             style='Primary.TButton')
        save_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=profile_window.destroy,
                               style='Secondary.TButton')
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def show_workout_plan(self):
        """Display workout plan in a new window"""
        if not self.user or not self.workout_plan:
            messagebox.showwarning("No Profile", "Please create a profile first!")
            return
        
        # Create new window
        plan_window = tk.Toplevel(self.root)
        plan_window.title(f"{self.user.name}'s Workout Plan")
        plan_window.geometry("800x600")
        plan_window.transient(self.root)
        
        # Main frame
        main_frame = ttk.Frame(plan_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = ttk.Label(main_frame, 
                          text=f"{self.user.name}'s Personalized Workout Plan",
                          style='Header.TLabel')
        header.pack(pady=10)
        
        # Profile info
        info_frame = ttk.LabelFrame(main_frame, text="Profile Information", padding="10")
        info_frame.pack(fill=tk.X, pady=10)
        
        info_text = f"""
Age: {self.user.age} years
Gender: {self.user.gender.capitalize()}
Goal: {WorkoutDatabase.GOAL_NAMES[self.user.goal - 1]}
Training Days: {self.user.training_days} days per week
"""
        
        age_reduction = WorkoutCalculator.calculate_age_reduction(self.user.age)
        if age_reduction > 0:
            info_text += f"\nNote: Workouts adjusted by {age_reduction}% for age"
        
        info_label = ttk.Label(info_frame, text=info_text, font=('Helvetica', 10))
        info_label.pack()
        
        # Scrolled text for workout plan
        workout_frame = ttk.LabelFrame(main_frame, text="Weekly Workout Plan", padding="10")
        workout_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        workout_text = scrolledtext.ScrolledText(workout_frame, wrap=tk.WORD, 
                                                 font=('Courier', 10),
                                                 height=20)
        workout_text.pack(fill=tk.BOTH, expand=True)
        
        # Insert workout plan
        for day_plan in self.workout_plan:
            workout_text.insert(tk.END, f"\n{'='*70}\n")
            workout_text.insert(tk.END, f"DAY {day_plan['day']}\n")
            workout_text.insert(tk.END, f"{'='*70}\n")
            workout_text.insert(tk.END, day_plan['workout'] + "\n\n")
        
        workout_text.config(state='disabled')
        
        # Close button
        close_btn = ttk.Button(main_frame, text="Close", command=plan_window.destroy,
                              style='Secondary.TButton')
        close_btn.pack(pady=10)
    
    def export_workout_plan(self):
        """Export workout plan to file"""
        if not self.user or not self.workout_plan:
            messagebox.showwarning("No Profile", "Please create a profile first!")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"workout_plan_{self.user.name.replace(' ', '_')}_{timestamp}.txt"
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=default_filename
        )
        
        if filename:
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
                
                messagebox.showinfo("Success", f"Workout plan exported to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export file:\n{str(e)}")
    
    def show_log_workout(self):
        """Show workout logging dialog"""
        if not self.user:
            messagebox.showwarning("No Profile", "Please create a profile first!")
            return
        
        # Create dialog
        log_window = tk.Toplevel(self.root)
        log_window.title("Log Workout")
        log_window.geometry("400x300")
        log_window.transient(self.root)
        log_window.grab_set()
        
        main_frame = ttk.Frame(log_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title = ttk.Label(main_frame, text="Log Completed Workout", style='Header.TLabel')
        title.pack(pady=(0, 20))
        
        # Day selection
        ttk.Label(main_frame, text="Which day did you complete?",
                 font=('Helvetica', 10, 'bold')).pack(pady=5)
        
        day_var = tk.IntVar(value=1)
        day_combo = ttk.Combobox(main_frame, width=20, state='readonly')
        day_combo['values'] = [f"Day {i}" for i in range(1, self.user.training_days + 1)]
        day_combo.current(0)
        day_combo.pack(pady=5)
        
        # Notes
        ttk.Label(main_frame, text="Notes (optional):",
                 font=('Helvetica', 10, 'bold')).pack(pady=5)
        notes_text = tk.Text(main_frame, height=5, width=40, font=('Helvetica', 10))
        notes_text.pack(pady=5)
        
        def save_log():
            day = day_combo.current() + 1
            notes = notes_text.get("1.0", tk.END).strip()
            
            log_entry = {
                'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'day': day,
                'notes': notes
            }
            self.user.progress_log.append(log_entry)
            self.save_user_data()
            
            messagebox.showinfo("Success", f"Great job completing Day {day}!")
            log_window.destroy()
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        save_btn = ttk.Button(button_frame, text="Log Workout", command=save_log,
                             style='Primary.TButton')
        save_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=log_window.destroy,
                               style='Secondary.TButton')
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def show_progress(self):
        """Show workout progress history"""
        if not self.user or not self.user.progress_log:
            messagebox.showinfo("No Progress", "No workout history available yet.\nStart logging your workouts!")
            return
        
        # Create window
        progress_window = tk.Toplevel(self.root)
        progress_window.title("Workout Progress")
        progress_window.geometry("600x500")
        progress_window.transient(self.root)
        
        main_frame = ttk.Frame(progress_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title = ttk.Label(main_frame, text="Your Workout Progress", style='Header.TLabel')
        title.pack(pady=10)
        
        stats = ttk.Label(main_frame,
                         text=f"Total Workouts Completed: {len(self.user.progress_log)}",
                         font=('Helvetica', 12, 'bold'))
        stats.pack(pady=10)
        
        # Scrolled text for history
        history_frame = ttk.LabelFrame(main_frame, text="Workout History", padding="10")
        history_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        history_text = scrolledtext.ScrolledText(history_frame, wrap=tk.WORD,
                                                font=('Helvetica', 10),
                                                height=20)
        history_text.pack(fill=tk.BOTH, expand=True)
        
        for i, entry in enumerate(self.user.progress_log, 1):
            history_text.insert(tk.END, f"{i}. {entry['date']} - Day {entry['day']}\n")
            if entry['notes']:
                history_text.insert(tk.END, f"   Notes: {entry['notes']}\n")
            history_text.insert(tk.END, "\n")
        
        history_text.config(state='disabled')
        
        close_btn = ttk.Button(main_frame, text="Close", command=progress_window.destroy,
                              style='Secondary.TButton')
        close_btn.pack(pady=10)
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
Gym Workout Planner v2.0 (GUI Edition)

Author: Aryan Kumawat

This interactive platform helps you create personalized 
workout plans based on your age, gender, fitness goals, 
and training schedule.

Features:
• Personalized workout routines
• Age-adjusted exercise intensity
• Multiple fitness goals
• Progress tracking
• Export workout plans
• Save and load user profiles
• Beautiful graphical interface

Built with Python & Tkinter
        """
        
        messagebox.showinfo("About Gym Workout Planner", about_text)
    
    def save_user_data(self):
        """Save user data to JSON file"""
        if self.user:
            try:
                with open(self.data_file, 'w') as f:
                    json.dump(self.user.to_dict(), f, indent=2)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save user data:\n{str(e)}")
    
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
            print(f"Error loading user data: {e}")
        return False


def main():
    """Main entry point"""
    root = tk.Tk()
    app = GymWorkoutPlannerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

