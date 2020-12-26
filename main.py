#!/usr/bin/env python

"""
Basic Image Slideshow for use on a raspberry Pi as a digital picture 
frame (version {}).
"""

import argparse
import configparser as cp
import os
import sys

from app import *

__version__ = '1.0'

CONFIGFILE = 'settings.conf'

def check_dir(dirpath):
	"""
	Checks if valid directory is passed to argparser.

	Source: https://stackoverflow.com/questions/11415570/directory-path-types-with-argparse
	"""
	
	if os.path.isdir(dirpath):
		return dirpath
	else:
		raise argparse.ArgumentTypeError("{0} is not a valid path".format(dirpath))

def save_settings_externally(configs, configfile=CONFIGFILE):
	
	config = cp.ConfigParser()
	config.read(configfile)

	config['SLIDESHOW']['frame_orientation'] = configs['frame_orientation']
	config['SLIDESHOW']['img_dir'] = configs['img_dir']
	config['SLIDESHOW']['time_delay'] = str(configs['time_delay'])
	
	global FRAME_ORIENTATION
	FRAME_ORIENTATION = configs['frame_orientation']
	global IMG_DIR
	IMG_DIR = configs['img_dir']
	global TIME_DELAY
	TIME_DELAY = configs['time_delay']
	
	# Save all values to file
	with open(configfile, 'w') as conf:
		config.write(conf)


def parse_arguments(argv):
	"""Setup argument parser for command line arguments."""
	
	config = cp.ConfigParser()
	config.read(CONFIGFILE)
	
	parser = argparse.ArgumentParser(description=__doc__.format(__version__))

	# Settings arguments
	parser.add_argument('--orientation', '-o',
						dest='frame_orientation',
						default=CONFIG['SLIDESHOW']['frame_orientation'],
						choices=('landscape', 'portrait'),
						metavar='FRAME_ORIENTATION',
						help=('Defines the orientation of the image frame, '
						'i.e whether it is landscape or portrait. The image '
						'will be rotated accordingly, if the program can '
						'find existing EXIF data.')
						)
	parser.add_argument('--img_dir', '-d',
						dest='img_dir',
						default=CONFIG['SLIDESHOW']['img_dir'],
						type=check_dir,
						metavar='IMG_DIR',
						help=('Defines the path to the folder with the '
						'images to be displayed by the slideshow app.')
						)
	parser.add_argument('--time_delay', '-t',
						dest='time_delay',
						default=CONFIG['SLIDESHOW']['time_delay'],
						type=int,
						metavar='TIME_DELAY',
						help=('Defines the time in seconds that the program '
						'waits before switching images.')
						)

	# Handling arguments
	parser.add_argument('--menu', '-m',
						dest='menu_start',
						default=False,
						type=bool,
						metavar='MENU_START',
						help=('If True, the application will start with the '
						'menu, otherwise it goes directly to the slideshow.')
						)

	return vars(parser.parse_args(argv))

def cli(argv=None):
    """CLI entry point."""
    kwargs = parse_arguments(argv or sys.argv[1:])
    save_settings_externally(kwargs)
    
    slideshow = SlideShowApp(kwargs['menu_start'])
    slideshow.run()
    slideshow.root.menu.update_vars()

if __name__ == "__main__":
	
	sys.exit(cli())
