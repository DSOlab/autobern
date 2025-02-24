#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import re
import argparse
import subprocess
import datetime
from time import sleep as psleep
import atexit
import getpass
from shutil import copyfile
import smtplib, ssl
import pybern.products.rnxdwnl_impl as rnxd
import pybern.products.fileutils.decompress as dcomp
import pybern.products.fileutils.compress as comp
import pybern.products.uploaders.uploaders as upld
from pybern.products.fileutils.keyholders import parse_key_file
from pybern.products.gnssdb_query import parse_db_credentials_file, query_sta_in_net, query_tsupd_net
from pybern.products.codesp3 import get_sp3
from pybern.products.codeerp import get_erp
from pybern.products.codeion import get_ion
from pybern.products.codedcb import get_dcb
from pybern.products.euref.utils import get_euref_exclusion_list
from pybern.products.bernparsers.bern_crd_parser import parse_bern52_crd
from pybern.products.gnssdates.gnssdates import pydt2gps, sow2dow
from pybern.products.utils.dctutils import merge_dicts
import pybern.products.bernparsers.bern_out_parse as bparse
import pybern.products.bernparsers.bern_addneq_parser as baddneq
import pybern.products.bernparsers.bernsta as bsta
import pybern.products.bernparsers.bernpcf as bpcf
import pybern.products.vmf1 as vmf1
import pybern.products.bernbpe as bpe
import pybern.products.atx2pcv as a2p
from pybern.products.formats.rinex import Rinex

VERSION='1.0-beta'

## path to crx2rnx program
crx2rnx_dir='/home/bpe/applications/RNXCMP_4.0.6_Linux_x86_64bit/bin/'
if not os.path.isdir(crx2rnx_dir):
    print('[ERROR] Invalid crx2rnx bin dir {:}'.format(crx2rnx_dir), file=sys.stderr)
    sys.exit(1)

## path to log files
log_dir='/home/bpe/data/proclog'
if not os.path.isdir(log_dir):
    print('[ERROR] Invalid temp/proc dir {:}'.format(log_dir), file=sys.stderr)
    sys.exit(1)

## list of temporary files created during program run that beed to be deleted
## before exit
temp_files = []

def update_temp_files(new_fn, old_fn=None):
    """ If (file) 'old_fn' exists in (global) temp_files list, replace it with
        new_fn.
        If 'old_fn' is not listed in temp_files list, just add new_fn to
        temp_files
    """
    index = -1
    if old_fn is not None:
        try:
            index = temp_files.index(old_fn)
        except:
            index = -1
    if index < 0:
        temp_files.append(new_fn)
    else:
        temp_files[index] = new_fn

def cleanup(verbosity=False):
    """ Remove every file listed in the tmp_files list; if any operation fails,
        the program will not thrrow.
    """
    verboseprint = print if int(verbosity) else lambda *a, **k: None

    for f in temp_files:
        try:
            #verboseprint('[DEBUG] Removing temporary file {:} atexit ...'.format(f), end='')
            os.remove(f)
            #verboseprint(' done')
        except:
            #verboseprint(' failed')
            pass
    return

def rmbpetmp(campaign_dir, dt, bpe_start, bpe_stop):
    """ This function will perform two operations:
        1. remove all files in the campaign's RAW directory, that match the
           patterns '[A-Z0-9]{4}DDD0.SMT' and '[A-Z0-9]{4}DDD0.[dDoO]'
        2. remove all files in the campaign's directories, that have last
           modification time tag between bpe_start and bpe_stop (aka remove
           all files in the campaign's directories that have been
           created/modified by the BPE run)
    """
    doy_str = dt.strftime('%j')
    yy_str = dt.strftime('%y')
    raw_dir = os.path.join(campaign_dir, 'RAW')

    for fn in os.listdir(raw_dir):
        if re.match(r"[A-Z0-9]{4}"+doy_str+r"0\.SMT", fn):
            os.remove(os.path.join(raw_dir, fn))
        elif re.match(r"[A-Z0-9]{4}"+doy_str+r"0\." + yy_str + r"[oOdD]", fn):
            os.remove(os.path.join(raw_dir, fn))

    for (dirpath, dirnames, filenames) in os.walk(campaign_dir):
        for filename in filenames:
            f = os.path.join(dirpath, filename)
            try:
                mtime = datetime.datetime.fromtimestamp(os.stat(f).st_mtime, tz=datetime.timezone.utc)
                if mtime>=bpe_start and mtime <=bpe_stop:
                    #verboseprint('[DEBUG] Removing temporary file {:} rmbpetmp ...'.format(f))
                    os.remove(f)
            except:
                pass

## callback function to be called at exit
atexit.register(cleanup, True)

def match_rnx_vs_sta(rinex_holdings, stafn, dt):
    """ Make sure that every station in rinex_holdings has a valid recdor for
        dt epoch in the .STA file stafn. If not, return an integer > 0.
    """
    sta = bsta.BernSta(stafn)
    binfo = sta.parse().filter([s[0:4].upper() for s in rinex_holdings ], True)

    for station in rinex_holdings:
        stainf = binfo.station_info(station.upper(), True)
        if stainf is None:
            print('[ERROR] Failed to find Type 002 entry for station {:} (file: {:})'.format(station.upper(), stafn))
            return 1
        matched = False
        for t2entry in stainf['type002']:
            domes = t2entry.sta_name[5:] if len(t2entry.sta_name)>4 else ''
            if t2entry.start_date <= dt and t2entry.stop_date >= dt:
                matched = True
                break
        if not matched:
            print('[ERROR] No valid entry found in STA file {:} for station {:} and date {:}'.format(stafn, station, dt.strftime('%Y%m%d %H:%M:%S'), file=sys.stderr))
            return 1

        #rinex_holdings[station]['domes'] = domes

    return 0;

def mark_exclude_stations(station_list, rinex_holdings):
    """ Given an exclusion list 'station_list' (aka a list of stations specified
        by their 4char-id), set the field rinex_holdings[station]['exclude']
        to true if the station is included in the station_list
    """
    exclusion_list = [x.lower() for x in station_list]
    for station in rinex_holdings:
        if station.lower() in station_list:
            rinex_holdings[station]['exclude'] = True
            print('[DEBUG] Marking station {:} as excluded! will not be processed.'.format(station))

def products2dirs(product_dict, campaign_dir, dt, add2temp_files=True):
    """ Transfer (link) downloaded products from their current folder to the
        campaign-specific folders. The product filenames are collected from the
        'product_dict' dictionary (e.g. using the product_dict['sp3']['local']
        key/value pair). More specifically:
        sp3: product_dict['sp3']['local'] -> $P/ORB and change extension to
             .PRE if needed
        erp: product_dict['erp']['local'] -> $P/ORB
        ion: product_dict['ion']['local'] -> $P/ATM
        dcb: product_dict['dcb']['local'] -> $P/ORB and change filename to
             'P1C1YYMM.DCB'
        vmf1: product_dict['vmf1']['local'] -> $P/GRD and change filename to
             'VMFYYDDD0.GRD'
    """
    gweek, gsow = pydt2gps(dt)
    gdow = sow2dow(gsow)

    rules_d = {'sp3': {'target_dir': 'ORB', 'target_fn': 'COD{:}{:}.PRE'.format(gweek,  gdow)},
        'erp': {'target_dir': 'ORB', 'target_fn': 'COD{:}{:}.ERP'.format(gweek,  gdow)},
        'ion': {'target_dir': 'ATM', 'target_fn': 'COD{:}{:}.ION'.format(gweek,  gdow)},
        'dcb': {'target_dir': 'ORB', 'target_fn': 'P1C1{:}.DCB'.format(dt.strftime('%y%m'))},
        'vmf1': {'target_dir': 'GRD', 'target_fn': 'VMF{:}0.GRD'.format(dt.strftime('%y%j'))}}

    for ptype, rules in rules_d.items():
        ## original downloaded product
        source = product_dict[ptype]['local']
        ## decompress if needed
        _, source = dcomp.os_decompress(source, True)
        ## rename rulues
        target = os.path.join(campaign_dir, rules['target_dir'], rules['target_fn'])
        ## mv ...
        os.rename(source, target)
        ## update 'local' field in dictionary
        product_dict[ptype]['local'] = target
        ## replace/append in temp_files list
        if add2temp_files: update_temp_files(target, source)

