import pygame.midi
import time
import threading

class MidiPlayer:
    def __init__(self, controller, bpm=120):

        self.controller = controller
        self.bpm = bpm
        self.is_playing = False
        self.current_step = 0
        self.play_thread = None
        pygame.midi.init()
        # Change the output to another device if needed...
        self.midi_out = pygame.midi.Output(0)  # Open MIDI output

        # Define MIDI notes for each track
        self.midi_notes = {
            0: None,  # Main Voice
            1: None,  # Chord 1
            2: None,  # Chord 2
            3: None,  # Chord 3
            4: None,  # Chord 4
            5: 35,    # Kick drum
            6: 38,    # Snare drum
            7: 46,    # Open Hi-hat
            8: 42,    # Closed Hi-hat
            9: 39     # Clap
        }

    def start(self):
        """Start playback in a separate thread."""
        if not self.is_playing:
            self.is_playing = True
            self.play_thread = threading.Thread(target=self.play_loop)
            self.play_thread.start()

    def stop(self):
        """Stop playback."""
        self.is_playing = False
        if self.play_thread is not None:
            self.play_thread.join()  # Wait for the thread to finish

    def play_loop(self):
        """Main loop for MIDI playback."""
        steps_per_second = (self.bpm / 60) * 4
        time_interval = 1 / steps_per_second

        while self.is_playing:
            self.play_step()
            time.sleep(time_interval)

    def play_step(self):
        """Play the notes for the current step in the drum pattern."""
        pattern = self.controller.get_pattern()

        for track in range(10):
            if pattern[track][self.current_step] == 1:
                note = self.midi_notes[track]
                if note:
                    self.play_midi_on(note)
        time.sleep(0.1)

        for track in range(10):
            if pattern[track][self.current_step] == 1:
                note = self.midi_notes[track]
                if note:
                    self.play_midi_off(note)

        # Move to the next step
        self.current_step = (self.current_step + 1) % 16

    def play_midi_on(self, note):
        """Send a MIDI note-on and note-off message for the given note."""
        self.midi_out.note_on(note, 127, 9)  # Channel 10 is index 9

    def play_midi_off(self, note):
        self.midi_out.note_off(note, 127, 9)

    def close(self):
        """Close the MIDI output."""
        self.midi_out.close()
        pygame.midi.quit()