# A class modelling (the collision map for) a race track.
# Objects of the class hold a name and several lists of collision rects
# modelling the track surface, ramps, different types of gimmicks and obstacles, ...
#
# Parameters floor_texture_path and bg_texture_path are the paths to the textures for the track and planet 
# as well as for the skybox-like background.
class Track:
    def __init__(self, name, floor_texture_path, bg_texture_path, track_surface_rects, key_checkpoint_rects, ramp_rects, finish_line_collider, 
            required_laps, init_player_pos_x, init_player_pos_y, init_player_angle):
        self.name = name

        # texture variables
        self.floor_texture_path = floor_texture_path
        self.bg_texture_path = bg_texture_path

        self.track_surface_rects = track_surface_rects
        
        self.key_checkpoints = [KeyCheckpoint(kc_rect) for kc_rect in key_checkpoint_rects]

        self.ramp_rects = ramp_rects

        self.finish_line_collider = finish_line_collider

        self.player_completed_laps = 0 # race track counts laps the player has completed
        self.required_laps = required_laps

        # initial player position and rotation
        self.init_player_pos_x = init_player_pos_x
        self.init_player_pos_y = init_player_pos_y
        self.init_player_angle = init_player_angle

    # Determines whether the passed rectangular collider is on the track surface or not.
    # 
    # Parameters:
    # other (CollisionRect)
    def is_on_track(self, other):
        for rect_coll in self.track_surface_rects:
            if rect_coll.overlap(other):
                return True
        return False

    # Determines whether the passed rectangular collider is on a ramp or not.
    #
    # Parameters:
    # other (CollisionRect)
    def is_on_ramp(self, other):
        for rect_coll in self.ramp_rects:
            if rect_coll.overlap(other):
                return True
        return False

    # Checks for each key checkpoint if the passed player collider
    # is over one (or more) key checkpoint.
    # If yes, these key checkpoints are marked as passed.
    def update_key_checkpoints(self, player_coll):
        for key_checkpoint in self.key_checkpoints:
            if key_checkpoint.collider.overlap(player_coll):
                key_checkpoint.passed = True

    # First updates the passed flags of the key checkpoints.
    # Then checks whether the player has crossed the finish line.
    # If so all key checkpoints are reset after checking whether player has passed all of them
    # (if so, the player is credited a completed lap).
    def update_lap_count(self, player_coll):
        self.update_key_checkpoints(player_coll)

        # if player has crossed the finish line
        if self.finish_line_collider.overlap(player_coll):
            # if player has honestly finished a lap
            if self.all_key_checkpoints_passed():
                # Increment completed laps.
                # If player has completed enough laps, initialize the finish sequence.
                self.player_completed_laps += 1
                print(str(self.player_completed_laps) + " laps completed!")
                if self.player_completed_laps >= self.required_laps:
                    print("race finished!")
            self.reset_key_checkpoints()

    # Returns true if and only if 
    # the player has passed all key checkpoints on the track.
    def all_key_checkpoints_passed(self):
        for key_checkpoint in self.key_checkpoints:
            if not key_checkpoint.passed:
                return False
        return True

    # Sets the passed-flags of all key checkpoints to false.
    def reset_key_checkpoints(self):
        for key_checkpoint in self.key_checkpoints:
            key_checkpoint.passed = False



# A key checkpoint for the lap counting system.
# Consists of a CollisionRect and a passed-flag.
#
# If the player passes all key checkpoints and then the finish line,
# this counts as a completed lap.
# In either case, the list of passed key checkpoints is reset.
class KeyCheckpoint:
    # Creates a new key checkpoint instance with the passed collision rect.
    # Initially, the checkpoint is marked as not passed by the player.
    def __init__(self, collider):
        self.collider = collider
        self.passed = False



