#!/usr/bin/env python

import os
os.environ['KIVY_NO_ARGS'] = '1'
from os.path import join, isdir
import random
import re

import helper_func as hf
import configparser as cp

import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.properties import (BooleanProperty, NumericProperty, ObjectProperty,
StringProperty)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton

# Automagically sets image to maximum resolution and Window to fullscreen
Window.fullscreen = 'auto'
CONFIGFILE = 'settings.conf'


CONFIG = cp.ConfigParser()
CONFIG.read(CONFIGFILE)

# Configuration
FRAME_ORIENTATION = CONFIG['SLIDESHOW']['frame_orientation']

if isdir(CONFIG['SLIDESHOW']['img_dir']):
    IMG_DIR = CONFIG['SLIDESHOW']['img_dir']
else:
    IMG_DIR = os.getcwd()

TIME_DELAY = CONFIG['SLIDESHOW']['time_delay']


class RootWidget(BoxLayout):
    """RootWidget is the base Widget of this application.
    """

    def __init__(self, **kwargs):
        """Constructor method
        """

        super(RootWidget, self).__init__(**kwargs)

        self.picture = Picture(img_dir=IMG_DIR,
                               time_delay=TIME_DELAY,
                               frame_orientation=FRAME_ORIENTATION)
        self.menu = Menu(img_dir=IMG_DIR,
                         time_delay=TIME_DELAY,
                         frame_orientation=FRAME_ORIENTATION)

        #self.add_widget(self.menu)
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

    def __init__(self, img_dir, time_delay, frame_orientation, *args, **kwargs):
        """Constructor method
        """

        super(Picture, self).__init__(*args, **kwargs)

        self.scheduled_event = None

        self._img_dir = img_dir
        # Defines how much time passes between image switch
        self.time_delay = int(time_delay)

        # Defines if the screen sits in landscape or portrait
        self.__frame_orientation = frame_orientation

        # Defines the initial starting image
        self.imgs = hf.list_img_paths(self.img_dir)
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
    def img_dir(self):
        return self._img_dir

    @img_dir.setter
    def img_dir(self, value):
        self._img_dir = value

    @img_dir.deleter
    def img_dir(self):
        del self._img_dir

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
        """On single tap, opens Menu Class to set configurations.
        """

        self.parent.add_widget(self.parent.menu)
        self.parent.remove_widget(self.parent.picture)


class Menu(BoxLayout):
    """Class that is called when entering the Menu by a single tap from Picture
    class.
    """

    # Configuration
    frame_orientation = StringProperty('')
    img_dir = StringProperty('')
    time_delay = NumericProperty(0)

    # For DirPopup
    dirdialog = ObjectProperty(None)
    cancel = ObjectProperty(None)


    #def __init__(self, frame_orientation=frame_orientation,
    #             img_dir=img_dir, time_delay=time_delay, **kwargs):
    def __init__(self, frame_orientation, img_dir, time_delay, **kwargs):
        """The constructor method
        """

        super(Menu, self).__init__(**kwargs)
        # DirDialog created in show_dirdialog
        self.dialog = None
        
        self.frame_orientation = frame_orientation
        self.img_dir = img_dir
        self.time_delay = time_delay

    def choose(self):
        self.img_dir = self.dialog.ids['filechooser'].path
        self.dismiss_popup()

    def close_menu(self, *args):
        """Close the menu and open Picture widget
        
        :param args: list with only one Boolean parameter to pass from kv to
        py script to trigger self.save_settings() or not
        :type args: list
        """
        if args[0]:
            self.save_settings()
        else:
            if FRAME_ORIENTATION == "landscape":
                self.ids["landscape"].state = "down"
                self.ids["portrait"].state = "normal"
            else:
                self.ids["landscape"].state = "normal"
                self.ids["portrait"].state = "down"
            self.ids["img_dir_text"].text = IMG_DIR
            self.ids["td_spin"].text_value = TIME_DELAY

        self.parent.picture = Picture(img_dir=IMG_DIR,
                                      time_delay=TIME_DELAY,
                                      frame_orientation=FRAME_ORIENTATION)
        self.parent.add_widget(self.parent.picture)
        self.parent.remove_widget(self.parent.menu)

    def dismiss_popup(self):
        """Closes the popup.
        """
        self._popup.dismiss()

    def save_settings(self):
        """Saves the settings of the config file.
        """

        # Reference:
        # https://stackoverflow.com/questions/31763187/is-there-builtin-way-to-get-a-togglebutton-groups-current-selection
        current = [t for t in ToggleButton.get_widgets('orientation')
                   if t.state == 'down'][0].text.lower()
        global FRAME_ORIENTATION
        FRAME_ORIENTATION = current
        CONFIG['SLIDESHOW']['frame_orientation'] = current

        # Image Directory
        global IMG_DIR
        IMG_DIR = self.ids.img_dir_text.text
        CONFIG['SLIDESHOW']['img_dir'] = self.ids.img_dir_text.text

        # Time Delay
        # Reference:
        # https://stackoverflow.com/questions/30202801/how-to-access-id-widget-of-different-class-from-a-kivy-file-kv
        global TIME_DELAY
        TIME_DELAY = self.ids.td_spin.output.text
        CONFIG['SLIDESHOW']['time_delay'] = self.ids.td_spin.output.text

        # Save all values to file
        with open(CONFIGFILE, 'w') as configfile:
            CONFIG.write(configfile)    


    def show_dirdialog(self):
        """Opens a DirDialog class allowing the user to choose a directory.
        """

        self.dialog = DirDialog(choice=self.choose, cancel=self.dismiss_popup)
        self._popup = Popup(title="Choose the directory containing your"
                            " picture. Enter the directory you wish to choose"
                            " before confirming.",
                            content=self.dialog,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def quit_app(self):
        """Quits the app and closes it.
        """
        
        App.get_running_app().stop()

    def update_vars(self):
        """Updates all the properties based on global vars.
        """
        self.frame_orientation = FRAME_ORIENTATION
        self.img_dir = IMG_DIR
        self.time_delay = TIME_DELAY
        
        if FRAME_ORIENTATION == "landscape":
            self.ids["landscape"].state = "down"
            self.ids["portrait"].state = "normal"
        else:
            self.ids["landscape"].state = "normal"
            self.ids["portrait"].state = "down"
        self.ids.img_dir_text.text = IMG_DIR
        self.ids.td_spin.output.text = TIME_DELAY


class SpinBox(BoxLayout):
    """Class allowing a text box filled only with numbers to add +1 or subtract
    minus 1 from the value in the text box.
    
    This class is linked to PosIntInput Class.
    """
    
    text_value = StringProperty('')
    output = ObjectProperty(None)

    def __init__(self, text_value=TIME_DELAY, **kwargs):
        """The constructor method
        """

        super(SpinBox, self).__init__(**kwargs)
        self.text_value = str(text_value)

    def plus(self):
        """Adds +1 to a number in string format
        """
        newval = int(self.text_value) + 1
        self.text_value = str(newval)

    def minus(self):
        """Subtracts 1 from a number in string format
        """
        newval = int(self.text_value) - 1
        if newval >= 1:
            self.text_value = str(newval)
        else:
            self.text_value = '1'


class PosIntInput(TextInput):
    """Allows only positive integer values to be inserted

    Reference:
    https://kivy.org/doc/stable/api-kivy.uix.textinput.html
    """
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):
        s = re.sub(self.pat, '', substring)
        return super(PosIntInput, self).insert_text(s, from_undo=from_undo)


class DirDialog(FloatLayout):
    """Dialog Box allowing the user to choose a specific directory where the
    images are saved.
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
