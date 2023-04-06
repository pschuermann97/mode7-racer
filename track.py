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
                return true