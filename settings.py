# Defines some general settings variables, like the used window resolution

# Window resolution.
# For convenience, we also store the halved values in variables 
# to make our code more readable.
WIN_RES = (WIDTH, HEIGHT) = 800, 450
HALF_WIDTH, HALF_HEIGHT = WIDTH // 2, HEIGHT // 2

# Focal length.
# Determines the angle of view (how much of the scene will be captured)
# and the magnification.
FOCAL_LEN = 250

# The default height of the horizon for mode-7 scenes if none else is specified.
# Choosing a quarter of the height of the frame has proven to be good in terms of perspective
# (consider the first F-Zero game on the Super Nintendo as an example).
STD_HORIZON = HALF_HEIGHT // 2

# scale factor for height of the stage (z axis in virtual coordinate system of environment)
SCALE = 20

# whether the game currently is in "creator mode", where the camera can move around freely in the scene
IN_DEV_MODE = True



# how dense the fog is in foggy scenes
FOG_DENSITY = 100

# how fast the player can move initially
INITIAL_PLAYER_MOVE_SPEED = 0.1

# how fast the player can rotate initially
INITIAL_PLAYER_ROTATION_SPEED = 0.05