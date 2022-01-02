#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import re
import datetime

def check_bpe_status(bpe_status):
    if not os.path.isfile(bpe_status):
       errmsg = '[ERROR] BPE Status file {:} not found!'.format(bpe_status)
       raise RuntimeError(errmsg)

    dct = {}
    with open(bpe_status, 'r') as fin:
        for line in fin.readlines():
            if line.strip() != '':
                # Status of RUNDD.PCF at 01-Jan-2022 21:19:07
                if re.match(r"Status of [A-Za-z0-9\.]+ at .*", line.strip()):
                    g = re.match(r"Status of ([A-Za-z0-9\.]+) at (.*)$", line.strip())
                    dct['pcf'] = g.group(1)
                    dct['at'] = datetime.datetime.strptime(str(g.group(2)), "%d-%b-%Y %H:%M:%S")
                # Session 190050: error
                elif re.match(r"Session [0-9a-zA-Z]+:.*", line.strip()):
                    g = re.match(r"Session ([0-9a-zA-Z]+):(.*)", line.strip())
                    dct['session'] = g.group(1)
                    dct['error'] = str(g.group(2)).strip()

    return dct

def find_error_description_in_log(log_file):
    ## fill the following list with dictionaries with keys, 'program', 'description'
    dct = []
    # print('inspecting file {:}'.format(log_file))
    with open(log_file, 'r') as lin:
        line = lin.readline()
        while line:
            if re.match(r"Call to [a-zA-Z0-9_]+ failed:", line.strip()):
                g = re.match(r"Call to ([a-zA-Z0-9_]+) failed:", line.strip())
                dct.append({'program':'', 'description':''})
                dct[len(dct)-1]['program'] = g.group(1)
            elif re.match(r"\*\*\* [a-zA-Z0-9 _]+:.*", line.strip()):
                while line and len(line.strip())>5:
                    dct[len(dct)-1]['description'] += (line.lstrip()+'\n')
                    line = lin.readline()
            line = lin.readline()
    return dct

def compile_error_report(bpe_status, campaign_dir, err_file=None):
    if err_file is not None:
        errfn = open(err_file, 'w')
    else:
        errfn = sys.stderr

    bdct = check_bpe_status(bpe_status)
    print('Error log for BPE; PCF: {:}, started at: {}, Session {:}, Error: {:}'.format(bdct['pcf'], bdct['at'], bdct['session'], bdct['error']), file=errfn)
    for log in os.listdir(os.path.join(campaign_dir, 'BPE')):
        pattern = bdct['session'] + r"_[0-9]+_[0-9]+\.LOG"
        #print('pattern {:} file {:}'.format(bdct['session'] + "_[0-9]+_[0-9]+\.LOG", os.path.basename(log)))
        if re.match(pattern, os.path.basename(log)):
            errors = find_error_description_in_log(os.path.join(campaign_dir, 'BPE', log))
            if errors != []:
                print('Log from file {:}'.format(log), file=errfn)
                for error in errors:
                    print('>> ERROR: {:}, {:}'.format(error['program'], error['description']), file=errfn)

def status_has_error(bpe_status):
    dct = check_bpe_status(bpe_status)
    return dct['error'] == 'error'
