#!/usr/bin/env python3
"""
Gym Workout Planner - Enhanced GUI Version with Advanced Features
Author: Aryan Kumawat
Includes: Weight tracking, Statistics, Rest recommendations, and more!
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import json
import os
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Optional matplotlib import for future graph features
try:
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# Import from existing modules
from gym import WorkoutDatabase, WorkoutCalculator
from gym_advanced import (
    AdvancedUser, WeightTracker, WorkoutStatistics,
    RestDayRecommender, CustomWorkoutManager
)


class EnhancedGymWorkoutPlannerGUI:
    """Enhanced GUI application with all advanced features"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Gym Workout Planner - Enhanced Edition")
        self.root.geometry("1000x750")
        self.root.resizable(True, True)
        
        # Color scheme - Modern and professional
        self.bg_color = "#f5f5f5"
        self.primary_color = "#4CAF50"
        self.secondary_color = "#2196F3"
        self.accent_color = "#FF9800"
        self.warning_color = "#FF5722"
        self.success_color = "#8BC34A"
        self.text_color = "#333333"
        
        self.user: Optional[AdvancedUser] = None
        self.workout_plan: List[Dict] = []
        self.data_file = "user_data_gui_enhanced.json"
        
        # Load user data
        self.load_user_data()
        
        # Setup GUI
        self.setup_styles()
        self.create_main_window()
        
    def setup_styles(self):
        """Setup ttk styles with modern theme"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Button styles
        style.configure('Primary.TButton',
                       background=self.primary_color,
                       foreground='white',
                       font=('Helvetica', 10, 'bold'),
                       padding=12)
        style.map('Primary.TButton',
                 background=[('active', '#45a049')])
        
        style.configure('Secondary.TButton',
                       background=self.secondary_color,
                       foreground='white',
                       font=('Helvetica', 9),
                       padding=8)
        style.map('Secondary.TButton',
                 background=[('active', '#1976D2')])
        
        style.configure('Accent.TButton',
                       background=self.accent_color,
                       foreground='white',
                       font=('Helvetica', 9, 'bold'),
                       padding=10)
        
        # Label styles
        style.configure('Title.TLabel',
                       font=('Helvetica', 22, 'bold'),
                       foreground=self.primary_color)
        
        style.configure('Subtitle.TLabel',
                       font=('Helvetica', 11),
                       foreground=self.text_color)
        
        style.configure('Header.TLabel',
                       font=('Helvetica', 14, 'bold'),
                       foreground=self.primary_color)
        
        style.configure('Stat.TLabel',
                       font=('Helvetica', 12),
                       foreground=self.text_color,
                       background='white',
                       padding=10)
    
    def create_main_window(self):
        """Create the enhanced main window with tabs"""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container
        main_container = ttk.Frame(self.root, padding="15")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_label = ttk.Label(header_frame, 
                               text="Gym Workout Planner - Enhanced Edition",
                               style='Title.TLabel')
        title_label.pack()
        
        if self.user:
            subtitle_label = ttk.Label(header_frame,
                                      text=f"Welcome back, {self.user.name}!",
                                      style='Subtitle.TLabel')
            subtitle_label.pack()
        else:
            subtitle_label = ttk.Label(header_frame,
                                      text="Create your profile to get started",
                                      style='Subtitle.TLabel')
            subtitle_label.pack()
        
        # Tabbed interface
        notebook = ttk.Notebook(main_container)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Tab 1: Workout Plan
        workout_tab = ttk.Frame(notebook, padding="10")
        notebook.add(workout_tab, text="  Workout Plan  ")
        self.create_workout_tab(workout_tab)
        
        # Tab 2: Progress & Stats
        stats_tab = ttk.Frame(notebook, padding="10")
        notebook.add(stats_tab, text="  Statistics  ")
        self.create_stats_tab(stats_tab)
        
        # Tab 3: Weight Tracking
        weight_tab = ttk.Frame(notebook, padding="10")
        notebook.add(weight_tab, text="  Weight Tracking  ")
        self.create_weight_tab(weight_tab)
        
        # Tab 4: Profile & Settings
        profile_tab = ttk.Frame(notebook, padding="10")
        notebook.add(profile_tab, text="  Profile  ")
        self.create_profile_tab(profile_tab)
        
        # Footer with quick actions
        footer_frame = ttk.Frame(main_container)
        footer_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Quick action buttons
        ttk.Button(footer_frame, text="Log Workout", command=self.show_log_workout,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(footer_frame, text="Rest Day Check", command=self.show_rest_recommendation,
                  style='Secondary.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(footer_frame, text="Export Plan", command=self.export_workout_plan,
                  style='Secondary.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Label(footer_frame,
                 text="Built with Python & Tkinter | Enhanced Edition v2.0",
                 font=('Helvetica', 8),
                 foreground='gray').pack(side=tk.RIGHT)
    
    def create_workout_tab(self, parent):
        """Create workout plan tab"""
        if not self.user or not self.workout_plan:
            ttk.Label(parent, text="Create a profile first to view your workout plan",
                     font=('Helvetica', 12)).pack(pady=50)
            ttk.Button(parent, text="Create Profile",
                      command=lambda: self.show_profile_form(),
                      style='Primary.TButton').pack()
            return
        
        # Profile summary
        summary_frame = ttk.LabelFrame(parent, text="Profile Summary", padding="10")
        summary_frame.pack(fill=tk.X, pady=(0, 10))
        
        summary_text = f"Age: {self.user.age} | Gender: {self.user.gender.capitalize()} | "
        summary_text += f"Goal: {WorkoutDatabase.GOAL_NAMES[self.user.goal - 1]} | "
        summary_text += f"Training Days: {self.user.training_days}/week"
        
        ttk.Label(summary_frame, text=summary_text, font=('Helvetica', 10)).pack()
        
        age_reduction = WorkoutCalculator.calculate_age_reduction(self.user.age)
        if age_reduction > 0:
            ttk.Label(summary_frame,
                     text=f"Note: Workouts adjusted by {age_reduction}% for age",
                     foreground='orange').pack()
        
        # Workout plan display
        plan_frame = ttk.LabelFrame(parent, text="Your Weekly Workout Plan", padding="10")
        plan_frame.pack(fill=tk.BOTH, expand=True)
        
        workout_text = scrolledtext.ScrolledText(plan_frame, wrap=tk.WORD,
                                                 font=('Courier', 10),
                                                 height=20)
        workout_text.pack(fill=tk.BOTH, expand=True)
        
        for day_plan in self.workout_plan:
            workout_text.insert(tk.END, f"\n{'='*70}\n")
            workout_text.insert(tk.END, f"DAY {day_plan['day']}\n")
            workout_text.insert(tk.END, f"{'='*70}\n")
            workout_text.insert(tk.END, day_plan['workout'] + "\n")
        
        workout_text.config(state='disabled')
    
    def create_stats_tab(self, parent):
        """Create statistics and analytics tab"""
        if not self.user:
            ttk.Label(parent, text="Create a profile first",
                     font=('Helvetica', 12)).pack(pady=50)
            return
        
        # Statistics display
        stats = WorkoutStatistics.get_statistics(self.user)
        
        if 'error' in stats:
            ttk.Label(parent, text="Complete some workouts to see statistics!",
                     font=('Helvetica', 12)).pack(pady=50)
            return
        
        # Stats grid
        stats_container = ttk.Frame(parent)
        stats_container.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Configure grid
        for i in range(3):
            stats_container.columnconfigure(i, weight=1)
        
        # Stat cards
        stats_data = [
            ("Total Workouts", stats['total_workouts'], self.primary_color),
            ("Current Streak", f"{stats['current_streak']} days", self.secondary_color),
            ("Longest Streak", f"{stats['longest_streak']} days", self.accent_color),
            ("Weekly Average", f"{stats['weekly_average']:.1f}", self.success_color),
            ("Most Active Day", f"Day {stats['most_active_day']}", self.primary_color),
            ("Progress Logs", len(self.user.progress_log), self.secondary_color),
        ]
        
        row = 0
        col = 0
        for title, value, color in stats_data:
            self.create_stat_card(stats_container, title, str(value), color, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        # Recent activity
        recent_frame = ttk.LabelFrame(parent, text="Recent Activity", padding="10")
        recent_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        if self.user.progress_log:
            recent_text = scrolledtext.ScrolledText(recent_frame, wrap=tk.WORD,
                                                   font=('Helvetica', 10),
                                                   height=8)
            recent_text.pack(fill=tk.BOTH, expand=True)
            
            for i, log in enumerate(reversed(self.user.progress_log[-10:]), 1):
                recent_text.insert(tk.END, f"{i}. {log['date']} - Day {log['day']}")
                if log.get('notes'):
                    recent_text.insert(tk.END, f" - {log['notes']}")
                recent_text.insert(tk.END, "\n")
            
            recent_text.config(state='disabled')
    
    def create_stat_card(self, parent, title, value, color, row, col):
        """Create a statistic display card"""
        card = ttk.Frame(parent, relief="solid", borderwidth=1)
        card.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
        
        # Card content
        content_frame = ttk.Frame(card)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        ttk.Label(content_frame, text=title, font=('Helvetica', 10),
                 foreground='gray').pack()
        ttk.Label(content_frame, text=value, font=('Helvetica', 24, 'bold'),
                 foreground=color).pack()
    
    def create_weight_tab(self, parent):
        """Create weight tracking tab"""
        if not self.user:
            ttk.Label(parent, text="Create a profile first",
                     font=('Helvetica', 12)).pack(pady=50)
            return
        
        # Add weight section
        add_frame = ttk.LabelFrame(parent, text="Add Weight Entry", padding="10")
        add_frame.pack(fill=tk.X, pady=(0, 10))
        
        input_frame = ttk.Frame(add_frame)
        input_frame.pack()
        
        ttk.Label(input_frame, text="Weight:", font=('Helvetica', 10, 'bold')).grid(
            row=0, column=0, padx=5)
        weight_entry = ttk.Entry(input_frame, width=10, font=('Helvetica', 10))
        weight_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(input_frame, text="Unit:", font=('Helvetica', 10, 'bold')).grid(
            row=0, column=2, padx=5)
        unit_var = tk.StringVar(value='kg')
        unit_combo = ttk.Combobox(input_frame, textvariable=unit_var, width=8, state='readonly')
        unit_combo['values'] = ['kg', 'lbs']
        unit_combo.grid(row=0, column=3, padx=5)
        
        def add_weight():
            try:
                weight = float(weight_entry.get())
                WeightTracker.add_weight_entry(self.user, weight, unit_var.get())
                self.save_user_data()
                messagebox.showinfo("Success", "Weight entry added!")
                weight_entry.delete(0, tk.END)
                self.create_main_window()  # Refresh
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid weight")
        
        ttk.Button(input_frame, text="Add", command=add_weight,
                  style='Primary.TButton').grid(row=0, column=4, padx=10)
        
        # Weight statistics
        if self.user.weight_log:
            stats_frame = ttk.LabelFrame(parent, text="Weight Statistics", padding="10")
            stats_frame.pack(fill=tk.X, pady=(0, 10))
            
            weight_stats = WeightTracker.get_weight_statistics(self.user)
            trend = WeightTracker.get_weight_trend(self.user)
            
            stats_grid = ttk.Frame(stats_frame)
            stats_grid.pack()
            
            unit = self.user.weight_log[-1]['unit']
            stats_info = [
                ("Current", f"{weight_stats['current']:.1f} {unit}"),
                ("Starting", f"{weight_stats['starting']:.1f} {unit}"),
                ("Change", f"{weight_stats['total_change']:+.1f} {unit}"),
                ("Trend", trend),
            ]
            
            for i, (label, value) in enumerate(stats_info):
                ttk.Label(stats_grid, text=f"{label}:", font=('Helvetica', 10, 'bold')).grid(
                    row=0, column=i*2, padx=10, pady=5)
                ttk.Label(stats_grid, text=value, font=('Helvetica', 10)).grid(
                    row=0, column=i*2+1, padx=10, pady=5)
            
            # Weight history
            history_frame = ttk.LabelFrame(parent, text="Weight History", padding="10")
            history_frame.pack(fill=tk.BOTH, expand=True)
            
            history_text = scrolledtext.ScrolledText(history_frame, wrap=tk.WORD,
                                                    font=('Helvetica', 10),
                                                    height=10)
            history_text.pack(fill=tk.BOTH, expand=True)
            
            for i, entry in enumerate(reversed(self.user.weight_log), 1):
                history_text.insert(tk.END,
                                   f"{i}. {entry['date']}: {entry['weight']} {entry['unit']}\n")
            
            history_text.config(state='disabled')
        else:
            ttk.Label(parent, text="No weight entries yet. Add your first entry above!",
                     font=('Helvetica', 11), foreground='gray').pack(pady=30)
    
    def create_profile_tab(self, parent):
        """Create profile management tab"""
        profile_frame = ttk.Frame(parent)
        profile_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        if self.user:
            # Display current profile
            ttk.Label(profile_frame, text="Current Profile",
                     font=('Helvetica', 16, 'bold')).pack(pady=(0, 20))
            
            info_text = f"""
