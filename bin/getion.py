#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import argparse
import datetime
from pybern.products.codeion import get_ion
from pybern.products.formats.ion import BernIon
from pybern.products.formats.ionex import Ionex
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
    description='Download Ionospheric information files estimated at CODE ac',
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
                    required=True,
                    help='The year of date.')

parser.add_argument('-d',
                    '--doy',
                    metavar='DOY',
                    dest='doy',
                    type=int,
                    required=True,
                    help='The day-of-year (doy) of date.')

parser.add_argument(
    '-e',
    '--code-euref',
    dest='code_euref',
    action='store_true',
    help=
    'Use CODE\'s EUREF solution products (note: not available for all types).')

parser.add_argument(
    '--validate-interval',
    dest='validate_interval',
    action='store_true',
    help=
    'Check that the passed in date (via \'-y\' and \'-d\') is spanned in the time interval given by the ionospheric information file.'
)

parser.add_argument('-f',
                    '--format',
                    default='bernese',
                    metavar='FORMAT',
                    dest='format',
                    choices=['bernese', 'ionex'],
                    required=False,
                    help='Choose between Bernese or IONEX format files.')

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
    'Choose type of solution; can be any of (or multiple of) \"rapid, prediction, current, p2, p5\". If more than one types are specified (using comma seperated values), the program will try all types in the order given untill a file is found and downloaded. E.g. \'--type=final,rapid,p5\' means that we first try for the final solution; if found it is downloaded and the program ends. If it is not found found, then the program will try to download the rapid solution and then the p5 solution.'
)


def validate_interval(pydt, filename, informat):
    dct = {
        'compressed': is_compressed(filename),
        'ctype': find_os_compression_type(filename)
    }
    ## if file is compressed, decompress first
    filename, decomp_filename = dc.os_decompress(filename)
    status = 0
    #try:
    ion = BernIon(decomp_filename) if informat == 'bernese' else Ionex(
        decomp_filename)
    fstart, fstop = ion.time_span()
    dstart, dstop = pydt, pydt + datetime.timedelta(seconds=86400)
    if dstart < fstart or dstop > fstop:
        status = 10
    print('Validation: File  start epoch: {:} stop epoch {:}'.format(
        fstart.strftime('%Y-%m-%d %H:%M:%S'),
        fstop.strftime('%Y-%m-%d %H:%M:%S')))
    print('Validation: Given start epoch: {:} stop epoch {:}'.format(
        dstart.strftime('%Y-%m-%d %H:%M:%S'),
        dstop.strftime('%Y-%m-%d %H:%M:%S')))
    if dct['compressed']:
        cc.os_compress(decomp_filename, dct['ctype'], True)
    return status
    #except:
    #  sys.exit(5)


if __name__ == '__main__':

    args = parser.parse_args()

    pydt = datetime.datetime.strptime(
        '{:4d}-{:03d}'.format(args.year, args.doy), '%Y-%j')

    types = args.types.split(',')

    input_dct = {'format': args.format}
    if args.code_euref:
        input_dct['acid'] = 'coe'
    if args.save_as:
        input_dct['save_as'] = args.save_as
    if args.save_dir:
        input_dct['save_dir'] = args.save_dir

    status = 10
    for t in types:
        input_dct['type'] = t
        try:
            status, remote, local = get_ion(pydt, **input_dct)
        except:
            pass
        if not status:
            print('Downloaded Ionospheric Information File: {:} as {:}'.format(
                remote, local))
            if args.validate_interval:
                j = validate_interval(pydt, local, input_dct['format'])
                if not j:
                    sys.exit(0)
                else:
                    print(
                        'Ionospheric file {:} does not include the correct interval!'
                    )
            else:
                sys.exit(0)

    sys.exit(status)