def prepare_products(dt, credentials_file, product_dict={}, product_dir=None, verbose=False, add2temp_files=True):
    """ Download products for date 'dt', using the credentials file
        'credentials_file', to the directory 'product_dir' and if needed, add
        them to temp_files list. The function will also decompress the
        downloaded files (if needed).

        Return: dictionary, success

        Returns a dictionary holding information for each product, e.g.
        return product_dict, where:
        product_dict['sp3'] = {'remote': remote, 'local': local, 'type': orbtype}
        product_dict['ion'] = {'remote': remote, 'local': local, 'type': iontype}

        and a boolean varibale to deonte if all products have been successefuly
        handled (aka True denotes success, False error)
        ...
    """
    ## write product information to a dictionary
    # product_dict = {}

    if product_dir is None: product_dir = os.getcwd()

    ## download sp3
    if 'sp3' not in product_dict:
        ptypes = ['final', 'final-rapid', 'early-rapid', 'ultra-rapid', 'current']
        for count,orbtype in enumerate(ptypes):
            try:
                status, remote, local = get_sp3(type=orbtype, pydt=dt, save_dir=product_dir)
                verboseprint('[DEBUG] Downloaded orbit file {:} of type {:} ({:})'.format(local, orbtype, status))
                product_dict['sp3'] = {'remote': remote, 'local': local, 'type': orbtype}
                break
            except:
                verboseprint('[DEBUG] Failed downloading sp3 file of type {:}'.format(orbtype))
                if count != len(ptypes) - 1:
                    verboseprint('[DEBUG] Next try for file of type {:}'.format(ptypes[count+1]))

    ## download erp
    if 'erp' not in product_dict:
        ptypes = ['final', 'final-rapid', 'early-rapid', 'ultra-rapid', 'current']
        for count,erptype in enumerate(ptypes):
            try:
                status, remote, local = get_erp(type=erptype, pydt=dt, span='weekly', save_dir=product_dir, code_dir='bswuser52')
                verboseprint('[DEBUG] Downloaded erp file {:} of type {:} ({:})'.format(local, erptype, status))
                product_dict['erp'] = {'remote': remote, 'local': local, 'type': erptype}
                break
            except:
                verboseprint('[DEBUG] Failed downloading erp file of type {:}'.format(erptype))
                if count != len(ptypes) - 1:
                    verboseprint('[DEBUG] Next try for file of type {:}'.format(ptypes[count+1]))

    ## download ion
    if 'ion' not in product_dict:
        ptypes = ['final', 'rapid', 'urapid', 'current']
        for count,iontype in enumerate(ptypes):
            try:
                status, remote, local = get_ion(type=iontype, pydt=dt, save_dir=product_dir)
                verboseprint('[DEBUG] Downloaded ion file {:} of type {:} ({:})'.format(local, iontype, status))
                product_dict['ion'] = {'remote': remote, 'local': local, 'type': iontype}
                break
            except:
                verboseprint('[DEBUG] Failed downloading ion file of type {:}'.format(iontype))
                if count != len(ptypes) - 1:
                    verboseprint('[DEBUG] Next try for file of type {:}'.format(ptypes[count+1]))

    ## download dcb
    if 'dcb' not in product_dict:
        days_dif = (datetime.datetime.now() - dt).days
        if days_dif > 0 and days_dif < 30:
            for i in range(3):
                try:
                    status, remote, local = get_dcb(type='current', obs='full', save_dir=product_dir)
                    product_dict['dcb'] = {'remote': remote, 'local': local, 'type': 'full'}
                    verboseprint('[DEBUG] Downloaded dcb file {:} of type {:} ({:})'.format(local, 'current', status))
                    break
                except:
                    verboseprint('[DEBUG] Failed downloading dcb file of type {:}'.format('current'), end='')
                    if i<2:
                        verboseprint(' retrying ...')
                    else:
                        verboseprint(' giving up...')
                    psleep(60)
        elif days_dif >= 30:
                status, remote, local = get_dcb(type='final', pydt=dt, obs='p1p2all', save_dir=product_dir)
                product_dict['dcb'] = {'remote': remote, 'local': local, 'type': 'p1p2all'}
        else:
            print('[ERROR] Don\'t know what DCB product to download!')
            raise RuntimeError

    ## if we failed throw, else decompress. Go in here only if all products
    ## are available (in the dict)
    for product in ['sp3', 'erp', 'ion', 'dcb']:
        if product not in product_dict:
            print('[ERROR] Failed to download (any) {:} file! Giving up current try'.format(product), file=sys.stderr)
            # raise RuntimeError
            return product_dict, False
        else:
            lfile = product_dict[product]['local']
            if lfile.endswith('.Z') or lfile.endswith('.gz'):
                c, d = dcomp.os_decompress(lfile, True)
                product_dict[product]['local'] = d

    ## download vmf1 grid
    idoy = int(dt.strftime('%j').lstrip('0'))
    iyear = int(dt.strftime('%Y'))
    merge_to = os.path.join(product_dir, 'VMFG_{:}.GRD'.format(dt.strftime('%Y%m%d')))
    vmf1_dict = vmf1.main(**{
        'year': iyear,
        'doy': idoy,
        'output_dir': product_dir,
        'config_file': credentials_file,
        'verbose': verbose,
        'merge_to': merge_to,
        'allow_fc': True,
        'del_after_merge': True
        })
    has_forecast = False
    for fn in vmf1_dict:
        if vmf1_dict[fn]['fc'] != 0:
            has_forecast = True
    product_dict['vmf1'] = {'local': merge_to, 'remote': None, 'type': 'forecast' if has_forecast else 'final' }

    if add2temp_files:
        for k,dct in product_dict.items():
            update_temp_files(dct['local'])

    return product_dict, True

def rinex3to2_mv(rinex_holdings, campaign_name, dt, add2temp_files=True):
    """ Rename any RINEX v3.x file found in the rinex_holdings dictionary, to
        a corresponding RINEX v2.x name, in the campaign's RAW/ directory.
        The function will examine all (sub)dictionaries included in the
        rinex_holdings dictionary (aka, rinex_holdings[station]['local'] values)
        if the station is not marked as 'excluded' (aka
        rinex_holdings[station]['exclude'] is set to True). If the 'local' file
        matches a RINEX v3.x pattern, it will be renamed to a corresponding
        RINEX v2.x filename and if needed moved to the campaign's RAW/
        directory.

        The station will return a copy of 'rinex_holdings', updated where
        needed with the new 'local' filename.

        Note: expects rinex_holding to be:
        { 'dyng': {'local':'/foo/bar/DYNG00GRC_...', 'exclude': False, ...} }
    """
    raw = os.path.join(os.getenv('P'), campaign_name.upper(), 'RAW')
    new_holdings = {}

    for station, dct in rinex_holdings.items():
        new_holdings[station] = rinex_holdings[station]
        if dct['local'] is not None and not dct['exclude']:
            # HERS00GBR_R_20200250000_01D_30S_MO.RNX
            rnx3_name = os.path.basename(dct['local'])
            if rnx3_name[-4:] == ".RNX":
                rnx2_name = rnx3_name[0:4] + '{:}0.{:}O'.format(dt.strftime('%j'), dt.strftime('%y'))
                os.rename(os.path.join(raw, rnx3_name), os.path.join(raw, rnx2_name))
                print('[DEBUG] Renamed {:} to {:}'.format(rnx3_name, os.path.join(raw, rnx2_name)))
                new_holdings[station]['local'] = os.path.join(raw, rnx2_name)
                if add2temp_files: update_temp_files(new_holdings[station]['local'], dct['local'])
    return new_holdings

def rinex3to2_link(rinex_holdings, campaign_name, dt, add2temp_files=True):
    raw = os.path.join(os.getenv('P'), campaign_name.upper(), 'RAW')
    new_holdings = {}

    for station, dct in rinex_holdings.items():
        new_holdings[station] = rinex_holdings[station]
        if dct['local'] is not None and not dct['exclude']:
            # HERS00GBR_R_20200250000_01D_30S_MO.RNX
            rnx3_name = os.path.basename(dct['local'])
            if rnx3_name[-4:] == ".RNX":
                rnx2_name = rnx3_name[0:4] + '{:}0.{:}O'.format(dt.strftime('%j'), dt.strftime('%y'))
                if os.path.isfile(os.path.join(raw, rnx2_name)):
                    os.remove(os.path.join(raw, rnx2_name))
                os.symlink(os.path.join(raw, rnx3_name), os.path.join(raw, rnx2_name))
                print('[DEBUG] Linked {:} to {:}'.format(rnx3_name, os.path.join(raw, rnx2_name)))
                new_holdings[station]['local'] = os.path.join(raw, rnx2_name)
                if add2temp_files: update_temp_files(new_holdings[station]['local'])
    return new_holdings

def rinex2raw(rinex_holdings, campaign_name, cp_not_mv=False, add2temp_files=True):
    """ Move RINEX files (included in rinex_holdings) to the campaign's RAW/
        directory, if the station is not marked as 'excluded'.
        The station will return a copy of 'rinex_holdings', updated where
        needed with the new 'local' filename.

        Note: expects rinex_holding to be:
        { 'dyng': {'local':'/foo/bar/DYNG00GRC_...', 'exclude': False, ...} }
    """
    raw = os.path.join(os.getenv('P'), campaign_name.upper(), 'RAW')
    new_holdings = {}

    for station, dct in rinex_holdings.items():
        if dct['local'] is not None and not dct['exclude']:
            fn = os.path.basename(dct['local'])
            pth = os.path.dirname(dct['local'])
            if cp_not_mv:
                copyfile(dct['local'], os.path.join(raw, fn))
            else:
                os.rename(dct['local'], os.path.join(raw, fn))
            new_holdings[station] = rinex_holdings[station]
            new_holdings[station]['local'] = os.path.join(raw, fn)

            if add2temp_files: update_temp_files(new_holdings[station]['local'], dct['local'])

        else:
            new_holdings[station] = rinex_holdings[station]
    return new_holdings

def rinex2uppercase(rinex_holdings, add2temp_files=True):
    """ Translate RINEX files (included in rinex_holdings) to uppercase
        filenames, if the station is not marked as 'excluded'.
        The station will return a copy of 'rinex_holdings', updated where
        needed with the new 'local' filename.

        Note: expects rinex_holding to be:
        { 'dyng': {'local':'/foo/bar/DYNG00GRC_...', 'exclude': False, ...} }
    """
    new_holdings = {}
    for station, dct in rinex_holdings.items():
        if dct['local'] is not None and not dct['exclude']:
            fn = os.path.basename(dct['local'])
            pth = os.path.dirname(dct['local'])
            fnu = fn.upper()
            os.rename(dct['local'], os.path.join(pth, fnu))
            new_holdings[station] = rinex_holdings[station]
            new_holdings[station]['local'] = os.path.join(pth, fnu)
            if add2temp_files: update_temp_files(new_holdings[station]['local'], dct['local'])
        else:
            new_holdings[station] = rinex_holdings[station]
    return new_holdings

