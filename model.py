class TrackerPattern:
    def __init__(self, num_tracks=10, num_steps=64, num_patterns=4):
        self.num_tracks = num_tracks
        self.num_steps = num_steps
        self.num_patterns = num_patterns
        # Initialize multiple patterns (each pattern is a list of tracks and steps)
        self.patterns = [[[0 for _ in range(num_steps)] for _ in range(num_tracks)] for _ in range(num_patterns)]
        self.current_pattern_index = 0  # Start with the first pattern
        self.metadata = {
            'bpm': 120,  # Default BPM value
        }

    def get_bpm(self):
        return self.metadata['bpm']

    def set_bpm(self, bpm):
        self.metadata['bpm'] = bpm

    def toggle_step(self, track, step):
        """Toggle a step (mark/unmark) in the drum pattern for the current pattern."""
        if track > 4:
            self.patterns[self.current_pattern_index][track][step] = 1 - self.patterns[self.current_pattern_index][track][step]

    def get_pattern(self):
        """Return the current pattern."""
        return self.patterns[self.current_pattern_index]

    def set_pattern(self, pattern):
        """Set the current pattern."""
        self.patterns[self.current_pattern_index] = pattern

    def set_note_for_track(self, track, step, note):
        """Set a MIDI note for the specified track and step."""
        if track > 4:
            self.toggle_step(track, step)
        else:
            self.patterns[self.current_pattern_index][track][step] = note
        return self.patterns[self.current_pattern_index]

    def set_current_pattern(self, index):
        """Set the current pattern to a specified index."""
        if index < self.num_patterns:
            self.current_pattern_index = index
        else:
            raise ValueError("Pattern index out of range")

    # Song-related methods
    def get_song_data(self):
        """Return all patterns and metadata for saving."""
        return {
            'patterns': self.patterns,
            'metadata': self.metadata,
        }

    def set_song_data(self, data):
        """Load song data including all patterns and metadata."""
        self.patterns = data['patterns']
        self.metadata = data['metadata']