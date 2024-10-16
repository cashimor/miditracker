# model.py

class TrackerPattern:
    def __init__(self, num_tracks=10, num_steps=64):
        self.num_tracks = num_tracks
        self.num_steps = num_steps
        # Initialize drum pattern (0 = unmarked, 1 = marked)
        self.pattern = [[0 for _ in range(num_steps)] for _ in range(num_tracks)]
        self.metadata = {
            'bpm': 120,  # Default BPM value
        }

    def get_bpm(self):
        return self.metadata['bpm']

    def set_bpm(self, bpm):
        self.metadata['bpm'] = bpm

    def toggle_step(self, track, step):
        """Toggle a step (mark/unmark) in the drum pattern."""
        if track > 4:
          self.pattern[track][step] = 1 - self.pattern[track][step]

    def get_pattern(self):
        """Return the current pattern."""
        return self.pattern

    def set_pattern(self, pattern):
        self.pattern = pattern

    def set_note_for_track(self, track, step, note):
        """Set a MIDI note for the specified track and step."""
        if track > 4:
            self.toggle_step(track, step)
            return self.pattern
        self.pattern[track][step] = note
        return self.pattern
