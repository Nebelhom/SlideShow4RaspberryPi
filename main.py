#!usr/bin/env python

from os import listdir, getcwd
import random

import pygame
from pygame.locals import *

pygame.init()

FORMATS = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'pcx', 'tga', 'tif', 'lbm',
           'pbm', 'pgm', 'ppm', 'xpm']

# Obtain the current display info for scaling of the image
# see line below pygame.transform.scale
infoObject = pygame.display.Info()
SCREEN_RES = (infoObject.current_w, infoObject.current_h)


def list_img_paths(cpath):
    """
    Lists all image filenames in the path directory, p.
    curpath: String: Correctly formatted path according to platform
    Returns:
    List of strings of image filenames.
    """

    return [i for i in listdir(cpath) if i.split('.')[-1].lower() in FORMATS]


def aspect_scale(img, resolution):
    """
    Scales 'img' to fit into box bx/by. This method will retain the original
    image's aspect ratio.
    Reference: http://www.pygame.org/pcr/transform_scale/

    img: Pygame Surface Object: Image loaded into Pygame
    resolution: tuple of integers: The resolution of the display

    Returns:
    Pygame Surface Object: Rescaled to fit the surface according to its aspect
    ratio.
    """

    bx, by = resolution
    ix, iy = img.get_size()
    if ix > iy:
        # fit to width
        scale_factor = bx / float(ix)
        sy = int(scale_factor * iy)
        if sy > by:
            scale_factor = by / float(iy)
            sx = int(scale_factor * ix)
            sy = by
        else:
            sx = bx
    else:
        # fit to height
        scale_factor = by / float(iy)
        sx = int(scale_factor * ix)
        if sx > bx:
            scale_factor = bx / float(ix)
            sx = bx
            sy = int(scale_factor * iy)
        else:
            sy = by

    return pygame.transform.scale(img, (sx, sy))


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
        * Deal with rotation images (orientation landscape vs. portrait)
            * Most likely decide on landscape or portrait and pick a good screen.
        * Switch the image and regular intervals (X Minutes)
        * After that look into motion sensor with Raspberry Pi Zero
        * The sleep function for Raspberry and wake up
        """

        img = pygame.image.load(self.img)
        black = (0, 0, 0)

        # Chooses the size of your display
        # Makes it portable to varying screens
        size = (0, 0)
        screen = pygame.display.set_mode(size, FULLSCREEN)
        screen.fill(black)

        running = True

        while running:
            new_img = random.choice(self.imgsrc)

            screen.fill((white))

            screen.blit(img, (0, 0))
            self.img = pygame.image.load(new_img)
            screen.fill(black)
            screen.blit(aspect_scale(self.img, SCREEN_RES), (0, 0))
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
