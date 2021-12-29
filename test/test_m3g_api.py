#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import re
import argparse
import datetime
import pybern.products.euref.m3g as m3g

d=m3g.get_network_view('EPN')
for k in d:
  print('{:} -> {:}'.format(k, d[k]))

l=m3g.get_m3g_network_stations('EPN', True)
for s in l: print('\tstation: {:}'.format(s))
