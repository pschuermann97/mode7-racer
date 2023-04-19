# Class representing a machine,
# including all physics engine related data (acceleration force, max speed, ...)
# and graphics
class Machine:
    def __init__(self, max_speed, acceleration, brake, speed_loss, centri, jump_duration_multiplier, idle_image, shadow_image):
        # ----------- physics variables initialization ----------------------



        # top speed
        self.max_speed = max_speed

        # acceleration force:
        # quantity of speed added per frame in which the player has the accelerator on
        self.acceleration = acceleration

        # brake force:
        # quantity of speed subtracted per frame in which the player holds down the brakes
        self.brake = brake

        # speed loss:
        # describes how well the machine retains speed when the player is not accelerating
        # more precisely, this is the quantity of speed subtracted in each frame
        # in which the player is not accelerating 
        # (but neither pushing the brakes)
        self.speed_loss = speed_loss

        # centrifugal force:
        # Determines how hard the machine is pushed towards the outside when steering.
        # More precisely, this is the percentage of the machine's maximum speed 
        # that is applied as centrifugal force.
        self.centri = centri

        # in seconds,
        # multiplied with the current speed in order to determine duration of a jump
        self.jump_duration_multiplier = jump_duration_multiplier



        # ----------- end of physics variables initialization ----------------------



        # ----------- graphics variables initialization ----------------------



        # image that is drawn when the machine is idle
        self.idle_image = idle_image

        # image of the shadow that the machine casts on the track
        # (should be drawn under the machine)
        self.shadow_image = shadow_image



        # ----------- end of graphics variables initialization ----------------------