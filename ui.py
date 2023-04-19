from settings.ui_settings import SPEED_DISPLAY_MULTIPLIER, NUMBER_IMAGES

# Handles updates to the UI in every frame.
# Drawing of the UI is done in the main module (App class).
class UI:
    # Parameters:
    # player: player instance to track with this UI instance
    # speed_meter_sprites: array of the sprites that form the speed meter
    # timer_sprites: array of the sprites that form the timer
    def __init__(self, player, speed_meter_sprites, timer_sprites):
        self.player = player
        self.speed_meter_sprites = speed_meter_sprites
        self.timer_sprites = timer_sprites

    # Updates (image components of the) UI sprites.
    def update(self, elapsed_milliseconds):
        # Update speed meter sprite images.
        # Least significant digit is at index 0,
        # most significant digit is at maximum index.
        display_speed = int(abs(self.player.current_speed * SPEED_DISPLAY_MULTIPLIER))
        for i in range(0, 4):
            self.speed_meter_sprites[i].image = NUMBER_IMAGES[
                (display_speed // (10 ** i)) % 10
            ]

        # update timer UI
        self.timer_sprites[0].image = NUMBER_IMAGES[
            int(elapsed_milliseconds) % 10
        ]
        self.timer_sprites[1].image = NUMBER_IMAGES[
            (int(elapsed_milliseconds) // 10) % 10
        ]
        self.timer_sprites[2].image = NUMBER_IMAGES[
            (int(elapsed_milliseconds) // 100) % 10
        ]
        self.timer_sprites[3].image = NUMBER_IMAGES[
            (int(elapsed_milliseconds) // 1000) % 10
        ]
        self.timer_sprites[4].image = NUMBER_IMAGES[
            (int(elapsed_milliseconds) // 10000) % 6
        ]
        self.timer_sprites[5].image = NUMBER_IMAGES[
            (int(elapsed_milliseconds) // 60000) % 10
        ]
        self.timer_sprites[6].image = NUMBER_IMAGES[
            (int(elapsed_milliseconds) // 600000) % 10
        ]