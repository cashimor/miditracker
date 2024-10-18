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
        self.pattern_sequence = [1] * 10  # Initially all pattern slots set to 0
        self.track_masks = [0b1111] * 10  # Initially all tracks enabled for each part (1111 = all tracks)


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
            'pattern_sequence': self.pattern_sequence,
            'track_masks': self.track_masks,
        }

    def set_song_data(self, data):
        """Load song data including all patterns and metadata."""
        self.patterns = data['patterns']
        self.metadata = data['metadata']
        if 'pattern_sequence' in data:
            self.pattern_sequence = data['pattern_sequence']
            self.track_masks = data['track_masks']

    def set_pattern_sequence(self, index, pattern_index):
        """Set a pattern in the sequence (index 0-9)."""
        if 0 <= index < 10:
            self.pattern_sequence[index] = pattern_index

    def set_track_mask(self, index, mask, value):
        """Set the 4-bit track mask for a particular pattern in the sequence."""
        print(f"{index} - {mask} - {value}")
        if 0 <= index < 10:
            if value == 1:
                self.track_masks[index] = self.track_masks[index] | mask
            else:
                self.track_masks[index] = self.track_masks[index] & (15 - mask)

    def get_pattern_sequence(self):
        """Return the current pattern sequence."""
        return self.pattern_sequence

    def get_track_masks(self):
        """Return the track masks for the pattern sequence."""
        return self.track_masks
