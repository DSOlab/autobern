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
sta.parse()
