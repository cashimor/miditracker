# ui.py (continued)

from PyQt5.QtWidgets import QMainWindow, QTableWidget, QVBoxLayout, QPushButton, QWidget, QTableWidgetItem

class TrackerApp(QMainWindow):
    def __init__(self, controller, midi_player):
        super().__init__()
        self.setWindowTitle('90s Sound Tracker')
        self.controller = controller
        self.midi_player = midi_player  # Pass the player to the UI

        # Main layout
        layout = QVBoxLayout()

        # Create a grid for notes (QTableWidget simulates tracker grid)
        self.grid = QTableWidget(16, 10)  # 16 rows (time steps) and 10 tracks
        layout.addWidget(self.grid)

        # Set track names as column headers
        track_names = [
            "Main Voice", "Chord 1", "Chord 2", "Chord 3", "Chord 4",
            "Kick", "Snare", "Open Hi-hat", "Closed Hi-hat", "Clap"
        ]
        self.grid.setHorizontalHeaderLabels(track_names)

        # Populate grid based on initial drum pattern
        self.update_grid()

        # Connect cell clicks to a function that updates the pattern
        self.grid.cellClicked.connect(self.toggle_step)

        # Add play and stop buttons
        self.play_button = QPushButton('Play')
        self.play_button.clicked.connect(self.start_playback)
        self.stop_button = QPushButton('Stop')
        self.stop_button.clicked.connect(self.stop_playback)
        layout.addWidget(self.play_button)
        layout.addWidget(self.stop_button)

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def update_grid(self):
        """Update the grid UI based on the drum pattern from the controller."""
        pattern = self.controller.get_pattern()
        for row in range(16):
            for col in range(10):
                if pattern[col][row] == 1:
                    self.grid.setItem(row, col, QTableWidgetItem("X"))
                else:
                    self.grid.setItem(row, col, QTableWidgetItem(""))

    def toggle_step(self, row, col):
        """Notify the controller to toggle the step in the model."""
        self.controller.toggle_step(col, row)
        self.update_grid()

    def start_playback(self):
        """Start the MIDI playback."""
        self.midi_player.start()

    def stop_playback(self):
        """Stop the MIDI playback."""
        self.midi_player.stop()

    def closeEvent(self, event):
        """Handle the window close event."""
        self.midi_player.stop()  # Ensure playback is stopped
        self.midi_player.close()  # Close MIDI resources
        event.accept()  # Allow the window to close