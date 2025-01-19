import sys
import csv
import os
from datetime import datetime, timedelta
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget


class PomodoroApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pomodoro Timer")

        # Make the window smaller
        self.resize(150, 100)

        # Set a custom icon
        self.setWindowIcon(QIcon("inner.png"))  # Replace "icon.png" with the path to your icon file

        # Keep the window on top
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        # Timer and state variables
        self.total_time = 50 * 60  # 25 minutes in seconds
        self.time_left = self.total_time
        self.distractions = 0
        self.timer_running = False
        self.start_time = None  # To track session start time

        # Layout
        self.layout = QVBoxLayout()

        # Timer Label
        self.timer_label = QLabel(self.format_time(self.time_left), self)
        self.timer_label.setStyleSheet("font-size: 24px;")  # Adjust font size for a smaller window
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.timer_label)

        # Distraction Label
        self.distraction_label = QLabel("Distracted: 0", self)
        self.distraction_label.setStyleSheet("font-size: 16px;")  # Adjust font size for a smaller window
        self.distraction_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.distraction_label)

        # Distraction Buttons
        distraction_layout = QHBoxLayout()
        self.plus_one_button = QPushButton("+1")
        self.plus_one_button.clicked.connect(lambda: self.add_distraction(1))
        distraction_layout.addWidget(self.plus_one_button)

        self.plus_two_button = QPushButton("+2")
        self.plus_two_button.clicked.connect(lambda: self.add_distraction(2))
        distraction_layout.addWidget(self.plus_two_button)

        self.plus_three_button = QPushButton("+3")
        self.plus_three_button.clicked.connect(lambda: self.add_distraction(3))
        distraction_layout.addWidget(self.plus_three_button)

        self.layout.addLayout(distraction_layout)

        # Control Buttons
        control_layout = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_timer)
        control_layout.addWidget(self.start_button)

        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_timer)
        control_layout.addWidget(self.pause_button)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(lambda: self.reset_timer(save=True))
        control_layout.addWidget(self.reset_button)

        self.layout.addLayout(control_layout)

        # Container
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        # QTimer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        # CSV File
        self.csv_file = "pomodoro_sessions.csv"
        self.initialize_csv()

    def initialize_csv(self):
        """Initialize the CSV file if it doesn't exist."""
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Start Time", "End Time", "Session Length", "Distractions"])

    def start_timer(self):
        """Start the timer."""
        if not self.timer_running:
            if self.start_time is None:  # Record session start time only once
                self.start_time = datetime.now()
            self.timer.start(1000)  # Tick every 1 second
            self.timer_running = True

    def pause_timer(self):
        """Pause the timer."""
        self.timer.stop()
        self.timer_running = False

    def reset_timer(self , save = True):
        """Reset the timer and save session data to CSV."""
        # Save the session to CSV
        if save :
            self.save_session_to_csv()

        # Reset variables
        self.timer.stop()
        self.time_left = self.total_time
        self.distractions = 0
        self.timer_running = False
        self.start_time = None

        # Update labels
        self.timer_label.setText(self.format_time(self.time_left))
        self.distraction_label.setText("Distracted: 0")

    def update_timer(self):
        """Update the timer every second."""
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.setText(self.format_time(self.time_left))
        else:
            self.timer.stop()
            self.timer_running = False
            # Save the session when the time runs out
            self.save_session_to_csv()
            self.reset_timer(save = False)

    def add_distraction(self, increment):
        """Add a distraction count."""
        self.distractions += increment
        self.distraction_label.setText(f"Distracted: {self.distractions}")

    def save_session_to_csv(self):
        """Save the current session data to a CSV file."""
        if self.start_time is None:
            return  # No session to save if timer wasn't started

        now = datetime.now()
        session_length = now - self.start_time

        # Format session length as HH:MM:SS
        session_length_str = str(timedelta(seconds=session_length.seconds))

        with open(self.csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                self.start_time.strftime("%Y-%m-%d"),      # Date
                self.start_time.strftime("%H:%M:%S"),      # Start Time
                now.strftime("%H:%M:%S"),                  # End Time
                session_length_str,                        # Session Length
                self.distractions                          # Distractions
            ])

    def closeEvent(self, event):
        """Handle app close event to save session data."""
        if self.start_time:  # Only save if the timer was started
            self.save_session_to_csv()
        event.accept()  # Accept the close event

    @staticmethod
    def format_time(seconds):
        """Format seconds into MM:SS format."""
        mins, secs = divmod(seconds, 60)
        return f"{mins:02}:{secs:02}"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PomodoroApp()
    window.show()
    sys.exit(app.exec_())
