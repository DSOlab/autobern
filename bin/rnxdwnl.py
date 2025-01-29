#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import os
import pybern.products.rnxdwnl_impl as rnxd
    
##  If only the formatter_class could be:
##+ argparse.RawTextHelpFormatter|ArgumentDefaultsHelpFormatter ....
##  Seems to work with multiple inheritance!
class myFormatter(argparse.ArgumentDefaultsHelpFormatter,
                  argparse.RawTextHelpFormatter):
    pass


def runmain():

    parser = argparse.ArgumentParser(
        formatter_class=myFormatter,
        description='Query DSO GNSS database and download RINEX (v2 or v3) files',
        epilog=('''
        National Technical University of Athens,
        Dionysos Satellite Observatory\n
        Send bug reports to:
        Xanthos Papanikolaou, xanthos@mail.ntua.gr
        Dimitris Anastasiou,danastasiou@mail.ntua.gr
        Updates: 2024-01-29 minor changes
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
                        help='A file containing credentials for connecting to the database; it will need to hold the variables \'GNSS_DB_USER\', \'GNSS_DB_PASS\', and optionaly \'GNSS_DB_HOST\' and \'GNSS_DB_NAME\'',
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
                        '--my-sql-host',
                        action='store',
                        required=False,
                        help='Host where the database server is located',
                        metavar='MYSQL_HOST',
                        dest='mysql_host',
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
