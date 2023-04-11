from settings import SPEED_DISPLAY_MULTIPLIER, NUMBER_IMAGES

# Handles updates to the UI in every frame.
# Drawing of the UI is done in the main module (App class).
class UI:
    # Parameters:
    # player: player instance to track with this UI instance
    # speed_meter_sprites: array of the sprites that form the speed meter
    def __init__(self, player, speed_meter_sprites):
        self.player = player
        self.speed_meter_sprites = speed_meter_sprites

    # Updates (image components of the) UI sprites.
    def update(self):
        # Update speed meter sprite images.
        # Least significant digit is at index 0,
        # most significant digit is at maximum index.
        for i in range(0, 4):
            self.speed_meter_sprites[i].image = NUMBER_IMAGES[
                (int(self.player.current_speed * SPEED_DISPLAY_MULTIPLIER) // (10 ** i)) % 10
            ]