def rename_rinex_markers(rinex_holdings, netsta_dct):
    """ In case of a databse incosistency, aka mark_name_OFF != mark_name_DSO
        update the 'MARKER NAME' field within the RINEX file(s) to match
        mark_name_DSO.
        Rinex files should be decompressed!
        Note, netsta_dct =
        [{'station_id': 1, 'mark_name_DSO': 'pdel', 'mark_name_OFF': 'pdel',..},{...}]
    """
    for dct in netsta_dct:
        if dct['mark_name_DSO'].upper() != dct['mark_name_OFF'].upper():
            if dct['mark_name_DSO'] in rinex_holdings:
                print('[NOTE ] Changing marker name of station {:}/{:} to match DSO name'.format(dct['mark_name_DSO'], dct['mark_name_OFF']))
                rnx = Rinex(rinex_holdings[dct['mark_name_DSO']]['local'])
                if not rnx.updateMarkerName(dct['mark_name_DSO'].upper()):
                    msg = '[ERROR] Failed to change \'MARKER NAME\' for station {:}, RINEX: {:}'.format(dct['mark_name_DSO'], rinex_holdings[dct['mark_name_DSO']]['local'])
                    raise RuntimeError(msg)
    return rinex_holdings


def decompress_rinex(rinex_holdings):
    """ rinex_holdings = {'pdel': {
        'local': '/home/bpe/applications/autobern/bin/pdel0250.16d.Z',
        'remote': 'https://cddis.nasa.gov/archive/gnss/data/daily/2016/025/16d/pdel0250.16d.Z'},
        'hofn': {...}}
        The retuned dictionary is a copy of the input one, but the names of the
        'local' rinex have been changed to the uncompressed filenames
    """
    def crx2rnx(crnx, station, new_holdings):
        ## Note that some files (e.g. Metrica's rinex3 may be .zip, observation
        ## RINEX, aka, do not need to be processed by CRX2RNX!
        if crnx.endswith('o') or crnx.endswith('O'):
            print('[NOTE ] Rinex file {:} seems to not be Hatanaka-compressed; skipping CRX2RNX call ...'.format(crnx))
            new_holdings[station]['local'] = crnx
            return

        ## decompress from Hatanaka; in rare cases, this may fail
        ## e.g. ERROR : The file seems to be truncated in the middle.
        try:
            crnx, drnx = dcomp.crx2rnx(crnx, True, crx2rnx_dir)
            # new_holdings[station] = rinex_holdings[station]
            new_holdings[station]['local'] = drnx
            update_temp_files(drnx, crnx)
        except:
            print('[WRNNG] CRX2RNX failed for RINEX file/station {:} ({:}); marking the RINEX/station as excluded'.format(crnx,station), file=sys.stderr)
            new_holdings[station]['local'] = None
            new_holdings[station]['exclude'] = 'CRX2RNX Error'

    new_holdings = {}
    for station, dct in rinex_holdings.items():
        if dct['local'] is not None and not dct['exclude']:
            crnx = dct['local']
            if not os.path.isfile(crnx):
                print('[ERROR] Failed to find downloaded RINEX file {:}'.format(crnx), file=sys.stderr)
                raise RuntimeError

            ## decompress to ascii (hatanaka compressed)
            if crnx.endswith('.Z') or crnx.endswith('.gz') or crnx.endswith('.zip'):
                cr = None
                try:
                    cr, drnx = dcomp.os_decompress(crnx, True)
                except:
                    print('[WRNNG] Failed to decompress RINEX file {:}'.format(crnx), file=sys.stderr)
                    print('[WRNNG] Note that the RINEX file {:} will be deleted from rinex_holdings and removed'.format(crnx), file=sys.stderr)
                    os.remove(crnx)
                    dct['local'] = None

                if cr is not None: ## file decompressed ...
                    assert(os.path.isfile(drnx))
                    new_holdings[station] = rinex_holdings[station]
                    crx2rnx(drnx, station, new_holdings)

            elif crnx.endswith('d') or crnx.endswith('crx'):
                ## else if hatanaka compressed
                new_holdings[station] = rinex_holdings[station]
                crx2rnx(crnx, station, new_holdings)

            else:
                new_holdings[station] = dct
    return new_holdings

def atx2pcv(options, dt, tmp_file_list=None):
    atxinf = options['atxinf'].upper()
    if atxinf[-4:] != '.ATX': atxinf += '.ATX'
    stainf = options['stainf'].upper()
    if stainf[-4:] != '.STA': stainf = stainf[0:-4]
    phginf = atxinf[0:-4]

    ## Set variables in PCF file
    pcf_file = os.path.join(os.getenv('U'), 'PCF', 'ATX2PCV.PCF')
    if not os.path.isfile(pcf_file):
        print('[ERROR] Failed to find PCF file {:}'.format(pcf_file), file=sys.stderr)
        sys.exit(1)

    pcf = bpcf.PcfFile(pcf_file)
    for var, value in zip(['ATXINF', 'PCVINF', 'STAINF', 'PHGINF', 'PCV'],[atxinf, '', stainf, phginf, options['pcvext'].upper()]):
        pcf.set_variable('V_'+var, value, 'rundd {}'.format(datetime.datetime.now().strftime('%Y%m%dT%H%M%S')))
    pcf.dump(os.path.join(os.getenv('U'), 'PCF', 'A2P_DD.PCF'))
    pcf_file = os.path.join(os.getenv('U'), 'PCF', 'A2P_DD.PCF')

    bern_task_id = options['campaign'].upper()[0] + 'A2P'
    bern_log_fn = os.path.join(log_dir, '{:}-{:}{:}.log'.format(options['campaign'], bern_task_id, dt.strftime('%y%j')))
    print('[DEBUG] Started ATX2PCV conversion (log: {:})'.format(bern_log_fn))
    with open(bern_log_fn, 'w') as logf:
        addtopath_load(options['b_loadgps'])
        subprocess.call(['{:}'.format(os.path.join(os.getenv('U'), 'SCRIPT', 'ntua_a2p.pl')), '{:}'.format(dt.strftime('%Y')), '{:}0'.format(dt.strftime('%j')), '{:}'.format(options['campaign'].upper())], stdout=logf, stderr=logf)

    bpe_status_file = os.path.join(os.getenv('P'), options['campaign'].upper(), 'BPE', 'ATX2PCV.RUN')
    if bpe.check_bpe_status(bpe_status_file)['error'] == 'error':
        errlog = os.path.join(os.getenv('P'), options['campaign'].upper(), 'BPE', 'bpe_a2p_error_{}.log'.format(os.getpid()))
        print('[ERROR] ATX2PCV failed due to error! see log file {:}'.format(errlog), file=sys.stderr)
        bpe.compile_error_report(bpe_status_file, os.path.join(os.getenv('P'), options['campaign'].upper()), errlog)

def translate_sta_indv_calibrations(options):
    """ Translate the .STA file options['stainf'], to a new .STA file located
        in the campaign's STA folder, and named
        'G'+ options['stainf'].upper() + '.STA'
        where all antenna SN numbers & strings are translated to the generic
        value 99999
    """
    print('[WRNNG] Translating all non-generic antenna SN\'s to generic value; new .STA file is: ', end='')
    TDIR = os.path.abspath(options['tables_dir'])
    sta = os.path.join(TDIR, 'sta', options['stainf'].upper()+'.STA')
    if not os.path.isfile(sta):
        sta = os.path.join(os.getenv('P'), options['campaign'].upper(), 'STA', options['stainf'].upper()+'.STA')
        if not os.path.isfile(sta):
            errmsg = '[ERROR] Failed to find .STA file {:} in either {:} or {:}'.format(options['stainf'].upper()+'.STA', os.path.join(TDIR, 'sta'), os.path.join(os.getenv('P'), options['campaign'].upper(), 'STA'))
            raise RuntimeError(errmsg)
    new_sta_fn = 'G' + options['stainf']
    new_sta = os.path.join(os.getenv('P'), options['campaign'].upper(), 'STA', new_sta_fn.upper()+'.STA')
    print('{:}'.format(new_sta))
    ## parse the station information file
    stainf = bsta.BernSta(sta).parse()
    ## translate all non-generic antenna serials to generic (aka 999999)
    stainf.antennas2generic()
    ## dump the new station information file
    stainf.dump_as_sta(new_sta)
    return new_sta_fn

