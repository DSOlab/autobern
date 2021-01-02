#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import os
import re


def is_compressed(filename):
    return find_os_compression_type(filename) is not None


def find_os_compression_type(filename):
    """ Find if filename is OS compressed
      filename: the filename to check
      return: compression type (if any) else None. The compression type is 
              returned as a string and can be any of: 
              ['.Z', '.gz', '.tar.gz', '.zip']
  """
    dct = [['.Z', re.compile('.*.Z$')], ['.tar.gz',
                                         re.compile('.*.tar.gz$')],
           ['.gz', re.compile('.*.gz$')], ['.zip',
                                           re.compile('.*.zip$')]]
    for tp in dct:
        xtype, rgx = tp
        if rgx.match(filename):
            return xtype
    return None


def name_of_decompressed(filename):
    """ Given a filename check if it is in compressed type (any of 
      ['.Z', '.gz', '.tar.gz', '.zip']; if indeed it is compressed return the
      name of the uncompressed file, else return the input filename.
    """
    dct = {
        '.Z': re.compile('.Z$'),
        '.tar.gz': re.compile('.tar.gz$'),
        '.gz': re.compile('.gz$'),
        '.zip': re.compile('.zip$')
    }
    ctype = find_os_compression_type(filename)
    if ctype is None:
        return filename
    try:
        return re.sub(dct[ctype], '', filename)
    except:
        raise RuntimeError('[ERROR] decompress:name_of_decompressed Failed!')
