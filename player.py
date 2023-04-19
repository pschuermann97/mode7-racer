import numpy
import pygame

from settings import IN_DEV_MODE, COLLISION_DETECTION_OFF # debug config
from settings import STD_ACCEL_KEY, STD_LEFT_KEY, STD_RIGHT_KEY, STD_BRAKE_KEY # button mapping config
from settings import PLAYER_SPRITE_PATH, PLAYER_SHADOW_SPRITE_PATH, NORMAL_ON_SCREEN_PLAYER_POSITION_X, NORMAL_ON_SCREEN_PLAYER_POSITION_Y # rendering config
from settings import PLAYER_COLLISION_RECT_WIDTH, PLAYER_COLLISION_RECT_HEIGHT # player collider config
from settings import HEIGHT_DURING_JUMP, JUMP_DURATION_MULTIPLIER # jumping

from collision import CollisionRect

class Player(pygame.sprite.Sprite):
    def __init__(self, max_speed, acceleration, brake_force, speed_loss, rotation_speed, centri,
        init_pos_x, init_pos_y, init_angle, current_race_track):
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
        self.centri = centri # how hard the player is pushed to the outside in corners

        # Rendering variables (for machine without shadow).
        # The x coordinate of the player is always fixed,
        # the y coordinate usually fixed as well 
        # changed according to some configured quadratic function during a jump. 
        super().__init__() # calling constructor of pygame's Sprite class (responsible for rendering)
        self.image = pygame.image.load(PLAYER_SPRITE_PATH)
        self.rect = self.image.get_rect()
        self.rect.topleft = [NORMAL_ON_SCREEN_PLAYER_POSITION_X, NORMAL_ON_SCREEN_PLAYER_POSITION_Y]

        # Create a new sprite object for the machine shadow
        # which remains fixed all the time.
        self.shadow_sprite = pygame.sprite.Sprite()
        self.shadow_sprite.image = pygame.image.load(PLAYER_SHADOW_SPRITE_PATH)
        self.shadow_sprite.rect = self.shadow_sprite.image.get_rect()
        # shadow sprite is created in a way that it is fine if player + shadow are at same screen coordinates
        self.shadow_sprite.rect.topleft = [NORMAL_ON_SCREEN_PLAYER_POSITION_X, NORMAL_ON_SCREEN_PLAYER_POSITION_Y]

        # collision
        self.current_race_track = current_race_track # race track collision map reference

        # player status flags/variables
        self.jumping = False
        self.jumped_off_timestamp = None # timestamp of when the player last jumped off a ramp
        # When jumping: this is the duration of the jump from start to landing.
        # Needed to compute the player y coordinate on screen while jumping.
        self.current_jump_duration = 0

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

        # Store the current rectangular collider of the player
        # for use in several environment checks and updates.
        current_collision_rect = CollisionRect(
            pos = self.position,
            w = PLAYER_COLLISION_RECT_WIDTH,
            h = PLAYER_COLLISION_RECT_HEIGHT
        )

        # Update the lap count.
        # To do so, the track object needs the current position of the player.
        self.current_race_track.update_lap_count(current_collision_rect)

        # Make player jump if on ramp.
        if self.current_race_track.is_on_ramp(current_collision_rect) and not self.jumping:
            self.jumping = True # set status flag
            self.current_jump_duration = JUMP_DURATION_MULTIPLIER * self.current_speed # compute duration of jump based on speed
            self.jumped_off_timestamp = time # timestamp for computing height in later frames
        if self.jumping:
            self.continue_jump(time)

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

        # Change player position
        self.position[0] += dx
        self.position[1] += dy

        # Change player rotation
        if keys[pygame.K_LEFT]:
            self.angle += self.rotation_speed
        if keys[pygame.K_RIGHT]:
            self.angle -= self.rotation_speed

        print("x: " + str(self.position[0]) + " y: " + str(self.position[1]) + " a: " + str(self.angle))

    # Moves the player's machine as in a race (accelerating, braking and steering).
    def racing_mode_movement(self):
        # collect key events
        keys = pygame.key.get_pressed()
        
        # Update player speed according to acceleration/brake inputs.
        # Increase speed when acceleration button pressed.
        if keys[STD_ACCEL_KEY]:
            self.current_speed += self.acceleration
        # Decrease speed heavily when brake button pressed.
        elif keys[STD_BRAKE_KEY]:
            # case 1: player currently moves forwards
            if self.current_speed > 0:
                self.current_speed -= self.brake_force  
                # Clamp speed to zero since the player
                # should not be able to drive backwards.
                if self.current_speed < 0:
                    self.current_speed = 0
            # case 2: player currently moves backwards (e.g. because of bouncing back)
            elif self.current_speed < 0:
                self.current_speed += self.brake_force
                # Clamp speed to zero since the player 
                # should not go forward again
                if self.current_speed > 0:
                    self.current_speed = 0
        # Decrease speed slightly when neither acceleration nor brake button pressed.
        # Decreasing hereby means approaching zero
        # (otherwise the player would move backwards at increasing speed
        # if no button is pressed).
        else:
            if self.current_speed > 0:
                self.current_speed -= self.speed_loss
                # Clamp speed to zero (from below) to prevent jitter.
                if self.current_speed < 0:
                    self.current_speed = 0
            elif self.current_speed < 0:
                self.current_speed += self.speed_loss 
                # Clamp speed to zero (from above) to prevent jitter.
                if self.current_speed > 0:
                    self.current_speed = 0

        # clamp speed between negative maximum speed and maximum speed
        if self.current_speed < -self.max_speed:
            self.current_speed = -self.max_speed
        if self.current_speed > self.max_speed:
            self.current_speed = self.max_speed

        # Compute sine and cosine of current angle 
        # to be able to update player position
        # based on their rotation.
        sin_a = numpy.sin(self.angle)
        cos_a = numpy.cos(self.angle)

        # Store the scaled versions of those two values for convenience.
        speed_sin, speed_cos = self.current_speed * sin_a, self.current_speed * cos_a # speed
        cf_sin, cf_cos = self.centri * speed_sin * -1, self.centri * speed_cos * -1 # centrifugal forces

        # Compute player's position in the next frame including the moved collision rect.
        next_frame_position_x = self.position[0] + speed_cos
        next_frame_position_y = self.position[1] + speed_sin
        frame_lookahead_collision_rect = CollisionRect(
            pos = numpy.array([next_frame_position_x, next_frame_position_y]), 
            w = PLAYER_COLLISION_RECT_WIDTH,
            h = PLAYER_COLLISION_RECT_HEIGHT
        )

        # Check if player would stay on track when moved as computed above.
        # If yes or if the player is jumping, move them.
        # If no, make them bounce back.
        #
        # Debug-only feature: if collision detection is turned off, the player is always moved, never bounced back.
        if self.current_race_track.is_on_track(frame_lookahead_collision_rect) or self.jumping or COLLISION_DETECTION_OFF:
            self.position[0] = next_frame_position_x
            self.position[1] = next_frame_position_y
        else:
            if not COLLISION_DETECTION_OFF:
                # player bounces back since their move speed is flipped
                self.current_speed = -self.current_speed

        # Steering.
        if keys[STD_LEFT_KEY]:
            # rotate player
            self.angle += self.rotation_speed

            # apply centrifugal force
            self.position[0] += -cf_sin
            self.position[1] += cf_cos
        if keys[STD_RIGHT_KEY]:
            self.angle -= self.rotation_speed

            self.position[0] += cf_sin
            self.position[1] += -cf_cos
    
    # Updates player status flags and moves the player
    # to its current screen Y position
    # depending on the time since the player jumped off the track.
    def continue_jump(self, time):
        # compute time since jump started
        elapsed_time = time - self.jumped_off_timestamp

        # moving up on screen = decreasing the y coordinate
        self.rect.topleft = [
            NORMAL_ON_SCREEN_PLAYER_POSITION_X, 
            NORMAL_ON_SCREEN_PLAYER_POSITION_Y - HEIGHT_DURING_JUMP(elapsed_time, self.current_jump_duration)
        ]

        # End jump (reset status flap) if jump duration reached
        # To prevent any visual artifacts, the player rect is reset to its normal y position on screen.
        if elapsed_time >= self.current_jump_duration:
            self.jumping = False

            self.rect.topleft = [
                NORMAL_ON_SCREEN_PLAYER_POSITION_X, NORMAL_ON_SCREEN_PLAYER_POSITION_Y
            ]

            # if the player lands out of the track bounds, they have failed the run
            current_collision_rect = CollisionRect(
                self.position,
                PLAYER_COLLISION_RECT_WIDTH,
                PLAYER_COLLISION_RECT_HEIGHT
            )
            if not self.current_race_track.is_on_track(current_collision_rect):
                print("player out of bounds!")