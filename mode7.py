import pygame
import numpy

# JIT compiler and range function for performance speedup
from numba import njit, prange

from settings import *

class Mode7:
    # initialization method that loads the textures 
    # and links this mode-7 renderer to the app
    def __init__(self, app):
        self.app = app



        # load floor texture
        self.floor_tex = pygame.image.load('2018_track_combined.png').convert()
        
        # store texture size for later use
        self.floor_tex_size = self.floor_tex.get_size()

        # Create 3D array representing the pixels representing the floor.
        # More precisely: copies the pixels from the surface representing the floor texture
        # into a new 3D array.
        self.floor_array = pygame.surfarray.array3d(self.floor_tex)



        # load ceiling texture
        self.ceil_tex = pygame.image.load('test_floor.png').convert()

        # scale ceiling texture to floor texture size
        self.ceil_tex = pygame.transform.scale(self.ceil_tex, self.floor_tex_size)

        # represenent ceiling by 3D array analogous to floor
        self.ceil_array = pygame.surfarray.array3d(self.ceil_tex)



        # create an array representing the screen pixels
        self.screen_array = pygame.surfarray.array3d(pygame.Surface(WIN_RES))

    def update(self):
        self.screen_array = self.render_frame(self.floor_array, self.ceil_array, self.screen_array, self.floor_tex_size)

    # Computes a single frame of the floor texture pixel by pixel.
    # Needs numba just-in-time compiler support (decorators) 
    # to achieve a reasonable framerate when executed every frame.
    @staticmethod
    @njit(fastmath=True, parallel=True)
    def render_frame(floor_array, ceil_array, screen_array, tex_size):
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

                # apply mode-7 style projection
                px = x / z * SCALE
                py = y / z * SCALE

                # Compute which pixel of the floor texture is over the point (i, j)
                floor_pos = int(px % tex_size[0]), int(py % tex_size[1])

                # look up the respective color in the floor array
                floor_col = floor_array[floor_pos]

                # Pixel of the ceil texture that is over the counterpart (i, -j) of (i, j)
                # has the same coordinates than the pixel of the floor texture
                # that is over (i, j).
                # By coordinates, we hereby mean coordinates in the texture coordinate system.
                ceil_pos = floor_pos

                # look up the respective color in the ceiling array
                ceil_col = ceil_array[ceil_pos]

                # To prevent ugly artifacts at the horizon:
                # compute some attenuation coefficient in the interval [0, 1] based on the "depth" value
                # and apply it component wise to the color vector representing the computed floor color.
                attenuation = min(max(1.5 * (abs(z) / HALF_HEIGHT), 0), 1)
                floor_col = (floor_col[0] * attenuation,
                    floor_col[1] * attenuation,
                    floor_col[2] * attenuation)
                ceil_col = (ceil_col[0] * attenuation,
                    ceil_col[1] * attenuation,
                    ceil_col[2] * attenuation)

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