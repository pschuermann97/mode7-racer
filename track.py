# A class modelling (the collision map for) a race track.
# Objects of the class hold a name and several lists of collision rects
# modelling the track surface, ramps, different types of gimmicks and obstacles, ...
#
# Parameters floor_texture_path and bg_texture_path are the paths to the textures for the track and planet 
# as well as for the skybox-like background.
class Track:
    def __init__(self, name, track_surface_rects, key_checkpoint_rects, ramp_rects, finish_line_collider, 
            dash_plate_rects, recovery_rects, has_guard_rails):
        self.name = name

        self.track_surface_rects = track_surface_rects
        
        self.key_checkpoints = [KeyCheckpoint(kc_rect) for kc_rect in key_checkpoint_rects]

        self.ramp_rects = ramp_rects

        self.finish_line_collider = finish_line_collider

        self.dash_plate_rects = dash_plate_rects

        self.recovery_zone_rects = recovery_rects

        # Flag determining whether the track has solid borders or not
        # (in the latter case, the player just falls off the track)
        self.has_guard_rails = has_guard_rails


    
    # ------------------ methods for collision detection ---------------------------



    # These methods check whether a passed rectangular collider 
    # collides with something on the track.  



    # Determines whether the passed rectangular collider is on the track surface or not.
    # 
    # Parameters:
    # other (CollisionRect)
    def is_on_track(self, other):
        return collides_with_list(self.track_surface_rects, other)

    # Determines whether the passed rectangular collider hits a dash plate on the track or not.
    #
    # Parameters:
    # other (CollisionRect)
    def is_on_dash_plate(self, other):
        return collides_with_list(self.dash_plate_rects, other)

    # Determines whether the passed rectangular collider hits a recovery zone on the track.
    #
    # Parameters:
    # other (CollisionRect)
    def is_on_recovery_zone(self, other):
        return collides_with_list(self.recovery_zone_rects, other)

    # Determines whether the passed rectangular collider is on a ramp or not.
    #
    # Parameters:
    # other (CollisionRect)
    def is_on_ramp(self, other):
        return collides_with_list(self.ramp_rects, other)

    # Determines whether the passed rectangular collider is on the finish line or not.
    #
    # Parameters:
    # other (CollisionRect)
    def is_on_finish_line(self, other):
        return self.finish_line_collider.overlap(other)



    # --------------------- end of methods for collision detection ---------------------------



    # --------------------- methods for handling the key checkpoints on the track ------------------



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



    # ----------------- end of the methods for handling the key checkpoints on the track



    # Capsulates the check whether the guard rails on this track 
    # are active in a specific frame.
    # Note that this might not only depend on whether the track has guard rails
    # but also traps on the track might be able to temporarily disable the track's guard rails. 
    def guard_rails_active(self):
        return self.has_guard_rails



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

# Checks whether the passed rectangular collider
# collides with any of the colliders in the passed list.
#
# Parameters:
# list      - list of CollisionRect
# other     - CollisionRect
def collides_with_list(coll_list, other):
    for rect_coll in coll_list:
        if rect_coll.overlap(other):
            return True
    return False

