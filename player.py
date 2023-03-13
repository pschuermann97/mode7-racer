import numpy

class Player:
    def __init__(self):
        self.position = (0, 0) # player initially is at origin position

    # Updates player data and position.
    # 
    # Parameters:
    # time: number of frames since the game started
    def update(self, time):
        # moving forward
        self.position = numpy.array([time, 0]) # player position changes depending on time, they move forward