def link2campaign(options, dt, add2temp_files=True):
    """ Link needed files from TABLES directory to campaign's corresponsing
        folders
    """
    PDIR = os.path.abspath(os.path.join(os.getenv('P'), options['campaign'].upper()))
    TDIR = os.path.abspath(options['tables_dir'])
    link_dict = []
    ## reference crd/vel/psd/fix files
    src = os.path.join(TDIR, 'crd', options['refinf'].upper()+'_R.CRD')
    dest = os.path.join(PDIR, 'STA', os.path.basename(src))
    link_dict.append({'src': src, 'dest': dest})

    src = os.path.join(TDIR, 'crd', options['refinf'].upper()+'_R.VEL')
    dest = os.path.join(PDIR, 'STA', os.path.basename(src))
    link_dict.append({'src': src, 'dest': dest})

    src = os.path.join(TDIR, 'fix', options['fixinf'].upper()+'.FIX')
    dest = os.path.join(PDIR, 'STA', os.path.basename(src))
    link_dict.append({'src': src, 'dest': dest})

    if options['refpsd'] is not None and options['refpsd'].strip() != '':
        src = os.path.join(TDIR, 'crd', options['refpsd'].upper()+'.PSD')
        dest = os.path.join(PDIR, 'STA', os.path.basename(src))
        link_dict.append({'src': src, 'dest': dest})

    ## regional crd file (linked to REG$YSS+0)
    src = os.path.join(TDIR, 'crd', options['aprinf'].upper()+'.CRD')
    dest = os.path.join(PDIR, 'STA', 'REG{:}0.CRD'.format(dt.strftime("%y%j")))
    link_dict.append({'src': src, 'dest': dest})

    ## sta file
    src = os.path.join(TDIR, 'sta', options['stainf'].upper()+'.STA')
    if not os.path.isfile(src):
        if not os.path.isfile(os.path.join(os.getenv('P'), options['campaign'].upper(), 'STA', options['stainf'].upper()+'.STA')):
            errmsg = '[ERROR] Failed to find .STA file {:} in either {:} or {:}'.format(options['stainf'].upper()+'.STA', os.path.join(TDIR, 'sta'), os.path.join(os.getenv('P'), options['campaign'].upper(), 'STA'))
            raise RuntimeError(errmsg)
    else:
        dest = os.path.join(PDIR, 'STA', os.path.basename(src))
        link_dict.append({'src': src, 'dest': dest})

    ## blq file (if any)
    if options['blqinf'] is not None and options['blqinf'].strip() != '':
        src = os.path.join(TDIR, 'blq', options['blqinf'].upper()+'.BLQ')
        dest = os.path.join(PDIR, 'STA', os.path.basename(src))
        link_dict.append({'src': src, 'dest': dest})

    ## pcv file if at tables/pcv and not in GEN
    pcv_file = '{:}.{:}'.format(options['pcvinf'].upper(), options['pcvext'].upper())
    if not os.path.isfile(os.path.join(os.getenv('X'), 'GEN', pcv_file)):
        pcv_path = os.path.join(TDIR, 'pcv')
        if not os.path.isfile(os.path.join(TDIR, pcv_path, pcv_file)):
            errmsg = '[ERROR] Failed to find PCV file {:} in neither tables dir or GEN!'.format(pcv_file)
            raise RuntimeError(errmsg)
        link_dict.append({'src': os.path.join(TDIR, pcv_path, pcv_file), 'dest': os.path.join(os.getenv('X'), 'GEN', pcv_file)})

    ## link the observation selection file (if not in GEN)
    if 'obssel' in options and options['obssel'] is not None and options['obssel'] != '':
        obssel_fn = options['obssel'].upper() + '.SEL'
        gen_obssel = os.path.join(os.getenv('X'), 'GEN', obssel_fn)
        if not os.path.isfile(gen_obssel):
            tab_obssel = os.path.join(TDIR, 'sel', obssel_fn)
            if not os.path.isfile(tab_obssel):
                errmsg = '[ERROR] Failed to find selection file {:} in either {:} or {:}'.format(obssel_fn, os.path.dirname(gen_obssel), os.path.dirname(tab_obssel))
                raise RuntimeError(msg)
            link_dict.append({'src': tab_obssel, 'dest': gen_obssel})

    for pair in link_dict:
        print('[DEBUG] Linking source {:} to {:}'.format(pair['src'], pair['dest']))
        if os.path.isfile(pair['dest']):
            print('[WRNNG] Removing file {:}; need to make a new link!'.format(pair['dest']), file=sys.stderr)
            os.remove(pair['dest'])
        os.symlink(pair['src'], pair['dest'])
        if add2temp_files: update_temp_files(pair['dest'])

def send_report_mail(options, message_head, message_body):
    """ Send report to recipients via mail.
        We need the following from the options dictionary:
        'send_mail_to',
        'mail_account_password', 'mail_account_username'
        The funcion will use smtp.gmail.com server to send the mail
    """
    recipients_list = options['send_mail_to'].split(',')
    if 'mail_account_password' not in options or 'mail_account_username' not in options:
        print('[ERROR] Failed to send mail! No username/password provided', file=sys.stderr)
    else:
        message = ""
        message += "Subject:{:}\n\n\n".format(message_head)
        message += message_body

        port = 465 # for SSL
        sender_email = options['mail_account_username']
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender_email, options['mail_account_password'])
            server.sendmail(sender_email, recipients_list, message)

def write_ts_record(adnq2_dct, ts_file, station, comment):
    """ station -> full station name (4char-id + domes)
        Update a station-specific cts (aka time-series) file with a new line,
        parsed from the adnq2_dct dictionary (which should be the result of
        parsing the 'final' ADDNEQ2 output file from BPE run)

        The function will loop hrough the 'adnq2_dct' dictionary to match
        records for station 'station'; these records are the ones to be used
        for cts updating.

        The fucntion will return True if the new record is indeed appended to
        the ts_file file, and False otherwise (e.g. failed to match station to
        any record in adnq2_dct)
    """
    for aa, dct in adnq2_dct.items():
        if dct['station_name'].lower() == station.lower():
            tfrom = dct['X_from']
            tto = dct['X_to']
            dt_seconds = int((tto-tfrom).seconds)/2
            t = datetime.timedelta(days=0, seconds=dt_seconds) + tfrom
            with open(ts_file, 'a') as ts_out:
                print('{:} {:+15.5f} {:9.5f} {:+15.5f} {:9.5f} {:+15.5f} {:9.5f} {:+13.8f} {:9.5f} {:+13.8f} {:9.5f} {:12.5f} {:9.5f} {:} {:}'.format(t.strftime("%Y-%m-%d %H:%M:%S"), dct['X_estimated_value'], dct['X_rms_error'], dct['Y_estimated_value'], dct['Y_rms_error'], dct['Z_estimated_value'], dct['Z_rms_error'], dct['Latitude_estimated_value'], dct['Latitude_rms_error'], dct['Longitude_estimated_value'], dct['Longitude_rms_error'], dct['Height_estimated_value'], dct['Height_rms_error'],datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), comment), file=ts_out)
            return True
    return False

def match_ts_file(ts_path, ts_file_pattern, station_id, station_domes):
    ts_file = ts_file_pattern
    ts_file = re.sub(r"\$\{" + "site_id"  + r"\}", station_id.lower(), ts_file)
    ts_file = re.sub(r"\$\{" + "SITE_ID"  + r"\}", station_id.upper(), ts_file)
    ts_file = re.sub(r"\$\{" + "site_domes"  + r"\}", station_domes.lower(), ts_file)
    ts_file = re.sub(r"\$\{" + "SITE_DOMES"  + r"\}", station_domes.upper(), ts_file)
    return os.path.join(ts_path, ts_file)

def update_ts(options, adnq2_fn):
    """ Given a (final) ADDNEQ2 file (result of BPE), update the involved
        stations cts file.
        The function will parse the ADDNEQ2 file and get estimateds and rms
        values for all stations included. It will then query the database to
        see what station cts files should be updated (that is query the
        database, using the network name, to see which stations have the field
        'upd_tssta' set to 1).
        For each of these stations, a new record will be appended in the
        corresponding cts file.

        The function will return a dictionary of stations for which the cts
        files where updated, in the sense:
        {
            'dion 1234M001': '/home/bpe.../dion.cts',
            'noa1 1234M001': '/home/bpe.../noa1.cts', ...
        }
        aka, the key is the site name (siteid+domes as recorded in the
        database) and the value is the corresponding time-series file as
        compiled from the corresponding options variables.

        Keys in options used:
            options['path_to_ts_files']
            options['config_file']
            options['network']
            options['ts_file_name']
    """
    ## path to ts files
    ts_path = options['path_to_ts_files']
    if not os.path.isdir(ts_path):
        print('[ERROR] Failed to located station time-series path {:}'.format(ts_path))
        return

    db_credentials_dct = parse_db_credentials_file(options['config_file'])
    tsupd_dict = query_tsupd_net(options['network'], db_credentials_dct)

    with open(adnq2_fn, 'r') as adnq2:
        adnq2_dct = bparse.parse_generic_out_header(adnq2)
        assert(adnq2_dct['program'] == 'ADDNEQ2')
        adnq2_dct = baddneq.parse_addneq_out(adnq2)
        adnq2_dct = adnq2_dct['stations']

    def station_in_addneq2(station_):
        for aa, dct in adnq2_dct.items():
            if dct['station_name'].lower().strip() == station_.lower().strip():
                return aa
        return None

    stations_updated = {}

    for qdct in tsupd_dict:
        sid = qdct['mark_name_DSO']
        sdm = qdct['mark_numb_OFF']
        station = '{:} {:}'.format(sid, sdm).strip()
        assert(qdct['network_name'].lower() == options['network'].lower())
        assert(qdct['upd_tssta'] == 1)

        ## we are only interested in this station, if it is included in the
        ## ADDNEQ2 output
        if station_in_addneq2(station) is not None:

            # ts_file = os.path.join(options['path_to_ts_files'], sid, '{:}.cts'.format(sid))
            ts_file = match_ts_file(options['path_to_ts_files'], options['ts_file_name'], sid, sdm)
            if not os.path.isfile(ts_file):
                print('[WRNNG] No station cts file found for station {:} (searching for {:})'.format(station, ts_file), file=sys.stderr)
            else:
                comment = options['ts_description'] if 'ts_description' in options else ''
                if not write_ts_record(adnq2_dct, ts_file, station, comment):
                    print('[WRNNG] Failed to update ts record for station {:}'.format(station), file=sys.stderr)
                else:
                    # stations_updated.append(station)
                    stations_updated[station] = ts_file

    return stations_updated

