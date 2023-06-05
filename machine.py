# Class representing a machine,
# including all physics engine related data (acceleration force, max speed, ...)
# and graphics
class Machine:
    def __init__(self, max_speed, boosted_max_speed, acceleration, boosted_acceleration, brake, speed_loss, 
            boosted_speed_loss, max_centri, centri_increase, centri_decrease, jump_duration_multiplier, boost_duration, max_energy, 
            boost_cost, hit_cost, recover_speed,
            rotation_speed, idle_anim, driving_anim, shadow_image_path):
        # ----------- physics variables initialization ----------------------



        # top speed
        self.max_speed = max_speed
        self.boosted_max_speed = boosted_max_speed # max speed when having a boost active

        # acceleration force:
        # quantity of speed added per frame in which the player has the accelerator on
        self.acceleration = acceleration
        self.boosted_acceleration = boosted_acceleration # accel force is different (usually stronger) when the booster is used

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

        # -------------------- centrifugal forces variables ------------------------------------------

        # centrifugal force:
        # Determines how hard the machine is pushed towards the outside when steering.
        # More precisely, the centrifugal forces varibales quantify the percentage of the machine's maximum speed 
        # that is applied as centrifugal force.

        # how much the centrifugal force increases in each frame the machine is turning
        self.centri_increase = centri_increase 

        # the limit for the maximum centrifugal force to be applied in a single frame
        self.max_centri = max_centri

        # how much the centrifugal force decreases in each frame the machine is not turning
        self.centri_decrease = centri_decrease

        # ---------------------- end of centrifugal forces variables -----------------------------------

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



        # images of the animation that is played when the machine is idle
        self.idle_anim = idle_anim

        # images of the animation that is played when the accelerator of the machine is on
        self.driving_anim = driving_anim

        # image of the shadow that the machine casts on the track
        # (should be drawn under the machine)
        self.shadow_image_path = shadow_image_path



        # ----------- end of graphics variables initialization ----------------------