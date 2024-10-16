# ui.py (continued)

from PyQt5.QtWidgets import QMainWindow, QTableWidget, QVBoxLayout, QPushButton, QWidget, QTableWidgetItem, QFileDialog
from PyQt5.QtWidgets import QHBoxLayout, QComboBox, QLabel, QSpinBox
from PyQt5.QtGui import QFontDatabase, QFont, QPalette, QColor

def midi_to_note_name(midi_note):
    """Convert a MIDI note number (0-127) to a note name."""
    if midi_note is None or midi_note == 0:
        return ""
    if midi_note == 128:
        return "REST"
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

        font_db = QFontDatabase()
        font_id = font_db.addApplicationFont("C64_Pro_Mono-STYLE.ttf")
        if font_id != -1:  # Font was loaded successfully
            c64_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.c64_font = QFont(c64_family, 11)
        else:  # Fallback to a standard monospace font
            self.c64_font = QFont("Courier", 11)  # Choose a common monospace font like Courier

        # Set the background to black and text to green (90s terminal style)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0))  # Black background
        palette.setColor(QPalette.WindowText, QColor(0, 255, 0))  # Green text
        self.setPalette(palette)

        # Main layout
        layout = QVBoxLayout()

        # Add BPM control
        bpm_layout = QHBoxLayout()
        bpm_label = QLabel("BPM:")
        bpm_label.setFont(self.c64_font)
        self.bpm_input = QSpinBox()
        self.bpm_input.setFont(self.c64_font)
        self.bpm_input.setRange(60, 240)  # Set BPM range
        self.bpm_input.setValue(self.controller.get_bpm())
        bpm_layout.addWidget(bpm_label)
        bpm_layout.addWidget(self.bpm_input)

        self.bpm_input.valueChanged.connect(self.update_bpm)

        # Create a horizontal layout for the Save and Load buttons
        button_layout = QHBoxLayout()

        # Create a grid for notes (QTableWidget simulates tracker grid)
        self.grid = QTableWidget(64, 10)  # 64 rows (time steps) and 10 tracks
        self.grid.setFont(self.c64_font)
        self.grid.setStyleSheet("QTableWidget { background-color: black; color: green; gridline-color: green; }"
                                "QTableWidget::item { border: 1px solid green; }")
        self.grid.horizontalHeader().setFont(self.c64_font)  # Horizontal headers (top)
        self.grid.verticalHeader().setFont(self.c64_font)  # Vertical headers (side)
        layout.addWidget(self.grid)

        # Set track names as column headers
        track_names = [
            "Main", "1", "2", "3", "4",
            "Kick", "Snare", "Open", "Closed", "Clap"
        ]
        self.grid.setHorizontalHeaderLabels(track_names)

        # Populate grid based on initial drum pattern
        self.update_grid()

        # Connect cell clicks to a function that updates the pattern
        self.grid.cellClicked.connect(self.toggle_step)

        # Add play and stop buttons
        self.play_button = QPushButton('Play')
        self.play_button.setFont(self.c64_font)
        self.play_button.setStyleSheet("QPushButton { background-color: green; color: black; }")
        self.play_button.clicked.connect(self.start_playback)
        self.stop_button = QPushButton('Stop')
        self.stop_button.setStyleSheet("QPushButton { background-color: green; color: black; }")
        self.stop_button.setFont(self.c64_font)
        self.stop_button.clicked.connect(self.stop_playback)


        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.stop_button)

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Add Save and Load buttons
        self.save_button = QPushButton('Save Song')
        self.save_button.setStyleSheet("QPushButton { background-color: green; color: black; }")
        self.save_button.setFont(self.c64_font)
        self.load_button = QPushButton('Load Song')
        self.load_button.setStyleSheet("QPushButton { background-color: green; color: black; }")
        self.load_button.setFont(self.c64_font)

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.load_button)

        # Connect buttons to their respective functions
        self.save_button.clicked.connect(self.save_song)
        self.load_button.clicked.connect(self.load_song)

        layout.addLayout(bpm_layout)
        layout.addLayout(button_layout)

        # Create a dropdown menu (QComboBox) for MIDI output devices
        self.midi_device_dropdown = QComboBox()
        self.midi_device_dropdown.setFont(self.c64_font)

        # Populate the dropdown with MIDI output devices
        self.update_midi_device_list()

        # When a user selects a device, call the method to set it
        self.midi_device_dropdown.currentIndexChanged.connect(self.on_device_selected)

        layout.addWidget(self.midi_device_dropdown)

        self.setLayout(layout)

        # Set the minimum size of the window based on your layout needs
        # Assuming each column is 50px wide and you have 10 columns
        column_width = 102
        number_of_columns = 10
        extra_padding = 60  # For padding, margins, and scroll bars
        button_height = 40  # Estimated height for buttons
        number_of_cells_visible = 16

        # Set the minimum size
        self.setMinimumSize(column_width * number_of_columns + extra_padding, button_height * number_of_cells_visible)


    def save_song(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Song", "", "Song Files (*.json)")
        if file_path:
            self.controller.save_song(file_path)

    def load_song(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Song", "", "Song Files (*.json)")
        if file_path:
            self.controller.load_song(file_path)
        self.update_grid()


    def next_step(self):
        self.cursor_step = self.cursor_step + 1
        if self.cursor_step > 63:
            self.cursor_step = 0
        self.grid.setCurrentCell(self.cursor_step, self.cursor_track)

    def keyPressEvent(self, event):
        """Handle key press events for note entry."""
        self.cursor_track = self.grid.currentColumn()
        self.cursor_step = self.grid.currentRow()

        key = event.text()
        if key in 'a':
            self.controller.add_note_to_track(self.cursor_track, self.cursor_step, 128)
            self.next_step()

        if key in 'f':
            self.controller.add_note_to_track(self.cursor_track, self.cursor_step, 0)
            self.next_step()

        # Handle number keys to change the octave
        if key in '01234567':
            self.current_octave = int(key)
            note = self.controller.get_pattern()[self.cursor_track][self.cursor_step]
            note = note % 12 + self.current_octave * 12
            self.controller.add_note_to_track(self.cursor_track, self.cursor_step, note)
            self.grid.setCurrentCell(0, 0)
            self.grid.setCurrentCell(9, 63)
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

        for row in range(64):  # 64 steps
            for col in range(10):  # 10 tracks
                if col < 5:
                    # Voice and chord tracks: display note names
                    midi_note = pattern[col][row]
                    note_name = midi_to_note_name(midi_note)  # Convert MIDI note to note name
                    item = QTableWidgetItem(note_name)
                    self.grid.setItem(row, col, item)

                else:
                    # Drum tracks: display 'X' if the value is 1
                    value = pattern[col][row]
                    if value == 1:
                        self.grid.setItem(row, col, QTableWidgetItem("X"))
                    else:
                        self.grid.setItem(row, col, QTableWidgetItem(""))
        self.bpm_input.setValue(self.controller.get_bpm())

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

    def update_midi_device_list(self):
        # Get the list of MIDI devices from the controller
        devices = self.midi_player.get_output_devices()

        # Clear the dropdown and repopulate with the new list
        self.midi_device_dropdown.clear()
        self.midi_device_dropdown.addItems(devices)

    def on_device_selected(self, index):
        # Get the selected device name from the dropdown
        selected_device = self.midi_device_dropdown.itemText(index)

        # Pass the selected device to the controller
        self.midi_player.set_output_device(selected_device)

    def update_bpm(self, value):
        self.controller.set_bpm(value)