#!usr/bin/env python

"""
A set of helper functions for the SlideShow4RaspberryPi project
"""


from os import listdir

from PIL import Image
from PIL.ExifTags import TAGS


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


def aspect_scale(img_dim, resolution):
    """
    Scales 'img_dim' tuple to fit into resolution tuple. This method will
    retain the original image's aspect ratio.
    Reference: http://www.pygame.org/pcr/transform_scale/

    img_dim: tuple of integers: dimensions of an image
    resolution: tuple of integers: The resolution of the display

    Returns:
    tuple of integers: Rescaled dimensions to fit the resolution according
    to its aspect ratio.
    """

    bx, by = resolution
    ix, iy = img_dim
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

    return (sx, sy)


def center_img(img_dim, resolution):
    """
    Returns coordinates that centers img on surface
    """
    iw, ih = img_dim
    rw, rh = resolution

    w = int((rw - iw) / 2)
    h = int((rh - ih) / 2)

    return (w, h)


def print_img_exif(fname):
    """
    Prints a dict of Exif values from an image.
    Used to visualise the values

    References:
    https://hhsprings.bitbucket.io/docs/programming/examples/python/PIL/ExifTags.html
    https://www.daveperrett.com/articles/2012/07/28/exif-orientation-handling-is-a-ghetto/
    """

    with Image.open(fname) as img:
        exif = {
            TAGS[k]: v
            for k, v in img._getexif().items()
            if k in TAGS
        }
        try:
            del exif["UserComment"]
        except KeyError:
            pass

        try:
            del exif["MakerNote"]
        except KeyError:
            pass

        print("File: ", fname, "\n\n")
        for key, val in exif.items():
            print(key, ": ", val)

def get_img_orientation(fname):
    """
    Returns image orientation using Pillow
    """
    with Image.open(fname) as img:
        exif = {
            TAGS[k]: v
            for k, v in img._getexif().items()
            if k in TAGS
        }
    return exif["Orientation"]

def get_img_size(fname):
    """
    Returns image size using Pillow
    """

    with Image.open(fname) as img:
        width, height = img.size
    return width, height

if __name__ == "__main__":
    #get_img_orientation("20190330_134242.jpg")
    #print("\n\n#############################\n\n")
    #get_img_orientation("20200511_184914.jpg")
    #print("Landscape: ", get_img_orientation("20190330_134242.jpg"))
    #print("Portrait: ", get_img_orientation("20200511_184914.jpg"))
    print("Image size ", get_img_size("20200511_184914.jpg"))
