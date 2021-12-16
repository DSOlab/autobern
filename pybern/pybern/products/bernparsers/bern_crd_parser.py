#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import os, sys
import datetime
from pybern.products.errors.errors import FileFormatError

FILE_FORMAT = 'GPSEST .CRD (Bernese v5.2)'

"""
IGS14: coordinate list
--------------------------------------------------------------------------------
LOCAL GEODETIC DATUM: IGS14_0           EPOCH: 2010-01-01 00:00:00

NUM  STATION NAME           X (M)          Y (M)          Z (M)     FLAG
"""

def parse_bern52_crd(fn):

    stadct = {}
    with open(fn, 'r') as fin:
        title = fin.readline().strip()
        stadct['title'] = title
        line = fin.readline()
        
        assert(line.startswith('----------------'))

        line = fin.readline()
        assert(line.startswith('LOCAL GEODETIC DATUM'))
        ref_frame = line.split()[3]
        stadct['ref_frame'] = ref_frame
        assert(line.split()[4] == 'EPOCH:')
        date = datetime.datetime.strptime(' '.join(line.split()[5:]), '%Y-%m-%d %H:%M:%S')
        stadct['date'] = date

        line = fin.readline()
        line = fin.readline()
        assert(line.strip() == 'NUM  STATION NAME           X (M)          Y (M)          Z (M)     FLAG')

        line = fin.readline()
        while True:
            try:
                line = fin.readline()
            except:
                break

            if len(line)<=1:
                break

            ls = line.split()
            name = line[5:10].strip()
            domes = line[10:20].strip()
            x, y, z = [ float(i) for i in line[20:66].split() ]
            flag = line[66:].strip() if len(line)>66 else ''
            stadct[name] = {'domes': domes, 'x': x, 'y': y, 'z': z, 'flag': flag}

    return stadct
