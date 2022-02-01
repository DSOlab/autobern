#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import re
import datetime
import pybern.products.bernparsers.bern_out_parse as bparse
import pybern.products.bernparsers.bern_gpsest_parser as bgpsest
import pybern.products.bernparsers.bern_addneq_parser as baddneq
import json

bout = sys.argv[1]
with open(bout, 'r') as f:
    dct = bparse.parse_generic_out_header(f)
    assert(dct['program'] == 'ADDNEQ2')
    full_dct = baddneq.parse_addneq_out(f)
    #full_dct = full_dct['stations']
    full_dct['stations']={}
    print(json.dumps(full_dct, indent=4, default=str))

#for aa,dct in full_dct.items():
#    tfrom = dct['X_from']
#    tto = dct['X_to']
#    dt_seconds = int((tto-tfrom).seconds)/2
#    t = datetime.timedelta(days=0, seconds=dt_seconds) + tfrom
#    print('{:} {:+15.5f} {:9.5f} {:+15.5f} {:9.5f} {:+15.5f} {:9.5f} {:+13.8f} {:9.5f} {:+13.8f} {:9.5f} {:12.5f} {:9.5f} {:}'.format(t.strftime("%Y-%m-%d %H:%M:%S"), dct['X_estimated_value'], dct['X_rms_error'], dct['Y_estimated_value'], dct['Y_rms_error'], dct['Z_estimated_value'], dct['Z_rms_error'], dct['Latitude_estimated_value'], dct['Latitude_rms_error'], dct['Longitude_estimated_value'], dct['Longitude_rms_error'], dct['Height_estimated_value'], dct['Height_rms_error'],datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

#print('{:3s} {:15s} {:8s} {:8s} {:8s} {:8s} {:8s} {:8s} {:9s} {:9s} {:9s} {:7s}'.format('A/A', 'Station', 'Xcorr', 'Xrms', 'Ycorr', 'Yrms', 'Zcorr', 'Zrms', 'LonCorr', 'LatCorr', 'HgtCorr', 'EFH'))
#for station_num in full_dct['stations']:
#    sta_dct = full_dct['stations'][station_num]
#    print('{:3d} {:15s} {:+8.4f} {:8.4f} {:+8.4f} {:8.4f} {:+8.4f} {:8.4f} {:+9.5f} {:+9.5f} {:+9.5f} {:7s}'.format(int(station_num), sta_dct['station_name'], sta_dct['X_correction'], sta_dct['X_rms_error'], sta_dct['Y_correction'], sta_dct['Y_rms_error'], sta_dct['Z_correction'], sta_dct['Z_rms_error'], sta_dct['Longitude_rms_error'], sta_dct['Latitude_rms_error'], sta_dct['Height_rms_error'], sta_dct['e/f/h']))
