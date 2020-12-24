#!/usr/bin/env python

"""
Basic Image Slideshow for use on a raspberry Pi as a digital picture 
frame (version {}).
"""

import argparse
import os
import sys

__version__ = '1.0'

def check_dir(dirpath):
	"""
	Checks if valid directory is passed to argparser.

	Source: https://stackoverflow.com/questions/11415570/directory-path-types-with-argparse
	"""
	
	if os.path.isdir(dirpath):
		return dirpath
	else:
		raise argparse.ArgumentTypeError("{0} is not a valid path".format(dirpath))

def parse_arguments(argv):
	"""Setup argument parser for command line arguments."""
	
	parser = argparse.ArgumentParser(description=__doc__.format(__version__))

	parser.add_argument('--orientation', '-o',
						dest='frame_orientation',
						default='landscape',
						choices=('landscape', 'portrait'),
						metavar='FRAME_ORIENTATION',
						help=('Defines the orientation of the image frame, '
						'i.e whether it is landscape or portrait. The image '
						'will be rotated accordingly, if the program can '
						'find existing EXIF data.')
						)
	parser.add_argument('--img_dir', '-d',
						dest='img_dir',
						default=os.getcwd(),
						type=check_dir,
						metavar='IMG_DIR',
						help=('Defines the path to the folder with the '
						'images to be displayed by the slideshow app.')
						)
	parser.add_argument('--time_delay', '-t',
						dest='time_delay',
						default=3,
						type=int,
						metavar='TIME_DELAY',
						help=('Defines the time in seconds that the program '
						'waits before switching images.')
						)
	return vars(parser.parse_args(argv))

def cli(argv=None):
    """CLI entry point."""
    kwargs = parse_arguments(argv or sys.argv[1:])
    
    print(kwargs)

if __name__ == "__main__":
	sys.exit(cli())
