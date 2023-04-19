# Settings for the machines that are controllable in the game.

from machine import Machine

# physics variables of the player machine
PLAYER_COLLISION_RECT_WIDTH = 1 # width of the player collider (the same for all machines)
PLAYER_COLLISION_RECT_HEIGHT = 1 # height of the player collider
JUMP_HEIGHT = 100 # maximum height the player gains throughout a jump (compared to its standard y coordinate)

# Quadratic function that computes the height of the player during a jump
# based on the time since the player jumped off the track.
# 
# Parameters:
# time: time since the player lift off (in seconds)
# jump_duration: the duration of the entire jump from start to landing
def HEIGHT_DURING_JUMP(time, jump_duration):
    return - ( time * ( time - jump_duration ) ) * JUMP_HEIGHT


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