Name: {self.user.name}
Age: {self.user.age} years
Gender: {self.user.gender.capitalize()}
Goal: {WorkoutDatabase.GOAL_NAMES[self.user.goal - 1]}
Training Days: {self.user.training_days} days per week
Total Workouts Logged: {len(self.user.progress_log)}
Weight Entries: {len(self.user.weight_log)}
"""
            
            info_frame = ttk.LabelFrame(profile_frame, text="Profile Information", padding="20")
            info_frame.pack(fill=tk.X, pady=10)
            
            ttk.Label(info_frame, text=info_text, font=('Helvetica', 11),
                     justify=tk.LEFT).pack()
            
            ttk.Button(profile_frame, text="Update Profile",
                      command=self.show_profile_form,
                      style='Primary.TButton').pack(pady=10)
        else:
            ttk.Label(profile_frame, text="No Profile Created",
                     font=('Helvetica', 14, 'bold')).pack(pady=20)
            ttk.Label(profile_frame, text="Create your profile to start your fitness journey!",
                     font=('Helvetica', 11)).pack(pady=10)
            ttk.Button(profile_frame, text="Create Profile",
                      command=self.show_profile_form,
                      style='Primary.TButton').pack(pady=20)
    
    def show_profile_form(self):
        """Show profile creation/editing form"""
        form_window = tk.Toplevel(self.root)
        form_window.title("Profile")
        form_window.geometry("500x550")
        form_window.transient(self.root)
        form_window.grab_set()
        
        main_frame = ttk.Frame(form_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Your Profile", style='Header.TLabel').pack(pady=(0, 20))
        
        # Form fields
        fields_frame = ttk.Frame(main_frame)
        fields_frame.pack(fill=tk.X, pady=10)
        
        # Name
        ttk.Label(fields_frame, text="Name:", font=('Helvetica', 10, 'bold')).grid(
            row=0, column=0, sticky='w', pady=8)
        name_entry = ttk.Entry(fields_frame, width=30, font=('Helvetica', 10))
        name_entry.grid(row=0, column=1, pady=8, padx=10)
        if self.user:
            name_entry.insert(0, self.user.name)
        
        # Age
        ttk.Label(fields_frame, text="Age:", font=('Helvetica', 10, 'bold')).grid(
            row=1, column=0, sticky='w', pady=8)
        age_spinbox = ttk.Spinbox(fields_frame, from_=1, to=110, width=28, font=('Helvetica', 10))
        age_spinbox.grid(row=1, column=1, pady=8, padx=10)
        if self.user:
            age_spinbox.set(self.user.age)
        
        # Gender
        ttk.Label(fields_frame, text="Gender:", font=('Helvetica', 10, 'bold')).grid(
            row=2, column=0, sticky='w', pady=8)
        gender_var = tk.StringVar(value=self.user.gender if self.user else "male")
        gender_frame = ttk.Frame(fields_frame)
        gender_frame.grid(row=2, column=1, pady=8, padx=10, sticky='w')
        ttk.Radiobutton(gender_frame, text="Male", variable=gender_var, value="male").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(gender_frame, text="Female", variable=gender_var, value="female").pack(side=tk.LEFT, padx=10)
        
        # Goal
        ttk.Label(fields_frame, text="Fitness Goal:", font=('Helvetica', 10, 'bold')).grid(
            row=3, column=0, sticky='w', pady=8)
        goal_combo = ttk.Combobox(fields_frame, width=28, font=('Helvetica', 10), state='readonly')
        goal_combo['values'] = [f"{i+1}. {name}" for i, name in enumerate(WorkoutDatabase.GOAL_NAMES)]
        goal_combo.current((self.user.goal - 1) if self.user else 0)
        goal_combo.grid(row=3, column=1, pady=8, padx=10)
        
        # Training days
        ttk.Label(fields_frame, text="Training Days/Week:", font=('Helvetica', 10, 'bold')).grid(
            row=4, column=0, sticky='w', pady=8)
        days_spinbox = ttk.Spinbox(fields_frame, from_=1, to=7, width=28, font=('Helvetica', 10))
        days_spinbox.grid(row=4, column=1, pady=8, padx=10)
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
                
                if not name or not name.replace(" ", "").isalpha():
                    messagebox.showerror("Error", "Please enter a valid name")
                    return
                
                if not (1 <= age <= 110):
                    messagebox.showerror("Error", "Age must be between 1 and 110")
                    return
                
                if not (1 <= training_days <= 7):
                    messagebox.showerror("Error", "Training days must be between 1 and 7")
                    return
                
                # Preserve existing data if updating
                if self.user:
                    old_logs = self.user.progress_log
                    old_weight = self.user.weight_log
                    self.user = AdvancedUser(name, age, gender, goal, training_days)
                    self.user.progress_log = old_logs
                    self.user.weight_log = old_weight
                else:
                    self.user = AdvancedUser(name, age, gender, goal, training_days)
                
                self.workout_plan = WorkoutCalculator.generate_workout_plan(self.user)
                self.save_user_data()
                
                messagebox.showinfo("Success", "Profile saved successfully!")
                form_window.destroy()
                self.create_main_window()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers")
        
        ttk.Button(button_frame, text="Save Profile", command=save_profile,
                  style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Cancel", command=form_window.destroy,
                  style='Secondary.TButton').pack(side=tk.LEFT, padx=5)
    
    def show_log_workout(self):
        """Show workout logging dialog"""
        if not self.user:
            messagebox.showwarning("No Profile", "Please create a profile first!")
            return
        
        log_window = tk.Toplevel(self.root)
        log_window.title("Log Workout")
        log_window.geometry("450x350")
        log_window.transient(self.root)
        log_window.grab_set()
        
        main_frame = ttk.Frame(log_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Log Completed Workout", style='Header.TLabel').pack(pady=(0, 20))
        
        ttk.Label(main_frame, text="Which day did you complete?",
                 font=('Helvetica', 10, 'bold')).pack(pady=5)
        
        day_combo = ttk.Combobox(main_frame, width=20, state='readonly', font=('Helvetica', 10))
        day_combo['values'] = [f"Day {i}" for i in range(1, self.user.training_days + 1)]
        day_combo.current(0)
        day_combo.pack(pady=10)
        
        ttk.Label(main_frame, text="Notes (optional):",
                 font=('Helvetica', 10, 'bold')).pack(pady=5)
        notes_text = tk.Text(main_frame, height=6, width=40, font=('Helvetica', 10))
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
            self.create_main_window()
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Log Workout", command=save_log,
                  style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Cancel", command=log_window.destroy,
                  style='Secondary.TButton').pack(side=tk.LEFT, padx=5)
    
    def show_rest_recommendation(self):
        """Show rest day recommendation dialog"""
        if not self.user:
            messagebox.showwarning("No Profile", "Please create a profile first!")
            return
        
        should_rest, message = RestDayRecommender.should_rest_today(self.user)
        
        title = "Rest Day Recommendation"
        if should_rest:
            messagebox.showwarning(title, message)
        else:
            messagebox.showinfo(title, message)
    
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
                    f.write("Stay consistent and track your progress!\n")
                    f.write("=" * 80 + "\n")
                
                messagebox.showinfo("Success", f"Workout plan exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export file:\n{str(e)}")
    
    def save_user_data(self):
        """Save user data to JSON file"""
        if self.user:
            try:
                with open(self.data_file, 'w') as f:
                    json.dump(self.user.to_dict(), f, indent=2)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save data:\n{str(e)}")
    
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
            print(f"Error loading user data: {e}")
        return False


def main():
    """Main entry point"""
    root = tk.Tk()
    app = EnhancedGymWorkoutPlannerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

