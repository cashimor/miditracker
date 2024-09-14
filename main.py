import sys
from PyQt5.QtWidgets import QApplication
from ui import TrackerApp  # Import your UI code

def main():
    # Create an instance of QApplication
    app = QApplication(sys.argv)

    # Create an instance of your UI
    window = TrackerApp()

    # Show the UI
    window.show()

    # Start the event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()