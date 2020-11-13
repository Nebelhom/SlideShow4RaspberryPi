#!/usr/bin/env python

import os
import configparser


class Config(object):
    """Description

    Reference:
    https://www.hackerearth.com/practice/notes/samarthbhargav/a-design-pattern-for-configuration-management-in-python/
    """

    def __init__(self, configfile='settings.conf'):

        # Configurations
        self._config = configparser.ConfigParser()
        self._config.read(configfile)

    @property
    def img_dir(self):
        if os.path.isdir(self._config['SLIDESHOW']['img_dir']):
            return self._config['SLIDESHOW']['img_dir']
        else:
            print("Current path is not valid. ",
                  "Using current working directory.")
            return os.getcwd()

    @img_dir.setter
    def img_dir(self, value):
        if isinstance(value, str):
            self.img_dir = value
        else:
            raise TypeError()

    @property
    def frame_orientation(self):
        return self._config['SLIDESHOW']['frame_orientation']

    @frame_orientation.setter
    def frame_orientation(self, value):
        if isinstance(value, str):
            if value in ('portrait', 'landscape'):
                self.frame_orientation = value
            else:
                print('The given string is neither the value "landscape" nor',
                      '"portrait". Please choose one or the other.')
                return
        else:
            raise TypeError()

    @property
    def time_delay(self):
        return int(self._config['SLIDESHOW']['time_delay'])

    @time_delay.setter
    def time_delay(self, value):
        if isinstance(value, int):
            self.img_dir = value
        else:
            raise TypeError()

    def __str__(self):
        output = ''
        for section in self._config.sections():
            output = output + '[' + section + ']\n'
            for (key, val) in self._config.items(section):
                output = output + key + ' = ' + val + '\n'
        return output

    def save_config(self, fname='settings.conf'):
        """Description
        """
        with open(fname, 'w') as configfile:
            self._config.write(configfile)


if __name__ == '__main__':
    config = Config()
    print(config.frame_orientation)
