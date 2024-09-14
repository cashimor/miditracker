# main.py

import sys
from PyQt5.QtWidgets import QApplication
from model import TrackerPattern
from controller import TrackerController
from ui import TrackerApp
from midi import MidiPlayer
import pygame.midi

def list_midi_devices():
    pygame.midi.init()
    for i in range(pygame.midi.get_count()):
        info = pygame.midi.get_device_info(i)
        (interface, name, is_input, is_output, opened) = info
        print(f"ID: {i} | Name: {name.decode()} | Output: {is_output}")
    pygame.midi.quit()

def main():
    list_midi_devices()

    # Create an instance of QApplication
    app = QApplication(sys.argv)

    # Initialize model (DrumPattern)
    drum_pattern = TrackerPattern()

    # Initialize controller with the model
    controller = TrackerController(drum_pattern)

    # Initialize MIDI player
    midi_player = MidiPlayer(controller, bpm=120)

    # Create and show the UI, passing the controller and MIDI player
    window = TrackerApp(controller, midi_player)
    window.show()

    # Start the event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()