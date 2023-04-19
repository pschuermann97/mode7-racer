import pygame
from machine import Machine

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
PLAYER_COLLISION_RECT_WIDTH = 1 # width of the player collider (the same for all machines)
PLAYER_COLLISION_RECT_HEIGHT = 1 # height of the player collider
JUMP_HEIGHT = 100 # maximum height the player gains throughout a jump (compared to its standard y coordinate)


# machines that are playable in the game

PURPLE_COMET = Machine(
    max_speed = 0.05,
    acceleration = 0.05 / 750, # 750 frame update units to get to top speed
    brake = (0.05 / 750) * 2, # brake is twice as strong as accelerator
    speed_loss = (0.05 / 750) / 3, # speed loss is a third the strength of the accelerator
    centri = 0.5, # 50% of current speed applied as centrifugal force
    jump_duration_multiplier = 2 / 0.05, # jump should last 2 seconds if machine at max speed
    rotation_speed = 0.01,
    idle_image_path = 'gfx/violet_machine.png',
    shadow_image_path = 'gfx/violet_machine_shadow.png'
)


# Quadratic function that computes the height of the player during a jump
# based on the time since the player jumped off the track.
# 
# Parameters:
# time: time since the player lift off (in seconds)
# jump_duration: the duration of the entire jump from start to landing
def HEIGHT_DURING_JUMP(time, jump_duration):
    return - ( time * ( time - jump_duration ) ) * JUMP_HEIGHT


# initial position/roation of the player in the logical world space
INITIAL_PLAYER_POSITION_X = 25.55
INITIAL_PLAYER_POSITION_Y = -119.78
INITIAL_PLAYER_ANGLE = -111.56

# how fast the background moves when the player rotates
BACKGROUND_ROTATION_SPEED = 50

# UI screen coordinates

# shield meter
SHIELD_METER_HEIGHT = 16

# speed meter
SPEED_METER_DIGIT_SPRITE_WIDTH = 16
SPEED_METER_DIGIT_SPRITE_HEIGHT = 16
RIGHT_MOST_SPEEDMETER_DIGIT_SCREEN_X_COORD = WIDTH - SPEED_METER_DIGIT_SPRITE_WIDTH
SPEED_METER_DIGIT_SCREEN_Y_COORD = HEIGHT - 1.5 * SPEED_METER_DIGIT_SPRITE_HEIGHT # no padding in sprite so we add one of 12px in code

# timer
TIMER_DIGIT_SPRITE_WIDTH = SPEED_METER_DIGIT_SPRITE_WIDTH
TIMER_DIGIT_SPRITE_HEIGHT = SPEED_METER_DIGIT_SPRITE_HEIGHT
RIGHT_MOST_TIMER_DIGIT_SCREEN_X_COORD = WIDTH - TIMER_DIGIT_SPRITE_WIDTH
TIMER_DIGIT_SCREEN_Y_COORD = SHIELD_METER_HEIGHT # timer should be right below the shield meter
TIMER_PADDING = TIMER_DIGIT_SPRITE_WIDTH / 2 # padding between minutes and seconds, seconds and milliseconds
# Computes the individual x offset for the timer digits
# (note that there are gaps 
# between the digits for the minutes and seconds + seconds and milliseconds)
def TIMER_DIGIT_X_OFFSET(i):
    if i <= 2: # milliseconds digits
        return RIGHT_MOST_TIMER_DIGIT_SCREEN_X_COORD - TIMER_DIGIT_SPRITE_WIDTH * i
    if i > 2 and i <= 4: # seconds digits
        return RIGHT_MOST_TIMER_DIGIT_SCREEN_X_COORD - TIMER_DIGIT_SPRITE_WIDTH * i - TIMER_PADDING
    return RIGHT_MOST_TIMER_DIGIT_SCREEN_X_COORD - TIMER_DIGIT_SPRITE_WIDTH * i - TIMER_PADDING * 2 # minute digits

# end of UI screen coordinates

# other UI configuration
SPEED_DISPLAY_MULTIPLIER = 1426 / PLAYER_MAX_SPEED # so max speed will be shown as 1426 km/h

# standard key bindings for racing mode movement
STD_ACCEL_KEY = pygame.K_SPACE # space = accelerate
STD_BRAKE_KEY = pygame.K_s # S = brake 
STD_LEFT_KEY = pygame.K_a # A = rotate left
STD_RIGHT_KEY = pygame.K_d # D = rotate right

# standard paths for the sprites used in the game
PLAYER_SPRITE_PATH = 'gfx/violet_machine.png'
PLAYER_SHADOW_SPRITE_PATH = 'gfx/violet_machine_shadow.png'
NUMBER_IMAGES = [ # index = pictured number
    pygame.image.load('gfx/numbers/small_numbers0.png'),
    pygame.image.load('gfx/numbers/small_numbers1.png'),
    pygame.image.load('gfx/numbers/small_numbers2.png'),
    pygame.image.load('gfx/numbers/small_numbers3.png'),
    pygame.image.load('gfx/numbers/small_numbers4.png'),
    pygame.image.load('gfx/numbers/small_numbers5.png'),
    pygame.image.load('gfx/numbers/small_numbers6.png'),
    pygame.image.load('gfx/numbers/small_numbers7.png'),
    pygame.image.load('gfx/numbers/small_numbers8.png'),
    pygame.image.load('gfx/numbers/small_numbers9.png'),
]

# race configuration
STD_REQUIRED_LAPS = 3 # number of laps normally required to finish a race