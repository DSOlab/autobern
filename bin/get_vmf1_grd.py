#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import argparse
import datetime
from shutil import copyfileobj
from pybern.products.downloaders.retrieve import http_retrieve
from pybern.products.fileutils.keyholders import parse_key_file

## https://vmf.geo.tuwien.ac.at/trop_products/GRID/2.5x2/VMF1/VMF1_OP/2021/
TUW_URL = 'https://vmf.geo.tuwien.ac.at'
OP_URL_DIR = '/trop_products/GRID/2.5x2/VMF1/VMF1_OP'
FC_URL_DIR = '/trop_products/GRID/2.5x2/VMF1/VMF1_FC'

def downloading_complete(dct,flag=None):
    """ Utility function: check if all files in the dictionary have been 
        successefully downloaded.
        You can se the flag to:
        * 'op' to only check for final products (forecast are ignored)
        * 'fc' to only check for forecast products (final are ignored)
        * None to either check final or forecast, i.e. a file is considered
          successefully downloaded in either case
    """
    if not flag:
        all([dct[x]['fc'] or dct[x]['op'] for x in dct])
    elif flag == 'fc':
        return all([dct[x]['fc'] for x in dct])
    elif flag=='op':
        return all([dct[x]['op'] for x in dct])
    else:
        raise RuntimeError('[ERROR] Invalid argument to downloading_complete function!')

def remove_local(dct):
    """ Utility function: remove files specified in the dct, which has the
        form: {...'VMFG_YYYYMMDD.H00':{'op':0/1, 'fc':0/1, 'fn':foo}...}
        For every entr, try to remove the 'fn' value if any of 'op', 'fc' is
        not zero. For more info on the passed in dictionary, see the main code.
    """
    for key, idct in dct.items():
        if idct['op'] or idct['fc']:
            try:
                os.remove(idct['fn'])
            except:
                pass

def get_credentials_from_args(arg_dict):
    """ Iterate through command line arguments to find the credentials needed
        to access the forecast vmf grid files.
        First see if we have a config file and parse from there the 
        credentials. Then check to see if we have username/password cmd options
        and resolve them.
        Note! some cmd options have a default value of None; guard against 
        this.
    """
    if 'config_file' in arg_dict and arg_dict['config_file']:
        d = parse_key_file(arg_dict['config_file']);
        username = d['TUWIEN_VMF1_USER'] if 'TUWIEN_VMF1_USER' in d else None
        password = d['TUWIEN_VMF1_PASS'] if 'TUWIEN_VMF1_PASS' in d else None
    if 'username' in arg_dict and arg_dict['username']:
        username = arg_dict['username']
    if 'password' in arg_dict and arg_dict['password']:
        password = arg_dict['password']
    try:
        assert(username != None)
        assert(password != None)
    except:
        raise RuntimeError('[ERROR] Could not resolve credentials for forecast grid file access')
    return username, password

def final_dir(dt):
    return '{:}/{:}/{:4d}'.format(TUW_URL, OP_URL_DIR, dt.year)


def forecast_dir(dt):
    return '{:}/{:}/{:4d}'.format(TUW_URL, FC_URL_DIR, dt.year)


def decompose_grid_fn(fn):
    """ Decompose a VMF1 grid file to a Python datetime instance. 
        Generic format of grid files is: VMFG_YYYYMMDD.H00. Return the
        corresponding datetime from YYYY, MM, DD and hour.
    """
    fn = os.path.basename(fn)
    m = re.match(r'VMFG_([0-9]{8})\.H([0-9]{2})$', fn)
    if not m:
        print('[ERROR] Invalid vmf1 grid filename', file=sys.stderr)
        raise RuntimeError('[ERROR] Invalid vmf1 grid filename')
    return datetime.datetime.strptime(
        '{:} {:}:00:00'.format(g.group(1), m.group(2)), '%Y%m%d %H:%M:%S')


##  If only the formatter_class could be:
##+ argparse.RawTextHelpFormatter|ArgumentDefaultsHelpFormatter ....
##  Seems to work with multiple inheritance!
class myFormatter(argparse.ArgumentDefaultsHelpFormatter,
                  argparse.RawTextHelpFormatter):
    pass


