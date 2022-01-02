#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import re
import argparse
import datetime
import pybern.products.formats.ssc as ssc

#if len(sys.argv) != 2:
#    print('[ERROR] Usage {:} [SSC FILE]'.format(sys.argv[0]))
#    sys.exit(1)
#
#print('{:}'.format('-'*80))
#ssc_recs = ssc.parse_ssc(sys.argv[1], ['dyng', 'zimm', 'ankr', 'aut1'], datetime.datetime.now())
#for site in ssc_recs:
#    x, y, z = site.extrapolate(datetime.datetime.now())
#    print('{:} {:} {:12.3f} {:12.3f} {:12.3f}'.format(site.id, site.domes, x, y, z))
#
#print('{:}'.format('-'*80))
#ssc_recs = ssc.parse_ssc(sys.argv[1], ['dyng', 'zimm', 'ankr', 'aut1'], datetime.datetime.strptime('1983-01-13', '%Y-%m-%d'))
#for site in ssc_recs:
#    x, y, z = site.extrapolate(datetime.datetime.now())
#    print('{:} {:} {:12.3f} {:12.3f} {:12.3f}'.format(site.id, site.domes, x, y, z))
#
#print('{:}'.format('-'*80))
#ssc_recs = ssc.parse_ssc(sys.argv[1], ['dyng', 'zimm', 'ankr', 'aut1'], datetime.datetime.strptime('2015-263', '%Y-%j'))
#for site in ssc_recs:
#    x, y, z = site.extrapolate(datetime.datetime.now())
#    print('{:} {:} {:12.3f} {:12.3f} {:12.3f}'.format(site.id, site.domes, x, y, z))
#
#print('{:}'.format('-'*80))
#ssc_recs = ssc.parse_ssc(sys.argv[1], ['dyng', 'zimm', 'ankr', 'aut1'], datetime.datetime.strptime('2015-262', '%Y-%j'))
#for site in ssc_recs:
#    x, y, z = site.extrapolate(datetime.datetime.now())
#    print('{:} {:} {:12.3f} {:12.3f} {:12.3f}'.format(site.id, site.domes, x, y, z))
#
#print('{:}'.format('-'*80))
#ssc_recs = ssc.parse_ssc(sys.argv[1], ['dyng', 'zimm', 'ankr', 'aut1'], datetime.datetime.strptime('2015-270', '%Y-%j'))
#for site in ssc_recs:
#    x, y, z = site.extrapolate(datetime.datetime.now())
#    print('{:} {:} {:12.3f} {:12.3f} {:12.3f}'.format(site.id, site.domes, x, y, z))

fn = ['EPN_A_IGb14_C2145.SSC', 'EPND_D2150_IGS14.SSC']
dir = '/home/bpe/tables/ssc'
fns = [os.path.join(dir, f) for f in fn]
ssc.ssc2crd(['dyng', 'kasi', 'aut1', 'noa1', 'mtna', 'akyr'], datetime.datetime.now(), *fns)
