# Settings for the race tracks and their collision maps.

import numpy # numpy arrays used for positions of rectangle colliders
from collision import CollisionRect
from track import Track, KeyCheckpoint 

# race configuration
STD_REQUIRED_LAPS = 3 # number of laps normally required to finish a race

# obstacle sizes for "prefab" obstacles
DASH_PLATE_HEIGHT = 1.5
DASH_PLATE_WIDTH = 1.5

# A class that capsulates the creation of the objects representing the race tracks in memory
# to avoid crowding the main module.
#
# Holds several static methods to create the different tracks.
class TrackCreator:
    # Creates the collision shape for the track whose sprite is named "track_2023.png"
    def create_track_2023():
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

        # (the only) dash plate
        dash_plate1 = CollisionRect(
            pos = numpy.array([32.4, -150.965]),
            w = DASH_PLATE_WIDTH,
            h = DASH_PLATE_HEIGHT
        )

        # (the only) recovery zone
        recovery_zone_1 = CollisionRect(
            pos = numpy.array([67.99, -75.64]),
            w = 2.28,
            h = 61.54
        )

        return Track(
            name = "track 2023",
            track_surface_rects = [rect1, rect2, rect3, rect4, rect5, rect6, rect7],
            key_checkpoint_rects = [rect7, rect5],
            ramp_rects = [ramp1],
            finish_line_collider = finish_line_coll,
            dash_plate_rects = [dash_plate1],
            recovery_rects = [recovery_zone_1],
            has_guard_rails = True
        )

    # for now this is just an empty track with the monochrome environment texture set
    def create_monochrome_track():
        finish_line_coll = CollisionRect(
            pos = numpy.array([1127.165, -116.6325]),
            w = 14.33,
            h = 1.145
        )

        track_surface = CollisionRect(
            pos = numpy.array([27.165, -116.6325]),
            w = 10000,
            h = 10000
        )

        return Track(
            name = "monochrome_track",
            track_surface_rects = [track_surface],
            key_checkpoint_rects = [],
            ramp_rects = [],
            finish_line_collider = finish_line_coll,
            dash_plate_rects = [],
            recovery_rects = [],
            has_guard_rails = False
        )

    # Creates the collision shape for the track whose sprite is named "track_2023_II.png".
    # For now, this is just the collision shape of the first track for testing purposes.
    def create_track_2023_II():
        # ------------ creating colliders for track ----------------------

        # ------------ rects kept from the first version of the track ----

        # top left-most rect
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

        # second-to-lowest horizontal rect
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

        # third-to-lowest horizontal rect
        rect5 = CollisionRect(
            pos = numpy.array([62.385, -125.59]),
            w = 19.55,
            h = 8.98
        )

        # top horizontal rect
        rect7 = CollisionRect(
            pos = numpy.array([46.08, -33.24]),
            w = 52.16,
            h = 11.86
        )

        # ------------ end of rects kept from the first version of the track ----

        # top right-most vertical rect
        rect8 = CollisionRect(
            pos = numpy.array([67.95, -45.725]),
            w = 8.42,
            h = 36.99
        )

        # bottom right-most vertical rect
        rect9 = CollisionRect(
            pos = numpy.array([67.95, -147.03]),
            w = 8.42,
            h = 97.135
        )

        # lowest horizontal rect
        rect10 = CollisionRect(
            pos = numpy.array([46.08, -191.55]),
            w = 52.16,
            h = 8.105
        )

        # lower left-most vertical rect
        rect11 = CollisionRect(
            pos = numpy.array([27.165, -186.8]),
            w = 14.33,
            h = 17.605
        )

        # second-to-top horizontal rect
        rect12 = CollisionRect(
            pos = numpy.array([56.43, -60.21]),
            w = 31.42,
            h = 8.01
        )

        # vertical rect connecting rects 12 and 14
        rect13 = CollisionRect(
            pos = numpy.array([44.82, -81.24]),
            w = 8.2,
            h = 50.06
        )

        # third-to-top horizontal rect
        rect14 = CollisionRect(
            pos = numpy.array([56.43, -102.47]),
            w = 31.42,
            h = 8.01
        )

        # ------------ end of track collider creation -------------------------

        # ------------ dash plate collider creation ---------------------------

        # first dash plate (in order of encounter when driving a normal lap)
        dash_plate1 = CollisionRect(
            pos = numpy.array([65.265, -136.89]),
            w = DASH_PLATE_WIDTH,
            h = DASH_PLATE_HEIGHT
        )

        # second dash plate (in order of encounter when driving a normal lap)
        dash_plate2 = CollisionRect(
            pos = numpy.array([70.756, -166.1]),
            w = DASH_PLATE_WIDTH,
            h = DASH_PLATE_HEIGHT
        )

        # third dash plate (in order of encounter when driving a normal lap)
        dash_plate3 = CollisionRect(
            pos = numpy.array([60.17, -188.88]),
            w = DASH_PLATE_WIDTH,
            h = DASH_PLATE_HEIGHT
        )

        # fourth dash plate (in order of encounter when driving a normal lap)
        dash_plate4 = CollisionRect(
            pos = numpy.array([39.89, -194.165]),
            w = DASH_PLATE_WIDTH,
            h = DASH_PLATE_HEIGHT
        )

        # left-most of the three dash plates before the small gap
        dash_plate_left = CollisionRect(
            pos = numpy.array([22.6, -179.17]),
            w = DASH_PLATE_WIDTH,
            h = DASH_PLATE_HEIGHT
        )

        # middle-one of the three dash plates before the small gap
        dash_plate_middle = CollisionRect(
            pos = numpy.array([25.235, -179.17]),
            w = DASH_PLATE_WIDTH,
            h = DASH_PLATE_HEIGHT
        )

        # right-most of the three dash plates before the small gap
        dash_plate_right = CollisionRect(
            pos = numpy.array([28, -179.17]),
            w = DASH_PLATE_WIDTH,
            h = DASH_PLATE_HEIGHT
        )

        # ------------ end of dash plate collider creation ---------------------------

        # finish line collider
        finish_line_coll = CollisionRect(
            pos = numpy.array([27.165, -116.6325]),
            w = 14.33,
            h = 1.145
        )

        # (the only) jump ramp
        ramp1 = CollisionRect(
            pos = numpy.array([27.165, -177.94]),
            w = 8.42,
            h = 0.12
        )

        # (the only) recovery
        recovery_zone_1 = CollisionRect(
            pos = numpy.array([56.81, -141.72]),
            w = 6.8,
            h = 24.21
        )

        return Track(
            name = "track 2023 II",
            track_surface_rects = [rect1, rect2, rect3, rect4, rect5, rect7, rect8, rect9, rect10, rect11, rect12, rect13, rect14],
            key_checkpoint_rects = [rect7, rect5],
            ramp_rects = [ramp1],
            finish_line_collider = finish_line_coll,
            dash_plate_rects = [dash_plate1, dash_plate2, dash_plate3, dash_plate4, dash_plate_left, dash_plate_middle, dash_plate_right],
            recovery_rects = [recovery_zone_1],
            has_guard_rails = True
        )

    # for now this is just an empty track with the monochrome environment texture set
    def create_event_horizon_track2():
        # finish line collider
        finish_line_coll = CollisionRect(
            pos = numpy.array([27.165, -95.3]),
            w = 14.33,
            h = 0.955
        )

        # -------------- track collision rect creation ---------------------

        # -------------- top left part of the track ------------------------

        # lower left-most rect
        rect1 = CollisionRect(
            pos = numpy.array([28.24, -111.04]),
            w = 14.08,
            h = 81.86
        )

        # top left-most rect
        rect2 = CollisionRect(
            pos = numpy.array([28.24, -34.39]),
            w = 14.08,
            h = 43.5
        )

        # third-to-top horizontal rect
        rect3 = CollisionRect(
            pos = numpy.array([52.3, -75.14]),
            w = 62.21,
            h = 10.06
        )

        # second-to-top horizontal rect
        rect4 = CollisionRect(
            pos = numpy.array([52.3, -51.35]),
            w = 62.21,
            h = 10.06
        )

        # top right-most vertical rect
        rect5 = CollisionRect(
            pos = numpy.array([79.01, -63.34]),
            w = 8.8,
            h = 33.85
        )

        # rect around the healing zone
        rect6 = CollisionRect(
            pos = numpy.array([35.78, -126.75]),
            w = 29.17,
            h = 50.44
        )

        # top horizontal rect
        rect7 = CollisionRect(
            pos = numpy.array([37.84, -16.7]),
            w = 33.45,
            h = 8.12
        )

        # small vertical rect before first jump
        rect8 = CollisionRect(
            pos = numpy.array([50.43, -23]),
            w = 8.27,
            h = 20.73
        )

        # -------------- end of rects for top left part of the track ----

        # -------------- rects for lower right part of the track -----------

        # left-most vertical rect
        rect9 = CollisionRect(
            pos = numpy.array([66.92, -124.9]),
            w = 8.545,
            h = 82.9
        )

        # lower horizontal rect
        rect10 = CollisionRect(
            pos = numpy.array([76.21, -162.47]),
            w = 13.56,
            h = 8.91
        )

        # right vertical rect
        rect11 = CollisionRect(
            pos = numpy.array([85.67, -148.74]),
            w = 8.2,
            h = 36.37
        )

        # top horizontal rect (right next to ramp)
        rect12 = CollisionRect(
            pos = numpy.array([84.735, -141.19]),
            w = 10.035,
            h = 21.26
        )

        # -------------- end of rects for lower right part of the track ----

        # -------------- end of track collision rect creation ---------------------

        # -------------- ramp collision rects creation ----------------------------

        ramp1 = CollisionRect(
            pos = numpy.array([50.4, -33.6]),
            w = 8.27,
            h = 0.23
        )

        ramp2 = CollisionRect(
            pos = numpy.array([79.16, -141.19]),
            w = 0.22,
            h = 21.26
        )

        # -------------- end of ramp collision rects creation ----------------------------

        # -------------- dash plate creation ---------------------------------------------

        # giant not-too-accurate dash plate before the first jump
        debug_dash_plate = CollisionRect(
            pos = numpy.array([50.4, -30.6]),
            w = 8.27,
            h = 0.23
        )

        # first dash plate when driving a proper lap around the track
        dash_plate1 = CollisionRect(
            pos = numpy.array([53.145, -71.66]),
            h = DASH_PLATE_HEIGHT,
            w = DASH_PLATE_WIDTH
        )

        # second dash plate when driving a proper lap around the track
        dash_plate2 = CollisionRect(
            pos = numpy.array([53.12, -54.52]),
            h = DASH_PLATE_HEIGHT,
            w = DASH_PLATE_WIDTH
        )

        # --------------- end of dash plate creation --------------------

        # only healing zone
        recovery_rect1 = CollisionRect(
            pos = numpy.array([36.07, -126.85]),
            w = 26.62,
            h = 48.51
        )

        return Track(
            name = "event_horizon_track2",
            track_surface_rects = [rect1, rect2, rect3, rect4, rect5, rect6, rect7, rect8, rect9, rect10, rect11, rect12],
            key_checkpoint_rects = [rect7, rect11, rect5],
            ramp_rects = [ramp1, ramp2],
            finish_line_collider = finish_line_coll,
            dash_plate_rects = [debug_dash_plate, dash_plate1, dash_plate2],
            recovery_rects = [recovery_rect1],
            has_guard_rails = True
        )