parser = argparse.ArgumentParser(
    formatter_class=myFormatter,
    description=
    'Download VMF1 grid files from https://vmf.geo.tuwien.ac.at/trop_products/GRID/2.5x2/VMF1/\nThe script allows downloading of both final and forecast grid files but note that for the later you will need credentials. The program will return an exit status of zero on a successeful run, else it will return a positive integer (>0).\nReference:  re3data.org: VMF Data Server; editing status 2020-12-14; re3data.org - Registry of Research Data Repositories. http://doi.org/10.17616/R3RD2H',
    epilog=('''National Technical University of Athens,
    Dionysos Satellite Observatory\n
    Send bug reports to:
    Xanthos Papanikolaou, xanthos@mail.ntua.gr
    Dimitris Anastasiou,danast@mail.ntua.gr
    March, 2021'''))

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
##  hour of day
parser.add_argument('--hour',
                    action='store',
                    required=False,
                    type=int,
                    help='The hour of day (integer in range [0-23]). This is for downloading individual hourly files (each file covers an 6-hour time span.',
                    metavar='HOUR',
                    dest='hour',
                    default=None)

##  download path
parser.add_argument(
    '-O',
    '--outpur-dir',
    action='store',
    required=False,
    help='The directory where the downloaded files shall be placed. Note that this does not affect the merged file (if \'--merge [MERGED_FILE]\' is used).',
    metavar='OUTPUT_DIR',
    dest='output_dir',
    default=os.getcwd())

##  merge individual (hourly) files
parser.add_argument('-m',
                    '--merge',
                    action='store',
                    required=False,
                    help='Merge/concatenate individual grid files to this final grid file. This can be a filename optionaly including path (if not path is set, then the file will be created in cwd).',
                    metavar='MERGED_FILE',
                    dest='merge_to',
                    default=None)

## allow forecast products to be used
parser.add_argument(
    '-f',
    '--allow-forecast',
    dest='allow_fc',
    action='store_true',
    help='If needed, allow the downloading of forecast VMF1 grid file(s)')

parser.add_argument(
    '--del-after-merge',
    dest='del_after_merge',
    action='store_true',
    help='Delete individual grid files after a successeful merge (aka only valid if \'--merge [MERGED_FILE]\' is set).')

##  merge individual (hourly) files
parser.add_argument('-c',
                    '--config-file',
                    action='store',
                    required=False,
                    help='If you request forecast grid files, you need credentials to access the data; if you provide a CONFIG_FILE here, the program will try to parse lines: \'TUWIEN_VMF1_USER=\"username\" and TUWIEN_VMF1_PASS=\"mypassword\" \' and use the \"username\"  and \"mypassword\" credentials to access the forecast data center',
                    metavar='CONFIG_FILE',
                    dest='config_file',
                    default=None)

parser.add_argument('-u',
                    '--username',
                    action='store',
                    required=False,
                    help='If you request forecast grid files, you need credentials to access the data; use this username to access the forecast data center. Note: this will overwite any \"username\" value found in the CONFIG_FILE (if you also specify one).',
                    metavar='USERNAME',
                    dest='username',
                    default=None)

parser.add_argument('-p',
                    '--password',
                    action='store',
                    required=False,
                    help='If you request forecast grid files, you need credentials to access the data; use this password to access the forecast data center. Note: this will overwite any \"password\" value found in the CONFIG_FILE (if you also specify one). Note that if you have special characters in the password string (e.g. \"!\") it\'d be better to enclose the password string in singe quotes (e.g. -p \'my!pass\').',
                    metavar='PASSWORD',
                    dest='password',
                    default=None)

parser.add_argument('--verbose',
                    dest='verbose',
                    action='store_true',
                    help='Trigger verbose run (prints debug messages).')

