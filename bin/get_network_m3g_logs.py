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
from pybern.products.euref.m3g import get_exportlog, get_m3g_network_stations
from pybern.products.downloaders.retrieve import web_retrieve
from pybern.products.bernparsers.bern_crd_parser import parse_bern52_crd

def match_log_files(log_dir, site9charid):
  ## note that log are supposed to be in lowercase
  site = site9charid.lower()
  pattern = site + r"_[0-9]{4}[0-9]{2}[0-9]{2}\.log"
  matches = []
  for f in os.listdir():
    if re.match(pattern, f): matches.append(f)
  return matches

class myFormatter(argparse.ArgumentDefaultsHelpFormatter,
                  argparse.RawTextHelpFormatter):
    pass


parser = argparse.ArgumentParser(
    formatter_class=myFormatter,
    description=
    'Given a network name, download latest M3G log files for all stations included in the network. If the user wants to skip a subset of the stations, then this can be done via the \'--exclude-m3g-network\' or the \'--exclude-EPN-IGS14\' switches (see help message)',
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
parser.add_argument('--skip-if-log-exists',
    action='store_true',
    help='Skip download if a log file for the station already exists; \'exists\' means that a log file name sssssssss_YYYYMMDD.log is present in the OUTPUT_DIRECTORY dir and is newer or of the same date as the latest M3G log file',
    dest='skip_if_exists')
parser.add_argument('--exclude-m3g-network',
    help='Ask the M3G repository for all stations in network specified, and exclude them from log file downloading',
    dest='exclude_m3g_net',
    metavar='EXCLUDE_M3G_NETWORK',
    default=None)
parser.add_argument('--exclude-EPN-IGS14',
    action='store_true',
    help='Download the remote file https://www.epncb.oma.be/ftp/station/coord/EPN/IGS14.CRD and skip any station (from log file downloading) that is recorded in this file',
    dest='get_epn_igs_crd')


if __name__ == '__main__':

    ## parse command line arguments
    args = parser.parse_args()

    ## check output directory
    if not os.path.isdir(args.save_dir):
        print('[ERROR] Failed to locate directory {:}'.format(args.save_dir))
        sys.exit(1)

    ## stations to exclude from log file downloading, 4-char ids, lowercase
    exclude_sta = []

    ## try downloading remote, reference file if needed ...
    if args.get_epn_igs_crd:
      status, target, saveas = web_retrieve('https://www.epncb.oma.be/ftp/station/coord/EPN/IGS14.CRD', save_dir=args.save_dir, fail_error=False)
      if status != 0:
          print('[ERROR] Failed to download remote file IGS14.CRD; fatal ...', file=sys.stderr)
          sys.exit(1)
      ## make a list of stations included in the crd_file
      stadct = parse_bern52_crd(saveas)
      stadct = [x.lower() for x in stadct]
      os.remove(saveas)
      exclude_sta += stadct

    ## should we exclude any M3G network ?
    if args.exclude_m3g_net is not None:
      try:
        excllist = get_m3g_network_stations(args.exclude_m3g_net, True)
      except:
        print('[ERROR] Failed to get metadata info for network id: {:} from M3G'.format(args.exclude_m3g_net), file=sys.stderr)
        sys.exit(1)
      excllist = [s.lower() for s in excllist if s not in exclude_sta]
      exclude_sta += excllist

    ## query database ...
    db_credentials_dct = parse_db_credentials_file(args.credentials_file)
    netsta_dct = query_sta_in_net(args.network, db_credentials_dct)

    ## loop through all stations in network, using their OFF name; if not
    ## included in the IGS14.CRD file, it means we need a log file ...
    for dct in netsta_dct:
        nsta = dct['mark_name_OFF']
        longn = dct['long_name'] if dct['long_name'] is not None else ''
        if nsta.lower() not in exclude_sta:
            if longn is None or longn == '':
                print('[WRNNG] Database missing long name for station {:}; assuming \'00GRC\''.format(nsta))
                longn = nsta + '00grc'
            try:
                saveas = get_exportlog(longn.upper(), args.save_dir, args.skip_if_exists)
                if saveas is not None:
                  print('[DEBUG] Downloaded log file for station {:}/{:} to {:}'.format(nsta, longn, saveas))
            except:
                print('[WRNNG] Failed to download log file for {:}/{:}'.format(nsta, longn))
