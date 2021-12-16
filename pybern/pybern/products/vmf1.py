#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import datetime
from shutil import copyfileobj
from pybern.products.downloaders.retrieve import http_retrieve
from pybern.products.fileutils.keyholders import parse_key_file

## https://vmf.geo.tuwien.ac.at/trop_products/GRID/2.5x2/VMF1/VMF1_OP/2021/
TUW_URL = 'https://vmf.geo.tuwien.ac.at'
OP_URL_DIR = '/trop_products/GRID/2.5x2/VMF1/VMF1_OP'
FC_URL_DIR = '/trop_products/GRID/2.5x2/VMF1/VMF1_FC'

## verbosity level
g_verbose_getvmf1 = False

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


#if __name__ == '__main__':
def main(**kwargs):
    """ Drive the get_vmf1_grd script
        For a full list of command line options (or **kwargs) see the
        rnxdwnl script in the bin/ folder
    """

    ## verbose global verbosity level
    g_verbose_getvmf1 = kwargs['verbose']
    ## verbose print
    verboseprint = print if kwargs['verbose'] else lambda *a, **k: None

    if 'hour' in kwargs and (kwargs['hour'] > 23 or kwargs['hour'] < 0):
        msg = '[ERROR] Invalid hour given (0<hour<24)'
        raise RuntimeError(msg)

    if 'output_dir' not in kwargs:
        kwargs['output_dir'] = os.getcwd()
    if not os.path.isdir(kwargs['output_dir']):
        msg = '[ERROR] Invaild output dir given!'
        raise RuntimeError(msg)

    ## do we allow forecast products ?
    if 'allow_fc' not in kwargs: kwargs['allow_fc'] = False

    ## Resolve the date from input args.
    if 'year' not in kwargs or 'doy' not in kwargs:
        msg = '[ERROR] Need to provide year/doy parameters!'
        raise RuntimeError(msg)

    dt = datetime.datetime.strptime('{:} {:03d}'.format(kwargs['year'], kwargs['doy']),
                                    '%Y %j')

    ## Where are we going to store local files?
    save_dir = kwargs['output_dir']

    ## should we merge files ?
    if 'merge_to' not in kwargs: kwargs['merge_to'] = None

    ## should we delete individual files after merge ?
    if 'del_after_merge' not in kwargs: kwargs['del_after_merge'] = True

    ## Generic format of grid files is: VMFG_YYYYMMDD.H00; make a list with the
    ## (remote) grid files we want.
    if 'hour' in kwargs:
        hours_ext = ['{:02d}'.format((int(kwargs['hour']) // 6) * 6)]
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
        throw = False
        if dt < datetime.datetime.now():
            try:
              status, target, saveas = http_retrieve(final_dir(dt), fn, save_dir=save_dir, fail_error=(not kwargs['allow_fc']))
              if not status:
                  grid_files_dict[fn]['op'] = 1
                  grid_files_dict[fn]['fn'] = saveas
                  verboseprint('\tFinal VMF1 grid file {:} downloaded and saved to {:}'.format(fn, saveas))
              else:
                  verboseprint('\tFailed downloading final VMF1 grid file {:}'.format(fn))
            except Exception as e:
                remove_local(grid_files_dict)
                msg = '[ERROR] Aborting because: {:}'.format(e)
                throw = True
            
            if throw: raise RuntimeError(msg)

    
    ## If forecast allowed and date is close to the current, try downloading
    ## forecast files. If we fail, exit. Of course we need to have credentials
    ## for that!
    ## We are only trying for forecast if:
    ## 1. we haven't already downloaded everything,
    ## 2. forecast files are allowed (via --allow-forecast)
    ## 3. date requested is less than 2 days from today
    if not downloading_complete(grid_files_dict, 'op') and kwargs['allow_fc'] and (datetime.datetime.now().date() - dt.date()).days < 2:
        verboseprint('Trying to download forecast grid files.')
        user, passwd = get_credentials_from_args(vars(args))
        for fn in grid_files_remote:
            if not grid_files_dict[fn]['op'] and (datetime.datetime.now().date() -
                                                dt.date()).days < 2:
                throw = False
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
                    msg = '[ERROR] Aborting! because {:}'.format(e)
                    throw = True
                
                if throw: raise RuntimeError(msg)

    ## Done downloading; if we don't have everything, delete what we downloaded
    ## and exit. Aka, a final check.
    for fn, status in grid_files_dict.items():
        if status['op'] + status['fc'] < 1 or not os.path.isfile(status['fn']):
            msg = '[ERROR] Failed to download grid file: {:}'.format(fn)
            print(msg, file=sys.stderr)
            remove_local(grid_files_dict)
            raise RuntimeError(msg)

    ## Merge individual grid files if needed.
    if kwargs['merge_to']:
        fn2merge = sorted([ status['fn'] for _, status in grid_files_dict.items() ])
        with open(kwargs['merge_to'], 'w') as fout:
            for fn in fn2merge:
                with open(fn, 'r') as fin:
                    copyfileobj(fin, fout)
        if kwargs['del_after_merge']:
            remove_local(grid_files_dict)
    
    ## return a dictionary with info
    return grid_files_dict
