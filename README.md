# Slideshow for Raspberry Pi

Slideshow is a package written in [Python3](https://www.python.org/) that shows
a basic slideshow using the [Kivy library (Version 2.0.0)](https://www.kivy.org)
on [Raspberry OS](https://www.raspberrypi.org/software/).

Author: Johannes Vogel (Nebelhom)

## Installation

This program was written in Python 3.8 using Kivy version 2.0.0 on Raspbian GNU/Linux 10 (buster).

Please refer to the respective installation guides Raspberry OS.

**NOTE:** It never hurts to utilise a [virtual environment](https://virtualenv.pypa.io/en/latest/)
to avoid library conflicts.

[Python installation](https://www.python.org/downloads/) (This should already be installed)

[Kivy Installation](https://kivy.org/doc/stable/installation/installation-rpi.html)

## How to Use

### How to start the program
The easiest method to use the program right now is to run `python main.py` from
the folder. 

### Main Parameters
There are three main parameters to adjust according to your preferences. These are:

* **Frame Orientation**
    * Defines the orientation of the image frame, i.e whether it is landscape or portrait.
    * The image will be rotated accordingly, if the program can find existing EXIF data.

* **Image Directory**
    * Defines the path to the directory with the images to be displayed by the slideshow app.
    * Supported Formats are: jpg/jpeg, png, gif, bmp, pcx, tga, tif, lbm, pbm, pgm, ppm, xpm
    * Paths to directories on external hard drives or USB sticks is supported

* **Time Delay**
    * Defines the time in seconds that the program waits before switching images.

### How to adjust main parameters
There are three ways to adjust the main parameters of the program as outlined above.

1. Open the file `settings.conf` with the text editor of your choice and adjust the parameters accordingly
    * Care must be taken to not introduce invalid input
1. Use the Command Line Tool as outlined below
1. Start the program and left-click into the application. This will open the menu in which you can adjust the main parameters.

## Command Line Interface
```
usage: main.py [-h] [--orientation FRAME_ORIENTATION] [--img_dir IMG_DIR]
               [--time_delay TIME_DELAY] [--menu MENU_START]

Basic Image Slideshow for use on a raspberry Pi as a digital picture frame
(version 1.0).

optional arguments:
  -h, --help            show this help message and exit
  --orientation FRAME_ORIENTATION, -o FRAME_ORIENTATION
                        Defines the orientation of the image frame, i.e
                        whether it is landscape or portrait. The image will be
                        rotated accordingly, if the program can find existing
                        EXIF data.
  --img_dir IMG_DIR, -d IMG_DIR
                        Defines the path to the folder with the images to be
                        displayed by the slideshow app.
  --time_delay TIME_DELAY, -t TIME_DELAY
                        Defines the time in seconds that the program waits
                        before switching images.
  --menu MENU_START, -m MENU_START
                        If True, the application will start with the menu,
                        otherwise it goes directly to the slideshow.
```
