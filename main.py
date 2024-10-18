# main.py

import pygame.midi
import sys
from PyQt5.QtWidgets import QApplication
from controller import TrackerController
from midi import MidiPlayer
from model import TrackerPattern
from ui import TrackerApp

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
    pattern = TrackerPattern()

    # Initialize controller with the model
    controller = TrackerController(pattern)

    # Initialize MIDI player
    midi_player = MidiPlayer(controller)

    # Create and show the UI, passing the controller and MIDI player
    window = TrackerApp(controller, midi_player)
    window.show()

    # Start the event loop
    result = app.exec_()
    midi_player.close()
    sys.exit(result)
if __name__ == "__main__":
    main()