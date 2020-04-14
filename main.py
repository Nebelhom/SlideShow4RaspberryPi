#!usr/bin/env python

from os import listdir, getcwd
import random

import pygame
from pygame.locals import *

pygame.init()

FORMATS = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'pcx', 'tga', 'tif', 'lbm',
           'pbm', 'pgm', 'ppm', 'xpm']

def list_img_paths(cpath):
    """
    Lists all image filenames in the path directory, p.
    curpath: String: Correctly formatted path according to platform
    Returns:
    List of strings of image filenames.
    """

    return [i for i in listdir(cpath) if i.split('.')[-1].lower() in FORMATS]


class SlideShow:
    """
    Write proper documentation!!!
    Runs slideshow using pygame
    """

    def __init__(self, imgpath=getcwd()):
        self.imgsrc = list_img_paths(imgpath)
        self.img = random.choice(self.imgsrc)
        self.imgpath = imgpath


    def run(self):
        """
        DEFINITION
        TODOs
        * Set up the github for version control and project structure
        * make image scaled to screen
        * Deal with rotation images (orientation landscape vs. portrait)
            * Most likely decide on landscape or portrait and pick a good screen.
        * Switch the image and regular intervals (X Minutes)
        * After that look into motion sensor with Raspberry Pi Zero
        * The sleep function for Raspberry and wake up
        """

        # Make image now scaled to surface and resizable acording to screen size
        # https://stackoverflow.com/questions/20002242/how-to-scale-images-to-screen-size-in-pygame

        img = pygame.image.load(self.img)

        white = (0, 0, 0)
        size = (0, 0)
        screen = pygame.display.set_mode(size, FULLSCREEN)
        screen.fill((white))
        running = True

        while running:
            new_img = random.choice(self.imgsrc)

            screen.fill((white))

            screen.blit(img, (0, 0))
            self.img = pygame.image.load(new_img)
            screen.fill(white)
            screen.blit(self.img, (0, 0))
            pygame.time.delay(3000)
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
