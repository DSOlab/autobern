#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import re
import argparse
import datetime
from pybern.products.fileutils.keyholders import parse_key_file
from pybern.products.gnssdb_query import parse_db_credentials_file, query_sta_in_net
from pybern.products.euref.utils import get_euref_exclusion_list, get_m3g_log
from pybern.products.downloaders.retrieve import web_retrieve
from pybern.products.bernparsers.bern_crd_parser import parse_bern52_crd

class myFormatter(argparse.ArgumentDefaultsHelpFormatter,
                  argparse.RawTextHelpFormatter):
    pass


parser = argparse.ArgumentParser(
    formatter_class=myFormatter,
    description=
    'Given a network name, download latest M3G log files for all station not part of EPN/IGS. To check which of the network stations are not EPN/IGS, the program will try to download the remote file https://www.epncb.oma.be/ftp/station/coord/EPN/IGS14.CRD; any station not included therein, will be a candidate for log-file download.',
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
parser.add_argument('-O',
                    '--out-dir',
                    required=False,
                    help='Directory to download log files to',
                    metavar='OUTPUT_DIRECTORY',
                    dest='save_dir',
                    default=os.getcwd())

if __name__ == '__main__':

    ## parse command line arguments
    args = parser.parse_args()

    ## check output directory
    if not os.path.isdir(args.save_dir):
        print('[ERROR] Failed to locate directory {:}'.format(args.save_dir))
        sys.exit(1)

    ## try downloading remote, reference file ...
    status, target, saveas = web_retrieve('https://www.epncb.oma.be/ftp/station/coord/EPN/IGS14.CRD', save_dir=args.save_dir, fail_error=False)
    if status != 0:
        print('[ERROR] Failed to download remote file IGS14.CRD; fatal ...', file=sys.stderr)
        sys.exit(1)
    ## make a list of stations included in the crd_file
    stadct = parse_bern52_crd(saveas)
    os.remove(saveas)

    ## query database ...
    db_credentials_dct = parse_db_credentials_file(args.credentials_file)
    netsta_dct = query_sta_in_net(args.network, db_credentials_dct)

    ## loop through all stations in network, using their OFF name; if not
    ## included in the IGS14.CRD file, it means we need a log file ...
    for dct in netsta_dct:
        nsta = dct['mark_name_OFF'].upper()
        longn = dct['long_name']
        if nsta not in stadct:
            if longn is None or longn == '':
                print('[WRNNG] Database missing long name for station {:}; assuming \'00GRC\''.format(nsta))
                longn = nsta + '00GRC'
            try:
                status, target, saveas = get_m3g_log(longn, None, args.save_dir)
                print('[DEBUG] Downloaded log file for station {:}/{:} to {:}'.format(nsta, longn, saveas))
            except:
                print('[WRNNG] Failed to download log file for {:}/{:}'.format(nsta, longn))

