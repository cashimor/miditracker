import time
import mido
from mido import Message

class MidiPlayer:
    def __init__(self, controller, bpm=120):
        self.controller = controller  # Controller to access the drum pattern
        self.bpm = bpm
        self.is_playing = False
        self.current_step = 0
        self.midi_out = mido.open_output()  # Open a MIDI output (virtual or real)

        # Define the MIDI notes for each track
        self.midi_notes = {
            0: None,     # Main Voice (no sound in MIDI)
            1: None,     # Chord 1 (optional, no drum sound in MIDI)
            2: None,     # Chord 2 (optional, no drum sound in MIDI)
            3: None,     # Chord 3 (optional, no drum sound in MIDI)
            4: None,     # Chord 4 (optional, no drum sound in MIDI)
            5: 35,       # Kick drum
            6: 38,       # Snare drum
            7: 46,       # Open Hi-hat
            8: 42,       # Closed Hi-hat
            9: 39        # Clap
        }

    def start(self):
        """Start the playback loop."""
        self.is_playing = True
        steps_per_second = (self.bpm / 60) * 4  # 4 steps per beat
        time_interval = 1 / steps_per_second

        while self.is_playing:
            self.play_step()
            time.sleep(time_interval)  # Wait for the next step

    def stop(self):
        """Stop the playback."""
        self.is_playing = False

    def play_step(self):
        """Play the notes for the current step in the drum pattern."""
        pattern = self.controller.get_pattern()  # Get the current drum pattern

        for track in range(10):
            if pattern[track][self.current_step] == 1:
                note = self.midi_notes[track]
                if note:
                    self.play_midi(note)

        # Move to the next step
        self.current_step = (self.current_step + 1) % 16

    def play_midi(self, note):
        """Send a MIDI note-on and note-off message for the given note."""
        self.midi_out.send(Message('note_on', note=note, velocity=64, channel=9))  # Channel 10 is index 9
        time.sleep(0.1)  # Short delay for the note to sound
        self.midi_out.send(Message('note_off', note=note, velocity=64, channel=9))