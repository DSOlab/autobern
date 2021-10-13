#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import os
import datetime
import sys

##  If only the formatter_class could be:
##+ argparse.RawTextHelpFormatter|ArgumentDefaultsHelpFormatter ....
##  Seems to work with multiple inheritance!
class myFormatter(argparse.ArgumentDefaultsHelpFormatter,
                  argparse.RawTextHelpFormatter):
    pass


parser = argparse.ArgumentParser(
    formatter_class=myFormatter,
    description='Query DSO GNSS database and download RINEX (v2 or v3) files',
    epilog=('''National Technical University of Athens,
    Dionysos Satellite Observatory\n
    Send bug reports to:
    Xanthos Papanikolaou, xanthos@mail.ntua.gr
    Dimitris Anastasiou,danast@mail.ntua.gr
    October, 2021'''))

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

##  download path
parser.add_argument(
    '-O',
    '--outpur-dir',
    action='store',
    required=False,
    help='The directory where the downloaded files shall be placed. Note that this does not affect the merged file (if \'--merge [MERGED_FILE]\' is used).',
    metavar='OUTPUT_DIR',
    dest='output_dir',
    default=os.getcwd())

parser.add_argument('-c',
                    '--credentials-file',
                    action='store',
                    required=False,
                    help='If you request forecast grid files, you need credentials to access the data; if you provide a CONFIG_FILE here, the program will try to parse lines: \'TUWIEN_VMF1_USER=\"username\" and TUWIEN_VMF1_PASS=\"mypassword\" \' and use the \"username\"  and \"mypassword\" credentials to access the forecast data center',
                    metavar='CREDENTIALS_FILE',
                    dest='credentials_file',
                    default=None)

parser.add_argument('-u',
                    '--username',
                    action='store',
                    required=False,
                    help='If you request forecast grid files, you need credentials to access the data; use this username to access the forecast data center. Note: this will overwite any \"username\" value found in the CONFIG_FILE (if you also specify one).',
                    metavar='USERNAME',
                    dest='username',
                    default=None)

parser.add_argument('-p',
                    '--password',
                    action='store',
                    required=False,
                    help='If you request forecast grid files, you need credentials to access the data; use this password to access the forecast data center. Note: this will overwite any \"password\" value found in the CONFIG_FILE (if you also specify one). Note that if you have special characters in the password string (e.g. \"!\") it\'d be better to enclose the password string in singe quotes (e.g. -p \'my!pass\').',
                    metavar='PASSWORD',
                    dest='password',
                    default=None)

parser.add_argument('-m',
                    '--my-sql-host',
                    action='store',
                    required=True,
                    help='If you request forecast grid files, you need credentials to access the data; use this password to access the forecast data center. Note: this will overwite any \"password\" value found in the CONFIG_FILE (if you also specify one). Note that if you have special characters in the password string (e.g. \"!\") it\'d be better to enclose the password string in singe quotes (e.g. -p \'my!pass\').',
                    metavar='MYSQL_HOST',
                    dest='mysql_host',
                    default=None)

parser.add_argument('--verbose',
                    dest='verbose',
                    action='store_true',
                    help='Trigger verbose run (prints debug messages).')

if __name__ == '__main__':

    args = parser.parse_args()

    ## verbose print
    verboseprint = print if args.verbose else lambda *a, **k: None
    
    ## Resolve the date from input args.
    dt = datetime.datetime.strptime('{:} {:03d}'.format(args.year, args.doy),
                                    '%Y %j')

    ## Where are we going to store local files?
    save_dir = args.output_dir if args.output_dir is not None else os.getcwd()
    if not os.path.isdir(save_dir):
        print('[ERROR] Failed to find requested directory \'{:}\''.format(save_dir), file=sys.stderr)
        sys.exit(5)
