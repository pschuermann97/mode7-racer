import numpy

class Player:
    def __init__(self, move_speed):
        self.position = (0, 0) # player initially is at origin position
        self.move_speed = move_speed # how fast the player can move through the scene

    # Updates player data and position.
    # 
    # Parameters:
    # time: number of frames since the game started
    def update(self, time):
        # moving forward
        self.position = numpy.array([time * self.move_speed, time * (self.move_speed / 2)]) # player position changes depending on time, they move forward