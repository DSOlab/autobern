#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import re
import argparse
import datetime
import pybern.products.bernbpe as bpe

stop = datetime.datetime.now(tz=datetime.timezone.utc)
start = stop - datetime.timedelta(days=5)
campaign_dir = '/home/bpe/data/GPSDATA/CAMPAIGN52/GREECE'


wlist = bpe.collect_warning_messages(campaign_dir, '005', start, stop)
print(wlist)
