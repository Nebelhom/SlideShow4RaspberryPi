#!usr/bin/env python

from os import listdir, getcwd
import random

import pygame
from pygame.locals import *

import helper_func as hf

pygame.init()

FORMATS = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'pcx', 'tga', 'tif', 'lbm',
           'pbm', 'pgm', 'ppm', 'xpm']

# Obtain the current display info for scaling of the image
# see line below pygame.transform.scale
infoObject = pygame.display.Info()
SCREEN_RES = (infoObject.current_w, infoObject.current_h)


class SlideShow:
    """
    Write proper documentation!!!
    Runs slideshow using pygame
    """

    def __init__(self, time_delay=3000, path2imgs=getcwd()):
        # Sorting out the images
        self.imgsrc = hf.list_img_paths(path2imgs)
        self.imgpath = random.choice(self.imgsrc)
        # will be populated as pygame.Surface in run method
        self.img = None

        # Defines how much time passes between image switch
        self.time_delay = time_delay


    def run(self):
        """
        DEFINITION
        TODOs
        * Deal with rotation images (orientation landscape vs. portrait)
            * Most likely decide on landscape or portrait and pick a good screen.
        * Switch the image and regular intervals (X Minutes)
        * After that look into motion sensor with Raspberry Pi Zero
        * The sleep function for Raspberry and wake up
        """

        black = (0, 0, 0)

        # Chooses the size of your display
        # Makes it portable to varying screens
        size = (0, 0)
        screen = pygame.display.set_mode(size, FULLSCREEN)

        running = True

        while running:
            self.imgpath = random.choice(self.imgsrc)
            self.img = pygame.image.load(self.imgpath)

            # Scale the image according to screen resolution
            new_dim = hf.aspect_scale(self.img.get_size(), SCREEN_RES)
            self.img = pygame.transform.scale(self.img, new_dim)
            # get the coordinates to center image
            centre_coord = hf.center_img(self.img.get_size(), SCREEN_RES)

            screen.fill(black)
            screen.blit(self.img, centre_coord)
            pygame.time.delay(self.time_delay)
            pygame.display.flip()

            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False
                if event.type is KEYDOWN and event.key == K_ESCAPE:
                    pygame.display.set_mode(size)
                if event.type is KEYDOWN and event.key == K_f:
                    pygame.display.set_mode(size, FULLSCREEN)


if __name__ == "__main__":
    sl = SlideShow()
    sl.run()
