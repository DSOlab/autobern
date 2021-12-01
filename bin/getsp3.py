#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys, os
import argparse
import datetime
from pybern.products.codesp3 import get_sp3, list_products
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
    description='Download Orbit Information (SP3) files estimated at CODE ac',
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
    '--validate-interval',
    dest='validate_interval',
    action='store_true',
    help=
    'Check that the passed in date (via \'-y\' and \'-d\') is spanned in the time interval given by the SP3 file.'
)

parser.add_argument(
    '-x',
    '--glonass-only',
    dest='glonass_only',
    action='store_true',
    help=
    'Use CODE\'s GLONASS-only solution products (note: only available for type=\'final\' and for a limited time span).'
)

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
    default='final',
    metavar='TYPE',
    dest='types',
    required=False,
    help=
    'Choose type of solution; can be any of (or multiple of) \"final, current, current-5d, urapid, ultra-rapid, frapid, final-rapid, erapid, early-rapid, prediction, p2, p5\". If more than one types are specified (using comma seperated values), the program will try all types in the order given untill a file is found and downloaded. E.g. \--type=final,urapid,p5\ means that we first try for the final solution; if found it is downloaded and the program ends. If it is not found found, then the program will try to download the ultra-rapid solution and then the p5 solution.'
)

parser.add_argument('-l',
                    '--list-products',
                    dest='list_products',
                    action='store_true',
                    help='List available ERP products and exit')
parser.add_argument('--verbose',
                    dest='verbose',
                    action='store_true',
                    help='Trigger verbose run (prints debug messages).')


def validate_interval(pydt, filename, verbose=False):
    dct = {
        'compressed': is_compressed(filename),
        'ctype': find_os_compression_type(filename)
    }
    ## if file is compressed, decompress first
    filename, decomp_filename = dc.os_decompress(filename)
    status = 0
    try:
        sp3 = Sp3(decomp_filename)
        fstart, fstop = sp3.time_span()
        dstart, dstop = pydt, pydt + datetime.timedelta(seconds=86400)
        if dstart < fstart or dstop > fstop:
            status = 10
        if verbose:
            print('\tValidation: File  start epoch: {:} stop epoch {:}'.format(
                fstart.strftime('%Y-%m-%d %H:%M:%S'),
                fstop.strftime('%Y-%m-%d %H:%M:%S')))
            print('\tValidation: Given start epoch: {:} stop epoch {:}'.format(
                dstart.strftime('%Y-%m-%d %H:%M:%S'),
                dstop.strftime('%Y-%m-%d %H:%M:%S')))
        if dct['compressed']:
            cc.os_compress(decomp_filename, dct['ctype'], True)
        return status
    except:
        return 20


if __name__ == '__main__':

    args = parser.parse_args()
    
    ## verbose print
    verboseprint = print if args.verbose else lambda *a, **k: None

    ## if we are just listing products, print them and exit.
    if args.list_products:
        list_products()
        sys.exit(0)

    ## if we have a year or a doy then both args must be there!
    if (args.year is not None and args.doy is None) or (args.doy is not None and args.year is None):
        print('[ERROR] Need to specify both Year and DayOfYear', file=sys.stderr)
        sys.exit(1)
    
    ## make a list with all posible product types.
    types = args.types.split(',')
    if args.glonass_only and not all([x == 'final' for x in types]):
        print('[ERROR] GLONASS-only files only available for final products', file=sys.stderr)
        sys.exit(10)

    ## store user options in a dictionary to pass to the download function.
    input_dct = {'acid': 'cox' if args.glonass_only else 'cod'}
    if args.year:
        input_dct['pydt'] = datetime.datetime.strptime(
            '{:4d}-{:03d}'.format(args.year, args.doy), '%Y-%j')
    if args.save_as:
        input_dct['save_as'] = args.save_as
    if args.save_dir:
        input_dct['save_dir'] = args.save_dir

    ## try downloading the ion file; if we fail do not throw, print the error
    ## message and return an intger > 0 to the shell. We will try downloading
    ## for all types provided by the user and stored in the 'types' array. When
    ## we succed, stop downloading.
    status = 10
    for t in types:
        input_dct['type'] = t
        try:
            status, remote, local = get_sp3(**input_dct)
        except Exception as e:
            verboseprint("{:}".format(str(e)), file=sys.stderr)
            status = 50
        if not status:
            ## file downloaded; if we need to, check the file's time interval.
            print('Downloaded SP3 Information File: {:} as {:}'.format(
                remote, local))
            if args.validate_interval:
                j = validate_interval(input_dct['dct'], local, args.verbose)
                if not j:
                    ## file's time interval ok, exit with OK
                    sys.exit(0)
                else:
                    ## file's time interval not ok; set the status acorrdingly, 
                    ## delete file and continue trying ....
                    print('SP3 file {:} does not include the correct interval!'.
                          format(local))
                    os.remove(local)
                    status=10
            else:
                ## file downloaded and file interval is not to be checked. exit
                ## with ok status.
                sys.exit(0)
    sys.exit(status)
