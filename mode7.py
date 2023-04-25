import pygame
import numpy

# JIT compiler and prange function for performance speedup
from numba import njit, prange

from settings.renderer_settings import *

class Mode7:
    # Initialization method that loads the textures (specified via path passed to constructor), 
    # links this mode-7 renderer to the app
    # and sets some status variables.
    # 
    # The horizon parameter describes the horizon height of the scenes rendered with this renderer
    # i.e. the minimum height of floor texture pixels 
    # (for this, note that the y coordinate decreases down the screen). 
    def __init__(self, app, floor_tex_path, bg_tex_path, is_foggy, horizon = STD_HORIZON):
        # linking renderer to the app
        self.app = app

        # intiailizing status variables
        self.is_foggy = is_foggy
        self.horizon = horizon

        # load floor texture
        self.floor_tex = pygame.image.load(floor_tex_path).convert()
        
        # store floor texture size for later use
        self.floor_tex_size = self.floor_tex.get_size()

        # Create 3D array representing the pixels representing the floor.
        # More precisely: copies the pixels from the surface representing the floor texture
        # into a new 3D array.
        self.floor_array = pygame.surfarray.array3d(self.floor_tex)

        # load background texture
        self.bg_tex = pygame.image.load(bg_tex_path).convert()

        # scale ceiling texture to floor texture size
        self.bg_tex_size = self.bg_tex.get_size()

        # represent ceiling by 3D array analogously to floor
        self.bg_array = pygame.surfarray.array3d(self.bg_tex)

        # create an array representing the screen pixels
        self.screen_array = pygame.surfarray.array3d(pygame.Surface(WIN_RES))

    # Updates the mode7-based environment.
    # A camera reference is passed to be able
    # to render the frame based on the camera's (and thus player's) current position and rotation.
    def update(self, camera):
        # rendering the frame
        self.screen_array = self.render_frame(
            floor_array = self.floor_array, 
            bg_array = self.bg_array, 
            screen_array = self.screen_array, 
            floor_tex_size = self.floor_tex_size, 
            bg_tex_size = self.bg_tex_size, 
            is_foggy = self.is_foggy, 
            pos = camera.position,
            angle = camera.angle,
            horizon = self.horizon
        )

    # Computes a single frame of the mode-7 environment pixel by pixel.
    # Needs numba just-in-time compiler support (decorators) 
    # to achieve a reasonable framerate when executed every frame.
    # 
    # Parameters:
    # floor_array: array containing the pixels of the floor texture
    # bg_array: array containing the pixels of the background texture
    # screen_array: array containing the rendered frame (updated pixel by pixel)
    # floor_tex_size: size of the floor texture
    # bg_tex_size: size of the background texture
    # is_foggy: whether the scene of which a frame is rendered has a fog effect in it
    # pos: current position of the camera
    # angle: current angle by which the camera is rotated
    # horizon: the min y coordinate of floor pixels (note: y increases down the screen)
    @staticmethod
    @njit(fastmath=True, parallel=True)
    def render_frame(floor_array, bg_array, screen_array, floor_tex_size, bg_tex_size, 
        is_foggy, pos, angle, horizon):
        # Compute the sine and cosine values of the player angle
        # to use them to render the environment based on the player's rotation.
        sin, cos = numpy.sin(angle), numpy.cos(angle)

        # Compute color value for every single pixel (i, j).
        # prange function (instead of range function) used for outer loop for performance reasons.
        for i in prange(WIDTH):
            # compute background image render
            for j in range(0, horizon):
                # background image is shifted by angle the player is rotated by
                screen_array[i][j] = bg_array[(i + int(angle * BACKGROUND_ROTATION_SPEED)) % bg_tex_size[0]][j % bg_tex_size[1]]
            # compute floor render
            for j in range(horizon, HEIGHT):
                # Let us imagine that the floor texture is tiled infinitely 
                # in both horizontal and vertical direction on a 2D plane.
                # Let us assume that this plane's horizontal and vertical axes
                # are labeled with px and py, respectively.
                # Furthermore assume that the screen's horizontal and vertical axes 
                # are labeled with x and z, respectively,
                # while y is an imaginary axis coming out of the screen.
                #
                # Idea: to emulate the mode-7 effect, compute which pixel of the floor texture 
                # is over the pixel (i, j) of the screen in this frame
                
                # First step: compute the raw x, y, z coordinates
                # without mode-7 style projection.
                #
                # We adjust the x coordinate so the texture is at the center of the screen.
                # Furthermore, the depth coordinate (y) is always shifted by the focal length of the camera.
                # Lastly, we need to add a small constant to the screen height coordinate (z)
                # to prevent divide-by-0 errors in the next step.
                x = HALF_WIDTH - i  
                y = j + FOCAL_LEN 
                z = j - horizon + 0.01 

                # Apply player's rotation (which is computed from the angle they are rotated by),
                # "standard formula for rotation in 2D space".
                rx = x * cos + y * sin
                ry = x * -sin + y * cos

                # Apply mode-7 style projection.
                # Camera position is used as offset here to allow movement
                px = (rx / z + pos[1]) * SCALE
                py = (ry / z + pos[0]) * SCALE

                # Compute which pixel of the floor texture is over the point (i, j)
                floor_pos = int(px % floor_tex_size[0]), int(py % floor_tex_size[1])

                # look up the respective color in the floor array
                floor_col = floor_array[floor_pos]

                # To prevent ugly artifacts at the horizon:
                # compute some attenuation coefficient in the interval [0, 1] based on the "depth" value
                attenuation = min(max(7.5 * (abs(z) / HALF_HEIGHT), 0), 1)

                # Compute a fog effect depending on whether the rendered scene is foggy.
                fog = (1 - attenuation) * FOG_DENSITY if is_foggy else 0
                
                # apply attenuation and optional fog effect (component-wise, to color vector)
                floor_col = (floor_col[0] * attenuation + fog,
                    floor_col[1] * attenuation + fog,
                    floor_col[2] * attenuation + fog)

                # fill the computed pixel into the screen array
                screen_array[i, j] = floor_col

        return screen_array

    def draw(self):
        # Draws the screen contents that were computed in the render_frame method.
        #
        # Copies values from the array representing the screen 
        # into the surface representing the screen.
        # This surface is automatically rendered by pygame.
        pygame.surfarray.blit_array(self.app.screen, self.screen_array)
