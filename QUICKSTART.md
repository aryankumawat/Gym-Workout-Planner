# 🚀 Quick Start Guide

## Run the Program

**GUI Version (Recommended - with graphical interface):**
```bash
python3 gym_gui.py
```

**Terminal Version (command-line interface):**
```bash
python3 gym.py
```

Both versions have the same features, choose the one you prefer!

## First Time Users

When you run the program for the first time, you'll see a menu like this:

```
================================================================================
                           GYM WORKOUT PLANNER                           
================================================================================

Main Menu:
  1. Create Profile
  2. View Workout Plan
  3. Export Workout Plan
  4. Log Completed Workout
  5. View Progress History
  6. About
  0. Exit

Enter your choice: 
```

## Step-by-Step Guide

### 1️⃣ Create Your Profile

Select option `1` and enter:
- **Name**: Your full name (e.g., "John Doe")
- **Age**: Your age in years (1-110)
- **Gender**: male or female
- **Goal**: Choose from 1-6:
  1. Losing Weight
  2. Staying Calm and Relax
  3. Increasing Heart Rate
  4. Stronger Legs
  5. Stronger ABS
  6. Stronger Shoulders and Arms
- **Training Days**: How many days per week (1-7)

### 2️⃣ View Your Workout Plan

Select option `2` to see your personalized weekly workout plan with:
- Your profile information
- Age-adjusted exercises (if applicable)
- Daily workout routines
- Exercise details (reps/mins and sets)

### 3️⃣ Export Your Plan

Select option `3` to save your workout plan as a text file:
- File is saved as `workout_plan_[YourName]_[timestamp].txt`
- Can be printed or shared
- Great for gym reference

### 4️⃣ Track Your Progress

Select option `4` after completing a workout:
- Choose which day you completed
- Add optional notes
- Build your workout history

### 5️⃣ View Your Progress

Select option `5` to see:
- Total workouts completed
- Dates and times of each workout
- Your notes for each session

## Example Usage

```
1. Start the program
2. Create profile (Name: Sarah, Age: 28, Gender: female, Goal: 4 - Stronger Legs, Days: 5)
3. View workout plan
4. Complete Day 1 workout at gym
5. Come back and log it: Menu → 4 → Day 1 → Add notes
6. Repeat for each workout day!
7. Export plan to take to gym: Menu → 3
```

## Tips 💡

- **First time?** Just follow the prompts - the program guides you through everything
- **Need a reminder?** Your profile is automatically saved and loads when you restart
- **Going to the gym?** Export your plan to have it on paper
- **Track consistently** Log your workouts to stay motivated
- **Update anytime** You can create a new profile anytime to change your goals

## Sample Workout Output

```
================================================================================
                              SARAH'S WORKOUT PLAN                              
================================================================================

Profile:
  Age: 28 years
  Gender: Female
  Goal: Stronger Legs
  Training Days: 5 days per week

--------------------------------------------------------------------------------
Day 1
--------------------------------------------------------------------------------
Gym workout for strong legs

Back squats (10 reps x 5 sets)
Hip thrusts (12 reps x 3 sets)
Overhead presses (10 reps x 5 sets)
Rack pulls (10 reps x 5 sets)
Squats (10 reps x 4 sets)
Dumbbell lunges (10 reps x 3 sets)
Leg curls (15 reps x 3 sets)
Standing calf raises (20 reps x 2 sets)
```

## Need Help?

- Select option `6` in the main menu to see the About section
- Read the full `readme.md` for detailed information
- All your data is saved in `user_data.json` (don't delete this!)

---

**Ready to start your fitness journey? Run `python3 gym.py` now!** 💪

