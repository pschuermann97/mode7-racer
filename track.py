# A class modelling (the collision map for) a race track.
# Objects of the class hold a name and several lists of collision rects
# modelling the track surface, ramps, different types of gimmicks and obstacles, ...
#
# Parameters floor_texture_path and bg_texture_path are the paths to the textures for the track and planet 
# as well as for the skybox-like background.
class Track:
    def __init__(self, name, track_surface_rects, key_checkpoint_rects, ramp_rects, finish_line_collider, 
            dash_plate_rects, recovery_rects):
        self.name = name

        self.track_surface_rects = track_surface_rects
        
        self.key_checkpoints = [KeyCheckpoint(kc_rect) for kc_rect in key_checkpoint_rects]

        self.ramp_rects = ramp_rects

        self.finish_line_collider = finish_line_collider

        self.dash_plate_rects = dash_plate_rects

        self.recovery_zone_rects = recovery_rects

    # Determines whether the passed rectangular collider is on the track surface or not.
    # 
    # Parameters:
    # other (CollisionRect)
    def is_on_track(self, other):
        for rect_coll in self.track_surface_rects:
            if rect_coll.overlap(other):
                return True
        return False

    # Determines whether the passed rectangular collider hits a dash plate on the track or not.
    #
    # Parameters:
    # other (CollisionRect)
    def is_on_dash_plate(self, other):
        for rect_coll in self.dash_plate_rects:
            if rect_coll.overlap(other):
                return True
        return False

    # Determines whether the passed rectangular collider hits a recovery zone on the track.
    #
    # Parameters:
    # other (CollisionRect)
    def is_on_recovery_zone(self, other):
        for rect_coll in self.recovery_zone_rects:
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

    # Determines whether the passed rectangular collider is on the finish line or not.
    #
    # Parameters:
    # other (CollisionRect)
    def is_on_finish_line(self, other):
        return self.finish_line_collider.overlap(other)

    # Checks for each key checkpoint if the passed player collider
    # is over one (or more) key checkpoint.
    # If yes, these key checkpoints are marked as passed.
    def update_key_checkpoints(self, player_coll):
        for key_checkpoint in self.key_checkpoints:
            if key_checkpoint.collider.overlap(player_coll):
                key_checkpoint.passed = True

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



