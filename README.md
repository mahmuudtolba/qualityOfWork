# Pomodoro Timer

A lightweight Pomodoro timer application built with PyQt5, designed to help you boost productivity and track distractions during your focus sessions.

---

## Features

- **Timer**: A 50-minute timer to follow the Pomodoro technique.
- **Distraction Tracking**: Log distractions (+1, +2, or +3) during your session.
- **Session History**: Automatically save session data, including start time, end time, session length, and distractions, to a CSV file.
- **User-Friendly UI**: Simple and intuitive interface for easy interaction.
- **Stay on Top**: Always-on-top window to keep the timer visible.
- **Custom Icon**: Option to add a custom window icon.

---

## How to Use

1. **Start the Timer**: Click the `Start` button to begin your session.
2. **Pause the Timer**: Click the `Pause` button to pause the session if needed.
3. **Reset the Timer**: Click the `Reset` button to stop the session, log it to the CSV file, and reset the timer.
4. **Log Distractions**: Use the `+1`, `+2`, or `+3` buttons to track distractions during the session.

---

## Installation

### Prerequisites

- Python 3.x
- PyQt5 library
- pyinstaller

### Setup

1. Clone or download the repository:
   ```bash
   git clone https://github.com/mahmuudtolba/pomodoro-timer.git
   cd pomodoro-timer
2. pyinstaller --onefile --windowed --icon=outer.png main.py
