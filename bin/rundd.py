#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import re
import argparse
import subprocess
import datetime
import atexit
from shutil import copyfile
import pybern.products.rnxdwnl_impl as rnxd
import pybern.products.fileutils.decompress as dcomp
from pybern.products.fileutils.keyholders import parse_key_file
from pybern.products.gnssdb_query import parse_db_credentials_file, query_sta_in_net
from pybern.products.codesp3 import get_sp3
from pybern.products.codeerp import get_erp
from pybern.products.codeion import get_ion
from pybern.products.codedcb import get_dcb
from pybern.products.euref.utils import get_euref_exclusion_list
from pybern.products.bernparsers.bern_crd_parser import parse_bern52_crd
import pybern.products.vmf1 as vmf1
import pybern.products.bernparsers.bernsta as bsta
import pybern.products.bernparsers.bernpcf as bpcf
import pybern.products.bernbpe as bpe

##
crx2rnx_dir='/home/bpe/applications/RNXCMP_4.0.6_Linux_x86_64bit/bin/'
if not os.path.isdir(crx2rnx_dir):
    print('[ERROR] Invalid crx2rnx bin dir {:}'.format(crx2rnx_dir), file=sys.stderr)
    sys.exit(1)
##
log_dir='/home/bpe/data/proclog'
if not os.path.isdir(log_dir):
    print('[ERROR] Invalid temp/proc dir {:}'.format(log_dir), file=sys.stderr)
    sys.exit(1)

##
#def path2dirs(pth):
#    dirs = []
#    it = 0
#    g = re.match(r"\/?([\$a-zA-Z0-9]+)\/?", pth)
#    while g:
#        dirs.append(g.group(1))
#        pth = pth.replace(g.group(0), '')
#        g=re.match(r"\/?([\$a-zA-Z0-9]+)\/?", pth)
#        it += 1
#        if it > 100:
#            print('[ERROR] Failed to resolve path to dirs! path is \'{:}\''.format(pth))
#            return []
#    return dirs
#
#def addtopath_load(bfn):
#    if not os.path.isfile(bfn):
#        print('[ERROR] Invalid LOADGPS.setvar file {:}'.format(bfn), file=sys.stderr)
#        sys.exit(1)
#    with open(bfn, 'r') as fin:
#        for line in fin.readlines():
#            ## skip the addtopath function decleration (if any)
#            if line.startswith('addtopath') and not re.match(r"addtopath()", line.strip()):
#                #print('>>{:}'.format(line))
#                dirs = path2dirs(line.split[1].strip().strip('"'))
#                if dirs == []:
#                    raise RuntimeError('Failed to resolve path!')
#                for i in range(len(dirs)):
#                    if dirs[i].startswith('$'):
#                        dirs[i] = os.getenv(dirs[i][1:])
#                # pth2add = os.path.join(dirs)
#                os.environ["PATH"] += os.pathsep + os.pathsep.join(dirs)
#    return

## list of temporary files created during program run that beed to be deleted 
## before exit
temp_files = []

def cleanup(tmp_file_list, verbosity=False):
    ## verbose print
    verboseprint = print if int(verbosity) else lambda *a, **k: None
    
    for f in tmp_file_list:
        try:
            verboseprint('[DEBUG] Removing temporary file {:} atexit ...'.format(f), end='')
            os.remove(f)
            verboseprint(' done')
        except:
            verboseprint(' failed')
            #pass
    return

## callback function to be called at exit
atexit.register(cleanup, temp_files, True)

def stainf2fn(stainf, tables_dir, campaign):
    """ Form and return a valid (aka existing) .STA file based on input 
        parameters
        stainf: Filename of the .STA file, excluding the '.STA' extension
        tables_dir: tables/ directory; the function expects that the .STA file
                should be located at tables/sta/ directory
        campaifn: Name of campaign; if the .STA file is not found in the 
                tables_dir/sta/ folder, hen the function will search for the
                file in $P/$campaign/STA
    """
    stainf_fn = os.path.join(tables_dir, 'sta', stainf+'.STA')
    if os.path.isfile(stainf_fn): return stainf_fn

    stainf_fn = os.path.join(os.getenv('P'), campaign, 'STA', stainf+'.STA')
    if os.path.isfile(stainf_fn): return stainf_fn
    
    raise RuntimeError('ERROR Failed to locate .STA file')

