#! /usr/bin/python

#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import re
import argparse
import pybern.products.bernparsers.bernsta as bsta

class myFormatter(argparse.ArgumentDefaultsHelpFormatter,
                  argparse.RawTextHelpFormatter):
    pass


parser = argparse.ArgumentParser(
    formatter_class=myFormatter,
    description=
    'Given a Bernese v5.2 station information file (aka .STA), translate all antennas with serial numbers other than \'999999\' to this, generic value. This will cause the relevant antenna/site to be indentified with no \'individual calibration\' value and instaed the generic antenna PCV will be used.',
    epilog=('''National Technical University of Athens,
    Dionysos Satellite Observatory\n
    Send bug reports to:
    Xanthos Papanikolaou, xanthos@mail.ntua.gr
    Dimitris Anastasiou,danast@mail.ntua.gr
    January, 2021'''))

parser.add_argument('-s',
                    '--sta',
                    metavar='STAINF',
                    dest='stainf',
                    required=True,
                    help='Station Information (.STA) file to consider')

if __name__ == '__main__':
    ## parse command line arguments
    args = parser.parse_args()

    if not os.path.isfile(args.stainf):
        print('[ERROR] Failed to locate station information file {:}'.format(args.stainf), file=sys.stderr)
        sys.exit(1)

    ## parse the station information file
    stainf = bsta.BernSta(args.stainf).parse()
    ## translate all non-generic antenna serials to generic (aka 999999)
    stainf.antennas2generic()
    ## dump the new station information file
    stainf.dump_as_sta()
