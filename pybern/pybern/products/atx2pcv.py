#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import os
import datetime
import sys
import re
import subprocess

import pybern.products.bernparsers.bernpcf as bpcf
import pybern.products.bernbpe as bpe

def deltmp(tmp_file_list):
    for file in tmp_file_list:
        try:
            os.remove(file)
        except:
            pass

def atx2pcv(**kwargs):
    """ Relevant kwargs:
        * atxinf
        * stainf
        * pcvext
        * recinf (e.g. "RECEIVER.", or "RECEIVER.NTUA")
    """ 
    tmp_files = []
    dt = datetime.datetime.now()

    kwargs['campaign'] = kwargs['campaign'].upper()

    atxinf = kwargs['atxinf']
    if atxinf[-4:] != '.ATX': atxinf += '.ATX'
    stainf = kwargs['stainf']
    if stainf[-4:] == '.STA': stainf = stainf[0:-4]
    phginf = os.path.basename(atxinf[0:-4])

    ## load the gps LOADVAR file
    bpe.addtopath_load(kwargs['b_loadgps'])
    campaign_dir = os.path.join(os.getenv('P'), kwargs['campaign'])

    ## if sta file is not in campaign's STA dir, link it there
    if os.path.dirname(stainf) != os.path.join(os.getenv('P'), kwargs['campaign'], 'STA'):
        src = stainf + '.STA'
        if not os.path.isfile(src):
            errmsg = '[ERROR] Failed to find .STA file {:}'.format(src)
            deltmp(tmp_files)
            raise RuntimeError(errmsg)
        dest = os.path.join(campaign_dir, 'STA', os.path.basename(stainf) + '.STA')
        os.symlink(src, dest)
        print('[DEBUG] Linked file {:} to {:}'.format(src, dest))
        tmp_files.append(dest)

    ## if the atx file is not in campaign's OUT dir, link it there
    if os.path.dirname(atxinf) != os.path.join(campaign_dir, 'OUT'):
        src = atxinf
        if not os.path.isfile(src):
            errmsg = '[ERROR] Failed to find .ATX file {:}'.format(src)
            deltmp(tmp_files)
            raise RuntimeError(errmsg)
        dest = os.path.join(campaign_dir, 'OUT', os.path.basename(atxinf))
        os.symlink(src, dest)
        print('[DEBUG] Linked file {:} to {:}'.format(src, dest))
        tmp_files.append(dest)
    
    ## Set variables in PCF file
    pcf_file = os.path.join(os.getenv('U'), 'PCF', 'ATX2PCV.PCF')
    if not os.path.isfile(pcf_file):
        errmsg = '[ERROR] Failed to find PCF file {:}'.format(pcf_file)
        deltmp(tmp_files)
        raise RuntimeError(errmsg)

    pcf = bpcf.PcfFile(pcf_file)
    for var, value in zip(['ATXINF', 'PCVINF', 'STAINF', 'PHGINF', 'PCV', 'RECINF'],[os.path.basename(atxinf), '', os.path.basename(stainf), phginf, kwargs['pcvext'].upper(), kwargs['recinf']]):
        pcf.set_variable('V_'+var, value, 'rundd {}'.format(datetime.datetime.now().strftime('%Y%m%dT%H%M%S')))
    pcf.dump(os.path.join(os.getenv('U'), 'PCF', 'A2P_DD.PCF'))
    pcf_file = os.path.join(os.getenv('U'), 'PCF', 'A2P_DD.PCF')
    tmp_files.append(pcf_file)
    
    ## call the ntua_a2p.pl script to run the PCF
    PID = '{}'.format(os.getpid())
    SESSION = '{:}0'.format(dt.strftime('%j'))
    bern_task_id = kwargs['campaign'].upper()[0] + 'A2P'
    bern_log_fn = os.path.join(campaign_dir, 'BPE', '{:}-{:}{:}.log'.format(kwargs['campaign'], bern_task_id, dt.strftime('%y%j')))
    print('[DEBUG] Started ATX2PCV conversion (log: {:})'.format(bern_log_fn))
    with open(bern_log_fn, 'w') as logf:
        subprocess.call(['{:}'.format(os.path.join(os.getenv('U'), 'SCRIPT', 'ntua_a2p.pl')), '{:}'.format(dt.strftime('%Y')), SESSION, '{:}'.format(kwargs['campaign']), pcf_file, PID], stdout=logf, stderr=logf)
    
    ## error checking
    bpe_status_file = os.path.join(campaign_dir, 'BPE', 'A2P_{}.RUN'.format(PID))
    if bpe.check_bpe_status(bpe_status_file)['error'] == 'error':
        errlog = os.path.join(campaign_dir, 'BPE', 'bpe_a2p_error_{}.log'.format(os.getpid()))
        print('[ERROR] ATX2PCV failed due to error! see log file {:}'.format(errlog), file=sys.stderr)
        bpe.compile_error_report(bpe_status_file, os.path.join(os.getenv('P'), kwargs['campaign']), PID, errlog)
        deltmp(tmp_files)
        return None
    
    ## remove everything from BPE that matches: [PID][SESSION]_[0-9]+_[0-9]+.[LOG|PRT]
    pattern = '{}{}'.format(PID, SESSION) + r"_[0-9]+_[0-9]+\.[LOGPRT]+"
    for file in os.listdir(os.path.join(campaign_dir, 'BPE')):
        if re.match(pattern, file):
            tmp_files.append(os.path.join(os.path.join(campaign_dir, 'BPE', file)))

    ## result (.PHG) file should be in campaign's OUT dir; move it to tables/pcv
    if not os.path.isfile(os.path.join(campaign_dir, 'OUT', phginf + '.PHG')):
        deltmp(tmp_files)
        errmsg = '[ERROR] BPE reported no error, but result file {:} not found!'.format(os.path.join(campaign_dir, 'OUT', phginf + '.PHG'))
        raise RuntimeError(errmsg)
    
    if 'pcvout' not in kwargs or kwargs['pcvout'] is None:
        # kwargs['pcvout'] = os.path.basename(atxinf[0:-3]) + '.PCV'
        kwargs['pcvout'] = os.path.basename(atxinf[0:-3]) + '.' + kwargs['pcvext']
    else:
        kwargs['pcvout'] += '.' + kwargs['pcvext']
    os.rename(os.path.join(campaign_dir, 'OUT', phginf + '.PHG'), kwargs['pcvout'])

    ## remove un-needed files
    deltmp(tmp_files)

    return kwargs['pcvout']