def match_rnx_vs_sta(rinex_holdings, stafn, dt):
    sta = bsta.BernSta(stafn)
    binfo = sta.parse().filter([s[0:4].upper() for s in rinex_holdings ], True)

    for station in rinex_holdings:
        stainf = binfo.station_info(station.upper(), True)
        if stainf is None:
            print('[ERROR] Failed to find Type 002 entry for station {:} (file: {:})'.format(station.upper(), stafn))
            return 1
        matched = False
        for t2entry in stainf['type002']:
            domes = t2entry.sta_name[4:] if len(t2entry.sta_name)>4 else ''
            if t2entry.start_date <= dt and t2entry.stop_date >= dt:
                matched = True
                break
        if not matched:
            print('[ERROR] No valid entry found in STA file {:} for station {:} and date {:}'.format(stafn, station, dt.strftime('%Y%m%d %H:%M:%S'), file=sys.stderr))
            return 1

        rinex_holdings[station]['domes'] = domes

    return 0;
    
def mark_exclude_stations(station_list, rinex_holdings):
   for station in rinex_holdings:
       if station in station_list:
           rinex_holdings[station]['exclude'] = True
           print('[DEBUG] Marking station {:} as excluded! will not be processed.'.format(station))

def products2dirs(product_dict, campaign_dir, temp_files=None):
    sp3 = product_dict['sp3']['local']
    _, sp3 = dcomp.os_decompress(sp3, True)
    target = os.path.join(campaign_dir, 'ORB', os.path.basename(sp3))
    target = re.sub(r"\.[A-Za-z0-9]{3}$", ".PRE", target)
    os.rename(sp3, target)
    if temp_files is not None: temp_files.append(target)

    erp = product_dict['erp']['local']
    _, erp = dcomp.os_decompress(erp, True)
    os.rename(erp, os.path.join(campaign_dir, 'ORB', os.path.basename(erp)))
    if temp_files is not None: temp_files.append(os.path.join(campaign_dir, 'ORB', os.path.basename(erp)))

    ion = product_dict['ion']['local']
    _, ion = dcomp.os_decompress(ion, True)
    os.rename(ion, os.path.join(campaign_dir, 'ATM', os.path.basename(ion)))
    if temp_files is not None: temp_files.append(os.path.join(campaign_dir, 'ATM', os.path.basename(ion)))
    
    dcb = product_dict['dcb']['local']
    _, dcb = dcomp.os_decompress(dcb, True)
    os.rename(dcb, os.path.join(campaign_dir, 'ORB', os.path.basename(dcb)))
    if temp_files is not None: temp_files.append(os.path.join(campaign_dir, 'ORB', os.path.basename(dcb)))
    
    vmf = product_dict['vmf1']['local']
    os.rename(vmf, os.path.join(campaign_dir, 'ATM', os.path.basename(vmf)))
    if temp_files is not None: temp_files.append(os.path.join(campaign_dir, 'ATM', os.path.basename(vmf)))

