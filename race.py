# A data class holding all data that belongs to a race.
# This includes:
# - file paths to floor and background sprites
# - the function that creates the collision map for the track
# - the number of laps required to win the race
# - the mode of the race (grand-prix, time-attack, ...)
class Race:
    def __init__(self, race_track_creator, floor_tex_path, bg_tex_path, required_laps, race_mode):
        self.race_track_creator = race_track_creator # function that creates the collision map for the race track
        self.floor_tex_path = floor_tex_path
        self.bg_tex_path = bg_tex_path
        self.required_laps = required_laps
        self.race_mode = race_mode

    def get_track(self):
        return self.race_track_creator()