# foreign module imports
import pygame
import sys

# modules from this project
from settings import *
from mode7 import Mode7
from player import Player

# The class that handles/orchestrates all tasks involved in running the game.
# This includes rendering the screen, 
# listening to events (e.g. keys pressed, ...)
# updating the game state and 
# handling the game's internal clock.
class App:
    def __init__(self):
        self.screen = pygame.display.set_mode(WIN_RES)
        self.clock = pygame.time.Clock()

        # Initializes the mode-7 renderer.
        # Second parameter is path to the floor texture.
        # Third parameter determines whether the rendered scene has a fog effect or not.
        self.mode7 = Mode7(self, 
            floor_tex_path = 'png/track_2023.png', 
            bg_tex_path = 'png/track_2023_bg.png',
            is_foggy = True
        )

        # Creates a player instance
        self.player = Player(
            move_speed = INITIAL_PLAYER_MOVE_SPEED,
            rotation_speed = INITIAL_PLAYER_ROTATION_SPEED
        )

    def update(self):
        # updates the player based on time elapsed since game start
        self.player.update(self.time)

        # causes the Mode7-rendered environment to update
        self.mode7.update(self.player)

        # updates clock
        self.clock.tick()

        # caption of the window displays current frame rate
        # (f'...' is a more readable + faster way to write format strings than with "%")
        pygame.display.set_caption(f'{self.clock.get_fps(): 0.1f}')

    def draw(self):
        self.mode7.draw()

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

            # update field counting the frames since game start
            self.get_time()

            # update game state
            self.update()

            # render frame
            self.draw()

if __name__ == '__main__':
    app = App()
    app.run()