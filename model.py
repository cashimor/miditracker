# model.py

class DrumPattern:
    def __init__(self, num_tracks=10, num_steps=16):
        self.num_tracks = num_tracks
        self.num_steps = num_steps
        # Initialize drum pattern (0 = unmarked, 1 = marked)
        self.pattern = [[0 for _ in range(num_steps)] for _ in range(num_tracks)]

    def toggle_step(self, track, step):
        """Toggle a step (mark/unmark) in the drum pattern."""
        self.pattern[track][step] = 1 - self.pattern[track][step]

    def get_pattern(self):
        """Return the current drum pattern."""
        return self.pattern