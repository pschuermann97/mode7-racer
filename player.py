import numpy
import pygame

from settings import IN_DEV_MODE
from settings import STD_ACCEL_KEY, STD_LEFT_KEY, STD_RIGHT_KEY, STD_BRAKE_KEY # button mapping config
from settings import PLAYER_SPRITE_PATH, NORMAL_ON_SCREEN_PLAYER_POSITION_X, NORMAL_ON_SCREEN_PLAYER_POSITION_Y # rendering config

class Player(pygame.sprite.Sprite):
    def __init__(self, max_speed, acceleration, brake_force, speed_loss, rotation_speed,
        init_pos_x, init_pos_y, init_angle):
        # logical transformation variables
        self.position = numpy.array([init_pos_x, init_pos_y])
        self.angle = init_angle

        # physics variables
        self.current_speed = 0 # how fast the player moves in the current frame
        self.max_speed = max_speed # how fast the player can move through the scene at max
        self.acceleration = acceleration # acceleration force applied to the player car per frame that the brake is pressed
        self.brake_force = brake_force # brake force applied to the player car per frame that the brake is pressed
        self.speed_loss = speed_loss # how much speed player loses when neither accelerating nor braking
        self.rotation_speed = rotation_speed # how fast the player can rotate

        # rendering variables
        super().__init__() # calling constructor of pygame's Sprite class (responsible for rendering)
        self.image = pygame.image.load(PLAYER_SPRITE_PATH)
        self.rect = self.image.get_rect()
        self.rect.topleft = [NORMAL_ON_SCREEN_PLAYER_POSITION_X, NORMAL_ON_SCREEN_PLAYER_POSITION_Y]


    # Updates player data and position.
    # 
    # Parameters:
    # time: number of frames since the game started
    def update(self, time):
        # move player according to steering inputs and current speed
        if IN_DEV_MODE:
            self.dev_mode_movement()
        else:
            self.racing_mode_movement()

    # Moves and rotates the camera freely based on player input. 
    def dev_mode_movement(self):
        # Compute sine and cosine of current angle 
        # to be able to update player position
        # based on their rotation.
        sin_a = numpy.sin(self.angle)
        cos_a = numpy.cos(self.angle)

        # Store the scaled versions of those two values for convenience.
        # Player always moves at maximum speed when in dev mode.
        speed_sin, speed_cos = self.max_speed * sin_a, self.max_speed * cos_a

        # Initialize the variables holding the change in player position
        # which are accumulated throughout the method.
        dx, dy = 0, 0

        # collect key events
        keys = pygame.key.get_pressed()

        # accumulate the change in player position based on the pressed keys.
        if keys[pygame.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pygame.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pygame.K_a]:
            dx += -speed_sin
            dy += speed_cos
        if keys[pygame.K_d]:
            dx += speed_sin
            dy += -speed_cos

        # Change player position.
        self.position[0] += dx
        self.position[1] += dy

        # Change player rotation
        if keys[pygame.K_LEFT]:
            self.angle += self.rotation_speed
        if keys[pygame.K_RIGHT]:
            self.angle -= self.rotation_speed

        print("x: " + str(self.position[0]) + " y: " + str(self.position[1]) + " a: " + str(self.angle))

    # Moves the player's machine as in a race.
    def racing_mode_movement(self):
        # collect key events
        keys = pygame.key.get_pressed()
        
        # Update player speed according to acceleration/brake inputs.
        # Increase speed when acceleration button pressed.
        if keys[STD_ACCEL_KEY]:
            self.current_speed += self.acceleration
        # Decrease speed heavily when brake button pressed.
        elif keys[STD_BRAKE_KEY]:
            self.current_speed -= self.brake_force   
        # decrease speed slightly when neither acceleration nor brake button pressed 
        else:
            self.current_speed -= self.speed_loss

        # clamp speed between 0 and maximum speed
        if self.current_speed < 0:
            self.current_speed = 0 
        if self.current_speed > self.max_speed:
            self.current_speed = self.max_speed

        # Compute sine and cosine of current angle 
        # to be able to update player position
        # based on their rotation.
        sin_a = numpy.sin(self.angle)
        cos_a = numpy.cos(self.angle)

        # Store the scaled versions of those two values for convenience.
        speed_sin, speed_cos = self.current_speed * sin_a, self.current_speed * cos_a

        # Forward movement.
        self.position[0] += speed_cos
        self.position[1] += speed_sin

        # Change player rotation
        if keys[STD_LEFT_KEY]:
            self.angle += self.rotation_speed
        if keys[STD_RIGHT_KEY]:
            self.angle -= self.rotation_speed