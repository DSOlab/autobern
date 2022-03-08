#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import re
import shutil
import subprocess
import gzip, tarfile, zipfile
import tempfile
#from sys import version_info as version_info
#if version_info.major == 2:
#    from cmpvar import find_os_compression_type, name_of_decompressed
#else:
from .cmpvar import find_os_compression_type, name_of_decompressed

def crx2rnx(filename, remove_compressed=True, path2crx2rnx=None):
    """ Decompress a Hatanaka-compressed RINEX file, to an obs file. This
        function will try to use the program CRX2RNX to perform the
        decompression.
        If CRX2RNX is not in the PATH (env. variable), you will need to provide
        it's path via the path2crx2rnx variable.
        Will throw if the operation fails!
    """
    if not os.path.isfile(filename):
        ermsg = '[ERROR] decompress::crx2rnx file {:} does not exist'.format(filename)
        raise RuntimeError(ermsg)

    ## what should the result, decompressed RINEX file be?
    if not filename.endswith('d') and not filename.endswith('crx'):
        ermsg = '[ERROR] RINEX {:} does not follow the Hatanaka naming convention!'.fromat(filename)
        raise RuntimeError(ermsg)
    urnx = re.sub(r'd$', 'o', filename) if filename.endswith('d') else re.sub(r'.crx', '.rnx', filename)
    
    if path2crx2rnx is not None:
        if not os.path.isdir(path2crx2rnx):
            ermsg = '[ERROR] decompress::crx2rnx directory {:} does not exist'.format(path2crx2rnx)
            raise RuntimeError(ermsg)
        if not os.path.isfile(os.path.join(path2crx2rnx, 'CRX2RNX')):
            ermsg = '[ERROR] decompress::crx2rnx file {:} does not exist'.format(os.path.join(path2crx2rnx, 'CRX2RNX'))
            raise RuntimeError(ermsg)

    prog = 'CRX2RNX' if path2crx2rnx == None else os.path.join(path2crx2rnx, 'CRX2RNX')

    # print('>> Calling shell with {:} {:}, expecting result {:}'.format(prog, filename, urnx))
    subprocess.check_call(['{:}'.format(prog), '-f', '{:}'.format(filename)], stderr=sys.stderr)
    if not os.path.isfile(urnx):
        ermsg = '[ERROR] Failed decompressing Hatanaka RINEX file {:}'.format(filename)
        raise RuntimeError(ermsg)

    if remove_compressed: os.remove(filename)
    
    return filename, urnx


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
    if ctype is None:
        return filename, filename
    noncmp_filename = name_of_decompressed(filename)
    status = 0
    ## use 7-zip on windows and uncompress on Linux
    if ctype == '.Z':
        if os.name == 'nt':  ## windows
            subprocess.check_call([
                "7z", "e", "-y", "-bso0", "{:}".format(filename),
                "-o{:}".format(os.path.dirname(noncmp_filename))
            ])
        else:
            try:
                subprocess.check_call(["uncompress", "-f", "{:}".format(filename)], stderr=sys.stderr)
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
                ##assert (len(flist) == 1 and
                ##        flist[0] == os.path.basename(noncmp_filename))
                ## print(">>num of files: {:}, here is the list: {:}".format(len(flist), flist))
                if len(flist) == 1:
                    noncmp_filename = os.path.join(os.path.dirname(filename), flist[0])
                zipin.extractall(os.path.dirname(filename))
                ## print(">>extractall ok-> extracted to {:}!".format(noncmp_filename));
        except:
            status = 4
    else:
        status = 5

    if status > 0 or not os.path.isfile(noncmp_filename):
        msg = "[ERROR] decompress::os_decompress failed to decompress file {:} (code: {:})".format(
            filename, status)
        msg += "note: expected descompressed file {:} not found!".format(noncmp_filename)
        raise RuntimeError(msg)
    else:
        if remove_original and ctype != '.Z':
            os.remove(filename)
    return filename, noncmp_filename
