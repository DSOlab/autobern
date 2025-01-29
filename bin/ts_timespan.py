#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import re
import argparse
import datetime
from pybern.products.fileutils.keyholders import parse_key_file
from pybern.products.gnssdb_query import parse_db_credentials_file, query_sta_in_net
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from math import ceil

class myFormatter(argparse.ArgumentDefaultsHelpFormatter,
                  argparse.RawTextHelpFormatter):
    pass

parser = argparse.ArgumentParser(
    formatter_class=myFormatter,
    description=
    'Given a network name, plot a couple of ',
    epilog=('''National Technical University of Athens,
    Dionysos Satellite Observatory\n
    Send bug reports to:
    Xanthos Papanikolaou, xanthos@mail.ntua.gr
    Dimitris Anastasiou,danast@mail.ntua.gr
    December, 2022'''))

parser.add_argument('-n',
                    '--network',
                    metavar='NETWORK',
                    dest='network',
                    required=True,
                    help='Network to consider')
parser.add_argument('-c',
                    '--credentials-file',
                    required=True,
                    help='Credentials to access the data base',
                    metavar='CREDENTIALS_FILE',
                    dest='credentials_file',
                    default=None)
parser.add_argument('-l',
                    '--log-dir',
                    required=False,
                    help='Directory where log files are stored',
                    metavar='LOG_DIRECTORY',
                    dest='log_dir',
                    default=os.getcwd())
parser.add_argument('--from',
                    required=False,
                    help='Starting epoch',
                    metavar='DATE_FROM',
                    dest='date_start',
                    type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'),
                    default=datetime.datetime.min)
parser.add_argument('--to',
                    required=False,
                    help='Ending epoch',
                    metavar='DATE_END',
                    dest='date_end',
                    type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'),
                    default=datetime.datetime.max)
parser.add_argument('-s',
                    '--reference_sta',
                    required=False,
                    help='The reference .STA file; if not specified, download https://www.epncb.oma.be/ftp/station/general/EUREF52.STA',
                    metavar='REFERENCE_STA',
                    dest='reference_sta',
                    default=None)
#parser.add_argument('-o',
#                    '--sta-file',
#                    required=True,
#                    help='The resulting .STA file, which holds records for all stations in network if they are recorded either in the reference .STA file or have a valid log file in the LOG_DIRECTORY dir',
#                    metavar='OUT_STA',
#                    dest='out_sta',
#                    default=None)
parser.add_argument('--skip-log-error',
    action='store_true',
    help='If not set, then the program will stop in case a log file cannot be parsed; if set, erronuous log files will be  skipped',
    dest='skip_log_error')

def parse_ts(tsfile, idct, sta, tstart, tend):
    dct = idct
    with open(tsfile, 'r') as fin:
        for line in fin.readlines():
            l = line.split()
            t = datetime.datetime.strptime(' '.join([l[0], l[1]]), '%Y-%m-%d %H:%M:%S')
            if t >= tstart and t < tend:
                if t not in dct:
                    dct[t] = [sta]
                else:
                    dct[t].append(sta)
    return dct


def dct2stalist(dct):
    stalist = []
    for t in dct:
        for s in dct[t]:
            if s not in stalist: stalist.append(s)
    return stalist

def dct2xy(dct, sta, val=1):
    x = []; y = []
    for t in dct:
        if sta in dct[t]:
            x.append(t)
            y.append(val)
    return x,y

def minmaxt(dct):
    mint = datetime.datetime.max
    maxt = datetime.datetime.min
    for t in dct:
        if t > maxt: maxt = t
        if t < mint: mint = t
    return mint, maxt

def deltayears(fromd, tod):
    return (tod - fromd).days / 365.25e0

def hist_data(dct, site):
    mint = datetime.datetime.max
    maxt = datetime.datetime.min
    numpts = 0
    for t in dct:
        if site in dct[t]:
            if t > maxt: maxt = t
            if t < mint: mint = t
            numpts += 1
    return numpts, deltayears(mint, maxt)

