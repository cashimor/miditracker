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