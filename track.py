from collision import CollisionRect

import numpy # numpy arrays used for positions of rectangle colliders

# A class modelling (the collision map for) a race track.
# Objects of the class hold a name and several lists of collision rects
# modelling the track surface, ramps, different types of gimmicks and obstacles, ...
class Track:
    def __init__(self, name, track_surface_rects, key_checkpoint_rects):
        self.name = name
        self.track_surface_rects = track_surface_rects
        
        self.key_checkpoints = [KeyCheckpoint(kc_rect) for kc_rect in key_checkpoint_rects]

    # Determines whether the passed rectangular collider is on the track surface or not.
    # 
    # Parameters:
    # other (CollisionRect)
    def is_on_track(self, other):
        for rect_coll in self.track_surface_rects:
            if rect_coll.overlap(other):
                return True

    # Checks for each key checkpoint if the passed player collider
    # is over one (or more) key checkpoint.
    # If yes, these key checkpoints are marked as passed.
    def update_key_checkpoints(self, player_coll):
        for key_checkpoint in self.key_checkpoints:
            if key_checkpoint.collider.overlap(player_coll):
                key_checkpoint.passed = True
                print("key checkpoint passed!")

# A class that capsulates the creation of the objects representing the race tracks in memory
# to avoid crowding the main module.
#
# Holds several static methods to create the different tracks.
class TrackCreator:
    # Creates the collision shape for the track whose sprite is named "track_2023.png"
    def create_track_1():
        # left-most rect
        rect1 = CollisionRect(
            pos = numpy.array([27.165, -99.615]),
            w = 14.33,
            h = 144.77
        )

        # rect next to rect1's lower end
        rect2 = CollisionRect(
            pos = numpy.array([39.17, -162.635]),
            w = 9.68,
            h = 18.73
        )

        # lowest horizontal rect
        rect3 = CollisionRect(
            pos = numpy.array([47.815, -157.725]),
            w = 26.97,
            h = 8.91
        )

        # second vertical rect from the right
        rect4 = CollisionRect(
            pos = numpy.array([56.925, -142.14]),
            w = 8.69,
            h = 40.08
        )

        # middle horizontal rect
        rect5 = CollisionRect(
            pos = numpy.array([62.385, -125.59]),
            w = 19.55,
            h = 8.98
        )

        # right-most vertical rect
        rect6 = CollisionRect(
            pos = numpy.array([67.95, -86.495]),
            w = 8.42,
            h = 118.53
        )

        # top horizontal rect
        rect7 = CollisionRect(
            pos = numpy.array([46.08, -33.24]),
            w = 52.16,
            h = 11.86
        )

        return Track(
            name = "track 2023",
            track_surface_rects = [rect1, rect2, rect3, rect4, rect5, rect6, rect7],
            key_checkpoint_rects = [rect7]
        )

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