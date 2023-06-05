# Settings for the machines that are controllable in the game.

import pygame
from machine import Machine
from animation import Animation

# physics variables of the player machine
PLAYER_COLLISION_RECT_WIDTH = 1 # width of the player collider (the same for all machines)
PLAYER_COLLISION_RECT_HEIGHT = 1 # height of the player collider
JUMP_HEIGHT = 100 # maximum height the player gains throughout a jump (compared to its standard y coordinate)
OBSTACLE_HIT_SPEED_RETENTION = 0.5 # percentage of its speed the player machine retains when hitting an obstacle
MIN_BOUNCE_BACK_FORCE = 0.005 # minimal force applied in opposite direction when the player hits a wall (to prevent player getting stuck just outside the track boundaries)

# reference values for machine stats
PURPLE_COMET_ACCELERATION = 5000 / 750
PURPLE_COMET_MAX_SPEED = 25

# maximum energy that a machine usually has
STD_MAX_ENERGY = 100

# Factor that is used to compute the amount of energy 
# the machine loses when hitting a normal obstacle 
# from the current speed of the player.
# Idea: at a speed of 1426 km/h (top speed of the Purple Comet, 0.05 in the interna of the physics engine), 
# a machine would normally lose 5 energy units
# (not applying the individual shield strength of the machine (Machine.hit_cost)).
HIT_COST_SPEED_FACTOR = 5 / PURPLE_COMET_MAX_SPEED

# Quadratic function that computes the height of the player during a jump
# based on the time since the player jumped off the track.
# 
# Parameters:
# time: time since the player lift off (in seconds)
# jump_duration: the duration of the entire jump from start to landing
def HEIGHT_DURING_JUMP(time, jump_duration):
    return - ( time * ( time - jump_duration ) ) * JUMP_HEIGHT

# speed of the animations of the machines
DRIVING_ANIM_SPEED = 12
IDLE_ANIM_SPEED = 12

# machines that are playable in the game

PURPLE_COMET_GRAPHICS_ROOT_PATH = "gfx/machines/purple_comet/"

PURPLE_COMET_SHADOW_IMAGE_PATH = PURPLE_COMET_GRAPHICS_ROOT_PATH + "violet_machine_shadow.png"

PURPLE_COMET_DRIVING_ANIMATION = Animation(
    frames = [
        pygame.image.load(PURPLE_COMET_GRAPHICS_ROOT_PATH + "violet_machine0001.png"),
        pygame.image.load(PURPLE_COMET_GRAPHICS_ROOT_PATH + "violet_machine0002.png"),
        pygame.image.load(PURPLE_COMET_GRAPHICS_ROOT_PATH + "violet_machine0003.png"),
        pygame.image.load(PURPLE_COMET_GRAPHICS_ROOT_PATH + "violet_machine0004.png")
    ],
    speed = DRIVING_ANIM_SPEED
)

PURPLE_COMET_IDLE_ANIMATION = Animation(
    frames = [
        pygame.image.load(PURPLE_COMET_GRAPHICS_ROOT_PATH + "violet_machine0000.png")
    ],
    speed = IDLE_ANIM_SPEED
)

PURPLE_COMET = Machine(
    max_speed = PURPLE_COMET_MAX_SPEED,
    boosted_max_speed = PURPLE_COMET_MAX_SPEED * 1.4,
    acceleration = PURPLE_COMET_ACCELERATION, # 750 frame update units to get to top speed
    boosted_acceleration = PURPLE_COMET_ACCELERATION * 10,
    brake = PURPLE_COMET_ACCELERATION * 2, # brake is twice as strong as accelerator
    speed_loss = PURPLE_COMET_ACCELERATION / 3, # speed loss is a third the strength of the accelerator
    boosted_speed_loss = PURPLE_COMET_ACCELERATION * 6,
    max_centri = 50, 
    centri_increase = 20,
    centri_decrease = 50,
    jump_duration_multiplier = 2 / PURPLE_COMET_MAX_SPEED, # jump should last 2 seconds if machine at max speed
    boost_duration = 2,
    max_energy = STD_MAX_ENERGY,
    boost_cost = 19,
    hit_cost = 1,
    recover_speed = 13,
    rotation_speed = 2.5,
    idle_anim = PURPLE_COMET_IDLE_ANIMATION,
    driving_anim = PURPLE_COMET_DRIVING_ANIMATION,
    shadow_image_path = PURPLE_COMET_SHADOW_IMAGE_PATH
)

FASTER_PURPLE_COMET = Machine(
    max_speed = PURPLE_COMET.max_speed * 1.1,
    boosted_max_speed = PURPLE_COMET.max_speed * 1.4,
    acceleration = PURPLE_COMET.acceleration / 2,
    boosted_acceleration = PURPLE_COMET.boosted_acceleration,
    brake = PURPLE_COMET.brake,
    speed_loss = PURPLE_COMET.speed_loss / 2,
    boosted_speed_loss = PURPLE_COMET.boosted_speed_loss / 20,
    max_centri = PURPLE_COMET.max_centri,
    centri_increase = PURPLE_COMET.centri_increase,
    centri_decrease = PURPLE_COMET.centri_decrease,
    jump_duration_multiplier = PURPLE_COMET.jump_duration_multiplier,
    boost_duration = 1.75,
    max_energy = STD_MAX_ENERGY,
    boost_cost = 14,
    hit_cost = 0.5,
    recover_speed = PURPLE_COMET.recover_speed / 2,
    rotation_speed = PURPLE_COMET.rotation_speed * 0.75,
    idle_anim = PURPLE_COMET_IDLE_ANIMATION,
    driving_anim = PURPLE_COMET_DRIVING_ANIMATION,
    shadow_image_path = PURPLE_COMET_SHADOW_IMAGE_PATH
)

SLOWER_PURPLE_COMET = Machine(
    max_speed = PURPLE_COMET.max_speed * 0.9,
    boosted_max_speed = PURPLE_COMET.max_speed * 1.5, # strong booster
    acceleration = PURPLE_COMET.acceleration * 2,
    boosted_acceleration = PURPLE_COMET.boosted_acceleration,
    brake = PURPLE_COMET.brake,
    speed_loss = PURPLE_COMET.speed_loss,
    boosted_speed_loss = PURPLE_COMET.boosted_speed_loss,
    boost_duration = 1,
    max_energy = STD_MAX_ENERGY,
    boost_cost = 22,
    hit_cost = 2,
    recover_speed = PURPLE_COMET.recover_speed * 2,
    max_centri = PURPLE_COMET.max_centri * 1.5,
    centri_increase = PURPLE_COMET.centri_increase * 1.5,
    centri_decrease = PURPLE_COMET.centri_decrease * 1.5,
    jump_duration_multiplier = PURPLE_COMET.jump_duration_multiplier,
    rotation_speed = PURPLE_COMET.rotation_speed * 1.3,
    idle_anim = PURPLE_COMET_IDLE_ANIMATION,
    driving_anim = PURPLE_COMET_DRIVING_ANIMATION,
    shadow_image_path = PURPLE_COMET_SHADOW_IMAGE_PATH
)

MACHINES = [PURPLE_COMET, FASTER_PURPLE_COMET, SLOWER_PURPLE_COMET]