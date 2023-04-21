import numpy
import pygame

from settings.debug_settings import IN_DEV_MODE, COLLISION_DETECTION_OFF # debug config
from settings.key_settings import STD_ACCEL_KEY, STD_LEFT_KEY, STD_RIGHT_KEY, STD_BRAKE_KEY # button mapping config
from settings.renderer_settings import NORMAL_ON_SCREEN_PLAYER_POSITION_X, NORMAL_ON_SCREEN_PLAYER_POSITION_Y # rendering config
from settings.machine_settings import PLAYER_COLLISION_RECT_WIDTH, PLAYER_COLLISION_RECT_HEIGHT # player collider config
from settings.machine_settings import HEIGHT_DURING_JUMP
from settings.machine_settings import OBSTACLE_HIT_SPEED_RETENTION 

from collision import CollisionRect

class Player(pygame.sprite.Sprite):
    # Constructor.
    # machine: the machine that is controlled by this player
    # current_race_track: the track that the player is playing
    def __init__(self, machine, init_pos_x, init_pos_y, init_angle, current_race_track):
        # logical transformation variables
        self.position = numpy.array([init_pos_x, init_pos_y])
        self.angle = init_angle

        # physics variables
        self.machine = machine # holds all relevant data on physical properties of the player machine
        self.current_speed = 0 # how fast the player moves in the current frame

        # Rendering variables (for machine without shadow).
        # The x coordinate of the player is always fixed,
        # the y coordinate usually fixed as well 
        # changed according to some configured quadratic function during a jump. 
        super().__init__() # calling constructor of pygame's Sprite class (responsible for rendering)
        self.image = pygame.image.load(self.machine.idle_image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = [NORMAL_ON_SCREEN_PLAYER_POSITION_X, NORMAL_ON_SCREEN_PLAYER_POSITION_Y]

        # Create a new sprite object for the machine shadow
        # which remains fixed all the time.
        self.shadow_sprite = pygame.sprite.Sprite()
        self.shadow_sprite.image = pygame.image.load(self.machine.shadow_image_path)
        self.shadow_sprite.rect = self.shadow_sprite.image.get_rect()
        # shadow sprite is created in a way that it is fine if player + shadow are at same screen coordinates
        self.shadow_sprite.rect.topleft = [NORMAL_ON_SCREEN_PLAYER_POSITION_X, NORMAL_ON_SCREEN_PLAYER_POSITION_Y]

        # collision
        self.current_race_track = current_race_track # race track collision map reference

        # player status flags/variables
        self.jumping = False
        self.jumped_off_timestamp = None # timestamp when the player last jumped off a ramp
        # When jumping: this is the duration of the jump from start to landing.
        # Needed to compute the player y coordinate on screen while jumping.
        self.current_jump_duration = 0
        self.finished = False # whether the player has finished the current race
        self.boosted = False
        self.last_boost_started_timestamp = None # timestamp of when the player last started a boost

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

        # Make player boost if on dash plate.
        if self.current_race_track.is_on_dash_plate(current_collision_rect) and not self.boosted:
            print("You got boost power!!!")
            self.boosted = True
            self.last_boost_started_timestamp = time # timestamp for determining when the boost should end
        if self.boosted:
            self.continue_boost(time)

        # Make player jump if on ramp.
        if self.current_race_track.is_on_ramp(current_collision_rect) and not self.jumping:
            self.jumping = True # set status flag
            self.current_jump_duration = self.machine.jump_duration_multiplier * self.current_speed # compute duration of jump based on speed
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
        speed_sin, speed_cos = self.machine.max_speed * sin_a, self.machine.max_speed * cos_a

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
        if keys[STD_ACCEL_KEY] and not self.finished:
            self.current_speed += self.machine.acceleration
        # Decrease speed heavily when brake button pressed.
        elif keys[STD_BRAKE_KEY] and not self.finished:
            # case 1: player currently moves forwards
            if self.current_speed > 0:
                self.current_speed -= self.machine.brake  
                # Clamp speed to zero since the player
                # should not be able to drive backwards.
                if self.current_speed < 0:
                    self.current_speed = 0
            # case 2: player currently moves backwards (e.g. because of bouncing back)
            elif self.current_speed < 0:
                self.current_speed += self.machine.brake
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
                self.current_speed -= self.machine.speed_loss
                # Clamp speed to zero (from below) to prevent jitter.
                if self.current_speed < 0:
                    self.current_speed = 0
            elif self.current_speed < 0:
                self.current_speed += self.machine.speed_loss 
                # Clamp speed to zero (from above) to prevent jitter.
                if self.current_speed > 0:
                    self.current_speed = 0

        # clamp speed between negative maximum speed and maximum speed
        current_max_speed = self.machine.boosted_max_speed if self.boosted else self.machine.max_speed
        if self.current_speed < -current_max_speed:
            self.current_speed = -current_max_speed
        if self.current_speed > current_max_speed:
            self.current_speed = current_max_speed

        # Compute sine and cosine of current angle 
        # to be able to update player position
        # based on their rotation.
        sin_a = numpy.sin(self.angle)
        cos_a = numpy.cos(self.angle)

        # Store the scaled versions of those two values for convenience.
        speed_sin, speed_cos = self.current_speed * sin_a, self.current_speed * cos_a # speed
        cf_sin, cf_cos = self.machine.centri * speed_sin * -1, self.machine.centri * speed_cos * -1 # centrifugal forces

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
                # Player bounces back since their move speed is flipped.
                # Player does not retain all of its speed.
                self.current_speed = -self.current_speed * OBSTACLE_HIT_SPEED_RETENTION

        # Steering.
        if keys[STD_LEFT_KEY] and not self.finished:
            # rotate player
            self.angle += self.machine.rotation_speed

            # apply centrifugal force
            self.position[0] += -cf_sin
            self.position[1] += cf_cos
        if keys[STD_RIGHT_KEY] and not self.finished:
            self.angle -= self.machine.rotation_speed

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

    # Called once per frame if the player currently has a booster active.
    # Checks whether the booster should end since its duration has exceeded.
    def continue_boost(self, time):
        # compute time since boost started
        elapsed_time = time - self.last_boost_started_timestamp

        # check whether boost should end
        if elapsed_time > self.machine.boost_duration:
            self.boosted = False

    # (Re-)sets the player object to the initial position
    # for the current race track.
    # Also resets all forces that are currently applied to the player.
    # Example usage: get the player to the start position at the start of a race
    def reinitialize(self):
        # reset position
        self.position = numpy.array([
            self.current_race_track.init_player_pos_x,
            self.current_race_track.init_player_pos_y
        ])

        # reset rotation
        self.angle = self.current_race_track.init_player_angle

        # reset forces
        self.current_speed = 0

        # reset status flags
        self.jumping = False
        self.finished = False
        self.boosted = False

        # reset screen position
        self.rect.topleft = [
            NORMAL_ON_SCREEN_PLAYER_POSITION_X,
            NORMAL_ON_SCREEN_PLAYER_POSITION_Y
        ]