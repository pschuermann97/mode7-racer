# A data class holding all data that belongs to a race.
# This includes:
# - file paths to floor and background sprites
# - the function that creates the collision map for the track that is played in this race
# - the number of laps required to win the race
# - the mode of the race (grand-prix, time-attack, ...)
class Race:
    def __init__(self, race_track_creator, floor_tex_path, bg_tex_path, required_laps, 
            init_player_pos_x, init_player_pos_y, init_player_angle, race_mode):
        # create collision map for played track using the passed function
        self.race_track = race_track_creator()
        
        # environment textures
        self.floor_texture_path = floor_tex_path
        self.bg_texture_path = bg_tex_path
        
        # lap counting
        self.player_completed_laps = 0
        self.required_laps = required_laps

        # initial player position and rotation
        self.init_player_pos_x = init_player_pos_x
        self.init_player_pos_y = init_player_pos_y
        self.init_player_angle = init_player_angle
        
        self.race_mode = race_mode

    # Returns True if and only if the registered player 
    # has finished the race on this track 
    # (i.e. finished the required number of laps).  
    def player_finished_race(self):
        return self.player_completed_laps >= self.required_laps

    # API for the App class to poll whether player has completed at least one lap.
    # Idea: player should only be able to boost after first lap completed
    def player_completed_first_lap(self):
        return self.player_completed_laps >= 1

    # First updates the passed flags of the key checkpoints of the track that this race is played on.
    # Then checks whether the player has crossed the finish line.
    # If so all key checkpoints are reset after checking whether player has passed all of them
    # (if so, the player is credited a completed lap).
    def update_lap_count(self, player_coll):
        self.race_track.update_key_checkpoints(player_coll)

        # if player has crossed the finish line
        if self.race_track.is_on_finish_line(player_coll):
            # if player has honestly finished a lap
            if self.race_track.all_key_checkpoints_passed():
                # Increment completed laps.
                # If player has completed enough laps, initialize the finish sequence.
                self.player_completed_laps += 1
                print(str(self.player_completed_laps) + " laps completed!")
                if self.player_finished_race():
                    print("race finished!")
            self.race_track.reset_key_checkpoints()



    # ------------- exposure of RaceTrack API ---------------------

    def is_on_track(self, other):
        return self.race_track.is_on_track(other)

    def is_on_dash_plate(self, other):
        return self.race_track.is_on_dash_plate(other)

    def is_on_recovery_zone(self, other):
        return self.race_track.is_on_recovery_zone(other)
    
    def is_on_ramp(self, other):
        return self.race_track.is_on_ramp(other)

    # ------------- end of exposure of RaceTrack API --------------