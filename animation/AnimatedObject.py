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
    # delta -  time since the last rendered game frame and the current one
    def advance(self, delta):
        self.current_anim.advance(delta)