def prepare_products(dt, credentials_file, product_dir=None, verbose=False, temp_files=None):
    ## write product information to a dictionary
    product_dict = {}

    if product_dir is None: product_dir = os.getcwd()

    ## download sp3
    for count,orbtype in enumerate(['final', 'final-rapid', 'early-rapid', 'ultra-rapid', 'current']):
        try:
            status, remote, local = get_sp3(type=orbtype, pydt=dt, save_dir=product_dir)
            verboseprint('[DEBUG] Downloaded orbit file {:} of type {:} ({:})'.format(local, orbtype, status))
            product_dict['sp3'] = {'remote': remote, 'local': local, 'type': orbtype}
            break
        except:
            verboseprint('[DEBUG] Failed downloading sp3 file of type {:}'.format(orbtype))

    ## download erp
    for count,erptype in enumerate(['final', 'final-rapid', 'early-rapid', 'ultra-rapid', 'current']):
        try:
            status, remote, local = get_erp(type=erptype, pydt=dt, span='daily', save_dir=product_dir)
            verboseprint('[DEBUG] Downloaded erp file {:} of type {:} ({:})'.format(local, erptype, status))
            product_dict['erp'] = {'remote': remote, 'local': local, 'type': erptype}
            break
        except:
            verboseprint('[DEBUG] Failed downloading erp file of type {:}'.format(erptype))
    
    ## download ion
    for count,iontype in enumerate(['final', 'rapid', 'current']):
        try:
            status, remote, local = get_ion(type=erptype, pydt=dt, save_dir=product_dir)
            verboseprint('[DEBUG] Downloaded ion file {:} of type {:} ({:})'.format(local, iontype, status))
            product_dict['ion'] = {'remote': remote, 'local': local, 'type': iontype}
            break
        except:
            verboseprint('[DEBUG] Failed downloading ion file of type {:}'.format(iontype))
    
    ## download dcb
    days_dif = (datetime.datetime.now() - dt).days
    if days_dif > 0 and days_dif < 30:
            status, remote, local = get_dcb(type='current', obs='full', save_dir=product_dir)
            product_dict['dcb'] = {'remote': remote, 'local': local, 'type': 'full'}
    elif days_dif >= 30:
            status, remote, local = get_dcb(type='final', pydt=dt, obs='p1p2all', save_dir=product_dir)
            product_dict['dcb'] = {'remote': remote, 'local': local, 'type': 'p1p2all'}
    else:
        print('[ERROR] Don\'t know what DCB product to download!')
        raise RuntimeError
    
    ## if we failed throw, else decompress
    for product in ['sp3', 'erp', 'ion', 'dcb']:
        if product not in product_dict:
            print('[ERROR] Failed to download (any) {:} file! Giving up ...'.format(product), file=sys.stderr)
            raise RuntimeError
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
        'credentials_file': credentials_file,
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

    return product_dict
    
def rinex2raw(rinex_holdings, campaign_name, cp_not_mv=False, temp_files=None):
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

            if temp_files is not None:
                try:
                    index = temp_files.index(dct['local'])
                    temp_files[index] = new_holdings[station]['local']
                except ValueError as e:
                    temp_files.append(new_holdings[station]['local'])

        else:
            new_holdings[station] = rinex_holdings[station]
    return new_holdings

def rinex2uppercase(rinex_holdings, temp_files=None):
    new_holdings = {}
    for station, dct in rinex_holdings.items():
        if dct['local'] is not None and not dct['exclude']:
            fn = os.path.basename(dct['local'])
            pth = os.path.dirname(dct['local'])
            fnu = fn.upper()
            os.rename(dct['local'], os.path.join(pth, fnu))
            new_holdings[station] = rinex_holdings[station]
            new_holdings[station]['local'] = os.path.join(pth, fnu)
            
            if temp_files is not None:
                try:
                    index = temp_files.index(dct['local'])
                    temp_files[index] = new_holdings[station]['local']
                except ValueError as e:
                    temp_files.append(new_holdings[station]['local'])
        else:
            new_holdings[station] = rinex_holdings[station]
    return new_holdings

def decompress_rinex(rinex_holdings):
    """ rinex_holdings = {'pdel': {
        'local': '/home/bpe/applications/autobern/bin/pdel0250.16d.Z', 
        'remote': 'https://cddis.nasa.gov/archive/gnss/data/daily/2016/025/16d/pdel0250.16d.Z'}, 
        'hofn': {...}}
        The retuned dictionary is a copy of the input one, but the names of the
        'local' rinex have been changed to the uncompressed filenames
    """
    new_holdings = {}
    for station, dct in rinex_holdings.items():
        if dct['local'] is not None and not dct['exclude']:
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
                    new_holdings[station] = rinex_holdings[station] ##{'local': rnx, 'remote': dct['remote'], 'exclude': dct['exclude']}
                    new_holdings[station]['local'] = rnx
            
            elif crnx.endswith('d') or crnx.endswith('crx'):
                ## else if hatanaka compressed
                drnx, rnx = dcomp.crx2rnx(crnx, True, crx2rnx_dir)
                new_holdings[station] = rinex_holdings[station] ##{'local': rnx, 'remote': dct['remote'], 'exclude': dct['exclude']}
                new_holdings[station]['local'] = rnx
            
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
        # print('[ERROR] Compiling error report to {:}'.format(err_report), file=sys.stderr)
        bpe.compile_error_report(bpe_status_file, os.path.join(os.getenv('P'), options['campaign'].upper()), errlog)
    sys.exit(9)

