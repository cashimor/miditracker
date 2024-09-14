# main.py

import sys
from PyQt5.QtWidgets import QApplication
from model import DrumPattern
from controller import DrumController
from ui import TrackerApp

def main():
    # Create an instance of QApplication
    app = QApplication(sys.argv)

    # Initialize model (DrumPattern)
    drum_pattern = DrumPattern()

    # Initialize controller with the model
    controller = DrumController(drum_pattern)

    # Create and show the UI, passing the controller to it
    window = TrackerApp(controller)
    window.show()

    # Start the event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()