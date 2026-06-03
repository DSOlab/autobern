#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import os
import sys

from pybern.products.fileutils.keyholders import parse_key_file
import pybern.products.uploaders.uploaders as upld


def expand_path(value):
    if value is None:
        return None
    return os.path.expanduser(os.path.expandvars(value))


def main():
    parser = argparse.ArgumentParser(
        description='Sync a local folder to a remote server with lftp using a config file.')

    parser.add_argument(
        '--config-file',
        dest='config_file',
        required=True,
        help='Path to the config file containing SAVE_DIR_HOST, SAVE_DIR_DIR, SAVE_DIR_URN, SAVE_DIR_PSS, and/or SAVE_DIR.')

    parser.add_argument(
        '--local-dir',
        dest='local_dir',
        required=False,
        help='Local directory to synchronize. If omitted, uses SAVE_DIR from the config file.')

    parser.add_argument(
        '--host',
        dest='host',
        required=False,
        help='Remote host. If omitted, uses SAVE_DIR_HOST from the config file.')

    parser.add_argument(
        '--remote-dir',
        dest='remote_dir',
        required=False,
        help='Remote directory on the host. If omitted, uses SAVE_DIR_DIR from the config file.')

    parser.add_argument(
        '--username',
        dest='username',
        required=False,
        help='Remote username. If omitted, uses SAVE_DIR_URN from the config file or anonymous.')

    parser.add_argument(
        '--password',
        dest='password',
        required=False,
        help='Remote password. If omitted, uses SAVE_DIR_PSS from the config file or empty string.')

    parser.add_argument(
        '--exclude',
        dest='exclude_globs',
        action='append',
        default=[],
        metavar='GLOB',
        help='Exclude files matching this glob when syncing. Can be used multiple times.')

    parser.add_argument(
        '--parallel',
        dest='parallel',
        type=int,
        default=3,
        help='Number of parallel transfers to use in lftp.')

    parser.add_argument(
        '--verbose',
        dest='verbose',
        action='store_true',
        help='Show verbose output from the lftp sync command.')



    args = parser.parse_args()

    try:
        options = {
            key.lower(): value
            for key, value in parse_key_file(args.config_file).items()
        }
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)

    for key, value in list(options.items()):
        if isinstance(value, str):
            if value.upper().strip() == 'YES':
                options[key] = True
                continue
            if value.upper().strip() == 'NO':
                options[key] = False

    local_dir = expand_path(args.local_dir or options.get('save_dir'))
    host = args.host or options.get('save_dir_host')
    remote_dir = args.remote_dir or options.get('save_dir_dir')
    username = args.username or options.get('save_dir_urn', 'anonymous')
    password = args.password or options.get('save_dir_pss', '')

    if not local_dir:
        print('[ERROR] Local directory not specified and SAVE_DIR is missing from config.', file=sys.stderr)
        sys.exit(1)

    if not host:
        print('[ERROR] Remote host not specified and SAVE_DIR_HOST is missing from config.', file=sys.stderr)
        sys.exit(1)

    if not remote_dir:
        print('[ERROR] Remote directory not specified and SAVE_DIR_DIR is missing from config.', file=sys.stderr)
        sys.exit(1)

    if not os.path.isdir(local_dir):
        print('[ERROR] Local directory does not exist: {:}'.format(local_dir), file=sys.stderr)
        sys.exit(1)

    try:
        upld.lftp_sync_folder(
            host,
            remote_dir,
            local_dir,
            username,
            password,
            exclude_globs=args.exclude_globs or None,
            parallel=args.parallel,
            only_newer=True,
            verbose=args.verbose,
            reverse=True)
        print('[INFO] Synchronized local directory {:} to remote {:}:{:}'.format(local_dir, host, remote_dir))
    except Exception as exc:
        print('[ERROR] lftp sync failed: {:}'.format(exc), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
