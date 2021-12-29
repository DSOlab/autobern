#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import re
import argparse
import datetime
import atexit
from pybern.products.fileutils.keyholders import parse_key_file
from pybern.products.gnssdb_query import parse_db_credentials_file, query_sta_in_net
from pybern.products.euref.utils import get_euref_exclusion_list, get_m3g_log
from pybern.products.downloaders.retrieve import web_retrieve
import pybern.products.bernparsers.bernsta as bsta
import pybern.products.formats.igs_log_file as igsl

temp_files = []
def cleanup(tmp_file_list):
    for f in tmp_file_list:
        try:
            print('[DEBUG] Removing temporary file {:}'.format(f))
            os.remove(f)
        except:
            pass


atexit.register(cleanup, temp_files)

class myFormatter(argparse.ArgumentDefaultsHelpFormatter,
                  argparse.RawTextHelpFormatter):
    pass

parser = argparse.ArgumentParser(
    formatter_class=myFormatter,
    description=
    'Given a network name, a reference (Bernese 5.2) .STA file and a list of igs log files, compile a new, valid .STA file that includes all sites of the network',
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
parser.add_argument('-l',
                    '--log-dir',
                    required=False,
                    help='Directory where log files are stored',
                    metavar='LOG_DIRECTORY',
                    dest='log_dir',
                    default=os.getcwd())
parser.add_argument('-s',
                    '--reference_sta',
                    required=False,
                    help='The reference .STA file; if not specified, download https://www.epncb.oma.be/ftp/station/general/EUREF52.STA',
                    metavar='REFERENCE_STA',
                    dest='reference_sta',
                    default=None)
parser.add_argument('-o',
                    '--sta-file',
                    required=True,
                    help='The resulting .STA file, which holds records for all stations in network if they are recorded either in the reference .STA file or have a valid log file in the LOG_DIRECTORY dir',
                    metavar='OUT_STA',
                    dest='out_sta',
                    default=None)
parser.add_argument('--skip-log-error',
    action='store_true',
    help='If not set, then the program will stop in case a log file cannot be parsed; if set, erronuous log files will be  skipped',
    dest='skip_log_error')

def get_latest_log(site, dir):
    site = site.lower()
    if len(site) > 4: site = site[0:4]

    pattern = site + r"[0-9]{2}[a-z]{3}_[0-9]{4}[0-9]{2}[0-9]{2}\.log"
    log = None
    t = datetime.datetime.min
    
    for f in os.listdir(dir):
      if re.match(pattern, f):
        g = re.match(site + r"[0-9]{2}[a-z]{3}_([0-9]{4}[0-9]{2}[0-9]{2})\.log", f)
        if t < datetime.datetime.strptime(str(g.group(1)), "%Y%m%d"):
          log = f
          t = datetime.datetime.strptime(str(g.group(1)), "%Y%m%d")

    return log, t

def logdir2sites(dir):
  sites = []
  pattern = r"[a-zA-Z0-9]{4}[0-9]{2}[a-z]{3}_[0-9]{4}[0-9]{2}[0-9]{2}\.log"
  for f in os.listdir(dir):
    if re.match(pattern, f):
      if f[0:4] not in sites: sites.append(f[0:4])
  return sites

if __name__ == '__main__':

    ## parse command line arguments
    args = parser.parse_args()

    ## check log directory
    if not os.path.isdir(args.log_dir):
        print('[ERROR] Failed to locate directory {:}'.format(args.log_dir))
        sys.exit(1)

    ## handle reference sta file
    if args.reference_sta is None:
        try:
            status, target, saveas = web_retrieve('https://www.epncb.oma.be/ftp/station/general/EUREF52.STA')
        except:
            print('[ERROR] Failed to download reference sta file', file=sys.stderr)
            saveas = None
            status = 1
    else:
        if not os.path.isfile(args.reference_sta):
            print('[ERROR] Failed to find reference sta file {:}'.format(args.reference_sta), file=sys.stderr)
            sys.exit(1)
        else:
            saveas = args.reference_sta
    if saveas is None:
        sys.exit(1)
    else:
        reference_sta = saveas

    ## query database ...
    db_credentials_dct = parse_db_credentials_file(args.credentials_file)
    netsta_dct = query_sta_in_net(args.network, db_credentials_dct)
    ## make a list of 4-char ids
    netsta_list = [ dct['mark_name_DSO'] for dct in netsta_dct ]

    ## parse the reference sta file and filter stations
    sta = bsta.BernSta(reference_sta)
    stainfo = sta.parse().filter([s.upper() for s in netsta_list], True)

    ## loop through the log files dir and get a list of site names
    sites = logdir2sites(args.log_dir)
    for site in sites:
      error = 0
      logfn, _ = get_latest_log(site, args.log_dir)
      print('[DEBUG] Parsing log file {:} ...'.format(logfn))
      try:
        error = stainfo.update_from_log(os.path.join(args.log_dir, logfn))
      except:
        error = 1
      if error:
        print('[WRNNG] Failed to parse log file {:}; cannot extract info to STA format for the given log-file'.format(os.path.join(args.log_dir, logfn)), file=sys.stderr)
      if error and not args.skip_log_error:
        sys.exit(1)

    ## dump the new infomation to a sta file
    stainfo.dump_as_sta(args.out_sta)
