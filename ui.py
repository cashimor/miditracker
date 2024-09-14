# ui.py

from PyQt5.QtWidgets import QMainWindow, QTableWidget, QVBoxLayout, QPushButton, QWidget, QTableWidgetItem

class TrackerApp(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.setWindowTitle('90s Sound Tracker')
        self.controller = controller  # The controller is passed to the UI

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

        # Add buttons for play/stop
        self.play_button = QPushButton('Play')
        self.stop_button = QPushButton('Stop')
        layout.addWidget(self.play_button)
        layout.addWidget(self.stop_button)

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def update_grid(self):
        """Update the grid UI based on the drum pattern from the controller."""
        pattern = self.controller.get_pattern()  # Get data from the controller
        for row in range(16):
            for col in range(10):
                if pattern[col][row] == 1:
                    self.grid.setItem(row, col, QTableWidgetItem("X"))
                else:
                    self.grid.setItem(row, col, QTableWidgetItem(""))

    def toggle_step(self, row, col):
        """Notify the controller to toggle the step in the model."""
        self.controller.toggle_step(col, row)  # Update data via controller
        self.update_grid()  # Refresh the UI based on updated data