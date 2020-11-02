#!/usr/bin/env python

import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout


import os
import random

import pygame

import helper_func as hf

"""
TODO:
Work on rotation of images. This is not trivial in kivy.
apparently need to use PushMatrix and PopMatrix.

Moving widget layout into kv stops this code from working.

Frustrating! Ideally try to move to kv language first and
then work on it.

RootWidget should be able to house both a menu and the slideshow.

Take into account and search for it "How to have Menu and Game in the
same menu" type query.
"""


class RootWidget(BoxLayout):
    """
    Description
    """

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)


class Picture(Image):
    """
    Description tbd
    """
    # Without this declaration, the value will not arrive in kv file
    # called as self.angle in the code below
    angle = NumericProperty(0)

    def __init__(self, path2imgs=os.getcwd(), time_delay=3,
                 frame_orientation='landscape', *args, **kwargs):
        super(Picture, self).__init__(*args, **kwargs)

        # Defines how much time passes between image switch
        self.time_delay = time_delay

        # Defines if the screen sits in landscape or portrait
        self.__frame_orientation = frame_orientation

        # Defines the initial starting image
        self.imgs = hf.list_img_paths(path2imgs)
        self.source = random.choice(self.imgs)
        self.set_angle()

        # Switches the image displayed after duration of
        # self.timedelay in seconds
        Clock.schedule_interval(self.change_image, self.time_delay)

    def change_image(self, *args):
        """
        Updates the path to picture.
        """
        self.source = random.choice(self.imgs)
        self.set_angle()
        print("angle is ", self.angle)


    def set_angle(self):
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

        Currently, flipping images is not supported as kivy makes it unnecessarily
        difficult to do so for little gain
        In landscape that would be EXIF value 2, 4, 5 and 7

        If there is an issue, please contact me and send me an example image.
        """
        o = hf.get_img_orientation(self.source)
        if self.__frame_orientation == "landscape":
            # This is landscape orientation
            if o == 1:
                self.angle = 0
            elif o == 3:
                self.angle = -180
            elif o == 6:
                self.angle = -90
            elif o == 8:
                self.angle = 90
            else:
                print("No valid image orientation value in the EXIF.\
                 Use as is.")

        elif self.__frame_orientation == "portrait":
            if o == 1:
                self.angle = 90
            elif o == 3:
                self.angle = -90
            # This is portrait orientation
            elif o == 6:
                self.angle = 0
            elif o == 8:
                self.angle = -180
            else:
                print("No valid image orientation value in the EXIF.\
                 Use as is.")
        else:
            raise SyntaxError("No valid image orientation was given. Did you\
                              check spelling?")        


class SlideShowApp(App):

    def build(self):
        root = RootWidget()
        return root


if __name__ == '__main__':
    SlideShowApp().run()