if __name__ == '__main__':

    args = parser.parse_args()
    
    ## verbose print
    verboseprint = print if args.verbose else lambda *a, **k: None

    if args.hour and (args.hour > 23 or args.hour < 0):
        print('[ERROR] Invalid hour given (0<hour<24)', file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(args.output_dir):
        print('[ERROR] Invaild output dir given!', file=sys.stderr)
        sys.exit(1)

    ## Resolve the date from input args.
    dt = datetime.datetime.strptime('{:} {:03d}'.format(args.year, args.doy),
                                    '%Y %j')

    ## Where are we going to store local files?
    save_dir = args.output_dir if args.output_dir is not None else os.getcwd()
    if not os.path.isdir(save_dir):
        print('[ERROR] Failed to find requested directory \'{:}\''.format(save_dir), file=sys.stderr)
        sys.exit(5)

    ## Generic format of grid files is: VMFG_YYYYMMDD.H00; make a list with the
    ## (remote) grid files we want.
    if args.hour:
        hours_ext = ['{:02d}'.format((args.hour // 6) * 6)]
    else:
        hours_ext = ['{:02d}'.format(h) for h in [0, 6, 12, 18]]
    grid_files_remote = [
        'VMFG_{:}.H{:}'.format(dt.strftime('%Y%m%d'), hstr)
        for hstr in hours_ext
    ]

    ## Make a dictionary to signal the download status for each file, aka
    ## something like {...'VMFG_YYYYMMDD.H00':{'op':0/1, 'fc':0/1, 'fn':foo}...}
    ## where 'op' is the status of the final download (0 if final product could 
    ## not be found/downloaded or 1 if the downloading was sucesseful), 'fc' is
    ## is the status of the forecast download (accordingly to 'op') and 'fn' is
    ## the local filename of the downloaded file.
    grid_files_dict = {}
    for i in grid_files_remote:
        grid_files_dict[i] = {'op': 0, 'fc': 0}
    
    ## Try downloading first for final products. If we can also try for the 
    ## forecast products, do not exit if download fails.
    verboseprint('Trying to download final grid files.')
    for fn in grid_files_remote:
        if dt < datetime.datetime.now():
            try:
              status, target, saveas = http_retrieve(final_dir(dt), fn, save_dir=save_dir, fail_error=(not args.allow_fc))
              if not status:
                  grid_files_dict[fn]['op'] = 1
                  grid_files_dict[fn]['fn'] = saveas
                  verboseprint('\tFinal VMF1 grid file {:} downloaded and saved to {:}'.format(fn, saveas))
              else:
                  verboseprint('\tFailed downloading final VMF1 grid file {:}'.format(fn))
            except Exception as e:
                remove_local(grid_files_dict)
                print('{:}'.format(e), file=sys.stderr)
                print('[ERROR] Aborting!', file=sys.stderr)
                sys.exit(1)
    
    ## If forecast allowed and date is close to the current, try downloading
    ## forecast files. If we fail, exit. Of course we need to have credentials
    ## for that!
    ## We are only trying for forecast if:
    ## 1. we haven't already downloaded everything,
    ## 2. forecast files are allowed (via --allow-forecast)
    ## 3. date requested is less than 2 days from today
    if not downloading_complete(grid_files_dict, 'op') and args.allow_fc and (datetime.datetime.now().date() - dt.date()).days < 2:
        verboseprint('Trying to download forecast grid files.')
        try:
            user, passwd = get_credentials_from_args(vars(args))
        except Exception as e:
            remove_local(grid_files_dict)
            print('{:}'.format(e), file=sys.stderr)
            print('[ERROR] Aborting!', file=sys.stderr)
            sys.exit(1)
        for fn in grid_files_remote:
            if not grid_files_dict[fn]['op'] and (datetime.datetime.now().date() -
                                                dt.date()).days < 2:
                try:
                    status, target, saveas = http_retrieve(forecast_dir(dt),
                                                        fn,
                                                        save_dir=save_dir,
                                                        username=user,
                                                        password=passwd)
                    if not status:
                        grid_files_dict[fn]['fc'] = 1
                        grid_files_dict[fn]['fn'] = saveas
                        verboseprint('\tForecast VMF1 grid file {:} downloaded and saved to {:}'.format(fn, saveas))
                    else:
                        verboseprint('\tFailed downloading forecast VMF1 grid file {:}'.format(fn))
                except Exception as e:
                    remove_local(grid_files_dict)
                    print('{:}'.format(e), file=sys.stderr)
                    print('[ERROR] Aborting!', file=sys.stderr)
                    sys.exit(1)

    ## Done downloading; if we don't have everything, delete what we downloaded
    ## and exit. Aka, a final check.
    for fn, status in grid_files_dict.items():
        if status['op'] + status['fc'] < 1 or not os.path.isfile(status['fn']):
            print('[ERROR] Failed to download grid file: {:}'.format(fn), file=sys.stderr)
            remove_local(grid_files_dict)
            sys.exit(2)

    ## Merge individual grid files if needed.
    if args.merge_to:
        fn2merge = sorted([ status['fn'] for _, status in grid_files_dict.items() ])
        with open(args.merge_to, 'w') as fout:
            for fn in fn2merge:
                with open(fn, 'r') as fin:
                    copyfileobj(fin, fout)
        if args.del_after_merge:
            remove_local(grid_files_dict)
