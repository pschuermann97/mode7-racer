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

SCALE = 100

# how dense the fog is in foggy scenes
FOG_DENSITY = 100

# how fast the player can initially move
INITIAL_PLAYER_MOVE_SPEED = 7