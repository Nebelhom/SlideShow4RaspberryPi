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
    """Lists all image filenames in the path directory.

    :param cpath: Directory path to images
    :type cpath: str

    :return: List of strings of image filenames
    :rtype: list
    """

    return [i for i in listdir(cpath) if i.split('.')[-1].lower() in FORMATS]


def aspect_scale(img_dim, resolution):
    """Takes the image dimensions and scales it to the given resolution.

    This method will retain the original image's aspect ratio.
    Reference: http://www.pygame.org/pcr/transform_scale/

    :param img_dim: Dimensions of an image
    :type img_dim: (int, int)
    :param resolution: The resolution of the display
    :type resolution: (int, int)

    :return: Rescaled dimensions to fit the resolution according to its aspect ratio.
    :rtype: (int, int)
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
    """Returns the coordinates that centers the image on the surface.

    :param img_dim: Dimensions of an image
    :type img_dim: (int, int)
    :param resolution: The resolution of the display
    :type resolution: (int, int)

    :return: The coordinates that centers the image on the surface.
    :rtype: (int, int)
    """
    
    iw, ih = img_dim
    rw, rh = resolution

    w = int((rw - iw) / 2)
    h = int((rh - ih) / 2)

    return (w, h)


def print_img_exif(fname):
    """Prints a dict of Exif values from an image using Pillow library

    Auxiliary function used to visualise the values for troubleshooting
    purposes.

    References:
    https://hhsprings.bitbucket.io/docs/programming/examples/python/PIL/ExifTags.html
    https://www.daveperrett.com/articles/2012/07/28/exif-orientation-handling-is-a-ghetto/

    :param fname: The path and filename to an image file
    :type fname: str
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
    """Returns the image orientation from the exif data using Pillow

    :param fname: The path and filename to an image file
    :type fname: str

    :return: Returns int value associated with orientation in exif data
    :rtype: int
    """

    try:
        with Image.open(fname) as img:
            exif = {
                TAGS[k]: v
                for k, v in img._getexif().items()
                if k in TAGS
            }
        return exif["Orientation"]
    except AttributeError:
        print("No exif tags found. Using standard landscape orientation...")
        return 6

def get_img_size(fname):
    """Returns image size of an image using the Pillow library

    :param fname: The path and filename to an image file
    :type fname: str

    :return: width and height associated with the size dimensions of an image
    :rtype: (int, int)
    """

    with Image.open(fname) as img:
        width, height = img.size
    return width, height

if __name__ == "__main__":
    #get_img_orientation("20190330_134242.jpg")
    #print("\n\n#############################\n\n")
    #get_img_orientation("20200511_184914.jpg")
    #print("Landscape: ", get_img_orientation("20190330_134242.jpg"))
    print("Portrait: ", type(get_img_orientation("20200511_184914.jpg")))
    #print("Image size ", get_img_size("20200511_184914.jpg"))
