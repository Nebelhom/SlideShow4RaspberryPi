#!/usr/bin/env python

import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup


import configparser as cp
import os
from os.path import join, isdir
import random

import helper_func as hf

"""
TODO:
RootWidget should be able to house both a menu and the slideshow.

Take into account and search for it "How to have Menu and Game in the
same menu" type query.
"""

# Automagically sets image to maximum resolution and Window to fullscreen
Window.fullscreen = 'auto'
CONFIGFILE = 'settings.conf'

# Configurations
CONFIG = cp.ConfigParser()
CONFIG.read(CONFIGFILE)
FRAME_ORIENTATION = CONFIG['DEFAULT']['orientation']
# Change this to CONFIG['DEFAULT']['img_dir'] as soon as you
# develop on raspberry pi
IMG_DIR = os.getcwd()
TIME_DELAY = int(CONFIG['DEFAULT']['time_delay'])


class RootWidget(BoxLayout):
    """RootWidget is the base Widget of this application.
    """


    def __init__(self, **kwargs):
        """Constructor method
        """

        super(RootWidget, self).__init__(**kwargs)

        self.picture = Picture(path2imgs=IMG_DIR,
                               time_delay=TIME_DELAY,
                               frame_orientation=FRAME_ORIENTATION)
        self.menu = Menu()

        self.add_widget(self.picture)

    def fullscreen_toggle(self):
        """Toggles between fullscreen and windowed mode.
        """

        if Window.fullscreen:
            Window.fullscreen = False
        else:
            # If set to True, the images will not have optimal resolution
            Window.fullscreen = 'auto'


class Picture(Image):
    """Key class extending the existing kivy.uix.image Image class to be used
    in the slide show.
    
    :param angle: The angle of image rotation in relation to the image's exif
                  orientation
    :type angle: int
    :param imgs: A list of all paths to relevant image files in the chosen
    image directory
    :type imgs: list
    :param scheduled_event: Shows whether an event is scheduled in kivy or not
    :type scheduled_event: None or kivy.clock.ClockEvent
    :param source: The path to the currently chosen image
    :type source: str
    :param time_delay: The time in seconds until the image shown is switched
    :type time_delay: int
    :param __frame_orientation: Defines if the screen is in 'landscape'
        or 'portrait' orientation, defaults to 'landscape'
    :type __frame_orientation: str
    """

    # Without this declaration, the value will not arrive in kv file
    # called as self.angle in the code below
    angle = NumericProperty(0)

    def __init__(self, path2imgs=os.getcwd(), time_delay=3,
                 frame_orientation='landscape', *args, **kwargs):
        """Constructor method
        """

        super(Picture, self).__init__(*args, **kwargs)

        self.scheduled_event = None

        self._path2imgs = path2imgs
        # Defines how much time passes between image switch
        self.time_delay = time_delay

        # Defines if the screen sits in landscape or portrait
        self.__frame_orientation = frame_orientation

        # Defines the initial starting image
        self.imgs = hf.list_img_paths(self.path2imgs)
        self.source = random.choice(self.imgs)
        self.set_angle()

        # Switches the image displayed after duration of
        # self.timedelay in seconds
        Clock.schedule_interval(self.change_image, self.time_delay)

    def change_image(self, *args):
        """Updates the path to image.

        NOTE: *args added to fit with Clock.schedule_interval call
        """

        self.source = random.choice(self.imgs)
        self.set_angle()

    @property
    def path2imgs(self):
        return self._path2imgs

    @path2imgs.setter
    def path2imgs(self, value):
        self._path2imgs = value

    @path2imgs.deleter
    def path2imgs(self):
        del self._path2imgs

    def set_angle(self):
        """
        Rotates the image according to its original orientation to fit the
        screen.
        
        Original orientation is obtained using EXIF data using the
        Pillow library (see helper.func.py). Depending on screen orientation,
        you can choose either landscape or portrait. The function with rotate
        accordingly.

        Anything but 1 and 6 are untested as I have not had any images like
        that.

        Currently, flipping images is not supported. In landscape that would be
        EXIF values 2, 4, 5 and 7. If there is an issue, please contact me and
        send me an example image.

        Reference:
        https://www.daveperrett.com/articles/2012/07/28/exif-orientation-handling-is-a-ghetto/


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

    def on_touch_down(self, touch):
        """Kivy standard function to capture a touch event and to link
           it to a method

        :param touch: a touch or click event with the screen
        :type touch: kivy.input.providers.mouse.MouseMotionEvent
        """

        # Reference:
        # https://stackoverflow.com/questions/64741710/python-3-kivy-react-only-to-double-tap-not-single-tap/64743622#64743622
        if self.scheduled_event is not None:
            self.scheduled_event.cancel()
            self.scheduled_event = None

        if touch.is_double_tap:
            self.parent.fullscreen_toggle()

        else:
            # 0.5 seems to be the right balance between response time and
            # ability to click fast enough. May differ on touchscreen
            double_tap_wait_s = 0.5
            self.scheduled_event = Clock.schedule_once(self.open_menu,
                                                       double_tap_wait_s)

    def open_menu(self, *args):
        """
        Placeholder function for when I need a single tap
        Planned is to open the menu
        """

        self.parent.add_widget(self.parent.menu)
        self.parent.remove_widget(self.parent.picture)


class Menu(BoxLayout):
    """Description
    """

    # Configuration
    frame_orientation = StringProperty(FRAME_ORIENTATION)
    img_dir = StringProperty(IMG_DIR)
    time_delay = NumericProperty(TIME_DELAY)

    # For DirPopup
    dirdialog = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def __init__(self, frame_orientation=FRAME_ORIENTATION,
                 img_dir=IMG_DIR, time_delay=TIME_DELAY, **kwargs):
        """The constructor method
        """

        super(Menu, self).__init__(**kwargs)
        # DirDialog created in show_dirdialog
        self.dialog = None

    def choose(self):
        self.img_dir = self.dialog.ids['filechooser'].path
        self.dismiss_popup()

    def close_menu(self):
        """Close the menu and open Picture widget
        """
        self.parent.add_widget(self.parent.picture)
        self.parent.remove_widget(self.parent.menu)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_dirdialog(self):
        self.dialog = DirDialog(choice=self.choose, cancel=self.dismiss_popup)
        self._popup = Popup(title="Choose the directory containing your"
                            " picture.",
                            content=self.dialog,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def quit_app(self):
        """Quits the app and closes it.
        """
        App.get_running_app().stop()


class SpinBox(BoxLayout):
    """Description
    """

    def __init__(self, **kwargs):
        """The constructor method
        """

        super(SpinBox, self).__init__(**kwargs)


class DirDialog(FloatLayout):
    """Description
    """
    choice = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def is_dir(self, directory, filename):
        return isdir(join(directory, filename))


class SlideShowApp(App):
    """The kivy.app Child starting the construction.
    """

    def build(self):
        root = RootWidget()
        return root

Factory.register('Menu', cls=Menu)
Factory.register('DirDialog', cls=DirDialog)

if __name__ == '__main__':
    SlideShowApp().run()
