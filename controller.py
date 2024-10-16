import json

class TrackerController:
    def __init__(self, pattern):
        self.pattern = pattern  # Model (Pattern instance)

    def toggle_step(self, track, step):
        """Toggle a step in the drum pattern and return the updated pattern."""
        self.pattern.toggle_step(track, step)
        return self.pattern.get_pattern()

    def get_pattern(self):
        """Get the current drum pattern."""
        return self.pattern.get_pattern()

    def add_note_to_track(self, track, step, note):
        """Add a MIDI note to the specified track (e.g., main voice or chord track)."""
        # Assuming each step can hold one MIDI note value for now
        self.pattern.set_note_for_track(track, step, note)

    def get_bpm(self):
        return self.pattern.get_bpm()

    def set_bpm(self, bpm):
        self.pattern.set_bpm(bpm)

    # Adjust saving to include metadata
    def save_song(self, filepath):
        song_data = self.pattern.get_song_data()
        with open(filepath, 'w') as f:
            json.dump(song_data, f)
        print(f"Song saved to {filepath}")

    def load_song(self, filepath):
        with open(filepath, 'r') as f:
            song_data = json.load(f)
        self.pattern.set_song_data(song_data)
        print(f"Song loaded from {filepath}")

    def switch_to_pattern(self, pattern_index):
        """Switch to the pattern at the given index."""
        self.pattern.set_current_pattern(pattern_index);

