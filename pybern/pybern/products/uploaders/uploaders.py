#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import ftplib
import os

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
