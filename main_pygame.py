#!usr/bin/env python

from os import getcwd
import random
import threading as th

import pygame
from pygame.locals import *

import helper_func as hf

pygame.init()

FORMATS = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'pcx', 'tga', 'tif', 'lbm',
           'pbm', 'pgm', 'ppm', 'xpm']
BLACK = (0, 0, 0)

# Obtain the current display info for scaling of the image
# see line below pygame.transform.scale
infoObject = pygame.display.Info()
SCREEN_RES = (infoObject.current_w, infoObject.current_h)


class SlideShow:
    """
    Write proper documentation!!!
    Runs slideshow using pygame
    """

    def __init__(self, time_delay=3, orientation="landscape",
                 path2imgs=getcwd()):

        # Sorting out the images
        self.imgsrc = hf.list_img_paths(path2imgs)
        self.imgpath = random.choice(self.imgsrc)
        # will be populated as pygame.Surface in run method
        self.img = None

        # Defines how much time passes between image switch
        self.time_delay = time_delay
        self.time2switch = True

        # Check the desired image orientation
        self.orientation = orientation

    def change_image(self):
        """
        Updates the path to picture.
        """

        self.imgpath = random.choice(self.imgsrc)

    def rotate_image(self):
        """
        Rotates the image according to its original orientation
        to fit the screen.
        Original orientation is obtained using EXIF data using the
        Pillow library (see helper.func.py)
        Depending on screen orientation, you can choose either landscape
        or portrait.
        The function with rotate accordingly.

        Reference:
        https://www.daveperrett.com/articles/2012/07/28/exif-orientation-handling-is-a-ghetto/


        Anything but 1 and 6 are untested as I have not had any images like that.
        If there is an issue, please contact me and send me an example image.
        """

        o = hf.get_img_orientation(self.imgpath)

        if self.orientation == "landscape":
            # This is landscape orientation
            if o == 1:
                pass
            elif o == 2:
                self.img = pygame.transform.flip(self.img, True, False)
            elif o == 3:
                self.img = pygame.transform.rotate(self.img, -180)
            elif o == 4:
                self.img = pygame.transform.flip(self.img, False, True)
            elif o == 5:
                self.img = pygame.transform.flip(self.img, True, False)
                self.img = pygame.transform.rotate(self.img, -90)
            elif o == 6:
                self.img = pygame.transform.rotate(self.img, -90)
            elif o == 7:
                self.img = pygame.transform.flip(self.img, True, False)
                self.img = pygame.transform.rotate(self.img, 90)
            elif o == 8:
                self.img = pygame.transform.rotate(self.img, 90)
            else:
                print("No valid image orientation value in the EXIF.\
                 Use as is.")

        elif self.orientation == "portrait":
            if o == 1:
                self.img = pygame.transform.rotate(self.img, 90)
            elif o == 2:
                self.img = pygame.transform.flip(self.img, True, False)
                self.img = pygame.transform.rotate(self.img, 90)
            elif o == 3:
                self.img = pygame.transform.rotate(self.img, 90)
            elif o == 4:
                self.img = pygame.transform.flip(self.img, True, False)
                self.img = pygame.transform.rotate(self.img, -90)
            elif o == 5:
                self.img = pygame.transform.flip(self.img, True, False)
            # This is portrait orientation
            elif o == 6:
                pass
            elif o == 7:
                self.img = pygame.transform.flip(self.img, False, True)
            elif o == 8:
                self.img = pygame.transform.rotate(self.img, -180)
            else:
                print("No valid image orientation value in the EXIF.\
                 Use as is.")
        else:
            raise SyntaxError("No valid image orientation was given. Did you\
             check spelling?")


    def signal_switch_image(self):
        """
        Called by Timer to switch when time is up
        """
        self.time2switch = True

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

        # Chooses the size of your display
        # Makes it portable to varying screens
        size = (0, 0)
        screen = pygame.display.set_mode(size, FULLSCREEN)

        running = True

        while running:
            if self.time2switch:

                # Changes the image
                self.change_image()

                # Creates new Timer thread
                # Reminder: Cannot restart the same thread
                self.time2switch = False
                timer = th.Timer(self.time_delay, self.signal_switch_image)
                timer.start()

            self.img = pygame.image.load(self.imgpath)
            self.rotate_image()

            # Scale the image according to screen resolution
            new_dim = hf.aspect_scale(self.img.get_size(), SCREEN_RES)
            self.img = pygame.transform.scale(self.img, new_dim)
            # get the coordinates to center image
            centre_coord = hf.center_img(self.img.get_size(), SCREEN_RES)

            screen.fill(BLACK)
            screen.blit(self.img, centre_coord)
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
