#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import os
import datetime
import sys
from pybern.products.fileutils.keyholders import extract_key_values
from pybern.products.downloaders.retrieve import web_retrieve

import mysql.connector
from mysql.connector import errorcode

## verbose print
g_verbose = False
verboseprint = print if g_verbose else lambda *a, **k: None

network_query=(
    """SELECT station.station_id, 
        station.mark_name_DSO, 
        stacode.mark_name_OFF, 
        stacode.station_name, 
        stacode.long_name,
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
        WHERE network.network_name=%s
        AND dataperiod.periodstart<=%s
        AND dataperiod.periodstop>=%s""")

station_query=(
    """SELECT station.station_id,
        station.mark_name_DSO,
        stacode.mark_name_OFF,
        stacode.station_name,
        stacode.long_name,
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
        JOIN  sta2nets ON sta2nets.station_id=station.station_id
        JOIN network ON network.network_id=sta2nets.network_id
        WHERE station.mark_name_DSO=%s
        AND dataperiod.periodstart<=%s
        AND dataperiod.periodstop>=%s""")

def query_dict_to_rinex_list(query_dict, pt):
    if 'rnx_v' not in query_dict:
        print('[WRNNG] No rinex version specified in query response; don\'t know how to make rinex')
        return []
    return make_rinex2_fn(query_dict['mark_name_OFF'], pt) if query_dict['rnx_v'] == 2 else make_rinex3_fn(query_dict['long_name'], pt)

def make_rinex3_fn(slong_name, pt):
    """ see http://acc.igs.org/misc/rinex304.pdf, 
        ch. 4 The Exchange of RINEX files
    """
    possible_rinex_fn = []
    for data_source in ['R', 'S']:
        for content_type in ['MO', 'GO']:
            possible_rinex_fn.append('{:}_{:}_{:}_01D_30S_{:}.crx.gz'.format(slong_name, data_source, pt.strftime('%Y%j%H%M'), content_type))
    return possible_rinex_fn

def make_rinex2_fn(station_id, pt):
    possible_rinex_fn = []
    for comp in ['Z', 'gz']:
        possible_rinex_fn.append('{:}{:}0.{:}d.{}'.format(station_id, pt.strftime('%j'), pt.strftime('%y'), comp))
    return possible_rinex_fn

def compare_query_result_dictionaries(dict_list):
    """ Given a list of dictionaries, compare the first dictionary to all the
        rest, key by key, and report any missing or different key/values

        Returns tow lists; the first one contains that keys that are different
        between any pair of dictionaries in the dict_list
        The second list, contains any key that is present in one or more of the 
        dictionaries, and missing from one or more of the rest.
    """
    sz = len(dict_list)
    if sz == 1: return [], []

    difs = []; missing = []
    dictA = dict_list[0]
    for dictB in dict_list[1:]:
        
        thispair_difs = []; thispair_missing = []

        ## check reference dictionary against current iteration ...
        for key in dictA:
            if key not in dictB:
                print('[WRNNG] Key {:} missing from query result line!'.format(key))
                thispair_missing.append(key)
            else:
                if dictA[key] != dictB[key]:
                    verboseprint('[WRNNG] Different values for key {:}; values are: {:} and {:}'.format(key, dictA[key],dictB[key]))
                    thispair_difs.append(key)
        
        ## check current iteration against referece dictionary ...
        dict1 = dictB
        dict2 = dictA
        for key in dict1:
            if key not in dict2:
                if key not in thispair_missing:
                    thispair_missing.append(key)
                    print('[WRNNG] Key {:} missing from query result line!'.format(key))
            else:
                if dict1[key] != dict2[key]:
                    if key not in thispair_difs:
                        thispair_difs.append(key)
                        vserboseprint('[WRNNG] Different values for key {:}; values are: {:} and {:}'.format(key, dict1[key],dict2[key]))

        ## add this pair's missing/different key/value pairs to the sum
        difs = list(set(difs + thispair_difs))
        missing = list(set(missing + thispair_missing))
                    
    return difs, missing

def download_station_rinex(query_dict, pt, output_dir=os.getcwd()):
    """ Perform a station query on the database and download a station
        RINEX file corresponding to the query's answer
    """
    verboseprint("[DEBUG] Here is the row dictionary fed to download: {}".format(query_dict))

    ## grab the first row/dictionary and formulate the url
    remote_path = query_dict['pth2rnx30s']
    for tf in zip(['%Y', '%j', '%m', '%d'],['_YYYY_', '_DDD_', '_MM_', '_DD_']):
        remote_path = remote_path.replace(tf[1], pt.strftime(tf[0]))
    
    remote_dir = query_dict['protocol'] + '://' + query_dict['url_domain'] + remote_path
    possible_rinex = query_dict_to_rinex_list(query_dict, pt)

    for fn in possible_rinex:
        remote_fn = remote_dir + fn
        verboseprint("[DEBUG] This is the remote file we should download: {:}".format(remote_fn))
        try:
            status, target, saveas = web_retrieve(remote_fn, save_dir=output_dir, username=query_dict['ftp_usname'], password=query_dict['ftp_passwd'])
            print('Downloaded remote file {:} to {:}'.format(target, saveas))
            return
        except:
            print('[WRNNG] Failed retrieving remote file {:}'.format(remote_fn))

