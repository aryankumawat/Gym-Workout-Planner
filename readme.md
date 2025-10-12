# Gym Workout Planner

An interactive, personalized gym workout planning platform that creates customized training programs based on your age, gender, fitness goals, and training schedule.

## Features

- **Personalized Workout Plans**: Get customized workout routines tailored to your specific goals
- **User Profiles**: Save and load your personal information
- **Progress Tracking**: Log your completed workouts and track your fitness journey
- **Age-Adjusted Intensity**: Automatically adjusts workout intensity based on age
- **Export Functionality**: Save your workout plan as a text file
- **Beautiful Graphical Interface**: Modern GUI with buttons and forms
- **Data Persistence**: Your profile and progress are automatically saved
- **Two Versions**: Choose between GUI (graphical) or Terminal (command-line) interface

## Workout Goals

Choose from 6 different fitness goals:
1. **Losing Weight** - Fat-burning focused exercises
2. **Staying Calm and Relax** - Stretching and relaxation routines
3. **Increasing Heart Rate** - High-intensity cardio exercises
4. **Stronger Legs** - Lower body strength training
5. **Stronger ABS** - Core strengthening exercises
6. **Stronger Shoulders and Arms** - Upper body strength training

## Getting Started

### Prerequisites

- Python 3.6 or higher
- No external dependencies required! Uses only Python standard library

### Installation

1. Clone or download this repository
2. Navigate to the project directory:
```bash
cd Gym-Workout-Planner
```

### Running the Program

**GUI Version (Recommended):**
```bash
python3 gym_gui.py
```

**Terminal Version:**
```bash
python3 gym.py
```

Or make them executable:
```bash
chmod +x gym_gui.py gym.py
./gym_gui.py  # GUI version
./gym.py      # Terminal version
```

## How to Use

> **For detailed GUI instructions, see [GUI_GUIDE.md](GUI_GUIDE.md)**
> 
> **For quick start, see [QUICKSTART.md](QUICKSTART.md)**

### First Time Setup

1. **Launch the program** - Run `python3 gym_gui.py` (GUI) or `python3 gym.py` (Terminal)
2. **Create your profile**:
   - Enter your name
   - Enter your age (1-110)
   - Select your biological sex (male/female)
   - Choose your fitness goal (1-6)
   - Specify training days per week (1-7)
3. **View your personalized workout plan**

### Main Menu Options

#### 1. Create/Update Profile
- Create a new profile or update your existing one
- All changes are automatically saved

#### 2. View Workout Plan
- See your complete weekly workout routine
- View profile information
- Check age-adjusted workout intensity

#### 3. Export Workout Plan
- Save your workout plan as a text file
- File includes complete profile and all workout days
- Timestamped filename for easy organization

#### 4. Log Completed Workout
- Track which workouts you've completed
- Add optional notes for each session
- Build your workout history

#### 5. View Progress History
- See all your completed workouts
- View dates and notes for each session
- Track your total workout count

#### 6. About
- Learn more about the application
- View features and version information

#### 0. Exit
- Safely exit the program
- All data is automatically saved

## Workout Plan Details

### Age-Based Adjustments

The program automatically adjusts workout intensity based on age:
- **Ages 60-65**: 0-5% reduction
- **Ages 65-75**: 5-25% reduction
- **Ages 75-80**: 25-40% reduction
- **Ages 80+**: 40-80% reduction (capped at 80%)

### Workout Structure

Each workout plan includes:
- Exercise name
- Number of repetitions or duration
- Number of sets
- Adjusted intensity based on age

### Training Schedule

The program intelligently alternates between:
- Your goal-specific workout
- Age and gender-appropriate general workout

This ensures balanced training that targets your specific goals while maintaining overall fitness.

## Data Storage

- Profile data is saved in `user_data.json`
- Automatically loads on program start
- Exported workout plans saved as `workout_plan_[name]_[timestamp].txt`

## Technical Details

### Architecture

The program is built with a clean, object-oriented architecture:

- **`Colors`** - ANSI color codes for terminal styling
- **`WorkoutDatabase`** - Stores all workout routines and goal information
- **`User`** - Represents user profile with serialization support
- **`WorkoutCalculator`** - Handles workout adjustments and plan generation
- **`GymWorkoutPlanner`** - Main application class with menu system

### Code Quality

- Type hints for better code clarity
- Comprehensive docstrings
- Error handling for user input
- Clean separation of concerns
- Easy to maintain and extend

## Example Workout Categories

### 1. Fat Loss Workout
- Plate thrusters
- Mountain climbers
- Box jumps
- Lunges
- And more...

### 2. Stretch and Relax
- Quad stretches
- Hamstring stretches
- Chest and shoulder stretches
- And more...

### 3. High-Intensity Exercises
- Jumping jacks
- Sprints
- Mountain climbers
- Squat jumps
- And more...

### 4. Strong Legs
- Back squats
- Hip thrusts
- Overhead presses
- Rack pulls
- And more...

### 5. Strong ABS
- Cross crunches
- Knee ups
- Hip thrusts
- Dragon flags
- And more...

### 6. Strong Shoulders and Arms
- Bench presses
- Triceps dips
- Pull ups
- Bent over rows
- And more...

## Contributing

Feel free to fork this project and submit pull requests with improvements!

### Ideas for Enhancement
- Add custom workout creation
- Include rest day recommendations
- Add weight tracking
- Include nutrition tips
- Create workout reminders
- Add exercise videos/images

## Author

**Aryan Kumawat**

## License

This project is available for personal and educational use.

## Acknowledgments

- Thanks to all fitness enthusiasts who inspired this project
- Built with Python and passion for fitness

---

**Stay consistent, track your progress, and achieve your fitness goals!**

