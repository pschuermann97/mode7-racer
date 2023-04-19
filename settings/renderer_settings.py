# Settings for the Mode7 renderer

# Window resolution.
# For convenience, we also store the halved values in variables 
# to make our code more readable.
WIN_RES = (WIDTH, HEIGHT) = 400, 225
HALF_WIDTH, HALF_HEIGHT = WIDTH // 2, HEIGHT // 2

# Focal length.
# Determines the angle of view (how much of the scene will be captured)
# and the magnification.
FOCAL_LEN = 250

# The default height of the horizon for mode-7 scenes if none else is specified.
# Choosing a quarter of the height of the frame has proven to be good in terms of perspective
# (consider the first F-Zero game on the Super Nintendo as an example).
STD_HORIZON = HALF_HEIGHT // 2

# the distance that the camera keeps from the player by default
CAM_DISTANCE = 4

# the pixel position that the player sprite has on the screen 
# when the player is driving on the track (i.e. not jumping/falling off)
NORMAL_ON_SCREEN_PLAYER_POSITION_X = 176
NORMAL_ON_SCREEN_PLAYER_POSITION_Y = 120

# scale factor for height of the stage (z axis in virtual coordinate system of environment)
SCALE = 20

# how dense the fog is in foggy scenes
FOG_DENSITY = 100

# how fast the background moves when the player rotates
BACKGROUND_ROTATION_SPEED = 50

