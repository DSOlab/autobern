#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import os
import re
import shutil
import subprocess
import gzip, tarfile, zipfile
import tempfile
from sys import version_info as version_info
if version_info.major == 2:
    from cmpvar import find_os_compression_type, name_of_decompressed
else:
    from .cmpvar import find_os_compression_type, name_of_decompressed


def os_compress(filename, ctype, remove_original=False):
    """ compress a file to any of the formats:
    ['.Z', '.gz', '.tar.gz', '.zip']
    If the instance is already compressed (to any format), no operation 
    will be performed. If it is uncompressed:
      1) then the file will be compressed
      3) if remove_original is set to True, then the original uncompressed
         file will be removed (only if the compression process is succeseful)
  """
    if not os.path.isfile(filename):
        raise RuntimeError(
            "[ERROR] compress::os_compress File {:} does not exist".format(
                filename))
    if ctype is None:
        return filename, filename
    if not ctype.startswith('.'):
        ctype = '.' + ctype

    compressed_file = '{:}{:}'.format(filename, ctype)
    status = 0
    if ctype == '.Z':
        try:
            subprocess.call(["compress", "-f", "{:}".format(filename)])
        except:
            status = 1
    elif ctype == '.gz':
        try:
            with open(filename,
                      'rb') as f_in, gzip.open(compressed_fileg, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        except:
            status = 2
    elif ctype == '.tar.gz':
        try:
            with tarfile.open(compressed_fileg, "w:gz") as tarout:
                tarout.add(filename, os.path.basename(filename))
        except:
            status = 3
    elif ctype == '.zip':
        try:
            with zipfile.ZipFile(compressed_fileg, "w") as zipout:
                zipout.write(filename, os.path.basename(filename))
        except:
            status = 4
    else:
        status = 5
    if status > 0 or not os.path.isfile(compressed_file):
        msg = "[ERROR] Failed to compress RINEX file {:} (code: {:})".format(
            filename, status)
        raise RuntimeError(msg)
    else:
        if remove_original and ctype != '.Z':
            os.remove(filename)
    return filename, compressed_file
