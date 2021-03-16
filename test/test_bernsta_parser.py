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

sta = bsta.BernSta("/home/xanthos/Builds/autobern/data/CODE.STA")
sta.parse()
