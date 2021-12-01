#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import ftplib

## get ftp directory listing
def ftp_dirlist(url, **kwargs):
    """
    :return: An integer denoting the download status; anything other than 0 
             denotes an error

    kwargs:
    dir : directory to get the listing of
    username: 'usrnm' Use the given username
    password: 'psswrd' Use the given password
  """
    ## username or password key(s) in kwargs
    if set(['username', 'password']).intersection(set(kwargs)):
        username = kwargs['username'] if 'username' in kwargs else ''
        password = kwargs['password'] if 'password' in kwargs else ''
    
    rdir = kwargs['dir'] if dir in kwargs else '.'

    ftp = ftplib.FTP(url)
    ftp.login(username, password)
    
    try:
        remote_files = ftp.nlst()
    except ftplib.error_perm:
        raise

    return remote_files
