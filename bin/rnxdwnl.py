#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import os
import datetime
import sys
from pybern.products.fileutils.keyholders import extract_key_values
from mysql.connector import connect, Error

def return_network_query(network, pdate):
    return """SELECT station.station_id, 
        station.mark_name_DSO, 
        stacode.mark_name_OFF, 
        stacode.station_name, 
        ftprnx.dc_name, 
        ftprnx.protocol, 
        ftprnx.url_domain, 
        ftprnx.pth2rnx30s, 
        ftprnx.pth2rnx01s, 
        ftprnx.ftp_usname, 
        ftprnx.ftp_passwd, 
        network.network_name, 
        dataperiod.rnx_v 
        FROM station 
        JOIN stacode ON station.stacode_id=stacode.stacode_id 
        JOIN dataperiod ON station.station_id=dataperiod.station_id 
        JOIN ftprnx ON dataperiod.ftprnx_id=ftprnx.ftprnx_id 
        JOIN sta2nets ON sta2nets.station_id=station.station_id 
        JOIN network ON network.network_id=sta2nets.network_id 
        WHERE network.network_name=\"{:}\" 
        AND dataperiod.periodstart<\"{:}\" 
        AND dataperiod.periodstop>\"{:}\";
    """.format(network, pdate.strftime('%Y-%m-%d'), pdate.strftime('%Y-%m-%d'))

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

parser.add_argument('-m',
                    '--my-sql-host',
                    action='store',
                    required=True,
                    help='Host where the database server is located',
                    metavar='MYSQL_HOST',
                    dest='mysql_host',
                    default=None)

parser.add_argument('-n',
                    '--database-name',
                    action='store',
                    required=True,
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
                    metavar='STATION_LIST',
                    dest='station_list',
                    nargs='+',
                    default=[])

parser.add_argument('--skip-download',
                    dest='skip_download',
                    action='store_true',
                    help='Do not download files, only show the query result')

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


    ## We now need credentials ... store them all in a credentials_dct dict
    if args.credentials_file:
        credentials_dct = extract_key_values(args.credentials_file, GNSS_DB_USER=None, GNSS_DB_PASS=None, GNSS_DB_HOST=None, GNSS_DB_NAME=None)
    if args.username: credentials_dct['GNSS_DB_USER'] = args.username
    if args.password: credentials_dct['GNSS_DB_PASS'] = args.password
    if args.mysql_host: credentials_dct['GNSS_DB_HOST'] = args.mysql_host
    if args.db_name: credentials_dct['GNSS_DB_NAME'] = args.db_name

    ## Connect to the database
    try:
        with connect(
            host=credentials_dct['GNSS_DB_HOST'],
            user=credentials_dct['GNSS_DB_USER'],
            password=credentials_dct['GNSS_DB_PASS'],
            database=credentials_dct['GNSS_DB_NAME']
        ) as connection:
            ## handle network query first ...
            if args.netowk is not None:
                with connection.cursor() as cursor:
                    cursor.execute(return_network_query(args.network, dt))
                    result = cursor.fetchall()
                    for row in result: print(row)
                
    except Error as e:
        print(e)