def plot_hist(dct, saveas):
    sites = dct2stalist(dct)
    n = len(sites)
    days_per_site = []
    span_per_site = []
    for idx,site in enumerate(sites):
        days, span = hist_data(dct, site)
        days_per_site.append(days)
        span_per_site.append(span)

    hcol = 'lightcoral'
    fig, (ax1, ax2) = plt.subplots(1, 2)
    counts, bins = np.histogram(days_per_site)
    ax1.hist(days_per_site, density=False, bins=bins, color=hcol)
    ax1.set_title('Number of days per site [days]')
    #mint,maxt=minmaxt(dct)
    #idy = ceil(deltayears(mint,maxt))
    counts, bins = np.histogram(span_per_site)
    #print(counts,bins)
    #bins = max(idy,bins)
    ax2.hist(span_per_site, density=False, bins=bins, color=hcol)
    ax2.set_title('Span per site [years]')
    plt.savefig(saveas, orientation='landscape', transparent=True)

def plot_ts(dct,saveas):
    colors = ['lightcoral', 'rosybrown', 'indianred', 'thistle']
    Nc = len(colors)
    font = {'family': 'serif',
        'color':  'darkred',
        'weight': 1,
        'size': 5,
    }

    sites = dct2stalist(dct)
    n = len(sites)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_ylim(-1,n+1)
    for i in range(n):
        site = sites[i]
        siteval = i
        x,y=dct2xy(dct,site,siteval)
        ax.scatter(x,y,s=2,c=colors[i%Nc],marker='o')
        ax.axhline(y=siteval,linewidth=.5,linestyle='--',c=colors[i%Nc])

    if n < 15:
        ax.set_yticks(range(n))
        ax.set_yticklabels(sites, font)
    else:
        ax2=ax.twinx()
        ax2.set_ylim(-1,n+1)
        ax2.set_yticks(range(n))
        labels = [ [x,''][i%2] for i,x in enumerate(sites) ]
        ax2.set_yticklabels(labels, font)
        ax.set_yticks(range(n))
        labels = [ ['',x][i%2] for i,x in enumerate(sites) ]
        ax.set_yticklabels(labels, font)

    mint,maxt = minmaxt(dct)
    ## see https://matplotlib.org/stable/gallery/text_labels_and_annotations/date.html
    if deltayears(mint,maxt) <= 1e0:
        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 4)))
        ax.xaxis.set_minor_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%b'))
    elif deltayears(mint,maxt) <= 3e0:
        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 6)))
        ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=(1, 3)))
        ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%b'))
    elif deltayears(mint,maxt) <= 5e0:
        ax.xaxis.set_major_locator(mdates.YearLocator(1,month=1,day=1))
        ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=(1, 6)))
        ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%b'))
    elif deltayears(mint,maxt) <= 12e0 :
        ax.xaxis.set_major_locator(mdates.YearLocator(2,month=1,day=1))
        ax.xaxis.set_minor_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    else :
        ax.xaxis.set_major_locator(mdates.YearLocator(4,month=1,day=1))
        ax.xaxis.set_minor_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    
    ax.get_xticklabels(which='major')[0].set(rotation=30, horizontalalignment='right')

    plt.savefig(saveas, orientation='landscape', transparent=True)

if __name__ == '__main__':

    ## parse command line arguments
    args = parser.parse_args()
    
    ## query database ...
    db_credentials_dct = parse_db_credentials_file(args.credentials_file)
    netsta_dct = query_sta_in_net(args.network, db_credentials_dct)
    
    ## make a list of 4-char ids
    netsta_list = [ dct['mark_name_DSO'] for dct in netsta_dct ]
    
    ## parse the config file (if any)
    options = parse_key_file(args.credentials_file)
    
    ## path to ts files
    ts_path = options['PATH_TO_TS_FILES']

    ## dictionary to hold results:
    dct = {}
    ## e.g. dct[datetime(2022,01,01)] = ['dion', 'akyr', ...]

    ## for every station of the network ...
    for sta in netsta_list:
        ## check if we have a ts file
        tsfile_final = os.path.join(ts_path, sta.lower(), sta.lower()+'.cts')
        if not os.path.isfile(tsfile_final):
            print('[DEBUG] No final ts file found for site: {:}'.format(sta), file=sys.stderr)
        else:
            dct = parse_ts(tsfile_final, dct, sta, args.date_start, args.date_end)

    ## plot
    plot_ts(dct, args.network.lower() + '_time_span.png')
    print('Time span plot for network dumped at file {:}'.format(args.network.lower() + '_time_span.png'))
    plot_hist(dct, args.network.lower() + '_histogram.png')
    print('Histogram plot for network dumped at file {:}'.format(args.network.lower() + '_histogram.png'))
