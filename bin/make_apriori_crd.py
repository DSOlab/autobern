#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import re
import argparse
import datetime
from pybern.products.fileutils.keyholders import parse_key_file
from pybern.products.bernparsers.bern_crd_parser import parse_bern52_crd
from pybern.products.gnssdb_query import parse_db_credentials_file, query_sta_in_net
import pybern.products.formats.ssc as ssc

class myFormatter(argparse.ArgumentDefaultsHelpFormatter,
                  argparse.RawTextHelpFormatter):
    pass


parser = argparse.ArgumentParser(
    formatter_class=myFormatter,
    description=
    '',
    epilog=('''National Technical University of Athens,
    Dionysos Satellite Observatory\n
    Send bug reports to:
    Xanthos Papanikolaou, xanthos@mail.ntua.gr
    Dimitris Anastasiou,danast@mail.ntua.gr
    January, 2021'''))

parser.add_argument('-n',
                    '--network',
                    metavar='NETWORK',
                    dest='network',
                    required=True,
                    help='Network to consider')
parser.add_argument('-c',
                    '--credentials-file',
                    required=True,
                    help='Credentials to access the data base',
                    metavar='CREDENTIALS_FILE',
                    dest='credentials_file',
                    default=None)
parser.add_argument('-o',
                    '--crd-out',
                    required=True,
                    help='',
                    metavar='CRD_OUTPUT',
                    dest='crd_out',
                    default=None)
parser.add_argument(
                    '--ssc-files',
                    nargs='*',
                    required=False,
                    help='',
                    metavar='SSC_FILES',
                    dest='ssc_files',
                    default=[])
parser.add_argument(
                    '--crd-files',
                    nargs='*',
                    required=False,
                    help='',
                    metavar='CRD_FILES',
                    dest='crd_files',
                    default=[])
parser.add_argument(
                    '--date',
                    required=False,
                    help='',
                    metavar='DATE',
                    dest='date',
                    default=None)
parser.add_argument(
                    '--date-format',
                    required=False,
                    help='',
                    metavar='DATE_FORMAT',
                    dest='date_format',
                    default="%Y-%m-%d")

def find_station_in_ssc_records(station, ssc_records):
    for idx, record in enumerate(ssc_records):
        if record.id == station:
            return idx
    return -1

def find_station_in_crd_records(station, crd_records):
    for idx, record in enumerate(crd_records):
        if station.upper() in record:
            return idx
    return -1

if __name__ == '__main__':

    ## parse command line arguments
    args = parser.parse_args()

    ## get the date ...
    if args.date is None:
        args.date = datetime.datetime.now()
    else:
        try:
            args.date = datetime.datetime.strptime(args.date, args.date_format)
        except:
            print('[ERROR] Failed to parse input date string {:} using the format string {:}'.format(args.date, args.date_format))
            sys.exit(1)
    
    ## query database ...
    db_credentials_dct = parse_db_credentials_file(args.credentials_file)
    netsta_dct = query_sta_in_net(args.network, db_credentials_dct)

    ## make a list of the stations in the network, using their 4-char id's
    sta_list = [s['mark_name_OFF'].upper() for s in netsta_dct]

    ## parse ssc file (in the order they were passed in) for the given station
    ## list
    ssc_records = []
    for sscfn in args.ssc_files:
        ssc_records += ssc.parse_ssc(sscfn, sta_list, args.date)

    ## parse records off from the CRD files
    crd_records = []
    for crdfn in args.crd_files:
        crd_records.append(parse_bern52_crd(crdfn))

    ## write header to crd file
    header = 'Coordinate Extrapolation from pybern'
    datum = 'IGS_14'
    flag = 'APR'
    num = 0
    sta_sofar = []
    with open(args.crd_out, 'w') as bout:
        print("{:}".format(header), file=bout)
        print("--------------------------------------------------------------------------------", file=bout)
        print("LOCAL GEODETIC DATUM: {:}           EPOCH: 2010-01-01 00:00:00".format(datum, args.date.strftime("%Y-%m-%d %H:%M:%S")), file=bout)
        print("", file=bout)
        print("NUM  STATION NAME           X (M)          Y (M)          Z (M)     FLAG", file=bout)
        print("", file=bout)
        for station in sta_list:
            num += 1
            station_found = False

            index = find_station_in_ssc_records(station, ssc_records)
            if index >=0 :
                x, y, z = ssc_records[index].extrapolate(args.date)
                print('{:3d}  {:} {:9s}{:+16.4f}{:+15.4f}{:+15.4f}'.format(num, ssc_records[index].id, ssc_records[index].domes, x, y, z), file=bout)
                sta_sofar.append(station)
                station_found = True
            
            else:
                index = find_station_in_crd_records(station, crd_records)
                if index >=0 :
                    sta_dct = crd_records[index][station.upper()]
                    print('{:3d}  {:} {:9s}{:+16.4f}{:+15.4f}{:+15.4f}'.format(num, station.upper(), sta_dct['domes'], sta_dct['x'], sta_dct['y'], sta_dct['z']), file=bout)
                    station_found = True
                    sta_sofar.append(station)
            
            if not station_found:
                print('[WRNNG] Failed to find station {:} in any of the provided SSC/CRD files!'.format(station), file=sys.stderr)
