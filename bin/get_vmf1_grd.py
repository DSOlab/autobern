#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import argparse
import datetime
import pybern.products.vmf1 as vmf1

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
            'Download VMF1 grid files from https://vmf.geo.tuwien.ac.at/trop_products/GRID/2.5x2/VMF1/\nThe script allows downloading of both final and forecast grid files but note that for the later you will need credentials. The program will return an exit status of zero on a successeful run, else it will return a positive integer (>0).\nReference:  re3data.org: VMF Data Server; editing status 2020-12-14; re3data.org - Registry of Research Data Repositories. http://doi.org/10.17616/R3RD2H',
            epilog=('''National Technical University of Athens,
                Dionysos Satellite Observatory\n
                Send bug reports to:
                Xanthos Papanikolaou, xanthos@mail.ntua.gr
                Dimitris Anastasiou,danast@mail.ntua.gr
                March, 2021'''))

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
##  hour of day
    parser.add_argument('--hour',
            action='store',
            required=False,
            type=int,
            help='The hour of day (integer in range [0-23]). This is for downloading individual hourly files (each file covers an 6-hour time span.',
                metavar='HOUR',
                dest='hour',
                default=None)

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

##  merge individual (hourly) files
            parser.add_argument('-m',
                    '--merge',
                    action='store',
                    required=False,
                    help='Merge/concatenate individual grid files to this final grid file. This can be a filename optionaly including path (if not path is set, then the file will be created in cwd).',
                    metavar='MERGED_FILE',
                    dest='merge_to',
                    default=None)

## allow forecast products to be used
            parser.add_argument(
                    '-f',
                    '--allow-forecast',
                    dest='allow_fc',
                    action='store_true',
                    help='If needed, allow the downloading of forecast VMF1 grid file(s)')

            parser.add_argument(
                    '--del-after-merge',
                    dest='del_after_merge',
                    action='store_true',
                    help='Delete individual grid files after a successeful merge (aka only valid if \'--merge [MERGED_FILE]\' is set).')

##  merge individual (hourly) files
            parser.add_argument('-c',
                    '--config-file',
                    action='store',
                    required=False,
                    help='If you request forecast grid files, you need credentials to access the data; if you provide a CONFIG_FILE here, the program will try to parse lines: \'TUWIEN_VMF1_USER=\"username\" and TUWIEN_VMF1_PASS=\"mypassword\" \' and use the \"username\"  and \"mypassword\" credentials to access the forecast data center',
                    metavar='CONFIG_FILE',
                    dest='config_file',
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

            parser.add_argument('--verbose',
                    dest='verbose',
                    action='store_true',
                    help='Trigger verbose run (prints debug messages).')

    cmdargs = parser.parse_args()
    return vmf1.main(**vars(cmdargs))

if __name__ == '__main__':

    args = parser.parse_args()
    holdings = runmain()
