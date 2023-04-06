from collision import CollisionRect

import numpy # numpy arrays used for positions of rectangle colliders



# A class modelling a race track.
# Objects of the class hold a name and several lists of collision rects
# modelling the track surface, ramps, different types of gimmicks and obstacles, ...
class Track:
    def __init__(self, name, track_surface_rects):
        self.name = name
        self.track_surface_rects = track_surface_rects

    # Determines whether the passed rectangular collider is on the track surface or not.
    # 
    # Parameters:
    # other (CollisionRect)
    def is_on_track(self, other):
        for rect_coll in self.track_surface_rects:
            if rect_coll.overlap(other):
                return True

# A class that capsulates the creation of the objects representing the race tracks in memory
# to avoid crowding the main module.
#
# Holds several static methods to create the different tracks.
class TrackCreator:
    def create_track_1():
        rect1 = CollisionRect(
            pos = numpy.array([27.165, -99.615]),
            w = 14.33,
            h = 144.77
        )

        return Track(
            name = "track 2023",
            track_surface_rects = [rect1]
        )