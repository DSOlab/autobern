#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import argparse
import subprocess
import datetime
import atexit
import pybern.products.rnxdwnl_impl as rnxd
import pybern.products.fileutils.decompress as dcomp
from pybern.products.fileutils.keyholders import parse_key_file
from pybern.products.gnssdb_query import parse_db_credentials_file, query_sta_in_net
from pybern.products.codesp3 import get_sp3
from pybern.products.codeerp import get_erp
from pybern.products.codeion import get_ion
from pybern.products.codedcb import get_dcb

##
crx2rnx_dir='/home/bpe/applications/RNXCMP_4.0.6_Linux_x86_64bit/bin/'

## list of temporary files created during program run that beed to be deleted 
## before exit
temp_files = []

def decompress_rinex(rinex_holdings):
    """ rinex_holdings = {'pdel': {
        'local': '/home/bpe/applications/autobern/bin/pdel0250.16d.Z', 
        'remote': 'https://cddis.nasa.gov/archive/gnss/data/daily/2016/025/16d/pdel0250.16d.Z'}, 
        'hofn': {...}}
        The retuned dictionat is a copy of the input one, but the names of the
        'local' rinex have been changed to the uncompressed filenames
    """
    new_holdings = {}
    for station, dct in rinex_holdings.items():
        if dct['local'] is not None:
            crnx = dct['local']
            if not os.path.isfile(crnx):
                print('[ERROR] Failed to find downloaded RINEX file {:}'.format(crnx), file=sys.stderr)
                raise RuntimeError

            ## decompress to ascii (hatanaka compressed)
            if crnx.endswith('.Z') or crnx.endswith('.gz'):
                cr = None
                try:
                    cr, drnx = dcomp.os_decompress(crnx, True)
                except:
                    print('[WRNNG] Failed to decompress RINEX file {:}'.format(crnx), file=sys.stderr)
                    print('[WRNNG] Note that the RINEX file {:} will be deleted from rinex_holdings and removed'.format(crnx), file=sys.stderr)
                    os.remove(crnx)
                if cr is not None:
                    assert(os.path.isfile(drnx))
                    ## decompress from Hatanaka
                    drnx, rnx = dcomp.crx2rnx(drnx, True, crx2rnx_dir)
                    new_holdings[station] = {'local': rnx, 'remote': dct['remote']}
            
            elif crnx.endswith('d') or crnx.endswith('crx'):
                ## else if hatanaka compressed
                drnx, rnx = dcomp.crx2rnx(drnx, True, crx2rnx_dir)
                new_holdings[station] = {'local': rnx, 'remote': dct['remote']}
            
            else:
                new_holdings[station] = dct
    return new_holdings

def bpe_exit(error):
    for fn in temp_files: os.remove(fn)
    sys.exit(error)

##  If only the formatter_class could be:
##+ argparse.RawTextHelpFormatter|ArgumentDefaultsHelpFormatter ....
##  Seems to work with multiple inheritance!
class myFormatter(argparse.ArgumentDefaultsHelpFormatter,
                  argparse.RawTextHelpFormatter):
    pass


parser = argparse.ArgumentParser(
    formatter_class=myFormatter,
    description=
    'Synchronize a folder with AIUB\s remote GEN directory',
    epilog=('''National Technical University of Athens,
    Dionysos Satellite Observatory\n
    Send bug reports to:
    Xanthos Papanikolaou, xanthos@mail.ntua.gr
    Dimitris Anastasiou,danast@mail.ntua.gr
    January, 2021'''))

parser.add_argument('-y',
                    '--year',
                    metavar='YEAR',
                    dest='year',
                    required=False,
                    help='The year of date.')
parser.add_argument('-d',
                    '--doy',
                    metavar='DOY',
                    dest='doy',
                    required=False,
                    help='The day-of-year (doy) of date.')
                    ##  merge individual (hourly) files
parser.add_argument('-c',
                    '--config-file',
                    required=False,
                    help='If you request forecast grid files, you need credentials to access the data; if you provide a CONFIG_FILE here, the program will try to parse lines: \'TUWIEN_VMF1_USER=\"username\" and TUWIEN_VMF1_PASS=\"mypassword\" \' and use the \"username\"  and \"mypassword\" credentials to access the forecast data center',
                    metavar='CONFIG_FILE',
                    dest='config_file',
                    default=None)
parser.add_argument('--verbose',
                    dest='verbose',
                    action='store_true',
                    help='Trigger verbose run (prints debug messages).')
parser.add_argument('-g',
                    '--campaign',
                    required=False,
                    help='',
                    metavar='CAMPAIGN',
                    dest='campaign',
                    default=None)
parser.add_argument('-n',
                    '--network',
                    required=False,
                    help='',
                    metavar='NETWORK',
                    dest='network',
                    default=None)
parser.add_argument(
                    '--elevation',
                    required=False,
                    help='',
                    metavar='ELEVATION',
                    dest='elevation',
                    default='3')
parser.add_argument(
                    '--satellite-system',
                    required=False,
                    help='',
                    metavar='SATELLITE_SYSTEM',
                    dest='sat_sys',
                    choices=['gps', 'mixed'],
                    default='mixed')
parser.add_argument(
                    '--loadgps-file',
                    required=False,
                    help='',
                    metavar='LOADGPS_FILE',
                    dest='b_loadgps',
                    default=None)
