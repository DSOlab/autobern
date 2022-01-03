#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import argparse
import datetime
import pybern.products.bernparsers.bernpcf as bpcf
import pybern.products.bernbpe as bpe
import pybern.products.atx2pcv as a2p

##  If only the formatter_class could be:
##+ argparse.RawTextHelpFormatter|ArgumentDefaultsHelpFormatter ....
##  Seems to work with multiple inheritance!
class myFormatter(argparse.ArgumentDefaultsHelpFormatter,
                  argparse.RawTextHelpFormatter):
    pass

def runmain():
    parser = argparse.ArgumentParser(
        formatter_class=myFormatter,
        description=
        'Transform an ATX file to (bernese-specific) PCV file',
        epilog=('''National Technical University of Athens,
        Dionysos Satellite Observatory\n
        Send bug reports to:
        Xanthos Papanikolaou, xanthos@mail.ntua.gr
        Dimitris Anastasiou,danast@mail.ntua.gr
        January, 2021'''))

    parser.add_argument('--verbose',
                        dest='verbose',
                        action='store_true',
                        help='Trigger verbose run (prints debug messages).')
    parser.add_argument('-g',
                        '--campaign',
                        required=False,
                        help='',
                        metavar='CAMPAIGN',
                        dest='campaign',
                        default=None)
    parser.add_argument('-a',
                        '--atx',
                        required=True,
                        help='The input ATX file',
                        metavar='ATXINF',
                        dest='atxinf',
                        default=None)
    parser.add_argument('-s',
                        '--sta',
                        required=True,
                        help='The input STA file',
                        metavar='STAINF',
                        dest='stainf',
                        default=None)
    parser.add_argument('-b',
                        '--loadgps-file',
                        required=True,
                        help='',
                        metavar='LOADGPS_FILE',
                        dest='b_loadgps',
                        default=None)
    parser.add_argument('-e',
                        '--pcv-ext',
                        required=False,
                        help='',
                        metavar='PCVEXT',
                        dest='pcvext',
                        default='I14')
    parser.add_argument('-r',
                        '--recinf',
                        required=False,
                        help='',
                        metavar='RECEIVER_FILE',
                        dest='recinf',
                        default='RECEIVER.')
    parser.add_argument('-o',
                        '--pcvout',
                        required=False,
                        help='',
                        metavar='OUTPUT_PCV_FILE',
                        dest='pcvout',
                        default=None)

    cmdargs = parser.parse_args()
    return a2p.atx2pcv(**vars(cmdargs))

if __name__ == '__main__':
    result = runmain()
    if result is not None:
        print('Created PCV file: {:}'.format(result))
    sys.exit(0)
