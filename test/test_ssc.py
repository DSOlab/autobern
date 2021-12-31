#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import re
import argparse
import datetime
import pybern.products.bernparsers.bloadvar as blvar
import pybern.products.formats.igs_log_file as ilog
import pybern.products.formats.ssc as sscpy

if len(sys.argv) != 2:
    print('[ERROR] Usage {:} [SSC FILE]'.format(sys.argv[0]))
    sys.exit(1)

ssc_recs = ssc.parse_ssc(argv[1], [], datetime.datetime.now())

