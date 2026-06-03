#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import ftplib
import os
import shlex
import subprocess

def ftp_upload(ip, remote_dir, localf, username, password):
    destination = ip
    if not os.path.isfile(localf):
        msg = '[ERROR] ftp_upload Failed to locate local file {:}'.format(localf)
        raise RuntimeError(msg)
    fn = os.path.basename(localf)
    session = ftplib.FTP(ip, username, password)
    if remote_dir != None and remote_dir.strip() != '':
        session.cwd(remote_dir)
        destination += '/{:}'.format(remote_dir)
    lfn = open(localf,'rb') # file to send
    session.storbinary('STOR {:}'.format(fn), lfn) # send the file
    lfn.close() # close file and FTP
    session.quit()
    destination += '/{:}'.format(fn)
    return localf, destination


def lftp_sync_folder(ip, remote_dir, local_dir, username, password,
                     exclude_globs=None, parallel=3, only_newer=True,
                     verbose=False, reverse=False, create_dirs=True):
    """Synchronize a local directory with a remote server using lftp.

    If reverse is False, the remote directory is mirrored into the local
    directory. If reverse is True, the local directory is mirrored into the
    remote directory.
    """
    if not os.path.isdir(local_dir):
        raise RuntimeError('[ERROR] lftp_sync_folder failed to locate local directory {:}'.format(local_dir))
    if remote_dir is None or remote_dir.strip() == '':
        raise RuntimeError('[ERROR] lftp_sync_folder failed to locate remote directory {:}'.format(remote_dir))

    if exclude_globs is None:
        exclude_globs = []

    args = ['mirror']
    if reverse:
        args.append('--reverse')
    if only_newer:
        args.append('--only-newer')
    if create_dirs:
        args.append('--create-dirs')
    if parallel and int(parallel) > 0:
        args.append('--parallel={:}'.format(int(parallel)))
    if verbose:
        args.append('--verbose')
    for glob in exclude_globs:
        args.extend(['--exclude-glob', glob])
    
    ## When reverse=True (upload), order must be: local_dir remote_dir
    ## When reverse=False (download), order must be: remote_dir local_dir
    if reverse:
        args.append(local_dir)
        args.append(remote_dir)
    else:
        args.append(remote_dir)
        args.append(local_dir)

    lcmd = ' '.join(shlex.quote(item) for item in args) + '; bye'
    process = subprocess.run(
        ['lftp', '-u', '{:},{:}'.format(username, password), '-e', lcmd, ip],
        shell=False,
        universal_newlines=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    if process.returncode:
        stderr = process.stderr.strip()
        if create_dirs and '--create-dirs' in args and "unrecognized option '--create-dirs'" in stderr:
            args = [item for item in args if item != '--create-dirs']
            lcmd = ' '.join(shlex.quote(item) for item in args) + '; bye'
            process = subprocess.run(
                ['lftp', '-u', '{:},{:}'.format(username, password), '-e', lcmd, ip],
                shell=False,
                universal_newlines=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            if process.returncode:
                raise RuntimeError(
                    '[ERROR] lftp_sync_folder failed with code {:}: {:}'.format(
                        process.returncode, process.stderr.strip()))
            return local_dir, remote_dir, process.stdout
        raise RuntimeError(
            '[ERROR] lftp_sync_folder failed with code {:}: {:}'.format(
                process.returncode, stderr))

    return local_dir, remote_dir, process.stdout
