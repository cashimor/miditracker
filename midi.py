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
        self.channel = 2  # MIDI channels are 0-indexed, so 3 is channel 2
        self.current_notes = [0] * 10
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

    def get_output_devices(self):
        # Get the number of available MIDI devices
        device_count = pygame.midi.get_count()

        # List to hold device names
        device_names = []

        # Loop through each device and get its name
        for device_id in range(device_count):
            info = pygame.midi.get_device_info(device_id)
            # info[1] is the device name, and info[3] indicates if it's an output device (1 for output)
            if info[3] == 1:  # Output devices only
                device_names.append(info[1].decode())  # info[1] returns a bytes object

        return device_names

    def set_output_device(self, device_name):
        self.stop()
        # Find the device ID that corresponds to the selected device name
        device_count = pygame.midi.get_count()
        for device_id in range(device_count):
            info = pygame.midi.get_device_info(device_id)
            if info[1].decode() == device_name and info[3] == 1:  # Output device
                # Close current output if any
                if self.midi_out:
                    self.midi_out.close()
                pygame.midi.quit()
                pygame.midi.init()
                # Open the new device
                self.midi_out = pygame.midi.Output(device_id)
                break

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
        for track in range(10):
            note = self.current_notes[track]
            if note > 0:
                channel = self.channel
                if track > 4:
                    channel = 9
                self.current_notes[track] = 0
                self.play_midi_off(channel,  note)

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
            if track < 5:
                note = pattern[track][self.current_step]
                if note > 0:
                    if self.current_notes[track] > 0:
                        self.play_midi_off(self.channel, self.current_notes[track])
                    self.play_midi_on(self.channel, note)
                    self.current_notes[track] = note
            else:
                if pattern[track][self.current_step] == 1:
                    if self.current_notes[track] > 0:
                       self.play_midi_off(9, self.current_notes[track])
                    note = self.midi_notes[track]
                    if note:
                        self.play_midi_on(9, note)
                        self.current_notes[track] = note

        # Move to the next step
        self.current_step = (self.current_step + 1) % 64

    def play_midi_on(self, channel, note):
        """Send a MIDI note-on and note-off message for the given note."""
        self.midi_out.note_on(note, 127, channel)  # Channel 10 is index 9

    def play_midi_off(self, channel, note):
        self.midi_out.note_off(note, 127, channel)

    def close(self):
        """Close the MIDI output."""
        self.midi_out.close()
        pygame.midi.quit()