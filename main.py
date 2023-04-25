# foreign module imports
import pygame
import sys

# import of the game settings
from settings.debug_settings import *
from settings.machine_settings import *
from settings.renderer_settings import *
from settings.track_settings import *
from settings.ui_settings import *
from settings.key_settings import STD_CONFIRM_KEY, STD_DEBUG_RESTART_KEY
from settings.league_settings import *

# other imports from this project
from mode7 import Mode7
from player import Player
from camera import Camera
from track import Track
from race import Race
from league import League
from settings.track_settings import TrackCreator
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
        # ------------- general initialization --------------------

        self.screen = pygame.display.set_mode(WIN_RES)
        self.clock = pygame.time.Clock()

        self.in_racing_mode = False

        # Creates a group of sprites that contains all the sprites
        # that move across the screen.
        self.moving_sprites = pygame.sprite.Group()

        # Creates a group of sprites for all that do not move
        self.static_sprites = pygame.sprite.Group()

        # Creates a group of sprites for all sprites in the UI.
        self.ui_sprites = pygame.sprite.Group()

        # ------------- end of general initialization -------------



        # ------------- (debug mode) game mode selection -----------------------

        if DEBUG_CHOOSE_GAME_MODE:
            print("Choose a game mode: ")
            print("1: League race")
            print("2: Single race")
            game_mode_choice = int(input("Your choice: "))
        else:
            game_mode_choice = DEFAULT_GAME_MODE

        # ------------- end of game mode selection ----------------



        # ------------- initialize game (depending on mode) -------

        if game_mode_choice == 1:
            self.init_league_race_mode()
        if game_mode_choice == 2:
            self.init_single_race_mode()


        # ------------- end of mode-dependent game initialization -------

        

    # Initialization for the league race mode:
    # a league consists of five consecutive races that the player has to complete.
    def init_league_race_mode(self):
        # reinitialize sprite groups as empty groups (to tidy up)
        self.initialize_sprite_groups()

        # league selection (todo)
        self.current_league = LEAGUES[0]

        # initialize the actual race mode
        self.init_race_mode(
            next_race = self.current_league.current_race()
        )

    # 
    def init_single_race_mode(self):
        # tidy up sprites
        self.initialize_sprite_groups()

        # ------------- track selection (todo) -------------

        race_choice = 3

        # ------------- end of track selection -------------

        # Init race mode and load race.
        # We exploit that a single race can be seen as a League object 
        # whose race list only contains one race.
        self.current_league = League( [SINGLE_MODE_RACES[race_choice]] )
        self.init_race_mode(next_race = self.current_league.current_race())
        
    # Contains some general (re-)initialization logic for any game mode
    # in which races are played. 
    # This includes creating the respective groups for sprites, 
    # initializing some status flags,
    # initializing the racing UI, ...
    #
    # Parameters:
    # next_race - next race that should be played after (re-)initialization
    def init_race_mode(self, next_race):
        # player can set this flag to True via a button press to indicate that the next race should be loaded
        self.should_load_next_race = False 

        # Declares the mode-7 renderer.
        # Initialized later when loading the race.
        self.mode7 = None

        # debug only: player chooses a machine
        # outside debug mode, the player is using Purple Comet
        if DEBUG_CHOOSE_MACHINE:
            print("0: Purple Comet")
            print("1: Faster Purple Comet")
            print("2: Slower Purple Comet")
            choice = int(input("Choose a machine: "))
            player_machine = MACHINES[choice]
        else:
            player_machine = DEFAULT_MACHINE # default machine can be changed in settings.machine_settings

        # Timestamp of the last frame rendered.
        # Needed to make up for different framerates on different machines.
        # If physics-related operations like accelerating, braking, restoring health, ...
        # are not scaled with the time between this frame and the last frame,
        # players with faster framerate accelerate faster etc.
        # because more frame updates in computed in the same time.
        self.get_time()
        self.last_frame = self.time

        # Creates a player instance and
        # assigns the race track to the player.
        # The player needs to know which race track they are driving on
        # so they can check whether they would leave the track with their movement in the current frame
        # or are hitting a track gimmick.
        self.player = Player(
            machine = player_machine,
            current_race = next_race
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
        # used for the timer that tracks the time since race start. 
        # Need to used method get_time since self.time field is not initialized at this point.
        self.race_start_timestamp = self.time

        # sets status flag
        self.in_racing_mode = True

        # load the next race track
        self.load_race(next_race)

    def update(self):
        # computes time since last frame
        delta = self.time - self.last_frame
        
        # For things only needed to be done during a race. 
        if self.in_racing_mode:
            # updates the player based on time elapsed since game start
            self.player.update(self.time, delta)

            # updates camera position (which is done mainly based on player position)
            self.camera.update()

            # causes the Mode7-rendered environment to update
            self.mode7.update(self.camera)

            # Update timer on UI if player has not finished the current race yet.
            if not self.player.finished:
                seconds_since_race_start = self.time - self.race_start_timestamp
                self.ui.update(
                    elapsed_milliseconds = seconds_since_race_start * 1000
                )

            # Checks whether player has finished the race.
            # If so, a status flag is set in the player instance if not done already.
            if self.current_league.current_race().player_finished_race() and not self.player.finished:
                self.player.finished = True

            # load next race if player finished the current one and pushed the confirm button (which set the flag)
            if self.should_load_next_race:
                self.player.finished = False
                self.load_race(self.current_league.next_race())

            # Checks whether player has completed at least one lap
            # and activates their boost power if so (and not activated yet).
            if self.current_league.current_race().player_completed_first_lap() and not self.player.has_boost_power:
                self.player.has_boost_power = True
                print("You got boost power!!!")

        # updates clock
        self.clock.tick()

        # caption of the window displays current frame rate
        # (f'...' is a more readable + faster way to write format strings than with "%")
        pygame.display.set_caption(f'{self.clock.get_fps(): 0.1f}')

        # log output for debug
        self.debug_logs()

        # timestamp of current frame for delta computation in next frame
        self.last_frame = self.time

    # (Re-)loads the passed race.
    def load_race(self, race):
        # reset all progress data stored for this race
        race.reset_data()

        # assign player the new race
        self.player.current_race = race
        
        # reset player to starting position of (new) race track
        self.player.reinitialize()

        # Replace renderer field with Mode-7 renderer for the new race track.
        # Third parameter determines whether the renderer has a fog effect applied or not.
        self.mode7 = Mode7(
            app = self,
            floor_tex_path = race.floor_texture_path,
            bg_tex_path = race.bg_texture_path,
            is_foggy = race.is_foggy
        )

        # reset timer
        self.race_start_timestamp = self.time

        # reset flag
        self.should_load_next_race = False

        print("---------------- race on " + race.race_track.name + " was restarted ------------------")

    # (Re-)initializes all sprite groups as empty groups.
    # Can be used to tidy up when switching game modes.
    def initialize_sprite_groups(self):
        self.moving_sprites = pygame.sprite.Group()
        self.static_sprites = pygame.sprite.Group()
        self.ui_sprites = pygame.sprite.Group()

    def draw(self):
        # draws the mode-7 environment
        self.mode7.draw()

        # draws static sprites (e.g. player shadow) to screen
        self.static_sprites.draw(self.screen)

        # draws moving sprites (e.g. player) to screen
        self.moving_sprites.draw(self.screen)

        # draws UI sprites to screen
        self.ui_sprites.draw(self.screen)

        # draws debug objects like energy bar
        if self.in_racing_mode:
            self.draw_racing_mode_debug_objects()

        # update the contents of the whole display
        pygame.display.flip()

    def get_time(self):
        # time since game started in seconds
        # (get_ticks returns this time in milliseconds)
        self.time = pygame.time.get_ticks() * 0.001

    def check_event(self):
        for event in pygame.event.get():
            # Terminate the process running the game 
            # if escape key is pressed or anything else caused the quit-game event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # check for key presses in menu screens
            if event.type == pygame.KEYDOWN:
                if event.key == STD_CONFIRM_KEY and self.player.finished:
                    self.should_load_next_race = True 
                if event.key == STD_DEBUG_RESTART_KEY and DEBUG_RESTART_RACE_ON_R:
                    self.load_race(self.current_league.current_race())

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

    def draw_racing_mode_debug_objects(self):
        # draw debug mode energy bar to screen
        pygame.draw.rect(
            self.screen, 
            pygame.Color(160, 0, 0), 
            pygame.Rect(
                ENERGY_METER_LEFT_X, # left
                ENERGY_METER_TOP_Y, # top
                (RIGHT_MOST_TIMER_DIGIT_SCREEN_X_COORD - ENERGY_METER_LEFT_X) * (self.player.current_energy / self.player.machine.max_energy), # pos x
                ENERGY_METER_TOP_Y + (ENERGY_METER_HEIGHT / 2) # pos y
            )
        )

# Execution of game loop if executed as a script.
if __name__ == '__main__':
    app = App()
    app.run()