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

if len(sys.argv) != 2:
    print('[ERROR] Need to provide a .STA file')
    sys.exit(1)

stafn = sys.argv[1]
sta = bsta.BernSta(stafn)
binfo = sta.parse().filter(['dion'.upper(), 'atal'.upper()], True)

# print(binfo.station_info('dion'.upper(), True))
# print(binfo.station_info('atal'.upper(), True))

print('-----------------------------------------------------------------------')
d = binfo.station_info('dion'.upper(), True)
a = binfo.station_info('atal'.upper(), True)

print(d['type002'])
print(a['type002'])

for stainf in [d, a]:
    for t in [datetime.datetime(2021, 1, 1), datetime.datetime(1970, 1, 1)]:
        date_matched = False
        for t2 in stainf['type002']:
            domes = t2.sta_name[4:] if len(t2.sta_name)>4 else ''
            if t2.start_date <= t and t2.stop_date >= t:
                date_matched = True
        if date_matched == False:
            print('Date {:} not matched for station {:}'.format(t.strftime('%Y%m%d'), stainf['type002'][0].sta_name))
    print('domes={:}'.format(domes))
