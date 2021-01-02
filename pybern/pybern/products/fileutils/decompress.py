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


def os_decompress(filename, remove_original=False):
    """ decompress a file for any of the formats:
    ['.Z', '.gz', '.tar.gz', '.zip']
    If the instance is not compressed, no operation will be performed.
    If it is compressed:
      1) then the file will be decompressed
      2) if remove_original is set to True, then the original compressed
         file will be removed (only if the decompression process is 
         succeseful)
  """
    if not os.path.isfile(filename):
        raise RuntimeError(
            "[ERROR] decompress::os_decompress file {:} does not exist".format(
                filename))
    ctype = find_os_compression_type(filename)
    if ctype is None: return filename, filename
    noncmp_filename = name_of_decompressed(filename)
    status = 0
    ## use 7-zip on windows and uncompress on Linux
    if ctype == '.Z':
        if os.name == 'nt':  ## windows
            subprocess.call([
                "7z", "e", "-y", "-bso0", "{:}".format(filename),
                "-o{:}".format(os.path.dirname(noncmp_filename))
            ])
        else:
            try:
                subprocess.call(
                    ["uncompress", "-f", "{:}".format(filename)])
            except:
                status = 1
    elif ctype == '.gz':
        try:
            with gzip.open(filename, 'rb') as f_in:
                with open(noncmp_filename, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
        except:
            status = 2
    elif ctype == '.tar.gz':
        try:
            with tarfile.open(filename, "r:gz") as tarin:
                ## TODO need to check tarball contents
                tarin.extractall(os.path.dirname(filename))
        except:
            status = 3
    elif ctype == '.zip':
        try:
            with zipfile.ZipFile(filename, "r") as zipin:
                flist = zipin.namelist()
                ## check .zip contents; it should only have one file, namely noncmp_filename
                assert (len(flist) == 1 and
                        flist[0] == os.path.basename(noncmp_filename))
                zipin.extractall(os.path.dirname(filename))
        except:
            status = 4
    else:
        status = 5

    if status > 0 or not os.path.isfile(noncmp_filename):
        msg = "[ERROR] decompress::os_decompress failed to decompress file {:} (code: {:})".format(
            filename, status)
        raise RuntimeError(msg)
    else:
        if remove_original and ctype != '.Z':
            os.remove(filename)
    return filename, noncmp_filename
