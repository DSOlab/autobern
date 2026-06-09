#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pybern')))

import pybern.products.rnxdwnl_implpg as rnxd  # pyright: ignore[reportMissingImports]
    
##  If only the formatter_class could be:
##+ argparse.RawTextHelpFormatter|ArgumentDefaultsHelpFormatter ....
##  Seems to work with multiple inheritance!
class myFormatter(argparse.ArgumentDefaultsHelpFormatter,
                  argparse.RawTextHelpFormatter):
    pass


def runmain():

    parser = argparse.ArgumentParser(
        formatter_class=myFormatter,
        description='Query the PostgreSQL GNSS database and download RINEX (v2.x 3.x 4.x) files',
        epilog=('''
        National Technical University of Athens,
        Dionysos Satellite Observatory\n
        Send bug reports to:
        Xanthos Papanikolaou, xanthos@mail.ntua.gr
        Dimitris Anastasiou, danastasiou@mail.ntua.gr
        Updates: 2024-01-29 minor changes
                 2026-06-09 [DA] turn to postgresql use of database
        First version:
                 October, 2021
        '''))

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
        help='The directory where the downloaded files shall be placed.',
        metavar='OUTPUT_DIR',
        dest='output_dir',
        default=os.getcwd())

    parser.add_argument('-c',
                        '--credentials-file',
                        action='store',
                        required=False,
                        help='A file containing credentials for connecting to the PostgreSQL database; it will need to hold the variables \'GNSS_DB_USER\', \'GNSS_DB_PASS\', and optionally \'GNSS_DB_HOST\' and \'GNSS_DB_NAME\'',
                        metavar='CREDENTIALS_FILE',
                        dest='credentials_file',
                        default=None)

    parser.add_argument('-u',
                        '--username',
                        action='store',
                        required=False,
                        help='Username used to connect to the database',
                        metavar='USERNAME',
                        dest='username',
                        default=None)

    parser.add_argument('-p',
                        '--password',
                        action='store',
                        required=False,
                        help='Password used to connect to the database',
                        metavar='PASSWORD',
                        dest='password',
                        default=None)

    parser.add_argument('-i',
                        '--db-host',
                        action='store',
                        required=False,
                        help='Host where the PostgreSQL database server is located',
                        metavar='DB_HOST',
                        dest='db_host',
                        default=None)

    parser.add_argument('-m',
                        '--database-name',
                        action='store',
                        required=False,
                        help='Name of the database',
                        metavar='DB_NAME',
                        dest='db_name',
                        default=None)

    parser.add_argument('-s',
                        '--station-list',
                        action='store',
                        required=False,
                        help='List of stations to query/download; provide as 4-char id',
                        metavar='STATION_LIST',
                        dest='station_list',
                        nargs='+',
                        default=[])

    parser.add_argument('-n',
                        '--network',
                        action='store',
                        required=False,
                        help='Network to query/download',
                        metavar='NETWORK',
                        dest='network',
                        default=None)

    parser.add_argument('--skip-download',
                        dest='skip_download',
                        action='store_true',
                        help='Do not download files, only show the query result')

    parser.add_argument('--verbose',
                        dest='verbose',
                        action='store_true',
                        help='Trigger verbose run (prints debug messages).')

    cmdargs = parser.parse_args()
    return rnxd.main(**vars(cmdargs))

if __name__ == '__main__':
    holdings = runmain()
