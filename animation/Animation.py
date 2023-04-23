# A class modelling a frame-based animation,
# consisting of a list of frames as well as a playback speed for the animation.
#
# Also keeps track of the frame of the animation that is currently displayed.
# 
# To allow for variying animation speeds, 
# the frame position is a floating point number (instead of an integer, as one might expect).
# The current frame number is the integer portion of the frame_position variable,
# while the fractional part of it quantifies the percentage of the duration of the current frame that has already elapsed
# (shoutout to the YouTuber Clear Code for the idea with the fractional frame position to allow for varying animation playback speed).
class Animation:
    def __init__(self, frames, speed):
        self.frames = frames # list of frames the animation consists of (contents have type pygame.Surface)
        self.speed = speed # parameter used to control how fast the animation is played
        self.frame_position = 0.0 # indicating the current position in the animation 

    # Returns the length of the animation in frames.
    def length(self):
        return len(self.frames)

    # Restarts the animation by jumping to first frame.
    def restart(self):
        self.frame_position = 0.0

    # Advances this animation by an amount that is proportional to the passed delta.
    # The delta is the time since the current frame of the game (not the animation!)
    # and the last frame of the game.
    # This is what makes the animation playback speed independent of the framerate
    # of the hardware that currently executes the game.
    def advance(self, delta):
        self.frame_position += delta * speed

    # Returns the current frame of this animation.
    def current_frame(self):
        # integer type cast cuts the fractional part, effectively flooring the number
        return self.frames[int(self.frame_position)]