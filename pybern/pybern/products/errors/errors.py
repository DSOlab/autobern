#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
from sys import version_info as version_info


class PybernError(Exception):

    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        #if version_info.major == 2:
        #    super(PyBernError, self).__init__(message)
        #else:
        super().__init__(message)


class ArgumentError(PybernError):

    def __init__(self, message, key=None, **kwargs):
        # if key in kwargs, report invalid value, else report missing value
        details = ''
        if key is not None:
            details = ' (argument that caused exception: \"{:}\" -> '.format(
                key)
            if key in kwargs:
                details += '\"{:}\")'.format(kwargs[key])
            else:
                details += '...missing...)'
        # Call the base class constructor with the parameters it needs
        message += details
        #if version_info.major == 2:
        #    super(ArgumentError, self).__init__(message)
        #else:
        super().__init__(message)


class FileFormatError(PybernError):

    def __init__(self, fileformat, line, errmsg):
        message = errmsg
        message += '\n\tFile Format: {:}'.format(fileformat)
        message += '\n\tError line :\'{:}\''.format(line.strip())
        #if version_info.major == 2:
        #    super(ArgumentError, self).__init__(message)
        #else:
        super().__init__(message)
