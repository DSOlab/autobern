#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import os, sys
import datetime
import re
import requests
from pybern.products.downloaders.retrieve import web_retrieve
from pybern.products.gnssdates.gnssdates import pydt2gps

def get_euref_exclusion_list(dt):
    URL = 'ftp://epncb.oma.be/pub/station/general/excluded/exclude.'
    week, dow = pydt2gps(dt)
    target = '{:}{:}'.format(URL, week)
    try:
        status, target, saveas = web_retrieve(target)
    except:
        print('[DEBUG] Failed to download EUREF\'s exclusion list file', file=sys.stderr)
        return []

    exclusion_list = []
    with open(saveas, 'r') as fin:
        for line in fin.readlines():
            exclusion_list.append(line.split()[0])
    
    os.remove(saveas)

    return exclusion_list



def get_m3g_log(station, filename=None, out_dir=None):
    """ Download m3g log file for  given station. Note that 'station'
        must be the (upper case) 9-char station id
    """
    usta = station.upper()
    target = 'https://gnss-metadata.eu/sitelog/exportlog?station=' + usta
    
    if filename is None:
        filename = station.lower() + '.log'
    filename_scr = filename + '.scr'

    if out_dir is None:
        out_dir = os.getcwd()

    status, target, saveas = web_retrieve(target, save_as=filename_scr, save_dir=out_dir)

    ## if the log is not found, the request will download a file but has htlm
    ## shit. Check that what we doenloaded is indeed a lo gile
    if status == 0:
        with open(saveas, 'r') as fin:
            line = fin.readline()
            if not line.lstrip().startswith(station[0:4]):
                status = 1

    if status != 0:
        try:
            os.remove(saveas)
        except:
            pass
        errmsg = '[ERROR] Failed to download remote log: {:}'.format(target)
        raise RuntimeError(errmsg)

    os.rename(saveas, filename)
    return status, target, filename
