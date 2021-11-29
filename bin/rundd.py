#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import argparse
import subprocess
import pprint
import shlex
import pybern.products.rnxdwnl_impl as rnxd
from pybern.products.fileutils.keyholders import parse_key_file

## list of temporary files created during program run that beed to be deleted 
## before exit
temp_files = []

def bpe_exit(error):
    for fn in temp_files: os.remove(fn)
    sys.exit(error)

def shell_source(sfile):
    """ Emulate bash 'source' with the target file sfile. Note that 'source'
        is not a program (but a script) hence it cannot be called via a 
        subprocess
    """
    command = shlex.split("bash -c 'source {:} && env'".format(sfile))
    proc = subprocess.Popen(command, stdout = subprocess.PIPE)
    for line in proc.stdout:
        (key, _, value) = line.strip().partition("=")
        os.environ[key] = value
    proc.communicate()
    #pprint.pprint(dict(os.environ))

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
    #for k,v in config_file_dict.items(): py:3
    for k,v in config_file_dict.iteritems():
        options[k.lower()] = v
    #for k,v in args.items(): py:3
    for k,v in vars(args).iteritems():
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
    shell_source(options['b_loadgps'])
    
    ## check that the campaign directory exists

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
    rinex_holdings = rnxd.main(**rnxdwnl_options)
