#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import subprocess
import argparse
import pybern.products.bernparsers.bloadvar as blvar

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

parser.add_argument(
    '-t',
    '--target',
    metavar='TARGET_DIR',
    dest='target',
    required=False,
    help='Local, target directory to synchronize')

parser.add_argument(
    '-l',
    '--log',
    metavar='LOG_FILE',
    dest='log_file',
    required=False,
    help='Log file to hold mirroring status/records')

parser.add_argument(
    '-b',
    '--bernese-loadvar',
    metavar='BERN_LOADVAR',
    dest='bern_loadvar',
    required=False,
    help='Specify a Bernese source file (i.e. the file BERN52/GPS/EXE/LOADGPS.setvar) which can be sourced; if such a file is set, then the local target directory is defined by the variable $X\GEN')

parser.add_argument('--verbose',
                    dest='verbose',
                    action='store_true',
                    help='Trigger verbose run (prints debug messages).')

if __name__ == '__main__':

    args = parser.parse_args()

    ## verbose print
    verboseprint = print if args.verbose else lambda *a, **k: None

    ##  we must at least have either a target (local) directory or a loadvar 
    ##+ file
    if not args.target and not args.bern_loadvar:
        print('[ERROR] Must at least specify either a target dir or a LOADVAR file', file=sys.stderr)
        sys.exit(1)

    ##  get the local, target dir
    if args.bern_loadvar:
        if not os.path.isfile(args.bern_loadvar):
            print('[ERROR] Failed to find LOADVAR file {:}; exiting'.format(args.bern_loadvar), file=sys.stderr)
            sys.exit(1)
        target_path = blvar.parse_loadvar(args.bern_loadvar)['X']
        target_dir = os.path.join(target_path, 'GEN')
    else:
        target_dir = args.target
    if not os.path.isdir(target_dir):
        print('[ERROR] Local GEN path does not exist: {:}'.format(target_dir), file=sys.stderr)
        sys.exit(1)

    ## mirror one-liner that uses lftp
    lcmd = "mirror --only-newer --parallel=3 --verbose --exclude-glob *.EPH {remote_dir} {local_dir}; bye".format(remote_dir='BSWUSER52/GEN', local_dir=target_dir)
    #result = subprocess.run(
    #    ['lftp', '-u', '{:},{:}'.format('anonymous', 'ntua@ntua.gr'), '-e', '{:}'.format(lcmd), '{:}'.format('ftp.aiub.unibe.ch')], shell=False, check=True)
    result = subprocess.run(
        ['lftp', '-u', '{:},{:}'.format('anonymous', 'ntua@ntua.gr'), '-e', '{:}'.format(lcmd), '{:}'.format('ftp.aiub.unibe.ch')], shell=False, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        print('[ERROR] Mirroring failed with errorcode: {:}'.format(result.returncode), file=sys.stderr)
        print('[ERROR] lftp/shell return lines: {:}'.format(result.stderr))
    else:
        if args.log_file:
            with open(args.log_file, 'w') as log:
                print(result.stdout, file=log)


    sys.exit(0)

