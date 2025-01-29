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

product_dict = {}
dt = datetime.datetime.today() - datetime.timedelta(days=1)
#ptypes = ['final', 'final-rapid', 'early-rapid', 'ultra-rapid', 'current']
ptypes = ['early-rapid', 'ultra-rapid', 'current']
for count,erptype in enumerate(ptypes):
    #try:
    status, remote, local = get_erp(type=erptype, pydt=dt, span='daily')
    print('[DEBUG] Downloaded erp file {:} of type {:} ({:})'.format(local, erptype, status))
    product_dict['erp'] = {'remote': remote, 'local': local, 'type': erptype}
    break
    #except:
    #    print('[DEBUG] Failed downloading erp file of type {:}'.format(erptype))
    #    if count != len(ptypes) - 1:
    #        print('[DEBUG] Next try for file of type {:}'.format(ptypes[count+1]))
