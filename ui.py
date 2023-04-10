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
        pass