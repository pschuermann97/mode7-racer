# Settings for the machines that are controllable in the game.

from machine import Machine

# physics variables of the player machine
PLAYER_COLLISION_RECT_WIDTH = 1 # width of the player collider (the same for all machines)
PLAYER_COLLISION_RECT_HEIGHT = 1 # height of the player collider
JUMP_HEIGHT = 100 # maximum height the player gains throughout a jump (compared to its standard y coordinate)
OBSTACLE_HIT_SPEED_RETENTION = 0.5 # percentage of its speed the player machine retains when hitting an obstacle
MIN_BOUNCE_BACK_FORCE = 0.005 # minimal force applied in opposite direction when the player hits a wall (to prevent player getting stuck just outside the track boundaries)

# maximum energy that a machine usually
STD_MAX_ENERGY = 100

# Factor that is used to compute the amount of energy 
# the machine loses when hitting a normal obstacle 
# from the current speed of the player.
# Idea: at a speed of 1426 km/h (top speed of the Purple Comet, 0.05 in the interna of the physics engine), 
# a machine would normally lose 5 energy units
# (not applying the individual shield strength of the machine (Machine.hit_cost)).
HIT_COST_SPEED_FACTOR = 5 / 0.05

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
    boosted_max_speed = 0.06,
    acceleration = 0.05 / 750, # 750 frame update units to get to top speed
    brake = (0.05 / 750) * 2, # brake is twice as strong as accelerator
    speed_loss = (0.05 / 750) / 3, # speed loss is a third the strength of the accelerator
    boosted_speed_loss = (0.05 / 750) / 6,
    centri = 0.3, # 50% of current speed applied as centrifugal force
    jump_duration_multiplier = 2 / 0.05, # jump should last 2 seconds if machine at max speed
    boost_duration = 2,
    max_energy = STD_MAX_ENERGY,
    boost_cost = 12,
    hit_cost = 1,
    recover_speed = 0.025,
    rotation_speed = 0.0075,
    idle_image_path = 'gfx/violet_machine.png',
    shadow_image_path = 'gfx/violet_machine_shadow.png'
)

FASTER_PURPLE_COMET = Machine(
    max_speed = PURPLE_COMET.max_speed * 1.1,
    boosted_max_speed = PURPLE_COMET.max_speed * 1.4,
    acceleration = PURPLE_COMET.acceleration / 2,
    brake = PURPLE_COMET.brake,
    speed_loss = PURPLE_COMET.speed_loss / 2,
    boosted_speed_loss = PURPLE_COMET.boosted_speed_loss,
    centri = PURPLE_COMET.centri,
    jump_duration_multiplier = PURPLE_COMET.jump_duration_multiplier,
    boost_duration = 1.75,
    max_energy = STD_MAX_ENERGY,
    boost_cost = 9,
    hit_cost = 0.5,
    recover_speed = PURPLE_COMET.recover_speed / 2,
    rotation_speed = PURPLE_COMET.rotation_speed * 0.75,
    idle_image_path = 'gfx/violet_machine.png',
    shadow_image_path = 'gfx/violet_machine_shadow.png'
)

SLOWER_PURPLE_COMET = Machine(
    max_speed = PURPLE_COMET.max_speed * 0.8,
    boosted_max_speed = PURPLE_COMET.max_speed * 1.5, # strong booster
    acceleration = PURPLE_COMET.acceleration * 2,
    brake = PURPLE_COMET.brake,
    speed_loss = PURPLE_COMET.speed_loss,
    boosted_speed_loss = PURPLE_COMET.speed_loss,
    boost_duration = 1.25,
    max_energy = STD_MAX_ENERGY,
    boost_cost = 16,
    hit_cost = 2,
    recover_speed = PURPLE_COMET.recover_speed * 2,
    centri = PURPLE_COMET.centri * 1.5,
    jump_duration_multiplier = PURPLE_COMET.jump_duration_multiplier,
    rotation_speed = PURPLE_COMET.rotation_speed * 1.3,
    idle_image_path = 'gfx/violet_machine.png',
    shadow_image_path = 'gfx/violet_machine_shadow.png'
)

MACHINES = [PURPLE_COMET, FASTER_PURPLE_COMET, SLOWER_PURPLE_COMET]