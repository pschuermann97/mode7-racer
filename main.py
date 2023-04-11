# foreign module imports
import pygame
import sys

# imports from this project
from settings import *
from mode7 import Mode7
from player import Player
from camera import Camera
from track import Track, TrackCreator
from ui import UI

# debug only imports
from collision import CollisionRect

# The class that handles/orchestrates all tasks involved in running the game.
# This includes rendering the screen, 
# listening to events (e.g. keys pressed, ...)
# updating the game state and 
# handling the game's internal clock.
class App:
    def __init__(self):
        self.screen = pygame.display.set_mode(WIN_RES)
        self.clock = pygame.time.Clock()

        # Creates a group of sprites that contains all the sprites
        # that move across the screen.
        self.moving_sprites = pygame.sprite.Group()

        # Creates a group of sprites for all that do not move
        self.static_sprites = pygame.sprite.Group()

        # Creates a group of sprites for all sprites in the UI.
        self.ui_sprites = pygame.sprite.Group()

        # Initializes the mode-7 renderer.
        # Third parameter determines whether the rendered scene has a fog effect or not.
        self.mode7 = Mode7(self, 
            floor_tex_path = 'gfx/track_2023.png', 
            bg_tex_path = 'gfx/track_2023_bg_resized.png',
            is_foggy = True
        )

        # Creates the race track collision map.
        self.race_track = TrackCreator.create_track_1()

        # Creates a player instance and
        # assigns the race track to the player.
        # The player needs to know which race track they are driving on
        # so they can check whether they would leave the track with their movement in the current frame.
        self.player = Player(
            max_speed = PLAYER_MAX_SPEED,
            acceleration = PLAYER_ACCELERATION,
            brake_force = PLAYER_BRAKE,
            speed_loss = PLAYER_SPEED_LOSS,
            rotation_speed = INITIAL_PLAYER_ROTATION_SPEED,
            centri = PLAYER_CENTRIFUGAL_FORCE,
            init_pos_x = INITIAL_PLAYER_POSITION_X,
            init_pos_y = INITIAL_PLAYER_POSITION_Y,
            init_angle = INITIAL_PLAYER_ANGLE,
            current_race_track = self.race_track
        )

        # need to add the player instance and the player shadow sprite to sprite group to be able to render it
        # order matters since player needs to be "in front of" the shadow
        self.static_sprites.add(self.player.shadow_sprite)
        self.moving_sprites.add(self.player)

        # Creates a camera instance
        # that tracks the player.
        self.camera = Camera(
            self.player,
            CAM_DISTANCE
        )

        # Creates sprites for the speed meter of the UI.
        self.speed_meter_sprites = [None, None, None, None]
        for i in range(0, 4):
            self.speed_meter_sprites[i] = pygame.sprite.Sprite() # digits are numbered from right to left
            self.speed_meter_sprites[i].image = NUMBER_IMAGES[0] # initially, all digits are 0
            self.speed_meter_sprites[i].rect = self.speed_meter_sprites[i].image.get_rect()
            self.speed_meter_sprites[i].rect.topleft = [
                RIGHT_MOST_SPEEDMETER_DIGIT_SCREEN_X_COORD - SPEED_METER_DIGIT_SPRITE_WIDTH * i, # offset sprites individually based on left-most one's x coord. 24px is sprite width
                SPEED_METER_DIGIT_SCREEN_Y_COORD
            ]

            # add to sprite group for UI sprites (for rendering, done in App class)
            self.ui_sprites.add(self.speed_meter_sprites[i])

        # Creates sprites for the timer of the UI (analogously as those for speed meter).
        self.timer_sprites = [None, None, None, None, None, None, None]
        for i in range(0, 7):
            self.timer_sprites[i] = pygame.sprite.Sprite()
            self.timer_sprites[i].image = NUMBER_IMAGES[0]
            self.timer_sprites[i].rect = self.timer_sprites[i].image.get_rect()
            self.timer_sprites[i].rect.topleft = [
                TIMER_DIGIT_X_OFFSET(i),
                TIMER_DIGIT_SCREEN_Y_COORD
            ]

            self.ui_sprites.add(self.timer_sprites[i])

        # Create instance of UI manager class
        self.ui = UI(
            player = self.player,
            speed_meter_sprites = self.speed_meter_sprites,
            timer_sprites = self.timer_sprites
        )

        # Take initial timestamp that is 
        # used for the timer that tracks the time since game start. 
        # Need to used method get_time since self.time field is not initialized at this point.
        self.get_time() # need to update current timestamp first
        self.game_start_timestamp = self.time

    def update(self):
        # updates the player based on time elapsed since game start
        self.player.update(self.time)

        # updates camera position (which is done mainly based on player position)
        self.camera.update()

        # causes the Mode7-rendered environment to update
        self.mode7.update(self.camera)

        # Computes the elapsed time since game start 
        # and updates UI.
        seconds_since_game_start = self.time - self.game_start_timestamp
        self.ui.update(
            elapsed_milliseconds = seconds_since_game_start * 1000
        )

        # updates clock
        self.clock.tick()

        # caption of the window displays current frame rate
        # (f'...' is a more readable + faster way to write format strings than with "%")
        pygame.display.set_caption(f'{self.clock.get_fps(): 0.1f}')

        # log output for debug
        self.debug_logs()

    def draw(self):
        # draws the mode-7 environment
        self.mode7.draw()

        # draws static sprites (e.g. player shadow) to screen
        self.static_sprites.draw(self.screen)

        # draws moving sprites (e.g. player) to screen
        self.moving_sprites.draw(self.screen)

        # draws UI sprites to screen
        self.ui_sprites.draw(self.screen)

        # update the contents of the whole display
        pygame.display.flip()

    def get_time(self):
        # time since game started in seconds
        # (get_ticks returns this time in milliseconds)
        self.time = pygame.time.get_ticks() * 0.001

    def check_event(self):
        for i in pygame.event.get():
            # Terminate the process running the game 
            # if escape key is pressed or anything else caused the quit-game event
            if i.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    # Main game loop, runs until termination of process.
    def run(self):
        while True:
            # handle events
            self.check_event()

            # update field counting the milliseconds since game start
            self.get_time()

            # update game state
            self.update()

            # render frame
            self.draw()


    # Logs various game state information to the console when key P is pressed. 
    def debug_logs(self):
        keys = pygame.key.get_pressed()

        # log of player's position for debug purposes
        if keys[pygame.K_p]:
            print("player position/angle: " + str(self.player.position[0]) + " " + str(self.player.position[1]) + ", " + str(self.player.angle))

        # log camera position for debug purposes
        # if keys[pygame.K_p]:
        #     print("cam position/angle: " + str(self.camera.position[0]) + " " + str(self.camera.position[1]) + ", " + str(self.camera.angle))

        # log whether player is on track
        # if keys[pygame.K_p]:
        #     if self.race_track.is_on_track( CollisionRect(self.player.position, PLAYER_COLLISION_RECT_WIDTH, PLAYER_COLLISION_RECT_HEIGHT) ):
        #         print("player on track!")

        # log player speed
        # if keys[pygame.K_p]:
        #     print("player speed:" + str(self.player.current_speed))

# Execution of game loop if executed as a script.
if __name__ == '__main__':
    app = App()
    app.run()