def check_downloaded_are_processed(rinex_holdings, addneq2_out, bern_log_fn):
    """ Check that the sites listed in (the final) ADDNEQ2 output file, are
        the same sites listed in the rinex_holdings; aka check that all
        dowloaded stations are indeed processed.
        In case of incosistencies, write missing stations to stderr and
        also append to the file bern_log_fn
    """
    with open(addneq2_out, 'r') as adnq2:
        adnq2_dct = bparse.parse_generic_out_header(adnq2)
        assert(adnq2_dct['program'] == 'ADDNEQ2')
        adnq2_dct = baddneq.parse_addneq_out(adnq2)
        adnq2_dct = adnq2_dct['stations']

    addneq2_sta_list = [ dct['station_name'].lower().strip() for aa,dct in adnq2_dct.items() ]
    rinex_sta_list = [ '{:} {:}'.format(staid, dict['domes']).lower().strip() for staid, dict in rinex_holdings.items() if 'local' in dict and dict['local'] is not None and not dict['exclude'] ]

    #assert(len(addneq2_sta_list) == len(rinex_sta_list))
    #for sta in addneq2_sta_list: assert(sta in rinex_sta_list)

    if len(addneq2_sta_list) != len(rinex_sta_list):
        with open(bern_log_fn, 'a') as fout:
            print('[WRNNG] Number of RINEX files downloaded not equal to number of sites included in the final ADDNEQ2', file=sys.stderr)
            print('\n[WRNNG] Number of RINEX files downloaded not equal to number of sites included in the final ADDNEQ2', file=fout)
            missing_from_addneq = [station for station in addneq2_sta_list if station not in rinex_sta_list]
            if len(missing_from_addneq)>0: print('[WRNNG] (cont\'d) Included in ADDNEQ2 but missing from RINEX holdings: {:}'.format(' '.join(missing_from_addneq)), file=sys.stderr)
            if len(missing_from_addneq)>0: print('[WRNNG] (cont\'d) Included in ADDNEQ2 but missing from RINEX holdings: {:}'.format(' '.join(missing_from_addneq)), file=fout)
            missing_from_holdings = [station for station in rinex_sta_list if station not in addneq2_sta_list]
            if len(missing_from_holdings)>0: print('[WRNNG] (cont\'d) Included in RINEX holdings but missing from ADDNEQ2: {:}'.format(' '.join(missing_from_holdings)), file=sys.stderr)
            if len(missing_from_holdings)>0: print('[WRNNG] (cont\'d) Included in RINEX holdings but missing from ADDNEQ2: {:}'.format(' '.join(missing_from_holdings)), file=fout)


def sta_id2domes(sta_id, netsta_dct):
    """ Translate a station 4-char id to its full name, aka id+domes. The info
        are serached for in the netsta_dct dictionary (which is a list of
        dictionaries with keys 'mark_name_DSO' and 'mark_numb_OFF'). The
        netsta_dct dictionary is normally a query result from the database.
    """
    for dct in netsta_dct:
        if dct['mark_name_DSO'].lower() == sta_id.lower():
            return dct['mark_numb_OFF']
    print('[WRNNG] No domes number found for station {:} (database query)'.format(sta_id))
    return ''


def compile_report(options, dt, bern_log_fn, netsta_dct, station_ts_updated, rinex_holdings):
    def get_rinex_version_info():
        version_info = {}
        for staid,rnx_dct in rinex_holdings.items():
            if not rnx_dct['exclude']:
                print('opening file {:}'.format(rnx_dct['local']))
                with open(rnx_dct['local'], 'r') as fin:
                    try:
                      fline = fin.readline()
                      if not fline.rstrip().endswith('RINEX VERSION / TYPE'):
                          print('[WRNNG] RINEX file {:} is missing version field!'.format(rnx_dct['local']), file=sys.stderr)
                          version = 'unknown'
                      else:
                          version = fline.split()[0].strip()
                    except:
                      version = 'unknown'
                if version in version_info:
                    version_info[version] += 1
                else:
                    version_info[version] = 1
        return version_info

    def get_station_rinex_holdings_info(sta_full_name):
        for staid,rnx_dct in rinex_holdings.items():
            full_name = '{}'.format(' '.join([staid,rnx_dct['domes']])).strip()
            if full_name.lower() == sta_full_name.lower():
                return rnx_dct
        return None

    def get_station_addneq2_holdings_info(sta_full_name, addneq2_dct):
        for num,record in addneq2_dct.items():
            if record['station_name'].lower().strip() == sta_full_name.lower().strip():
                return record
        return None

    def get_station_tsupdate_info(sta_full_name):
        for k,v in station_ts_updated.items():
            if k.lower().strip() == sta_full_name.lower().strip():
                return v
        return ''

    ## the final ADDNEQ2 output file (to be parsed)
    final_out = os.path.join(os.getenv('P'), options['campaign'].upper(), 'OUT', '{:}{:}0.OUT'.format(options['solution_id'], dt.strftime('%y%j')))

    ## parse the ADDNEQ2 output file and keep site information
    addneq2_info = {}
    with open(final_out, 'r') as adnq2:
        adnq2_dct = bparse.parse_generic_out_header(adnq2)
        assert(adnq2_dct['program'] == 'ADDNEQ2')
        adnq2_dct = baddneq.parse_addneq_out(adnq2)
        ## extract some info
        addneq2_info = {'obs_count':adnq2_dct['statistics']['total_number_of_observations'],
            'par_count': adnq2_dct['statistics']['total_number_of_adjusted_parameters'],
            'rms': adnq2_dct['statistics']['a_posteriori_rms_of_unit_weight'],
            'xdof': adnq2_dct['statistics']['chi**2/dof']}
        ## only keep station-specific info
        adnq2_dct = adnq2_dct['stations']

    report_dict = []

    ## loop through all sites in network (from db query) ...
    for ndct in netsta_dct:
        station = ndct['mark_name_DSO']
        sta_full_name = '{:} {:}'.format(station, ndct['mark_numb_OFF']).strip()

        ## did we update the station's time-series records ?
        ## tsupdated = True if '{:} {:}'.format(ndct['mark_name_DSO'], ndct['mark_numb_OFF']).strip().lower() in [x.lower().strip() for x in station_ts_updated] else False

        ## grap rinex_holdings info for this site
        rnx_info = get_station_rinex_holdings_info(sta_full_name)

        ## grap addneq2 info for the site
        nq0_info = get_station_addneq2_holdings_info(sta_full_name, adnq2_dct)

        warnings = []

        ## everything ok?
        if rnx_info is not None and rnx_info['local'] is not None and not rnx_info['exclude'] and nq0_info is None:
            wmsg = '[WRNNG] Station {:}: Local RINEX available and station not excluded but not included in the final ADDNEQ2 file!'.format(sta_full_name)
            print('{}'.format(wmsg), file=sys.stderr)
            warnings.append(wmsg)
        if nq0_info is not None and (rnx_info is None or (rnx_info is not None and rnx_info['exclude'])):
            wmsg = '[WRNNG] Station {:}: Local RINEX is marked as excluded but station was included in final ADDNEQ2 file!'.format(sta_full_name)
            print('{}'.format(wmsg), file=sys.stderr)
            warnings.append(wmsg)
        if nq0_info is not None and (rnx_info is None or (rnx_info is not None and rnx_info['local'] is None)):
            wmsg = '[WRNNG] Station {:}: Local RINEX is not recorded but station was included in final ADDNEQ2 file!'.format(sta_full_name)
            print('{}'.format(wmsg), file=sys.stderr)
            warnings.append(wmsg)

        tsupdated = True if sta_full_name.strip().lower() in [x.lower().strip() for x in station_ts_updated] else False

        # report_dict.append(merge_dicts(merge_dicts(rnx_info, nq0_info, True),{'sort_by':sta_full_name, 'tsupdated':tsupdated}, True))
        report_dict.append(merge_dicts(merge_dicts(rnx_info, nq0_info, True),{'sort_by':sta_full_name}, True))

    ## sort based on site name
    report_dict = sorted(report_dict, key=lambda x: x['sort_by'])

    ## write the report
    num_reference_sites = 0
    with open(bern_log_fn, 'a') as logfn:
        print('\n{:15s} {:8s} {:8s} {:8s} {:8s} {:8s} {:8s} {:9s} {:9s} {:9s} {:7s} {:15s} {:45s} {:5s}'.format('Station', 'Xcorr', 'Xrms', 'Ycorr', 'Yrms', 'Zcorr', 'Zrms', 'LonCorr', 'LatCorr', 'HgtCorr', 'EFH', 'T-S Updated', 'Remote RINEX filename', 'Excl.'), file=logfn)
        print('{:15s} {:8s} {:8s} {:8s} {:8s} {:8s} {:8s} {:9s} {:9s} {:9s} {:7s} {:15s} {:45s} {:5s}'.format('-'*15, '-'*8, '-'*8, '-'*8, '-'*8, '-'*8, '-'*8, '-'*9, '-'*9, '-'*9, '-'*7, '-'*15, '-'*45, '-'*5), file=logfn)
        for record in report_dict:
            site_fullname = record['sort_by']
            print('{:15s} '.format(record['sort_by']), end='', file=logfn)

            ## print info from addneq2
            if 'X_correction' in record:
                print('{:+8.4f} {:8.4f} {:+8.4f} {:8.4f} {:+8.4f} {:8.4f} {:+9.5f} {:+9.5f} {:+9.5f} {:7s} '.format(record['X_correction'], record['X_rms_error'], record['Y_correction'], record['Y_rms_error'], record['Z_correction'], record['Z_rms_error'], record['Longitude_rms_error'], record['Latitude_rms_error'], record['Height_rms_error'], record['e/f/h']), end='', file=logfn)
                if record['e/f/h'].lower() == 'HELMR'.lower() or record['e/f/h'][0:3].lower() == 'FIX'.lower():
                    num_reference_sites += 1
            else:
                print('{:91s} '.format(''), end='', file=logfn)

            ## print ts-update info
            _tsfile = get_station_tsupdate_info(site_fullname)
            if _tsfile.strip() != '': _tsfile = os.path.basename(_tsfile)
            print('{:15s}'.format(_tsfile), end='', file=logfn)

            ## print rinex_holdings info
            if 'local' in record:
                remote_rnx = os.path.basename(record['remote']) if record['remote'] is not None else 'download skipped'
                print(' {:45s} {:5s}'.format(remote_rnx, str(record['exclude'])), file=logfn)
            else:
                print(' {:^45s} {:^5s}'.format('x','x'), file=logfn)

        ## append general info
        sites_processed = len(adnq2_dct)
        site_ts_upadted = len(station_ts_updated)
        sites_in_network = len(netsta_dct)
        sites_downloaded = len([site for site,rnx in rinex_holdings.items() if rnx['local'] != None and not rnx['exclude']])
        print('', file=logfn)
        print('Number of sites in network    {:}'.format(sites_in_network), file=logfn)
        print('Number of RINEX downloaded    {:} (excluding skipped if any)'.format(sites_downloaded), file=logfn)
        print('Number of sites processed     {:}'.format(sites_processed), file=logfn)
        print('Number of time-series updated {:}'.format(site_ts_upadted), file=logfn)
        print('Number of reference stations  {:}'.format(num_reference_sites), file=logfn)
        print('Number of observations        {:} (total)'.format(addneq2_info['obs_count']), file=logfn)
        print('Number of parameters          {:} (adjusted)'.format(addneq2_info['par_count']), file=logfn)
        print('RMS a-posteriori              {:} (unit weight)'.format(addneq2_info['rms']), file=logfn)
        print('x^2 / DoF                     {:}'.format(addneq2_info['xdof']), file=logfn)
        # statistics on RINEX versions used
        rnx_info_dct = get_rinex_version_info()
        rnx_info_str = ''
        for k,v in rnx_info_dct.items(): rnx_info_str += k + ':' + str(v) + ' '
        print('RINEX version statistics      {:}'.format(rnx_info_str), file=logfn)

        ## append warning messages
        for wrn in warnings: print('{}'.format(wrn), file=logfn)

    print('[DEBUG] Addneq2 file {:} parsed; summary written to {:}'.format(final_out, bern_log_fn))
    return bern_log_fn