parser.add_argument(
                    '--tables_dir',
                    required=False,
                    help='',
                    metavar='TABLES_DIR',
                    dest='tables_dir',
                    default=None)
parser.add_argument(
                    '--skip-rinex-download',
                    action='store_true',
                    help='Skip download of RINEX files; only consider RINEX files already available for network/date',
                    dest='skip_rinex_download')


if __name__ == '__main__':

    ## parse command line arguments
    args = parser.parse_args()

    ## relative to absolute path for config file
    args.config_file = os.path.abspath(args.config_file)

    ## parse the config file (if any)
    config_file_dict = parse_key_file(args.config_file)

    ## merge args and config_file_dict to options; all keys are lowercase and
    ## master values (in case same keys are recorded in both dictionaries) are
    ## considered to be in args
    options = {}
    for k,v in config_file_dict.items():
        options[k.lower()] = v
    for k,v in vars(args).items():
        if v is not None:
            options[k.lower()] = v

    ##
    #print('------------------------------------------------------------------')
    #for k in options: print('{:.20s} -> {:.20s}'.format(k, options[k]))
    #print('------------------------------------------------------------------')

    ## verbose print
    verboseprint = print if options['verbose'] else lambda *a, **k: None

   ## source the LOADGPS files (enviromental variables)
    if not os.path.isfile(options['b_loadgps']):
        print('[ERROR] Failed to located LOADGPS file {:}'.format(options['b_loadgps']), file=sys.stderr)
        bpe_exit(1)
    #exec(open(options['b_loadgps']).read())
    subprocess.call("{}".format(options['b_loadgps']), shell=True)
    
    ## check that the campaign directory exists

    ## date we are solving for as datetime instance
    dt = datetime.datetime.strptime('{:}-{:03d}'.format(options['year'], int(options['doy'])), '%Y-%j')

    ## download the RINEX files for the given network. Hold results int the
    ## rinex_holdings variable. RINEX files are downloaded to the DATAPOOL area
    rnxdwnl_options = {
        'year': int(options['year']),
        'doy': int(options['doy'].lstrip('0')),
        'output_dir': os.getenv('D'),
        'credentials_file': options['config_file'],
        'network': options['network'],
        'verbose': options['verbose']
    }
    #if args.skip_rinex_download:
    #    rinex_holdings = {}
    #else:
    #    rinex_holdings = rnxd.main(**rnxdwnl_options)
    ## print(rinex_holdings)

    ## get info on the stations that belong to the network, aka
    ## [{'station_id': 1, 'mark_name_DSO': 'pdel', 'mark_name_OFF': 'pdel',..},{...}]
    #db_credentials_dct = parse_db_credentials_file(options['config_file'])
    #netsta_dct = query_sta_in_net(options['network'], db_credentials_dct)

    ## uncompress (to obs) all RINEX files of the network/date
    #rinex_holdings = decompress_rinex(rinex_holdings)

    ## write product information to a dictionary
    product_dict = {}

    ## download sp3
    for count,orbtype in enumerate(['final', 'final-rapid', 'early-rapid', 'ultra-rapid', 'current']):
        try:
            status, remote, local = get_sp3(type=orbtype, pydt=dt, save_dir=os.getenv('D'))
            verboseprint('[DEBUG] Downloaded orbit file {:} of type {:} ({:})'.format(local, orbtype, status))
            product_dict['sp3'] = {'remote': remote, 'local': local, 'type': orbtype}
            break
        except:
            verboseprint('[DEBUG] Failed downloading sp3 file of type {:}'.format(orbtype))
    ## download erp
    for count,erptype in enumerate(['final', 'final-rapid', 'early-rapid', 'ultra-rapid', 'current']):
        try:
            status, remote, local = get_erp(type=erptype, pydt=dt, span='daily', save_dir=os.getenv('D'))
            verboseprint('[DEBUG] Downloaded erp file {:} of type {:} ({:})'.format(local, erptype, status))
            product_dict['erp'] = {'remote': remote, 'local': local, 'type': erptype}
            break
        except:
            verboseprint('[DEBUG] Failed downloading erp file of type {:}'.format(erptype))
    ## download ion
    for count,iontype in enumerate(['final', 'rapid', 'current']):
        try:
            status, remote, local = get_ion(type=erptype, pydt=dt, save_dir=os.getenv('D'))
            verboseprint('[DEBUG] Downloaded ion file {:} of type {:} ({:})'.format(local, iontype, status))
            product_dict['ion'] = {'remote': remote, 'local': local, 'type': iontype}
            break
        except:
            verboseprint('[DEBUG] Failed downloading ion file of type {:}'.format(iontype))
    ## download dcb
    days_dif = (datetime.datetime.now() - dt).days
    if days_dif > 0 and days_dif < 30:
            status, remote, local = get_dcb(type='current', obs='full', save_dir=os.getenv('D'))
            product_dict['dcb'] = {'remote': remote, 'local': local, 'type': 'full'}
    elif days_dif >= 30:
            status, remote, local = get_dcb(type='final', pydt=dt, obs='p1p2all', save_dir=os.getenv('D'))
            product_dict['dcb'] = {'remote': remote, 'local': local, 'type': 'p1p2all'}
    else:
        print('[ERROR] Don\'t know what DCB product to download!')
        sys.exit(1)

