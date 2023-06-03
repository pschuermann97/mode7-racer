# Settings for the in-race UI.

import pygame
from settings.renderer_settings import WIDTH, HEIGHT
from settings.machine_settings import PURPLE_COMET_MAX_SPEED # for speed display factor

# UI screen coordinates

# speed meter
SPEED_METER_DIGIT_SPRITE_WIDTH = 16
SPEED_METER_DIGIT_SPRITE_HEIGHT = 16
RIGHT_MOST_SPEEDMETER_DIGIT_SCREEN_X_COORD = WIDTH - SPEED_METER_DIGIT_SPRITE_WIDTH
SPEED_METER_DIGIT_SCREEN_Y_COORD = HEIGHT - 1.5 * SPEED_METER_DIGIT_SPRITE_HEIGHT # no padding in sprite so we add one of 12px in code

# energy meter
NUM_TIMER_DIGITS = 7 # some timer-related variables need to be defined here since timer and energy bar are aligned
TIMER_DIGIT_SPRITE_WIDTH = SPEED_METER_DIGIT_SPRITE_WIDTH
RIGHT_MOST_TIMER_DIGIT_SCREEN_X_COORD = WIDTH - TIMER_DIGIT_SPRITE_WIDTH
ENERGY_METER_HEIGHT = 16
ENERGY_METER_TOP_Y = 4 # offset of the energy meter from the top of the screen
ENERGY_METER_LEFT_X = RIGHT_MOST_TIMER_DIGIT_SCREEN_X_COORD - TIMER_DIGIT_SPRITE_WIDTH * NUM_TIMER_DIGITS

# timer

TIMER_DIGIT_SPRITE_HEIGHT = SPEED_METER_DIGIT_SPRITE_HEIGHT
TIMER_DIGIT_SCREEN_Y_COORD = ENERGY_METER_TOP_Y + ENERGY_METER_HEIGHT # timer should be right below the shield meter
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
SPEED_DISPLAY_MULTIPLIER = 1426 / PURPLE_COMET_MAX_SPEED # so max speed of Purple Comet will be shown as 1426 km/h



# standard paths for the number sprites used in the game
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