# Class representing a machine,
# including all physics engine related data (acceleration force, max speed, ...)
# and graphics
class Machine:
    def __init__(self, max_speed, boosted_max_speed, acceleration, brake, speed_loss, boosted_speed_loss, 
            centri, jump_duration_multiplier, boost_duration, max_energy, boost_cost, hit_cost, recover_speed,
            rotation_speed, idle_image_path, shadow_image_path):
        # ----------- physics variables initialization ----------------------



        # top speed
        self.max_speed = max_speed
        self.boosted_max_speed = boosted_max_speed # max speed when having a boost active

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
        self.boosted_speed_loss = boosted_speed_loss # speed loss is different when having a boost active

        # centrifugal force:
        # Determines how hard the machine is pushed towards the outside when steering.
        # More precisely, this is the percentage of the machine's maximum speed 
        # that is applied as centrifugal force.
        self.centri = centri

        # in seconds,
        # multiplied with the current speed in order to determine duration of a jump
        self.jump_duration_multiplier = jump_duration_multiplier

        # duration of a boost in seconds
        self.boost_duration = boost_duration

        # maximum amount energy this machine can have
        self.max_energy = max_energy

        # how much energy the machine loses when using the booster
        self.boost_cost = boost_cost

        # used in determining the amount of energy the machine loses when hitting obstacles
        self.hit_cost = hit_cost

        # how fast the machine recovers energy when in a recovery zone
        self.recover_speed = recover_speed

        # how fast the player can rotate when steering
        self.rotation_speed = rotation_speed



        # ----------- end of physics variables initialization ----------------------



        # ----------- graphics variables initialization ----------------------



        # image that is drawn when the machine is idle
        self.idle_image_path = idle_image_path

        # image of the shadow that the machine casts on the track
        # (should be drawn under the machine)
        self.shadow_image_path = shadow_image_path



        # ----------- end of graphics variables initialization ----------------------