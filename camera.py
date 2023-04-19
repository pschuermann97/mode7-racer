import numpy # for numpy array type for cam position and sin, cos

from settings.renderer_settings import CAM_DISTANCE

class Camera:
    def __init__(self, player, cam_dist = CAM_DISTANCE):
        # Declare position and angle variables of the camera.
        # Initialized with dummy values
        # which are overwritten in first frame of the game.
        self.position = numpy.array([0.0, 0.0])
        self.angle = 0

        self.tracked_player = player # the player that this camera should track
        self.camera_distance = cam_dist # distance the camera should keep to the player

    # Camera should always be behind the player,
    # at a certain distance.
    def update(self):
        # The offset can be computed the same way that the player's position
        # is updated when the player moves backwards.
        offset = numpy.array([
            - self.camera_distance * numpy.cos(self.tracked_player.angle), 
            - self.camera_distance * numpy.sin(self.tracked_player.angle)
        ])

        # for simplicity cam pos = player pos for now
        self.position = self.tracked_player.position + offset

        # camera always looks in the same direction as the player
        self.angle = self.tracked_player.angle