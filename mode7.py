import pygame
import numpy

# JIT compiler and range function for performance speedup
from numba import njit, prange

from settings import *

class Mode7:
    # initialization method that loads the textures, 
    # links this mode-7 renderer to the app
    # and sets some status variables.
    def __init__(self, app, is_foggy):
        self.app = app
        self.is_foggy = is_foggy



        # load floor texture
        self.floor_tex = pygame.image.load('2018_track_combined.png').convert()
        
        # store floor texture size for later use
        self.floor_tex_size = self.floor_tex.get_size()

        # Create 3D array representing the pixels representing the floor.
        # More precisely: copies the pixels from the surface representing the floor texture
        # into a new 3D array.
        self.floor_array = pygame.surfarray.array3d(self.floor_tex)



        # load ceiling texture
        self.ceil_tex = pygame.image.load('test_floor.png').convert()

        # scale ceiling texture to floor texture size
        self.ceil_tex_size = self.ceil_tex.get_size()

        # represenent ceiling by 3D array analogous to floor
        self.ceil_array = pygame.surfarray.array3d(self.ceil_tex)



        # create an array representing the screen pixels
        self.screen_array = pygame.surfarray.array3d(pygame.Surface(WIN_RES))

    def update(self, player):
        # rendering the frame
        self.screen_array = self.render_frame(self.floor_array, self.ceil_array, self.screen_array, self.floor_tex_size, self.ceil_tex_size, self.is_foggy, player.position)

    # Computes a single frame of the floor texture pixel by pixel.
    # Needs numba just-in-time compiler support (decorators) 
    # to achieve a reasonable framerate when executed every frame.
    # 
    # Parameters:
    # floor_array: array containing the pixels of the floor texture
    # ceil_array: array containing the pixels of the ceiling texture
    # screen_array: array containing the rendered frame (updated pixel by pixel)
    # tex_size: size of the floor texture
    # is_foggy: whether the scene of which a frame is rendered has a fog effect in it
    # pos: current position of the player
    @staticmethod
    @njit(fastmath=True, parallel=True)
    def render_frame(floor_array, ceil_array, screen_array, floor_tex_size, ceil_tex_size, is_foggy, pos):
        # Compute color value for every single pixel (i, j).
        # prange function (instead of range function) used for outer loop for performance reasons.
        for i in prange(WIDTH):
            for j in range(HALF_HEIGHT, HEIGHT):
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
                z = j - HALF_HEIGHT + 0.01 

                # Apply mode-7 style projection.
                # Player position is used as offset here to allow movement
                px = (x / z + pos[1]) * SCALE
                py = (y / z + pos[0]) * SCALE

                # Compute which pixel of the floor texture is over the point (i, j)
                floor_pos = int(px % floor_tex_size[0]), int(py % floor_tex_size[1])

                # look up the respective color in the floor array
                floor_col = floor_array[floor_pos]

                # Pixel of the ceil texture that is over the counterpart (i, -j) of (i, j)
                # has the same coordinates than the pixel of the floor texture
                # that is over (i, j).
                # By coordinates, we hereby mean coordinates in the texture coordinate system.
                ceil_pos = int(px % ceil_tex_size[0]), int(py % ceil_tex_size[1])

                # look up the respective color in the ceiling array
                ceil_col = ceil_array[ceil_pos]

                # To prevent ugly artifacts at the horizon:
                # compute some attenuation coefficient in the interval [0, 1] based on the "depth" value
                attenuation = min(max(7.5 * (abs(z) / HALF_HEIGHT), 0), 1)

                # Compute a fog effect depending on whether the rendered scene is foggy.
                fog = (1 - attenuation) * FOG_DENSITY if is_foggy else 0
                
                # apply attenuation and optional fog effect (component-wise, to color vector)
                floor_col = (floor_col[0] * attenuation + fog,
                    floor_col[1] * attenuation + fog,
                    floor_col[2] * attenuation + fog)
                ceil_col = (ceil_col[0] * attenuation + fog,
                    ceil_col[1] * attenuation + fog,
                    ceil_col[2] * attenuation + fog)

                # fill the computed pixel into the screen array
                screen_array[i, j] = floor_col
                screen_array[i, -j] = ceil_col

        return screen_array

    def draw(self):
        # Draws the screen contents that were computed in the render_frame method.
        #
        # Copies values from the array representing the screen 
        # into the surface representing the screen.
        # This surface is automatically rendered by pygame.
        pygame.surfarray.blit_array(self.app.screen, self.screen_array)