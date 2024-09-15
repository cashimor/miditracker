# ui.py (continued)

from PyQt5.QtWidgets import QMainWindow, QTableWidget, QVBoxLayout, QPushButton, QWidget, QTableWidgetItem
from PyQt5.QtCore import Qt

def midi_to_note_name(midi_note):
    """Convert a MIDI note number (0-127) to a note name."""
    if midi_note is None or midi_note == 0:
        return ""
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = midi_note // 12  # Calculate the octave
    note = midi_note % 12  # Get the note within the octave
    return f"{note_names[note]}{octave}"

class TrackerApp(QMainWindow):
    def __init__(self, controller, midi_player):
        super().__init__()
        self.setWindowTitle('90s Sound Tracker')
        self.controller = controller
        self.midi_player = midi_player  # Pass the player to the UI
        self.current_octave = 4  # Default octave is 4
        self.cursor_track = 0
        self.cursor_step = 0

        # Mapping of keys to relative note positions (semitones)
        self.key_to_note = {
            'z': 0, 's': 1, 'x': 2, 'd': 3, 'c': 4,
            'v': 5, 'g': 6, 'b': 7, 'h': 8, 'n': 9,
            'j': 10, 'm': 11
        }

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

    def next_step(self):
        self.cursor_step = self.cursor_step + 1
        if self.cursor_step > 15:
            self.cursor_step = 0
        self.grid.setCurrentCell(self.cursor_step, self.cursor_track)

    def keyPressEvent(self, event):
        """Handle key press events for note entry."""
        key = event.text()

        # Handle number keys to change the octave
        if key in '01234567':
            self.current_octave = int(key)
            note = self.controller.get_pattern()[self.cursor_track][self.cursor_step]
            note = note % 12 + self.current_octave * 12
            self.controller.add_note_to_track(self.cursor_track, self.cursor_step, note)
            self.grid.setCurrentCell(0, 0)
            self.grid.setCurrentCell(9, 15)
            self.grid.setCurrentCell(self.cursor_step, self.cursor_track)

        # Handle note input
        if key in self.key_to_note:
            # Calculate the MIDI note based on the current octave and key
            note = (self.current_octave * 12) + self.key_to_note[key]
            # Add the note to the main voice track
            self.controller.add_note_to_track(self.cursor_track, self.cursor_step, note)
            self.next_step()

            # Optional: Play the note immediately for feedback
            # self.midi_player.play_midi(note)

        # Call the parent method for default key handling
        super().keyPressEvent(event)
        self.update_grid()

    def update_grid(self):
        """Update the table to display the current pattern."""
        pattern = self.controller.get_pattern()

        for row in range(16):  # 16 steps
            for col in range(10):  # 10 tracks
                if col < 5:
                    # Voice and chord tracks: display note names
                    midi_note = pattern[col][row]
                    note_name = midi_to_note_name(midi_note)  # Convert MIDI note to note name
                    item = QTableWidgetItem(note_name)
                    # item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Disable editing
                    self.grid.setItem(row, col, item)

                else:
                    # Drum tracks: display 'X' if the value is 1
                    value = pattern[col][row]
                    if value == 1:
                        self.grid.setItem(row, col, QTableWidgetItem("X"))
                    else:
                        self.grid.setItem(row, col, QTableWidgetItem(""))

    def toggle_step(self, row, col):
        if col < 5:
            self.cursor_track = col
        self.cursor_step = row

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