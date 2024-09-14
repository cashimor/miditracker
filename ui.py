from PyQt5.QtWidgets import QMainWindow, QTableWidget, QVBoxLayout, QPushButton, QWidget

class TrackerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('90s Sound Tracker')

        # Main layout
        layout = QVBoxLayout()

        # Create a grid for notes (QTableWidget simulates tracker grid)
        # Now there are 10 columns for 10 tracks (main voice, chords, drums, etc.)
        self.grid = QTableWidget(16, 10)  # 16 rows (time steps) and 10 tracks
        layout.addWidget(self.grid)

        # Set track names as column headers
        track_names = [
            "Main Voice", "Chord 1", "Chord 2", "Chord 3", "Chord 4",
            "Kick", "Snare", "Open Hi-hat", "Closed Hi-hat", "Clap"
        ]
        self.grid.setHorizontalHeaderLabels(track_names)

        # Add buttons for play/stop
        self.play_button = QPushButton('Play')
        self.stop_button = QPushButton('Stop')
        layout.addWidget(self.play_button)
        layout.addWidget(self.stop_button)

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)