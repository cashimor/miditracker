class DrumController:
    def __init__(self, drum_pattern):
        self.drum_pattern = drum_pattern  # Model (DrumPattern instance)

    def toggle_step(self, track, step):
        """Toggle a step in the drum pattern and return the updated pattern."""
        self.drum_pattern.toggle_step(track, step)
        return self.drum_pattern.get_pattern()

    def get_pattern(self):
        """Get the current drum pattern."""
        return self.drum_pattern.get_pattern()