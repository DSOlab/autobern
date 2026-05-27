#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import argparse
import fnmatch
import shutil
import email.utils
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse, unquote
from urllib.request import Request, urlopen
import pybern.products.bernparsers.bloadvar as blvar

DEFAULT_AIUB_BASE_URL = 'https://www.aiub.unibe.ch/download'
AIUB_S3TEST_BASE_URL = 'https://downloadtest.aiub.unibe.ch/'


class DirectoryListingParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() != 'a':
            return
        for key, value in attrs:
            if key.lower() == 'href' and value:
                self.hrefs.append(value)


def url_for(base_url, remote_path):
    return base_url.rstrip('/') + '/' + remote_path.strip('/') + '/'


def remote_timestamp(url):
    try:
        request = Request(url, method='HEAD')
        with urlopen(request, timeout=30) as response:
            last_modified = response.headers.get('Last-Modified')
    except (HTTPError, URLError):
        return None
    if not last_modified:
        return None
    parsed = email.utils.parsedate_to_datetime(last_modified)
    if parsed is None:
        return None
    return parsed.timestamp()


def list_remote_directory(url):
    request = Request(url)
    with urlopen(request, timeout=60) as response:
        content_type = response.headers.get('Content-Type', '')
        if 'html' not in content_type.lower():
            raise RuntimeError('Remote URL does not look like a directory listing: {:}'.format(url))
        html = response.read().decode('utf-8', errors='replace')

    parser = DirectoryListingParser()
    parser.feed(html)
    entries = []
    base_path = urlparse(url).path.rstrip('/') + '/'
    for href in parser.hrefs:
        if href in ('../', './') or href.startswith('#') or href.startswith('?'):
            continue
        absolute_url = urljoin(url, href)
        parsed = urlparse(absolute_url)
        if parsed.scheme not in ('http', 'https') or parsed.netloc != urlparse(url).netloc:
            continue
        if not parsed.path.startswith(base_path):
            continue
        rel_path = unquote(parsed.path[len(base_path):])
        if rel_path == '' or '/' in rel_path.strip('/'):
            continue
        entries.append((rel_path.rstrip('/'), absolute_url, href.endswith('/') or parsed.path.endswith('/')))
    return entries


def download_file(remote_url, local_file, verboseprint):
    tmp_file = local_file + '.tmp'
    with urlopen(Request(remote_url), timeout=120) as response:
        with open(tmp_file, 'wb') as fout:
            shutil.copyfileobj(response, fout)
        last_modified = response.headers.get('Last-Modified')
    if last_modified:
        parsed = email.utils.parsedate_to_datetime(last_modified)
        if parsed is not None:
            os.utime(tmp_file, (parsed.timestamp(), parsed.timestamp()))
    os.replace(tmp_file, local_file)
    verboseprint('[DEBUG] Downloaded {:} -> {:}'.format(remote_url, local_file))


def mirror_https(remote_url, local_dir, exclude_globs, verboseprint):
    os.makedirs(local_dir, exist_ok=True)
    for name, entry_url, is_dir in list_remote_directory(remote_url):
        if is_dir:
            mirror_https(entry_url.rstrip('/') + '/', os.path.join(local_dir, name), exclude_globs, verboseprint)
            continue
        if any(fnmatch.fnmatch(name, pattern) for pattern in exclude_globs):
            verboseprint('[DEBUG] Skipping excluded remote file {:}'.format(entry_url))
            continue

        local_file = os.path.join(local_dir, name)
        rtime = remote_timestamp(entry_url)
        if os.path.isfile(local_file) and rtime is not None and os.path.getmtime(local_file) >= rtime:
            verboseprint('[DEBUG] Skipping newer/equal local file {:}'.format(local_file))
            continue
        download_file(entry_url, local_file, verboseprint)

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
    Dimitris Anastasiou,danastasiou@mail.ntua.gr
    January, 2021
    Update: 2025.05.21 :[DA] update for BERN54
    '''))

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
    help='Specify a Bernese source file (i.e. the file BERN5/LOADGPS.setvar) which can be sourced; if such a file is set, then the local target directory is defined by the variable $X\GEN')

parser.add_argument('--verbose',
                    dest='verbose',
                    action='store_true',
                    help='Trigger verbose run (prints debug messages).')

parser.add_argument('--base-url',
                    metavar='URL',
                    dest='base_url',
                    default=DEFAULT_AIUB_BASE_URL,
                    help='AIUB HTTPS base URL')

parser.add_argument('--s3test',
                    dest='s3test',
                    action='store_true',
                    help='Use AIUB HTTPS test environment ({:})'.format(AIUB_S3TEST_BASE_URL))

parser.add_argument('--remote-dir',
                    metavar='REMOTE_DIR',
                    dest='remote_dir',
                    default='BSWUSER54',
                    help='Remote directory below the AIUB base URL; only used with --target')

if __name__ == '__main__':

    args = parser.parse_args()
    base_url = AIUB_S3TEST_BASE_URL if args.s3test else args.base_url

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
        target_path = blvar.parse_loadvar(args.bern_loadvar)['GLOBAL']
        model_dir = os.path.join(target_path, 'MODEL')
        config_dir = os.path.join(target_path, 'CONFIG')
        verboseprint('[DEBUG] Synchronizing local directory {:}'.format(model_dir))
        verboseprint('[DEBUG] Synchronizing local directory {:}'.format(config_dir))
        target_dir = [model_dir, config_dir]
        remote_dir = ['BSWUSER54/MODEL','BSWUSER54/CONFIG']
    else:
        target_dir = [args.target]
        remote_dir = [args.remote_dir]

    for local in target_dir:    
        if not os.path.isdir(local):
            print('[ERROR] Local GLOBAL path does not exist: {:}'.format(local), file=sys.stderr)
            sys.exit(1)

    for local, remote in zip(target_dir, remote_dir):
        remote_url = url_for(base_url, remote)
        verboseprint('[DEBUG] Mirroring {:} -> {:}'.format(remote_url, local))
        try:
            mirror_https(remote_url, local, ['*.EPH'], verboseprint)
            if args.log_file:
                with open(args.log_file, 'a') as log:
                    print('Mirrored {:} -> {:}'.format(remote_url, local), file=log)
        except Exception as exc:
            print('[ERROR] Mirroring failed for {:}: {:}'.format(remote_url, exc), file=sys.stderr)
            sys.exit(1)


    sys.exit(0)
