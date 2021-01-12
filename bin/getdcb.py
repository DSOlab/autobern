#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import argparse
import datetime
from pybern.products.codedcb import get_dcb, list_products
from pybern.products.formats.sp3 import Sp3
import pybern.products.fileutils.decompress as dc
import pybern.products.fileutils.compress as cc
from pybern.products.fileutils.cmpvar import is_compressed, find_os_compression_type


##  If only the formatter_class could be:
##+ argparse.RawTextHelpFormatter|ArgumentDefaultsHelpFormatter ....
##  Seems to work with multiple inheritance!
class myFormatter(argparse.ArgumentDefaultsHelpFormatter,
                  argparse.RawTextHelpFormatter):
    pass


parser = argparse.ArgumentParser(
    formatter_class=myFormatter,
    description=
    'Download Differential Code Bias (DCB) files estimated at CODE ac',
    epilog=('''National Technical University of Athens,
    Dionysos Satellite Observatory\n
    Send bug reports to:
    Xanthos Papanikolaou, xanthos@mail.ntua.gr
    Dimitris Anastasiou,danast@mail.ntua.gr
    January, 2021'''))

parser.add_argument('-y',
                    '--year',
                    metavar='YEAR',
                    dest='year',
                    type=int,
                    required=False,
                    help='The year of date.')

parser.add_argument('-d',
                    '--doy',
                    metavar='DOY',
                    dest='doy',
                    type=int,
                    required=False,
                    help='The day-of-year (doy) of date.')

parser.add_argument(
    '-o',
    '--output',
    metavar='OUTPUT',
    dest='save_as',
    required=False,
    help='Save the downloaded file using this file(name); can include path.')

parser.add_argument(
    '-O',
    '--output-dir',
    metavar='OUTPUT_DIR',
    dest='save_dir',
    required=False,
    help='Save the downloaded file under the given directory name.')

parser.add_argument(
    '-t',
    '--type',
    #default='final',
    choices=['final', 'rapid', 'current'],
    metavar='TYPE',
    dest='type',
    required=False,
    help=
    'Choose type of solution; can be any of \"final, rapid, current\". Can be ommited if CODE_TYPE unambiguously defines a DCB file.'
)

parser.add_argument('-s',
                    '--time-span',
                    metavar='TIME_SPAN',
                    dest='span',
                    required=False,
                    choices=['daily', 'monthly'],
                    default='monthly',
                    help='Choose between daily of monthly DCB files.')

parser.add_argument('-c',
                    '--code-type',
                    metavar='CODE_TYPE',
                    dest='obs',
                    required=False,
                    default='p1c1',
                    help='Choose the code type(s) that the DCB file includes')

parser.add_argument('-l',
                    '--list-products',
                    dest='list_products',
                    action='store_true',
                    help='List available DCB products and exit')

if __name__ == '__main__':

    args = parser.parse_args()

    if args.list_products:
        list_products()
        sys.exit(0)

    input_dct = {'span': args.span, 'obs': args.obs}
    if args.year is not None or args.doy is not None:
        pydt = datetime.datetime.strptime(
            '{:4d}-{:03d}'.format(args.year, args.doy), '%Y-%j')
        input_dct['pydt'] = pydt
    if args.type is not None:
        input_dct['type'] = args.type
    if args.save_as:
        input_dct['save_as'] = args.save_as
    if args.save_dir:
        input_dct['save_dir'] = args.save_dir

    status = 10
    #try:
    status, remote, local = get_dcb(**input_dct)
    #except:
    #    status = 50
    if not status:
        print('Downloaded DCB Information File: {:} as {:}'.format(
            remote, local))
        sys.exit(0)

    sys.exit(status)
