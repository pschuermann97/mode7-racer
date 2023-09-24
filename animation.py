# This module builds an animation-graph-like API 
# which can be used to play and transition between the multiple animations 
# of an animated object in the game.



# A class modelling a frame-based animation,
# consisting of a list of frames as well as a playback speed for the animation.
#
# Also keeps track of the frame of the animation that is currently displayed.
# 
# To allow for varying animation speeds, 
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
        self.frame_position += delta * self.speed

        # in case of overflow, wrap around
        while self.frame_position > self.length():
            self.frame_position -= self.length()

    # Returns the current frame of this animation.
    def current_frame(self):
        # integer type cast cuts the fractional part, effectively flooring the number
        return self.frames[int(self.frame_position) % self.length()]



# A class representing an animated object with its different animations.
# Also keeps track of which animation is currently playing.
#
# Animations are stored in a dictionary with strings as keys.
class AnimatedObject:
    def __init__(self, animations):
        self.animations = animations # dictionary containing the animations
        self.current_anim = None # current animation (object variable is created but cannot be initialized meaningfully)
    
    # Switches to the animation which is identified by the passed key (string).
    def switch_animation(self, new_anim_key):
        # actual switching
        self.current_anim = self.animations[new_anim_key]

        # restart animation to have a well-defined start/transition
        self.current_anim.restart()

    # Returns the current frame of the current animation.
    def current_frame(self):
        return self.current_anim.current_frame()
    
    # Makes the current animation advance by an amount that is proportional to the passed delta.
    # 
    # Parameters:
    # delta -  time between the last rendered game frame and the current one
    def advance_current_animation(self, delta):
        self.current_anim.advance(delta)



# A class handling the animations for the machines that are controllable in the game.
class AnimatedMachine(AnimatedObject):
    # Constructor that sets up animation automaton for machine. 
    def __init__(self, driving_anim, idle_anim):
        super().__init__({ "idle": idle_anim, "driving": driving_anim })

    def switch_to_driving_animation(self):
        self.switch_animation("driving")

    def switch_to_idle_animation(self):
        self.switch_animation("idle")