def query_station(cursor, station, pt,  output_dir=os.getcwd()):
    ## execute the query ...
    cursor.execute(station_query, (station, pt, pt))

    ## grab all results from cursor and see if we are dealing with an empty set
    verboseprint('[DEBUG] Processing rows for station {:} rowcount={:}'.format(station, cursor.rowcount))
    rows = cursor.fetchall()
    if not rows or rows == {}:
        verboseprint('[WRNNG] Empty set returned for station {:} and date {:}.'.format(station, pt.strftime('%Y-%m-%d')))
        return -1
    
    ## compare rows (if multiple); the only acceptable result is that two
    ## different rows differ in the network_name key/column
    difs, missing = compare_query_result_dictionaries(rows)
    if difs != [] and difs != ['network_name']:
        print('[ERROR] Query results are different between queries! Can\'t handle that! (maybe an erronuous data enrty?)', file=sys.sdterr)
        return 2
    if missing != []:
        print('[ERROR] Query results are different between queries! Can\'t handle that! (maybe an erronuous data enrty?)', file=sys.stderr)
        return 3

    return download_station_rinex(rows[0], pt, output_dir)


def query_network(cursor, network, pt, output_dir=os.getcwd()):
    ##
    if not network: return 0

    ## execute the query ...
    cursor.execute(network_query, (network, pt, pt))

    ## grab all results from cursor and see if we are dealing with an empty set
    verboseprint('[DEBUG] Processing rows for network {:} rowcount={:}'.format(network, cursor.rowcount))
    rows = cursor.fetchall()
    if not rows or rows == {}:
        verboseprint('[WRNNG] Empty set returned for network {:} and date {:}.'.format(network, pt.strftime('%Y-%m-%d')))
        return -1

    for row in rows:
        download_station_rinex(row, pt, output_dir)


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

parser.add_argument('-i',
                    '--my-sql-host',
                    action='store',
                    required=True,
                    help='Host where the database server is located',
                    metavar='MYSQL_HOST',
                    dest='mysql_host',
                    default=None)

parser.add_argument('-m',
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

if __name__ == '__main__':

    args = parser.parse_args()

    ## verbose global verbosity level
    g_verbose = args.verbose
    
    ## Resolve the date from input args.
    dt = datetime.datetime.strptime('{:} {:03d}'.format(args.year, args.doy),
                                    '%Y %j')

    ## Where are we going to store local files?
    save_dir = args.output_dir if args.output_dir is not None else os.getcwd()
    if not os.path.isdir(save_dir):
        print('[ERROR] Failed to find requested directory \'{:}\''.format(save_dir), file=sys.stderr)
        sys.exit(5)


    ## We now need credentials ... store them all in a credentials_dct dict
    credentials_dct = {'GNSS_DB_USER':None, 'GNSS_DB_PASS':None, 'GNSS_DB_HOST':None, 'GNSS_DB_NAME':None}
    if args.credentials_file:
        credentials_dct = extract_key_values(args.credentials_file, **credentials_dct)
    if args.username: credentials_dct['GNSS_DB_USER'] = args.username
    if args.password: credentials_dct['GNSS_DB_PASS'] = args.password
    if args.mysql_host: credentials_dct['GNSS_DB_HOST'] = args.mysql_host
    if args.db_name: credentials_dct['GNSS_DB_NAME'] = args.db_name

    ## Connect to the database
    try:
        cnx = mysql.connector.connect(
            host=credentials_dct['GNSS_DB_HOST'], 
            database=credentials_dct['GNSS_DB_NAME'], 
            user=credentials_dct['GNSS_DB_USER'], 
            password=credentials_dct['GNSS_DB_PASS'])
        ## get a cursor to perform queries ...
        cursor = cnx.cursor(dictionary=True)
        ## ask the database for stations first
        for station in args.station_list:
            query_station(cursor, station, dt, save_dir)
        ## query the database for networks
        query_network(cursor, args.network, dt, save_dir)
        ## close the cursor
        cursor.close()
    except mysql.connector.Error as err:
        print('[ERROR] Failed to connect to database!', file=sys.stderr)
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("[ERROR ] Something is wrong with your user name or password", file=sys.stderr)
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("[ERROR] Database does not exist", file=sys.stderr)
        else:
            print('[ERROR] ' + str(err), file=sys.stderr)
    else:
        cnx.close()
