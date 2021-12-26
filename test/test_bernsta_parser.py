#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import re
import argparse
import datetime
from shutil import copyfileobj
import pybern.products.bernparsers.bernsta as bsta

if len(sys.argv) != 3:
    print('[ERROR] Need to provide a .STA and an IGS_LOG_FILE file')
    sys.exit(1)

stafn = sys.argv[1]
sta = bsta.BernSta(stafn)
binfo = sta.parse()
#print('Here is the list of stations in the STA file:')
#[ print('\t{:}'.format(sta)) for sta in binfo.stations ]
#print('Here is the info on station: WTZR')
#print(binfo.station_info('WTZR', True))

# binfo.dump_as_sta(None, ['WTZR 14201M010', 'DYNG 12602M006'])
# new_binfo = binfo.filter(['WTZR 14201M010', 'DYNG 12602M006'], True)
# new_binfo.dump_as_sta()

## let's use a log file to update/insert a station
logfn = sys.argv[2]
d = binfo.update_from_log(logfn)
