import pygame

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

# whether the game currently is in "developer mode", where the camera can move around freely in the scene
IN_DEV_MODE = False

# whether collisions with the track borders and obstacles are being detected (i.e. solid)
COLLISION_DETECTION_OFF = False

# how dense the fog is in foggy scenes
FOG_DENSITY = 100

# physics variables of the player machine
PLAYER_MAX_SPEED = 0.05
PLAYER_ACCELERATION = PLAYER_MAX_SPEED / 500 # how fast the player can accelerate
PLAYER_BRAKE = PLAYER_ACCELERATION * 2 # how strong the players brakes are
PLAYER_SPEED_LOSS = PLAYER_ACCELERATION / 3 # how much speed the player loses when neither accelerating nor braking
PLAYER_CENTRIFUGAL_FORCE = 0.5 # centrifugal force applied in corners (more precisely, percentage of max speed that is applied as centrifugal force)
PLAYER_COLLISION_RECT_WIDTH = 1 # width of the player collider
PLAYER_COLLISION_RECT_HEIGHT = 1 # height of the player collider
PLAYER_LOOKAHEAD_RECT_WIDTH = 1 # width of the collider that is used to "look ahead" to check whether the player will leave the track in the next frame
PLAYER_LOOKAHEAD_RECT_HEIGHT = 2 # height of the collider that is used to "look ahead"
JUMP_DURATION = 2 # duration of a jump in seconds
JUMP_HEIGHT = 100 # maximum height the player gains throughout a jump (compared to its standard y coordinate)

# Quadratic function that computes the height of the player during a jump
# based on the time since the player jumped off the track.
# Uses configuration variables for jumping from the physics section.
def HEIGHT_DURING_JUMP(time):
    return - ( ( time - ( JUMP_DURATION / 2 ) ) * ( time - ( JUMP_DURATION / 2 ) ) ) + JUMP_HEIGHT

# how fast the player can rotate initially
INITIAL_PLAYER_ROTATION_SPEED = 0.01

# initial position/roation of the player in the logical world space
INITIAL_PLAYER_POSITION_X = 25.55
INITIAL_PLAYER_POSITION_Y = -119.78
INITIAL_PLAYER_ANGLE = -111.56

# how fast the background moves when the player rotates
BACKGROUND_ROTATION_SPEED = 50

# standard key bindings for racing mode movement
STD_ACCEL_KEY = pygame.K_SPACE # space = accelerate
STD_BRAKE_KEY = pygame.K_s # S = brake 
STD_LEFT_KEY = pygame.K_a # A = rotate left
STD_RIGHT_KEY = pygame.K_d # D = rotate right

# standard paths for the sprites used in the game
PLAYER_SPRITE_PATH = 'gfx/violet_machine.png'