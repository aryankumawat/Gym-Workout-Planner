# 🖥️ GUI Version User Guide

## Overview

The GUI (Graphical User Interface) version provides a modern, user-friendly interface with buttons, forms, and windows that you can click and navigate with your mouse.

## Starting the GUI

Run the following command:
```bash
python3 gym_gui.py
```

A window will open with the main menu.

## Main Window

When you launch the application, you'll see:

### Header
- **Title**: "🏋️ Gym Workout Planner" in large, green text
- **Welcome Message**: Shows your name if you have a profile, or a welcome message

### Main Menu Buttons (in a 3x2 grid)

**Row 1:**
1. **👤 Create/Update Profile** - Create or edit your profile
2. **📋 View Workout Plan** - See your personalized workout plan
3. **💾 Export Workout Plan** - Save your plan to a text file

**Row 2:**
4. **✓ Log Workout** - Mark a workout as completed
5. **📊 View Progress** - See your workout history
6. **ℹ️ About** - Learn about the application

**Bottom:**
- **❌ Exit** - Close the application

### Footer
- Shows author information at the bottom

## Using Each Feature

### 1️⃣ Create/Update Profile

**Click the "👤 Create/Update Profile" button**

A new window opens with a form containing:
- **Name**: Text field for your name
- **Age**: Number selector (1-110)
- **Gender**: Radio buttons (Male/Female)
- **Fitness Goal**: Dropdown menu with 6 options:
  1. Losing Weight
  2. Staying Calm and Relax
  3. Increasing Heart Rate
  4. Stronger Legs
  5. Stronger ABS
  6. Stronger Shoulders and Arms
- **Training Days/Week**: Number selector (1-7)

**Buttons:**
- **💾 Save Profile**: Saves your information
- **❌ Cancel**: Closes the window without saving

### 2️⃣ View Workout Plan

**Click the "📋 View Workout Plan" button**

Opens a large window showing:
- **Header**: Your name and "Personalized Workout Plan"
- **Profile Information Box**: Shows your age, gender, goal, training days
  - If applicable, shows age adjustment percentage
- **Weekly Workout Plan**: Scrollable text area with all your daily workouts
  - Each day is clearly separated
  - Shows exercise names, reps/mins, and sets

**Button:**
- **Close**: Returns to main menu

### 3️⃣ Export Workout Plan

**Click the "💾 Export Workout Plan" button**

Opens a file save dialog:
- Choose where to save the file
- Default filename includes your name and timestamp
- Saves as a nicely formatted text file
- Shows success message with file location

### 4️⃣ Log Workout

**Click the "✓ Log Workout" button**

Opens a dialog window with:
- **Day Selection**: Dropdown to choose which day you completed
- **Notes Field**: Large text box for optional notes
  - Record how you felt
  - Note any achievements
  - Track weights used, etc.

**Buttons:**
- **✓ Log Workout**: Saves the workout log
- **Cancel**: Closes without saving

### 5️⃣ View Progress

**Click the "📊 View Progress" button**

Opens a window showing:
- **Total Workouts Completed**: Number at the top
- **Workout History**: Scrollable list showing:
  - Date and time of each workout
  - Which day you completed
  - Your notes (if any)

**Button:**
- **Close**: Returns to main menu

### 6️⃣ About

**Click the "ℹ️ About" button**

Shows a popup with:
- Application version
- Author information
- Feature list
- Credits

**Button:**
- **OK**: Closes the popup

## Tips for Using the GUI

### Navigation
- **Click buttons** to navigate between features
- **Close windows** by clicking the X or Close button
- **Fill forms** by clicking in fields and typing

### Data Entry
- **Name field**: Type your full name
- **Number fields**: Use arrow buttons or type directly
- **Dropdowns**: Click to see options, then select
- **Radio buttons**: Click to select (only one can be selected)
- **Text areas**: Click and type, supports multiple lines

### Error Messages
- **Red error boxes**: Show validation errors
  - Read the message
  - Fix the issue
  - Try again
- **Yellow warnings**: Show missing information
  - Create a profile first if needed

### Success Messages
- **Green success boxes**: Confirm actions worked
  - Profile saved
  - Workout logged
  - File exported

## Keyboard Shortcuts

- **Tab**: Move between form fields
- **Enter**: Submit forms (when focused on a button)
- **Esc**: Close some dialogs
- **Ctrl+Q** or **Cmd+Q**: Quit application

## Window Management

### Resizing
- Most windows can be resized by dragging edges
- Main window starts at 900x700 pixels
- Minimum sizes are set for readability

### Multiple Windows
- Profile and other dialogs open on top of main window
- Complete your action in the dialog before returning to main menu
- Some dialogs are "modal" (must be closed before using main window)

## Color Scheme

The GUI uses a professional color scheme:
- **Green (#4CAF50)**: Primary buttons and headers
- **Blue (#2196F3)**: Secondary buttons
- **Orange (#FF9800)**: Accents
- **Light Gray (#f0f0f0)**: Backgrounds
- **Dark Gray (#333333)**: Text

## Scrolling

Large content areas have scrollbars:
- **Workout Plan**: Scroll to see all days
- **Progress History**: Scroll to see all logged workouts
- **Notes Field**: Scroll when writing long notes

Use:
- Mouse wheel to scroll
- Click and drag scrollbar
- Arrow keys when focused in text area

## File Operations

### Saving Profile
- Automatically saves to `user_data.json`
- Saves on every profile update
- Loads automatically on startup

### Exporting Workouts
- Opens file browser dialog
- Choose location and filename
- Creates formatted text file
- Can be opened in any text editor

## Troubleshooting

### GUI doesn't open
```bash
# Check if tkinter is installed
python3 -m tkinter

# A test window should appear
```

### Window appears but is blank
- Wait a few seconds for loading
- Try closing and reopening
- Check terminal for error messages

### Buttons don't work
- Make sure window is focused (click on it)
- Try clicking directly on button text
- Check if a dialog window is open on top

### Can't type in fields
- Click inside the field first
- Make sure no other dialog is open
- Check if field is read-only (some dropdowns)

### Changes not saving
- Click "Save" button before closing
- Check for error messages
- Verify `user_data.json` file permissions

## Differences from Terminal Version

| Feature | GUI Version | Terminal Version |
|---------|-------------|------------------|
| Interface | Windows & Buttons | Text & Numbers |
| Navigation | Click buttons | Type numbers |
| Forms | Visual forms | Question prompts |
| Display | Formatted windows | Plain text |
| Scrolling | Mouse wheel | Page through |
| Colors | Full color | ANSI colors |
| Ease of Use | Very intuitive | Requires typing |

## System Requirements

- **Python**: 3.6 or higher
- **Tkinter**: Included with Python
- **Operating System**: 
  - macOS ✅
  - Windows ✅
  - Linux ✅ (may need `python3-tk` package)

## Getting Help

If you encounter issues:
1. Check this guide
2. Read the main README.md
3. Check terminal output for errors
4. Verify Python and tkinter installation

## Best Practices

1. **Create Profile First**: Before using other features
2. **Save Often**: Click save when making changes
3. **Export Plans**: Save before going to gym
4. **Log Consistently**: Track every workout
5. **Add Notes**: Record useful information
6. **Review Progress**: Check history regularly

---

**Enjoy your fitness journey with the GUI version!** 💪🖥️

