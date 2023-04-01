import numpy
import pygame

from settings import IN_DEV_MODE, STD_ACCEL_KEY, STD_LEFT_KEY, STD_RIGHT_KEY, PLAYER_SPRITE_PATH, NORMAL_PLAYER_POSITION_X, NORMAL_PLAYER_POSITION_Y

class Player(pygame.sprite.Sprite):
    def __init__(self, move_speed, rotation_speed):
        # logical transformation variables
        self.position = numpy.array([0.0, 0.0]) # player initially is at origin position
        self.angle = 0 # player initially looks forward

        # physics variables
        self.move_speed = move_speed # how fast the player can move through the scene
        self.rotation_speed = rotation_speed # how fast the player can rotate

        # rendering variables
        super().__init__() # calling constructor of pygame's Sprite class (responsible for rendering)
        self.image = pygame.image.load(PLAYER_SPRITE_PATH)
        self.rect = self.image.get_rect()
        self.rect.topleft = [NORMAL_PLAYER_POSITION_X, NORMAL_PLAYER_POSITION_Y]


    # Updates player data and position.
    # 
    # Parameters:
    # time: number of frames since the game started
    def update(self, time):
        # movement
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
        speed_sin, speed_cos = self.move_speed * sin_a, self.move_speed * cos_a

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
        # Compute sine and cosine of current angle 
        # to be able to update player position
        # based on their rotation.
        sin_a = numpy.sin(self.angle)
        cos_a = numpy.cos(self.angle)

        # Store the scaled versions of those two values for convenience.
        speed_sin, speed_cos = self.move_speed * sin_a, self.move_speed * cos_a

        # Initialize the variables holding the change in player position
        # which are accumulated throughout the method.
        dx, dy = 0, 0

        # collect key events
        keys = pygame.key.get_pressed()

        # Forward movement.
        if keys[STD_ACCEL_KEY]:
            self.position[0] += speed_cos
            self.position[1] += speed_sin

        # Change player rotation
        if keys[STD_LEFT_KEY]:
            self.angle += self.rotation_speed
        if keys[STD_RIGHT_KEY]:
            self.angle -= self.rotation_speed