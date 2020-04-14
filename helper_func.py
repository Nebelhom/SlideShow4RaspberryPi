#!usr/bin/env python

"""
A set of helper functions for the SlideShow4RaspberryPi project
"""


from os import listdir


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
