# Debug mode settings

from settings.machine_settings import MACHINES

# whether the game currently is in "developer mode", where the camera can move around freely in the scene
IN_DEV_MODE = False

# whether collisions with the track borders and obstacles are being detected (i.e. solid)
COLLISION_DETECTION_OFF = True

# whether the debug menu for choosing a machine appears before starting the game
DEBUG_CHOOSE_MACHINE = False
DEFAULT_MACHINE = MACHINES[2]