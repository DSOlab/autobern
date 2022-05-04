#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import os
import datetime
import sys
import re
from pybern.products.fileutils.keyholders import extract_key_values
from pybern.products.downloaders.retrieve import web_retrieve
import mysql.connector
from mysql.connector import errorcode
import locale ## for local datetimes (TREECOMP)

g_verbose_rnxdwnl = False

network_query=(
    """SELECT station.station_id, 
        station.mark_name_DSO, 
        stacode.mark_name_OFF,
        stacode.mark_numb_OFF,
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
        stacode.mark_numb_OFF,
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

def b2gr3(dt):
    """ Format a datetime instance's month as a 3-char string
        Needs locale package and el_GR available
        sudo apt install locales-all
    """
    locale.setlocale(locale.LC_ALL, "el_GR")
    mgr = dt.strftime("%b")
    locale.setlocale(locale.LC_ALL,locale.getdefaultlocale())
    return mgr

def rinex_exists_as(possible_rinex, output_dir=os.getcwd()):
    """ Given a list of (possible rinex) files, this function will search for
        a matching file, where matching is one of the following:
        * same as input,
        * decompressed (.Z, .gz)
        * Hatanaka-decompressed (d, .crx)
    """
    for prnx in possible_rinex:
        ## check for the fully compressed file
        fn = os.path.join(output_dir, prnx)
        if os.path.isfile(fn):
            return fn
        ## check for the decompressed Hatanaka version, aka no .Z or .gz
        for ext in ['.Z', '.gz']:
            if prnx.endswith(ext):
                rnx = re.sub(r'{:}$'.format(ext), '', prnx)
                fn = os.path.join(output_dir, rnx)
                if os.path.isfile(fn): return fn
        ## check for the fully-decompressed RINEX
        for ext in ['.Z', '.gz']:
            if prnx.endswith(ext):
                hrnx = re.sub(r'{:}$'.format(ext), '', prnx)
                if hrnx.endswith('d'):
                    fn = os.path.join(output_dir, hrnx[-1]+'o')
                    if os.path.isfile(fn): return fn
                elif hrnx.endswith('crx'):
                    fn = os.path.join(output_dir, hrnx[-3]+'rnx')
                    if os.path.isfile(fn): return fn
    return None


def query_dict_to_rinex_list(query_dict, pt):
    """ Given a query response row as dictionary (quer_dict), as answer from 
        a station_query query, formulate a list of candidate RINEX files to
        be downloaded (for the station described in the row). The function 
        will take into account if the station (for the given date) has RINEX
        v2 or v3 data holdings.
        ----------------------------------------------------------------------
        05/02/2022 Update: Special care for Metrica/SmartNet RINEX!
            These are received by a a DSO server and ARE MARKED WITH THE RECORD:
            'dc_name': 'DSO_MTRC'. If this holds, extra parameters are used to
            compile the list of possible RINEX names to search for.
    """
    if 'rnx_v' not in query_dict:
        print('[WRNNG] No rinex version specified in query response; don\'t know how to make rinex')
        return []
    # return make_rinex2_fn(query_dict['mark_name_OFF'], pt) if query_dict['rnx_v'] == 2 else make_rinex3_fn(query_dict['long_name'], pt)
    if query_dict['rnx_v'] == 2:
        return make_rinex2_fn(query_dict['mark_name_OFF'], pt)
    else:
        return make_rinex3_fn(query_dict['long_name'], pt, query_dict['mark_name_OFF'], query_dict['dc_name']=='DSO_MTRC')

def make_rinex3_fn(slong_name, pt, mark_name_off=None, allow_metrica_names=False):
    """ Given a station long-name (e.g. DYNG00GRC) and a python datetime 
        instance (pt), make a list of possible RINEX v3.x files that can hold
        data for the station/date.
        see http://acc.igs.org/misc/rinex304.pdf, 
        ch. 4 The Exchange of RINEX files
        ----------------------------------------------------------------------
        05/02/2022 Update: Added the parameters mark_name_off and 
            allow_metrica_names to handle the downloading of Metrica/SmartNet
            data received by DSO. These are RINEX 3, but follow a different
            naming convention, namely: ssssddd0.rnx.zip
            If allow_metrica_names is set to True, then a name following the 
            above convention will be added to the list of possible RINEX files
            returned, where the parameter mark_name_off is also used.
    """
    possible_rinex_fn = []
    for data_source in ['R', 'S']:
        for content_type in ['MO', 'GO']:
            possible_rinex_fn.append('{:}_{:}_{:}_01D_30S_{:}.crx.gz'.format(slong_name, data_source, pt.strftime('%Y%j%H%M'), content_type))
    ## Special naming convention for METRICA/SmartNet data coming to DSO!
    if allow_metrica_names:
        possible_rinex_fn = [ '{:}{:}0.rnx.zip'.format(mark_name_off, pt.strftime('%j')) ]
    return possible_rinex_fn

def make_rinex2_fn(station_id, pt):
    possible_rinex_fn = []
    for comp in ['Z', 'gz']:
        possible_rinex_fn.append('{:}{:}0.{:}d.{}'.format(station_id, pt.strftime('%j'), pt.strftime('%y'), comp))
    ## TREECMP data are UNIX compressed but **not** Hatanaka compressed
    comp = 'Z'
    possible_rinex_fn.append('{:}{:}0.{:}o.{}'.format(station_id, pt.strftime('%j'), pt.strftime('%y'), comp))
    return possible_rinex_fn

def compare_query_result_dictionaries(dict_list):
    """ Given a list of dictionaries, compare the first dictionary to all the
        rest, key by key, and report any missing or different key/values

        Returns tow lists; the first one contains that keys that are different
        between any pair of dictionaries in the dict_list
        The second list, contains any key that is present in one or more of the 
        dictionaries, and missing from one or more of the rest.
    """
    verboseprint = print if g_verbose_rnxdwnl else lambda *a, **k: None
    
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

def download_station_rinex(query_dict, pt, holdings, output_dir=os.getcwd()):
    """ given a station query result as dictionary (query_dict), parse and
        formulate the correct fields to enable RINEX download. The function
        will formulate:
        1. the remote url (path)
        2. a list of candidate RINEX (2 or 3) files
        Then it will iteratively try to download the remote RINEX files, trying
        all RINEX files in the possible_rinex list
        If a RINEX file is successefully downloaded, the holdings dictionary 
        will be update with an entry of type:
        holdings = { ...., mark_name_DSO: {'local': saved_RINEX_filename, 
                                           'remote': remote_RINEX_downloaded}
                                       ...}
    """
    verboseprint = print if g_verbose_rnxdwnl else lambda *a, **k: None
    verboseprint("[DEBUG] Here is the row dictionary fed to download: {}".format(query_dict))

    ## grab the first row/dictionary and formulate the url
    remote_path = query_dict['pth2rnx30s']
    for tf in zip(['%Y', '%j', '%m', '%d', '%y', '%d'],['_YYYY_', '_DDD_', '_MM_', '_DD_', '_YY_', '_DOM_']):
        remote_path = remote_path.replace(tf[1], pt.strftime(tf[0]))
    ## some urls may contain the 'official' station name, as _OFF_STA_NAME_
    remote_path = remote_path.replace('_OFF_STA_NAME_', query_dict['mark_name_OFF'])
    remote_path = remote_path.replace('_UOFF_STA_NAME_', query_dict['mark_name_OFF'].upper())
    if query_dict['station_name'] is not None:
        remote_path = remote_path.replace('_FULL_STA_NAME_', query_dict['station_name'])
    ## TREECOMP data also include a local month name
    remote_path = remote_path.replace('_GRM3_', b2gr3(pt))
    ## here is the final URL
    remote_dir = query_dict['protocol'] + '://' + query_dict['url_domain'] + remote_path

    ## make a list of candidate RINEX filenames to (try to) download
    possible_rinex = query_dict_to_rinex_list(query_dict, pt)

    ## check if any of the possible RINEX files already exist in the specified
    ## location (compressed or not).
    old_rnx = rinex_exists_as(possible_rinex, output_dir)
    if old_rnx is not None:
        ## well ok, but let's check the file size first before skipping download
        fsz = os.path.getsize(old_rnx) // 1024 ##Kb
        if fsz < 10:
            print('[DEBUG] A version of RINEX ({:}) already exists localy but is too small ({:}Kb)'.format(old_rnx, fsz))
            os.remove(old_rnx)
        else:
            verboseprint('[DEBUG] Skipping download for {:}; RINEX already exists as {:}'.format(query_dict['mark_name_DSO'], old_rnx))
            print('[DEBUG] Skipping download for {:}; RINEX already exists as {:}'.format(query_dict['mark_name_DSO'], old_rnx))
            holdings[query_dict['mark_name_DSO']]={'local': old_rnx, 'remote': None}
            return

    ## iteratively try downloading RINEX files from possible_rinex; stop when
    ## we succed
    for fn in possible_rinex:
        remote_fn = remote_dir + fn
        verboseprint("[DEBUG] This is the remote file we should download: {:}".format(remote_fn))
        use_active_ftp = True if query_dict['dc_name'] == 'TREECOMP2' else False
        try:
            status, target, saveas = web_retrieve(remote_fn, save_dir=output_dir, username=query_dict['ftp_usname'], password=query_dict['ftp_passwd'], active=use_active_ftp)
            verboseprint('[DEBUG] Downloaded remote file {:} to {:}'.format(target, saveas))
            holdings[query_dict['mark_name_DSO']]={'local': saveas, 'remote': target}
            return
        except:
            print('[WRNNG] Failed retrieving remote file {:}'.format(remote_fn))

def query_station(cursor, station, pt, holdings, output_dir=os.getcwd()):
    """ Given a cursor to the GNSS database, perform a station query as
        defined in station_query, for a given station 4-char id (station) and
        a python datetime instance (pt).
        If we get several lines back from the database (for the query), check
        the lines to see if and where they differ; the only acceptable 
        difference should be in the 'network_name' column, aka a station can
        belong to several networks. If that condition is not met trigger an 
        error.
        In case the above check is ok, proceed to download the corresponding 
        RINEX file for the station/date.
        Holdings is a dictionary that holds station RINEX download results. It
        will be passed to download_station_rinex and if we succed in RINEX
        download a new entry will be apended for the given station.
    """
    verboseprint = print if g_verbose_rnxdwnl else lambda *a, **k: None
    
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

    ## procced to station RINEX download ...
    return download_station_rinex(rows[0], pt, holdings, output_dir)

def query_network(cursor, network, pt, holdings, output_dir=os.getcwd()):
    """ Given a cursor to the GNSS database, perform a network query as
        defined in network_query, for a given network name (network) and a
        a python datetime instance (pt).
        In case the query returns results, proceed to download the corresponding 
        RINEX files for all stations in the network (each line we get back from
        the query, is a record for a unique station belonging to the network)
        Holdings is a dictionary that holds station RINEX download results. It
        will be passed to download_station_rinex and if we succed in RINEX
        download a new entry will be apended for the given station.
    """
    verboseprint = print if g_verbose_rnxdwnl else lambda *a, **k: None

    ## handle case where network is None
    if not network: return 0

    ## execute the query ...
    cursor.execute(network_query, (network, pt, pt))

    ## grab all results from cursor and see if we are dealing with an empty set
    verboseprint('[DEBUG] Processing rows for network {:} rowcount={:}'.format(network, cursor.rowcount))
    rows = cursor.fetchall()
    if not rows or rows == {}:
        verboseprint('[WRNNG] Empty set returned for network {:} and date {:}.'.format(network, pt.strftime('%Y-%m-%d')))
        return -1

    ## every row in the response string, is a station row; handle the station
    for row in rows:
        download_station_rinex(row, pt, holdings, output_dir)

def main(**kwargs):
    """ Drive the rnxdwnl script
        For a full list of command line options (or **kwargs) see the
        rnxdwnl script in the bin/ folder
    """

    ## if no station_list provided, make an empty one
    if 'station_list' not in kwargs: kwargs['station_list'] = []

    ## args = parser.parse_args()
    # for k in kwargs: print('rnx: {:} -> {:}'.format(k, kwargs[k]))

    ## verbose global verbosity level
    g_verbose_rnxdwnl = kwargs['verbose']
    
    ## Resolve the date from input args.
    dt = datetime.datetime.strptime('{:} {:03d}'.format(kwargs['year'], kwargs['doy']),
                                    '%Y %j')

    ## Where are we going to store local files?
    save_dir = kwargs['output_dir'] if kwargs['output_dir'] is not None else os.getcwd()
    if not os.path.isdir(save_dir):
        print('[ERROR] Failed to find requested directory \'{:}\''.format(save_dir), file=sys.stderr)
        sys.exit(5)

    ## We now need credentials ... store them all in a credentials_dct dict
    credentials_dct = {'GNSS_DB_USER':None, 'GNSS_DB_PASS':None, 'GNSS_DB_HOST':None, 'GNSS_DB_NAME':None}
    if kwargs['credentials_file']:
        credentials_dct = extract_key_values(kwargs['credentials_file'], **credentials_dct)
    for k,v in zip(['username', 'password', 'mysql_host', 'db_name'], ['GNSS_DB_USER', 'GNSS_DB_PASS', 'GNSS_DB_HOST', 'GNSS_DB_NAME']):
        if k in kwargs and kwargs[k] is not None: credentials_dct[v] = kwargs[k]

    ## create a dictionary to hold RINEX download results
    holdings = {}

    connection_error = 0
    ## Connect to the database
    try:
        cnx = mysql.connector.connect(
            host=credentials_dct['GNSS_DB_HOST'], 
            database=credentials_dct['GNSS_DB_NAME'], 
            user=credentials_dct['GNSS_DB_USER'], 
            password=credentials_dct['GNSS_DB_PASS'],
            connect_timeout=10)
        ## get a cursor to perform queries ...
        cursor = cnx.cursor(dictionary=True)
        ## ask the database for stations first
        for station in kwargs['station_list']:
            query_station(cursor, station, dt, holdings, save_dir)
        ## query the database for networks
        query_network(cursor, kwargs['network'], dt, holdings, save_dir)
        ## close the cursor
        cursor.close()
    except mysql.connector.Error as err:
        print('[ERROR] Failed to connect to database!', file=sys.stderr)
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("[ERROR] Something is wrong with your user name or password", file=sys.stderr)
            connection_error = 10
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("[ERROR] Database does not exist", file=sys.stderr)
            connection_error = 11
        else:
            print('[ERROR] ' + str(err), file=sys.stderr)
            connection_error = 12
    else:
        cnx.close()

    if connection_error > 0:
        msg = '[ERROR] Failed to connect to to database at {:}@{:}; fatal!'.format(credentials_dct['GNSS_DB_NAME'], credentials_dct['GNSS_DB_HOST'])
        raise RuntimeError(msg)

    return holdings
