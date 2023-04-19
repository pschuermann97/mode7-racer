# Settings for the race tracks and their collision maps.

import numpy # numpy arrays used for positions of rectangle colliders
from collision import CollisionRect
from track import Track, KeyCheckpoint 

# race configuration
STD_REQUIRED_LAPS = 3 # number of laps normally required to finish a race

# A class that capsulates the creation of the objects representing the race tracks in memory
# to avoid crowding the main module.
#
# Holds several static methods to create the different tracks.
class TrackCreator:
    # Creates the collision shape for the track whose sprite is named "track_2023.png"
    def create_track_1():
        # creating colliders for track

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

        # end of track collider creation

        # finish line collider
        finish_line_coll = CollisionRect(
            pos = numpy.array([27.165, -116.6325]),
            w = 14.33,
            h = 1.145
        )

        # (the only) jump ramp
        ramp1 = CollisionRect(
            pos = numpy.array([67.95, -145.82]),
            w = 8.42,
            h = 0.12
        )

        return Track(
            name = "track 2023",
            floor_texture_path = "gfx/track_2023.png",
            bg_texture_path = "gfx/track_2023_bg_resized.png",
            track_surface_rects = [rect1, rect2, rect3, rect4, rect5, rect6, rect7],
            key_checkpoint_rects = [rect7, rect5],
            ramp_rects = [ramp1],
            finish_line_collider = finish_line_coll,
            required_laps = STD_REQUIRED_LAPS,
            init_player_pos_x = 25.55,
            init_player_pos_y = -119.78,
            init_player_angle = -111.56
        )

    def create_track_2():
        # for now this is just an empty track with the monochrome environment texture set
        finish_line_coll = CollisionRect(
            pos = numpy.array([1127.165, -116.6325]),
            w = 14.33,
            h = 1.145
        )

        track_surface = CollisionRect(
            pos = numpy.array([27.165, -116.6325]),
            w = 100,
            h = 100
        )

        return Track(
            name = "monochrome_track",
            floor_texture_path = "gfx/monochrome_track.png",
            bg_texture_path = "gfx/monochrome_track_bg.png",
            track_surface_rects = [track_surface],
            key_checkpoint_rects = [],
            ramp_rects = [],
            finish_line_collider = finish_line_coll,
            required_laps = STD_REQUIRED_LAPS,
            init_player_pos_x = 25.55,
            init_player_pos_y = -119.78,
            init_player_angle = -111.56
        )