def make_cluster_file(options, rinex_holdings):
    ## make cluster file
    cluster_file = os.path.join(os.getenv('P'), options['campaign'], 'STA', options['campaign']+'.CLU')
    with open(cluster_file, 'w') as fout:
        print("""Cluster file automaticaly created by rundd on {:}
--------------------------------------------------------------------------------

STATION NAME      CLU
****************  ***""".format(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')), file=fout)
        sta_counter = 0
        for sta in rinex_holdings:
            if rinex_holdings[sta]['local'] is not None and not rinex_holdings[sta]['exclude']:
                print('{:16s}  {:3d}'.format(' '.join([sta.upper(), rinex_holdings[sta]['domes']]), sta_counter//options['files_per_cluster']+1), file=fout)
                sta_counter += 1
    return cluster_file, sta_counter

def count_reference_sta(options, rinex_holdings):
    refcrd_fn = options['refinf'] + '_R.CRD'
    refcrd_fn_list = [ os.path.join(x, refcrd_fn) for x in [os.path.join(options['tables_dir'], 'crd'), os.path.join(os.getenv('P'), options['campaign'], 'STA')]]
    refcrd = None

    for rfn in refcrd_fn_list:
        if os.path.isfile(rfn):
            refcrd = rfn
            break;
    if refcrd is None:
        errmsg = '[ERROR] Failed to find reference coordinate file {:} or {:}'.format(refcrd_fn_list[0], refcrd_fn_list[1])
        raise RuntimeError(errmsg)

    crddct = parse_bern52_crd(refcrd)
    refsta_list = [ '{:} {:}'.format(k.lower(), v['domes']) for k,v in crddct.items() if k not in ['title', 'ref_frame', 'date'] ]
    dwnldsta_list = [ '{:} {:}'.format(k.lower(), v['domes']) for k,v in rinex_holdings.items() ]
    return [ s for s in refsta_list if s in dwnldsta_list ]

def compile_warnings_report(warnings, logfn):
    unique_warnings = []
    for w in warnings:
        subroutine = w['subroutine']
        description = w['description']
        if not {'subroutine':subroutine, 'description':description} in unique_warnings:
            unique_warnings.append({'subroutine':subroutine, 'description':description})

    with open(logfn, 'a') as fout:
        print('\n{:20s} {:50s}\n{:20s} {:50s}'.format('SubRoutine', 'Description (*)', '-'*20, '-'*50), file=fout)
        for w in unique_warnings:
            print('{:20s} {:50s}'.format(w['subroutine'], w['description']), file=fout)
        print('(*) Only unique subroutine/description pairs reported; one warning may have occured many times\n', file=fout)

def print_initial_loginfo(options, logfn):
    with open(logfn, 'w') as fout:
        print('{}-{} started at {}'.format('rundd', VERSION, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), file=fout)
        print('user: {} PID: {} System: {}'.format(getpass.getuser(), os.getpid(), '||'.join(os.uname())), file=fout)
        print('\n{:25s} {:25s}\n{:25s} {:25s}'.format('Parameter', 'Value', '-'*25, '-'*25), file=fout)
        for k,v in options.items(): print('{:25s} {:25s}'.format(str(k), str(v)), file=fout)
        print('', file=fout)

def append_product_info(products_dict, logfn):
    with open(logfn, 'a') as fout:
        print('{:15s} {:15s} {:55s} {:55s}\n{:15s} {:15s} {:55s} {:55s}'.format('Product', 'Type', 'Remote', 'Local', '-'*15, '-'*15, '-'*55, '-'*55), file=fout)
        for prodtype, proddict in products_dict.items():
            print('{:15s} {:15s} {:55s} {:55s}'.format(str(prodtype), str(proddict['type']), str(proddict['remote']), str(proddict['local'])), file=fout)
        print('', file=fout)

def appendf2f(source_fn, target_fn, header=None):
    with open(source_fn, 'r') as fin:
        text = fin.read()
    with open(target_fn, 'a') as fout:
        if header is not None: print('{}'.format(header), file=fout)
        fout.write(text)

def append2f(fn, text, header=None):
    with open(fn, 'a') as fout:
        if header is not None: print('{}'.format(header), file=fout)
        fout.write(text)
        print('', file=fout)

def upload_sinex(options):
    ## try locating the SINEX file
    final_snx = os.path.join(os.getenv('P'), options['campaign'].upper(), 'SOL', '{:}{:}0.SNX'.format(options['solution_id'], dt.strftime('%y%j')))
    ret = final_snx, None
    if not os.path.isfile(final_snx):
        print('[ERROR] Failed to locate (final) SINEX file {:}. Cannot upload!'.format(final_snx), file=sys.stderr)
        return ret
    ## compress the file
    _, snxZ = comp.os_compress(final_snx, '.Z', False)
    ## upload the file
    try:
        ret = upld.ftp_upload(options['epnd_ftp_ip'], 'snxin', snxZ, options['epnd_ftp_username'], options['epnd_ftp_password'])
        # ret = final_snx, '{:}/snxin/{:}'.format(options['epnd_ftp_ip'], snxZ)
    except:
        print('[ERROR] Failed to upload (final) SINEX file {:} to {:}!'.format(final_snx, options['epnd_ftp_ip']), file=sys.stderr)
    ## remove the compressed file
    if os.path.isfile(snxZ): os.remove(snxZ)
    return ret

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
                    choices=["GPS", "GLONASS", "GALILEO", "GPS/GAL", "GPS/GLO", "GAL/GLO"],
                    default='GPS/GLO')
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
                    '--use-euref-exclusion-list',
                    action='store_true',
                    help='Use EUREF\'s exclusion list, ftp://epncb.oma.be/pub/station/general/excluded/exclude.WWWW',
                    dest='use_epn_exclude_list')
parser.add_argument(
                    '--exclusion-list',
                    required=False,
                    help='Optionally us a file where the first column is the name of the station to be excluded from the processing; all other columns are ignored. The file can have many rows.',
                    metavar='EXCLUSION_LIST',
                    dest='exclusion_list',
                    default=None)
parser.add_argument(
                    '--min-reference-stations',
                    required=False,
                    help='If a value larger than 0 is provided, then the program will check if the number of reference sites to be used (according to the downloaded RINEX list) is larger than this value; if not it will stop. The reference station list is read from a file using the \'REFINF\' variable and inspecting one of the files: \'$tables_dir/crd/$REFINF_R.CRD\' or \'$P/$campaign/$REFINF_R.CRD\'',
                    metavar='MIN_REFERENCE_SITES',
                    dest='min_reference_sites',
                    type=int,
                    default=4)
parser.add_argument(
                    '--stations-per-cluster',
                    required=False,
                    help='Stations per cluster',
                    metavar='STATIONS_PER_CLUSTER',
                    dest='files_per_cluster',
                    type=int,
                    default=4)
parser.add_argument(
                    '--solution-id',
                    required=False,
                    help='Final solution identifier; preliminary, reduced and free-network solution will be named accordingly.',
                    metavar='FINAL_SOLUTION_ID',
                    dest='solution_id',
                    default=None)
parser.add_argument(
                    '--pcf-file',
                    required=False,
                    help='PCF file to use for Bernese; this file should exist in $U/PCF/ folder',
                    metavar='PCF_FILE',
                    dest='pcf_file',
                    default=None)
parser.add_argument(
                    '--atlinf',
                    required=False,
                    help="""The filename of the atl (i.e atmospheric tidal loading) corrections file.
If the values is left blank, then no atl file is going to be used
If you do specify a file, do **not** use an extension; also the file
should be placed either in the ${TABLES_DIR}/atl directory or in the
campaign's /STA directory.""",
                    metavar='ATLINF',
                    dest='atlinf',
                    default=None)
parser.add_argument(
                    '--pcv-ext',
                    required=False,
                    help="""Extension of the PCV input file, e.g. \'I14\'""",
                    metavar='PCV_EXT',
                    dest='pcvext',
                    default=None)
parser.add_argument(
                    '--refpsd',
                    required=False,
                    help="""PSD Information file""",
                    metavar='REFPSD',
                    dest='refpsd',
                    default=None)
parser.add_argument(
                    '--aprinf',
                    required=False,
                    help="""A-priori CRD file (containing all regional sites). Must be located in $TABLES_DIR/crd (provide no extension; .CRD is assumed)""",
                    metavar='APRINF',
                    dest='aprinf',
                    default=None)
parser.add_argument(
                    '--ts-file-name',
                    required=False,
                    help="""""",
                    metavar='TS_FILE_NAME',
                    dest='ts_file_name',
                    default=None)
## Warning !!
## Following variables (aka with action=store_true) should always default to
## False. If the switch is set to True/YES in the config file, then this value
## will prevail.
parser.add_argument(
                    '--ignore-indv-calibrations',
                    action='store_true',
                    help='If set, then the given station information (.STA) file will be examined and all antennas with individual calibrations (aka when their SN numbers in the respective STA file are not 99999) will be translated to the generic SN. In the process, a new .STA file will be created; it will be a copy of the original (aka the one passed in) but with all antenna SN\'s set to 99999.',
                    dest='ignore_indv_calibrations')
parser.add_argument(
                    '--skip-remove',
                    action='store_true',
                    help='',
                    dest='skip_remove')
parser.add_argument(
                    '--skip-rinex-download',
                    action='store_true',
                    help='Skip download of RINEX files; only consider RINEX files already available for network/date',
                    dest='skip_rinex_download')
parser.add_argument('--verbose',
                    dest='verbose',
                    action='store_true',
                    help='Trigger verbose run (prints debug messages).')
parser.add_argument(
                    '--download-max-tries',
                    required=False,
                    help='Maximum number of tries when downloading products. Each new try is started after \'download_sleep_for\' seconds after the previous fail.',
                    metavar='PRODUCT_DOWNLOAD_MAX_TRIES',
                    dest='product_download_max_tries',
                    type=int,
                    default=3)
parser.add_argument(
                    '--download-sleep-for',
                    required=False,
                    help='when product download has failed, wait for \'download_sleep_for\' seconds before starting a new try.',
                    metavar='PRODUCT_DOWNLOAD_SLEEP_FOR',
                    dest='product_download_sleep_for',
                    type=int,
                    default=1*60)
parser.add_argument(
                    '--upload-to-epnd',
                    action='store_true',
                    dest='upload_to_epnd',
                    help='If set, then the progeam will try to upload the final SINEX file to EPNDensification FTP site, using the credentials that should exist in the corresponding config file (entries: \'EPND_FTP_IP\', \'EPND_FTP_USERNAME\', \'EPND_FTP_PASSWORD\')'
                    )

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
    ## translate YES/NO to True/False
    for k,v in config_file_dict.items():
        if v.upper().strip() == "YES": options[k.lower()] = True
        elif v.upper().strip() == "NO": options[k.lower()] = False
    for k,v in vars(args).items():
        if v is not None:
            ## special care for True/False variables! if the corresponding
            ## option in the config file is True, config file prevails!
            if type(v) is bool and k in options:
                options[k] = bool(options[k]) or v
            else:
                options[k.lower()] = v
        elif v is None and k not in options:
            options[k.lower()] = v

    ## parse the config file (if any) without expanding variables, to get
    ## only TS_FILE_NAME
    #ts_file_name = parse_key_file(args.config_file, False, False)['TS_FILE_NAME']
    #print('>> Note: new ts_file_name = {:}'.format(ts_file_name))

    ## print key/value pairs in options
    # print('-------------------------------------------------------------------')
    # for k,v in options.items():
    #     print('{:} -> {:}'.format(k, v))
    # sys.exit(9)

    ## verbose print
    verboseprint = print if options['verbose'] else lambda *a, **k: None

    ## load the b_loadgps file
    bpe.addtopath_load(options['b_loadgps'])

    ## date we are solving for as datetime instance
    dt = datetime.datetime.strptime('{:}-{:03d}'.format(options['year'], int(options['doy'])), '%Y-%j')

    ## make the log file --cat any info there--
    logfn = os.path.join(log_dir, 'rundd_{}_{}.log'.format(dt.strftime('%y%j'), os.getpid()))
    print_initial_loginfo(options, logfn)

    ## if the user specified an ATX file, run the ATX2PCV script
    if 'atxinf' in options and options['atxinf'] is not None and options['atxinf'].strip() != '':
        atxinf = os.path.join(options['tables_dir'], 'atx', options['atxinf'] + '.ATX')
        pcvout = os.path.join(options['tables_dir'], 'pcv', options['campaign'].upper() + '.PCV')
        stainf = os.path.join(options['tables_dir'], 'sta', options['stainf'].upper() + '.STA')
        pcvext = options['pcvext']
        pcv_file = a2p.atx2pcv({'atxinf':atxinf, 'pcvout':pcvout, 'stainf':stainf, 'pcvext':pcvext})
        options['pcvfile'] = pcv_file

    ## get info on the stations that belong to the network, aka
    ## [{'station_id': 1, 'mark_name_DSO': 'pdel', 'mark_name_OFF': 'pdel',..},{...}]
    db_credentials_dct = parse_db_credentials_file(options['config_file'])
    netsta_dct = query_sta_in_net(options['network'], db_credentials_dct)

    ## if needed, alter the .STA file to only hold generic calibrations; aka
    ## translate individual calibrations to generic ones in the .STA file
    ## WARNING! Note that this will change the options['stainf'] value
    if options['ignore_indv_calibrations']:
        options['stainf'] = translate_sta_indv_calibrations(options)

    ## link needed files from tables_dir to campaign-specific directories
    link2campaign(options, dt, temp_files)

    ## download the RINEX files for the given network. Hold results in the
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
    print('[DEBUG] Size of RINEX holdings {:}'.format(len(rinex_holdings)))

    ## for every station add a field in its dictionary ('exclude') denoting if
    ## the station needs to be excluded from the processing and also get its
    ## domes number
    for station in rinex_holdings:
        rinex_holdings[station]['exclude'] = False
        rinex_holdings[station]['domes'] = sta_id2domes(station, netsta_dct)

    ## check if we need to exclude station from EUREF's list
    if options['use_epn_exclude_list']:
        mark_exclude_stations(get_euref_exclusion_list(dt), rinex_holdings)

    ## check if we have a file with stations to exclude
    if options['exclusion_list'] is not None:
        staexcl = []
        with open(options['exclusion_list'], 'r') as fin:
            staexcl = [x.split()[0].lower() for x in fin.readlines()]
        mark_exclude_stations(staexcl, rinex_holdings)

    ## uncompress (to obs) all RINEX files of the network/date
    rinex_holdings = decompress_rinex(rinex_holdings)

    ## rename marker names to match mark_name_DSO if needed
    rinex_holdings = rename_rinex_markers(rinex_holdings, netsta_dct)

    ## validate stations using the STA file and get domes
    ## stafn = stainf2fn(options['stainf'], options['tables_dir'], options['campaign'].upper())
    stafn = os.path.join(os.getenv('P'), options['campaign'].upper(), 'STA', options['stainf'].upper() + '.STA')
    if match_rnx_vs_sta(rinex_holdings, stafn, dt) > 0:
        print('[ERROR] Aborting processing!', file=sys.stderr)
        append2f(logfn, 'Failed to validate station records in STA file', 'FATAL ERROR; Processing stoped')
        sys.exit(1)

    ## download and prepare products; do not give up if the first try fails,
    ## maybe some product is udated/written on the remote server. Retry a few
    ## times after waiting
    product_download_max_tries = options['product_download_max_tries']
    product_download_sleep_for = options['product_download_sleep_for']
    product_download_try = 0
    products_ok = False
    products_dict = {}
    while product_download_try < product_download_max_tries and not products_ok:
        #try:
        products_dict, products_ok = prepare_products(dt, options['config_file'], products_dict, os.getenv('D'), options['verbose'], True)
            ## products downloaded and prepared; break loop
            ## product_download_try = product_download_max_tries + 1
        #except Exception as e:
        #    product_download_try += 1
        #    print('[WRNNG] Failed downloading/preparing products. Try {:}/{:}'.format(product_download_try, product_download_max_tries), file=sys.stderr)
        #    if product_download_try >= product_download_max_tries:
        #        print('[ERROR] Failed to download products! Traceback info {:}'.format(e), file=sys.stderr)
        #        append2f(logfn, 'Failed to download products! Traceback info {:}'.format(e), 'FATAL ERROR; Processing stoped')
        #        ## Send ERROR mail
        #        with open(logfn, 'r') as lfn: message_body = lfn.read()
        #        message_head = 'autobpe.rundd.{}-{}@{} {:}'.format(options['pcf_file'], options['network'], dt.strftime('%y%j'), 'ERROR')
        #        send_report_mail(options, message_head, message_body)
        #        sys.exit(1)
        if not products_ok:
            print('[WRNNG] Sleeping for {:} seconds and retrying ....'.format(product_download_sleep_for), file=sys.stderr)
            psleep(product_download_sleep_for)
    products2dirs(products_dict, os.path.join(os.getenv('P'), options['campaign'].upper()), dt, True)
    append_product_info(products_dict, logfn)

    ## check that we have at least min_reference_sites reference sites included
    ## in the processing
    if options['min_reference_sites'] > 0:
        ref_sta = count_reference_sta(options, rinex_holdings)
        if len(ref_sta) < options['min_reference_sites']:
            print('[ERROR] Too few reference sites available for processing! Stoping the analysis now!', file=sys.stderr)
            append2f(logfn, 'Too few reference sites available for processing!', 'FATAL ERROR; Processing stoped')
            ## Send ERROR mail
            with open(logfn, 'r') as lfn: message_body = lfn.read()
            message_head = 'autobpe.rundd.{}-{}@{} {:}'.format(options['pcf_file'], options['network'], dt.strftime('%y%j'), 'ERROR')
            send_report_mail(options, message_head, message_body)
            sys.exit(1)
        else:
            print('[DEBUG] Initial number of reference stations (downloaded) {:}'.format(len(ref_sta)))

    ## transfer (uncompressed) rinex files to the campsign's RAW directory
    ## TODO at production, change cp_not_mv parameter
    rinex_holdings = rinex2raw(rinex_holdings, options['campaign'], True, True)
    ## rinex 2 uppercase
    rinex_holdings = rinex2uppercase(rinex_holdings, True)
    ## rinex3 names to rinex2
    rinex_holdings = rinex3to2_link(rinex_holdings, options['campaign'], dt, True)

    ## make cluster file
    cluster_file, num_stations = make_cluster_file(options, rinex_holdings)
    print('[DEBUG] Created cluster file {:} with total number of stations {:}'.format(cluster_file, num_stations))

    ## Set solution identifiers
    solution_id = {'final': options['solution_id'] }
    for descr, sid in zip(['prelim', 'reduced', 'free_net'], [ 'P', 'R', 'N']):
        if options['solution_id'][-1] == sid:
            print('[ERROR] Final solution identifier cannot end in {:}; reserved for {:} solution'.format(sid, descr), file=sys.stderr)
            append2f(logfn, 'Final solution identifier cannot end in {:}; reserved for {:} solution'.format(sid, descr), 'FATAL ERROR; Processing stoped')
            ## Send ERROR mail
            with open(logfn, 'r') as lfn: message_body = lfn.read()
            message_head = 'autobpe.rundd.{}-{}@{} {:}'.format(options['pcf_file'], options['network'], dt.strftime('%y%j'), 'ERROR')
            send_report_mail(options, message_head, message_body)
            sys.exit(1)
        solution_id[descr] = options['solution_id'][0:-1] + sid
    for descr, sid in solution_id.items():
        print('[DEBUG] {:} solution identifier set to {:}'.format(descr.upper(), sid))

    ## Set variables in PCF file
    pcf_file = os.path.join(os.getenv('U'), 'PCF', options['pcf_file'])
    if not os.path.isfile(pcf_file):
        print('[ERROR] Failed to find PCF file {:}'.format(pcf_file), file=sys.stderr)
        append2f(logfn, 'Failed to find PCF file {:}'.format(pcf_file), 'FATAL ERROR; Processing stoped')
        ## Send ERROR mail
        with open(logfn, 'r') as lfn: message_body = lfn.read()
        message_head = 'autobpe.rundd.{}-{}@{} {:}'.format(options['pcf_file'], options['network'], dt.strftime('%y%j'), 'ERROR')
        send_report_mail(options, message_head, message_body)
        sys.exit(1)
    pcf = bpcf.PcfFile(pcf_file)
    for var, value in zip(['B', 'C', 'E', 'F', 'N', 'BLQINF', 'ATLINF', 'STAINF', 'CRDINF', 'SATSYS', 'PCV', 'PCVINF', 'ELANG', 'FIXINF', 'REFINF', 'REFPSD', 'CLU', 'OBSSEL'],['COD', solution_id['prelim'], solution_id['final'], solution_id['reduced'], solution_id['free_net'], options['blqinf'], options['atlinf'], options['stainf'], options['campaign'].upper(), options['sat_sys'].upper(), options['pcvext'].upper(), options['pcvinf'].upper(), options['elevation_angle'], options['fixinf'], options['refinf'], options['refpsd'], options['files_per_cluster'], options['obssel'].upper()+'.SEL']):
        pcf.set_variable('V_'+var, value, 'rundd {}'.format(datetime.datetime.now().strftime('%Y%m%dT%H%M%S')))
    pcf.dump(os.path.join(os.getenv('U'), 'PCF', 'RUNDD.PCF'))
    pcf_file = os.path.join(os.getenv('U'), 'PCF', 'RUNDD.PCF')

    ## Just a reminder, here is an entry of rinex_holdings
    ## hofn {'local': '/home/bpe/data/GPSDATA/CAMPAIGN52/GREECE/RAW/HOFN0050.19O', 'remote': 'ftp://anonymous:anonymous@igs.ensg.ign.fr/pub/igs/data/2019/005/hofn0050.19d.Z', 'exclude': False, 'domes': '10204M002'}

    ## ready to call the perl script for processing ...
    bpe_start_at = datetime.datetime.now(tz=datetime.timezone.utc)
    bern_task_id = '{:}'.format(os.getpid())
    bern_log_fn = os.path.join(log_dir, '{:}-{:}{:}.log'.format(options['campaign'], bern_task_id, dt.strftime('%y%j')))
    temp_files.append(bern_log_fn) ## delete it at exit
    print('[DEBUG] Firing up the Bernese Processing Engine (log: {:})'.format(bern_log_fn))
    append2f(logfn, 'Firing up the Bernese Processing Engine at {:} UTC'.format(bpe_start_at.strftime('%x %X')))
    with open(bern_log_fn, 'w') as logf:
        subprocess.call(['{:}'.format(os.path.join(os.getenv('U'), 'SCRIPT', 'ntua_pcs.pl')), '{:}'.format(dt.strftime('%Y')), '{:}0'.format(dt.strftime('%j')), '{:}'.format(pcf_file), 'USER', '{:}'.format(options['campaign'].upper()), bern_task_id], stdout=logf, stderr=logf)
    bpe_stop_at = datetime.datetime.now(tz=datetime.timezone.utc)
    append2f(logfn, 'Bernese Processing Engine stoped at {:} UTC'.format(bpe_stop_at.strftime('%x %X')))

    ## check if we have an error; if we do, make a report and paste it to the
    ## log file
    bpe_error = False
    bpe_status_file = os.path.join(os.getenv('P'), options['campaign'].upper(), 'BPE', 'R2S_{}.RUN'.format(bern_task_id))
    if bpe.check_bpe_status(bpe_status_file)['error'] == 'error':
        errlog = os.path.join(log_dir, 'bpe_error_{:}.log'.format(bern_task_id))
        print('[ERROR] BPE failed due to error! see log file {:}'.format(logfn), file=sys.stderr)
        bpe.compile_error_report(bpe_status_file, os.path.join(os.getenv('P'), options['campaign'].upper()), bern_task_id, errlog)
        appendf2f(errlog, logfn, 'Error Report') ## paste error report to log-file
        temp_files.append(errlog) ## delete it at exit
        bpe_error = True

    ## update station-specif time-series (if needed)
    station_ts_updated = {}
    if options['update_sta_ts'] and not bpe_error:
        station_ts_updated = update_ts(options, os.path.join(os.getenv('P'), options['campaign'].upper(), 'OUT', '{:}{:}0.OUT'.format(solution_id['final'], dt.strftime('%y%j'))))

    ## compile a quick report based on the ADDNEQ2 output file for every
    ## station (appended to the log-file)
    if not bpe_error:
        compile_report(options, dt, logfn, netsta_dct, station_ts_updated, rinex_holdings)

    ## assert that all stations (RINEX) downloaded are indeed included in the
    ## processing
    if not bpe_error:
        check_downloaded_are_processed(rinex_holdings, os.path.join(os.getenv('P'), options['campaign'].upper(), 'OUT', '{:}{:}0.OUT'.format(solution_id['final'], dt.strftime('%y%j'))), logfn)

    ## collect warning messages in a list (of dictionaries for every warning)
    if not bpe_error:
        warning_messages = bpe.collect_warning_messages(os.path.join(os.getenv('P'), options['campaign'].upper()), dt.strftime('%j'), bpe_start_at, bpe_stop_at)
        compile_warnings_report(warning_messages, logfn)

    ## upload SINEX files if needed (SINEX to EPND ftp)
    if not bpe_error and options['upload_to_epnd']:
        if 'epnd_ftp_ip' in options and options['epnd_ftp_ip'].strip() != '':
            final_sinex, uploaded_to = upload_sinex(options)
            if not uploaded_to:
                append2f(logfn, 'Failed to upload local final SINEX file {:} to {:}'.format(final_sinex,options['epnd_ftp_ip']), '')
            else:
                append2f(logfn, 'Uploaded local (final) SINEX file {:} to {:}'.format(final_sinex,uploaded_to))
                print('[DEBUG] Uploaded local (final) SINEX file {:} to {:}'.format(final_sinex,uploaded_to))

    ## do we need to send mail ?
    if 'send_mail_to' in options and options['send_mail_to'] is not None:
        #message_file = errlog if bpe_error else bern_log_fn
        message_file = logfn
        message_head = 'autobpe.rundd.{}-{}@{} {:}'.format(options['pcf_file'], options['network'], dt.strftime('%y%j'), 'ERROR' if bpe_error else '')
        with open(message_file, 'r') as fin:
            message_body = fin.read()
        send_report_mail(options, message_head, message_body)

    ## remove all files created/modified by BPE
    if not options['skip_remove']:
        rmbpetmp(os.path.join(os.getenv('P'), options['campaign'].upper()), dt, bpe_start_at, bpe_stop_at)
    else:
        print('[NOTE ] Skipping removal of files! campaign dirs will not be cleared')
