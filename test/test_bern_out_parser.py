#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import re
import argparse
import datetime
import json
from shutil import copyfileobj
import pybern.products.bernparsers.bern_out_parse as bparse
import pybern.products.bernparsers.bern_gpsest_parser as bgpsest
import pybern.products.bernparsers.bern_addneq_parser as baddneq
import pybern.products.bernparsers.bern_baslst_parser as bbaslst
import pybern.products.bernparsers.bern_helmr1_parser as bhelmr1

if len(sys.argv) != 2:
    print('[ERROR] Need to provide a .OUT file')
    sys.exit(1)

bout = sys.argv[1]
with open(bout, 'r') as f:
    dct = bparse.parse_generic_out_header(f)
    if dct['program'] == 'GPSEST':
        #try:
        full_dct = bgpsest.parse_gpsest_out(f)
        #print(json.dumps(full_dct, indent=4, default=str))
        #except Exception as e:
        #  print('OOPS! exception thrown!')
        #  print(e)
    elif dct['program'] == 'ADDNEQ2':
        #try:
        full_dct = baddneq.parse_addneq_out(f)
        print(json.dumps(full_dct, indent=4, default=str))
    elif dct['program'] == 'BASLST':
        #try:
        full_dct = bbaslst.parse_baslst_out(f)
        print(json.dumps(full_dct, indent=4, default=str))
    elif dct['program'] == 'HELMR1':
        #try:
        full_dct = bhelmr1.parse_helmr1_out(f)
        print(json.dumps(full_dct, indent=4, default=str))

print(dct)
