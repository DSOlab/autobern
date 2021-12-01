#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import argparse
import datetime
from pybern.products.codetrp import get_trp, list_products
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
    description='Download Tropospheric information files estimated at CODE ac',
    epilog=('''National Technical University of Athens,
    Dionysos Satellite Observatory\n
    Send bug reports to:
    Xanthos Papanikolaou, xanthos@mail.ntua.gr
    Dimitris Anastasiou,danast@mail.ntua.gr
    December, 2020'''))

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
    '-e',
    '--code-euref',
    dest='code_euref',
    action='store_true',
    help=
    'Use CODE\'s EUREF solution products (note: not available for all types).')
"""
parser.add_argument(
    '--validate-interval',
    dest='validate_interval',
    action='store_true',
    help=
    'Check that the passed in date (via \'-y\' and \'-d\') is spanned in the time interval given by the ionospheric information file.'
)
"""
parser.add_argument(
    '-f',
    '--format',
    default='bernese',
    metavar='FORMAT',
    dest='format',
    choices=['bernese', 'sinex'],
    required=False,
    help='Choose between Bernese or tropospheric SINEX format files.')

parser.add_argument(
    '-o',
    '--output',
    metavar='OUTPUT',
    dest='save_as',
    required=False,
    help='Save the downloaded file using this file(name); can include path.')

parser.add_argument('-l',
                    '--list-products',
                    dest='list_products',
                    action='store_true',
                    help='List available tropospheric products and exit')

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
    default='final',
    metavar='TYPE',
    dest='types',
    required=False,
    help=
    'Choose type of solution; can be any of (or multiple of) \"final, rapid, urapid, urapid-sites\". If more than one types are specified (using comma seperated values), the program will try all types in the order given untill a file is found and downloaded. E.g. \'--type=final,rapid,urapid\' means that we first try for the final solution; if found it is downloaded and the program ends. If it is not found found, then the program will try to download the rapid solution and then the urapid solution.'
)
parser.add_argument('--verbose',
                    dest='verbose',
                    action='store_true',
                    help='Trigger verbose run (prints debug messages).')

if __name__ == '__main__':

    args = parser.parse_args()

    ## if we are just listing products, print them and exit.
    if args.list_products:
        list_products()
        sys.exit(0)
    
    ## verbose print
    verboseprint = print if args.verbose else lambda *a, **k: None

    ## if we have a year or a doy then both args must be there!
    if (args.year is not None and args.doy is None) or (args.doy is not None and args.year is None):
        print('[ERROR] Need to specify both Year and DayOfYear')
        sys.exit(1)
    
    ## make a list with all posible product types.
    types = args.types.split(',')

    ## store user options in a dictionary to pass to the download function.
    input_dct = {'format': args.format}
    if args.year:
        input_dct['pydt'] = datetime.datetime.strptime(
            '{:4d}-{:03d}'.format(args.year, args.doy), '%Y-%j')
    if args.code_euref:
        input_dct['acid'] = 'coe'
    if args.save_as:
        input_dct['save_as'] = args.save_as
    if args.save_dir:
        input_dct['save_dir'] = args.save_dir

    ## try downloading the trp file; if we fail do not throw, print the error
    ## message and return an intger > 0 to the shell.
    status = 10
    for t in types:
        input_dct['type'] = t
        try:
            status, remote, local = get_trp(**input_dct)
        except Exception as e:
            verboseprint("{:}".format(str(e)), file=sys.stderr)
            status = 50
        if not status:
            print('Downloaded Tropospheric Information File: {:} as {:}'.format(
                remote, local))
            sys.exit(0)

    sys.exit(status)