def link2campaign(options, dt, tmp_file_list=None):
    PDIR = os.path.abspath(os.path.join(os.getenv('P'), options['campaign'].upper()))
    TDIR = os.path.abspath(options['tables_dir'])
    link_dict = []
    ## reference crd/vel/psd files
    src = os.path.join(TDIR, 'crd', options['refinf'].upper()+'_R.CRD')
    dest = os.path.join(PDIR, 'STA', os.path.basename(src))
    link_dict.append({'src': src, 'dest': dest})
    
    src = os.path.join(TDIR, 'crd', options['refinf'].upper()+'_R.VEL')
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
    dest = os.path.join(PDIR, 'STA', os.path.basename(src))
    link_dict.append({'src': src, 'dest': dest})

    ## blq file (if any)
    if options['blqinf'] is not None and options['blqinf'].strip() != '':
        src = os.path.join(TDIR, 'blq', options['blqinf'].upper()+'.BLQ')
        dest = os.path.join(PDIR, 'STA', os.path.basename(src))
        link_dict.append({'src': src, 'dest': dest})

    ## pcv file if at tables/pcv and not in GEN
    pcv_file = options['pcvinf'].upper() + '.' + options['pcvext'].upper()
    if not os.path.isfile(os.path.join(os.getenv('X'), 'GEN', pcv_file)):
        pcv_path = os.path.join(TDIR, 'pcv')
        if not os.path.isfile(os.path.join(TDIR, pcv_path, pcv_file)):
            errmsg = '[ERROR] Failed to find PCV file {:} in neither tables dir or GEN!'.format(pcv_file)
            raise RuntimeError(errmsg)
        link_dict.append({'src': os.path.join(TDIR, pcv_path, pcv_file), 'dest': os.path.join(os.getenv('X'), 'GEN', pcv_file)})

    for pair in link_dict:
        print('[DEBUG] Linking source {:} to {:}'.format(pair['src'], pair['dest']))
        os.symlink(pair['src'], pair['dest'])
        if tmp_file_list is not None:
            tmp_file_list.append(pair['dest'])

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
                    '--skip-rinex-download',
                    action='store_true',
                    help='Skip download of RINEX files; only consider RINEX files already available for network/date',
                    dest='skip_rinex_download')
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
        if v.upper() == "YES": options[k] = True
        elif v.upper() == "NO": options[k] = False
    for k,v in vars(args).items():
        if v is not None:
            options[k.lower()] = v
        elif v is None and k not in options:
            options[k.lower()] = v

    ##
    print('------------------------------------------------------------------')
    for k in options: print('{:.20s} -> {:}'.format(k, options[k]))
    print('------------------------------------------------------------------')

    ## verbose print
    verboseprint = print if options['verbose'] else lambda *a, **k: None

    ## check that the campaign directory exists

    ## date we are solving for as datetime instance
    dt = datetime.datetime.strptime('{:}-{:03d}'.format(options['year'], int(options['doy'])), '%Y-%j')

    ## if the user specified an ATX file, run the ATX2PCV script
    if options['atxinf'] != None and options['atxinf'].strip() != '':
        atx2pcv(options, dt, temp_files)

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
    if args.skip_rinex_download:
        rinex_holdings = {}
    else:
        rinex_holdings = rnxd.main(**rnxdwnl_options)


    ## for every station add a field in its dictionary ('exclude') denoting if 
    ## the station needs to be excluded from the processing
    for station in rinex_holdings:
        rinex_holdings[station]['exclude'] = False
        rinex_holdings[station]['domes'] = None

    ## check if we need to exclude station from EUREF's list
    if options['use_epn_exclude_list']:
        mark_exclude_stations(get_euref_exclusion_list(dt), rinex_holdings)

    ## check if we have a file with stations to exclude
    if options['exclusion_list'] is not None:
        staexcl = []
        with open(options['exclusion_list'], 'r') as fin:
            staexcl = [x.split()[0].lower() for x in fin.readlines()]
        mark_exclude_stations(staexcl, rinex_holdings)

    ## get info on the stations that belong to the network, aka
    ## [{'station_id': 1, 'mark_name_DSO': 'pdel', 'mark_name_OFF': 'pdel',..},{...}]
    db_credentials_dct = parse_db_credentials_file(options['config_file'])
    netsta_dct = query_sta_in_net(options['network'], db_credentials_dct)

    ## uncompress (to obs) all RINEX files of the network/date
    rinex_holdings = decompress_rinex(rinex_holdings)

    ## validate stations using the STA file and get domes
    stafn = stainf2fn(options['stainf'], options['tables_dir'], options['campaign'].upper())
    if match_rnx_vs_sta(rinex_holdings, stafn, dt) > 0:
        print('[ERROR] Aborting processing!', file=sys.stderr)
        sys.exit(1)

    ## download and prepare products
    try:
        products_dict = prepare_products(dt, options['config_file'], os.getenv('D'), options['verbose'])
    except Exception as e:
        print('[ERROR] Failed to download products! Traceback info {:}'.format(e), file=sys.stderr)
        sys.exit(1)
    products2dirs(products_dict, os.path.join(os.getenv('P'), options['campaign'].upper()), temp_files)

    ## check that we have at least min_reference_sites reference sites included
    ## in the processing
    if options['min_reference_sites'] > 0:
        refcrd_fn = options['refinf'] + '_R.CRD'
        refcrd_fn_list = [ os.path.join(x, refcrd_fn) for x in [os.path.join(options['tables_dir'], 'crd'), os.path.join(os.getenv('P'), options['campaign'], 'STA')]]
        refcrd = None
        
        for rfn in refcrd_fn_list:
            if os.path.isfile(rfn):
                refcrd = rfn
                break;
        if refcrd is None:
            print('[ERROR] Failed to find reference coordinate file {:} or {:}'.format(refcrd_fn_list[0], refcrd_fn_list[1]), file=sys.stderr)
            sys.exit(1)

        crddct = parse_bern52_crd(refcrd)
        ref_sta = [ s for s in rinex_holdings if s in crddct ]
        if len(ref_sta) < options['min_reference_sites']:
            print('[ERROR] Too few reference sites available for processing! Stoping the analysis now!', file=sys.stderr)
            sys.exit(1)

    ## transfer (uncompressed) rinex files to the campsign's RAW directory
    ## TODO at production, change cp_not_mv parameter
    rinex_holdings = rinex2raw(rinex_holdings, options['campaign'], True, temp_files)
    ## rinex 2 uppercase
    rinex_holdings = rinex2uppercase(rinex_holdings, temp_files)

    ## make cluster file
    with open(os.path.join(os.getenv('P'), options['campaign'], 'STA', options['campaign']+'.CLU'), 'w') as fout:
        print("""Cluster file automaticaly created by rundd on {:}
--------------------------------------------------------------------------------

STATION NAME      CLU
****************  ***
        """.format(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')), file=fout)
        sta_counter = 0
        for sta in rinex_holdings:
            if rinex_holdings[sta]['local'] is not None and not rinex_holdings[sta]['exclude']:
                print('{:16s}  {:3d}'.format(sta.upper()+' '+rinex_holdings[sta]['domes'], sta_counter//options['files_per_cluster']+1), file=fout)
                sta_counter += 1
    print('[DEBUG] Created cluster file {:} with total number of stations {:}'.format(os.path.join(os.getenv('P'), options['campaign'], 'STA', options['campaign']+'.CLU'), sta_counter))

    ## Set solution identifiers
    solution_id = {'final': options['solution_id'] }
    for descr, sid in zip(['prelim', 'reduced', 'free_net'], [ 'P', 'R', 'N']):
        if options['solution_id'][-1] == sid:
            print('[ERROR] Final solution identifier cannot end in {:}; reserved for {:} solution'.format(sid, descr), file=sys.stderr)
            sys.exit(1)
        solution_id[descr] = options['solution_id'][0:-1] + sid
    for descr, sid in solution_id.items():
        print('[DEBUG] {:} solution identifier set to {:}'.format(descr, sid))

    ## Set variables in PCF file
    pcf_file = os.path.join(os.getenv('U'), 'PCF', options['pcf_file'])
    if not os.path.isfile(pcf_file):
        print('[ERROR] Failed to find PCF file {:}'.format(pcf_file), file=sys.stderr)
        sys.exit(1)
    pcf = bpcf.PcfFile(pcf_file)
    for var, value in zip(['B', 'C', 'E', 'F', 'N', 'BLQINF', 'ATLINF', 'STAINF', 'CRDINF', 'SATSYS', 'PCV', 'PCVINF', 'ELANG', 'FIXINF', 'REFINF', 'REFPSD', 'CLU'],['COD', solution_id['prelim'], solution_id['final'], solution_id['reduced'], solution_id['free_net'], options['blqinf'], options['atlinf'], options['stainf'], options['campaign'].upper(), options['sat_sys'].upper(), options['pcvext'].upper(), options['pcvinf'].upper(), options['elevation_angle'], options['fixinf'], options['refinf'], options['refpsd'], options['files_per_cluster']]):
        pcf.set_variable('V_'+var, value, 'rundd {}'.format(datetime.datetime.now().strftime('%Y%m%dT%H%M%S')))
    pcf.dump(os.path.join(os.getenv('U'), 'PCF', 'RUNDD.PCF'))
    pcf_file = os.path.join(os.getenv('U'), 'PCF', 'RUNDD.PCF')

    ## link needed files from tables_dir to campaign-specifi directories
    link2campaign(options, dt, temp_files)

    ## ready to call the perl script for processing ...
    bpe_start_at = datetime.datetime.now()
    bern_task_id = options['campaign'].upper()[0] + 'DD'
    bern_log_fn = os.path.join(log_dir, '{:}-{:}{:}.log'.format(options['campaign'], bern_task_id, dt.strftime('%y%j')))
    print('[DEBUG] Firing up the Bernese Processing Engine (log: {:})'.format(bern_log_fn))
    with open(bern_log_fn, 'w') as logf:
        addtopath_load(options['b_loadgps'])
        #print('{:}'.format(os.path.join(os.getenv('U'), 'SCRIPT', 'ntua_pcs.pl')), '{:}'.format(dt.strftime('%Y')), '{:}0'.format(dt.strftime('%j')), '{:}'.format(pcf_file), 'USER', '{:}'.format(options['campaign'].upper(), '{:}'.format(bern_task_id)))
        subprocess.call(['{:}'.format(os.path.join(os.getenv('U'), 'SCRIPT', 'ntua_pcs.pl')), '{:}'.format(dt.strftime('%Y')), '{:}0'.format(dt.strftime('%j')), '{:}'.format(pcf_file), 'USER', '{:}'.format(options['campaign'].upper(), '{:}'.format(bern_task_id))], stdout=logf, stderr=logf)

    ## check if we have an error; if we do, make a report
    bpe_status_file = os.path.join(os.getenv('P'), options['campaign'].upper(), 'BPE', options['campaign'].upper()[0:3] + '_.RUN')
    if bpe.check_bpe_status(bpe_status_file)['error'] == 'error':
        errlog = os.path.join(os.getenv('P'), options['campaign'].upper(), 'BPE', 'bpe_error_{}.log'.format(os.getpid()))
        print('[ERROR] BPE failed due to error! see log file {:}'.format(errlog), file=sys.stderr)
        # print('[ERROR] Compiling error report to {:}'.format(err_report), file=sys.stderr)
        bpe.compile_error_report(bpe_status_file, os.path.join(os.getenv('P'), options['campaign'].upper()), errlog)
