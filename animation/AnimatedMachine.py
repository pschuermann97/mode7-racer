# A class handling the animations for the machines that are controllable in the game.
class AnimatedMachine(AnimatedObject):
    def __init__(self, driving_anim, idle_anim):
        self.animations = { "idle": idle_anim, "driving": driving_anim }

    def switch_to_driving_animation(self):
        self.switch_animation("driving")

    def switch_to_idle_animation(self):
        self.switch_animation("idle")