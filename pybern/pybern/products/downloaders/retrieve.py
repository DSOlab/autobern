#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import re
import os
import shutil
from contextlib import closing
import requests
import urllib.request
from urllib.error import HTTPError, URLError
import socket
import ftplib
import paramiko
from scp import SCPClient

def url_split(target):
    return target[0:target.rindex('/')], target[target.rindex('/') + 1:]

def ftp_retrieve_active(ftpip, path, username, password, remote, local):
    status = 1
    ftp = ftplib.FTP(host=ftpip, user=username, passwd=password, acct='', timeout=10)
    # print('--> Downloading active with ftpip=[{:}], path=[{:}], username=[{:}], password=[{:}], remote=[{:}], local=[{:}]'.format(ftpip, path, username, password, remote, local))
    ftp.set_pasv(False)
    if path != '': ftp.cwd(path)
    try:
        ## query size so that we fail if the remote does not exist and no local
        ## file is created
        assert( ftp.size(remote) )
        ftp.retrbinary("RETR " + remote, open(local, 'wb').write)
        status = 0
    except FTP.error_perm:
        os.remove(local)
    ftp.close()
    return status

def ftp_retrieve(url, filename=None, **kwargs):
    """
    :return: An integer denoting the download status; anything other than 0 
             denotes an error

    kwargs:
    save_as:  'foobar' Save remote file as 'foobar' (can include path)
    save_dir: 'foo/bar' Directory to save remote file; if both save_dir and 
               save_as are given, then the local file will be the concatenation
               of these two, aka os.path.join(save_dir, save_as)
    username: 'usrnm' Use the given username
    password: 'psswrd' Use the given password
    active  : (boolean) true or false
    fail_error: True/False Throw exception if download fails. By default
               the function will throw if the download fails
  """
    # print('>> called ftp_retrieve with args: url={:}, filename={:}, kwargs={:}'.format(url, filename, kwargs))
    if filename is None:
        url, filename = url_split(url)
    # print('>> split url and filename to {:} and {:}'.format(url, filename))
    saveas = kwargs['save_as'] if 'save_as' in kwargs else filename
    if 'save_dir' in kwargs:
        if not os.path.isdir(kwargs['save_dir']):
            msg = '[ERROR] retrieve::http_retrieve Directory does not exist {:}'.format(
                kwargs['save_dir'])
            raise RuntimeError(msg)
        saveas = os.path.join(kwargs['save_dir'], saveas)
        # print('>> saveas is now {:}'.format(saveas))
    if not 'fail_error' in kwargs:
        kwargs['fail_error'] = True

    ## username or password key(s) in kwargs
    if set(['username', 'password']).intersection(set(kwargs)):
        username = kwargs['username'] if 'username' in kwargs else ''
        password = kwargs['password'] if 'password' in kwargs else ''
        if (not username or username == '') and (not password or password == ''):
            pass
        else:
            ## need to construct a string of type:
            ## 'ftp://username:password@server/path/to/file' from (url=)
            ## 'server/path/to/file'
            # print('>> using credentials .... ')
            url = re.sub(r'^ftp://', 'ftp://{:}:{:}@'.format(username, password), url)

    target = '{:}/{:}'.format(url, filename)

    status = 0
    
    ## Handle active FTP
    if 'active' in kwargs and kwargs['active'] == True:
        g=re.match(r'ftp://[^@]*([^/]*)(.*)', url)
        ftpip = g.group(1).lstrip('@')
        target = filename
        path = g.group(2).replace(target, '')
        status = ftp_retrieve_active(ftpip, path, username, password, target, saveas)
    else:
        # print(">> Note that target={:}".format(target))
        try:
            with closing(urllib.request.urlopen(target, timeout=10)) as r:
                with open(saveas, 'wb') as f:
                    shutil.copyfileobj(r, f)
        except:
            status = 1
    ## For debugging
    #try:
    #    with closing(urllib.request.urlopen(target, timeout=10)) as r:
    #        with open(saveas, 'wb') as f:
    #            shutil.copyfileobj(r, f)
    #except HTTPError as error:
    #    print('Data not retrieved because {:}\nURL: {}', error, target)
    #except URLError as error:
    #    if isinstance(error.reason, socket.timeout):
    #        print('socket timed out - URL {}', target)
    #    else:
    #        print('some other error happened')
    #    status = 1
    
    if not os.path.isfile(saveas):
        status += 1

    if status > 0 and kwargs['fail_error'] == True:
        msg = '[ERROR] retrieve::ftp_retrieve Failed to download file {:}'.format(
            target)
        raise RuntimeError(msg)

    return status, target, saveas

def createSSHClient(server, port, user, password, timeout):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password, timeout=float(timeout))
    return client

def scp_retrieve(url, filename=None, **kwargs):
    """ Expects url = 'ssh://147.102.106.88/foo/bar/koko.rnx'
    """
    if filename is None:
        url, filename = url_split(url)
    saveas = kwargs['save_as'] if 'save_as' in kwargs else filename
    if 'save_dir' in kwargs:
        if not os.path.isdir(kwargs['save_dir']):
            msg = '[ERROR] retrieve::http_retrieve Directory does not exist {:}'.format(
                kwargs['save_dir'])
            raise RuntimeError(msg)
        saveas = os.path.join(kwargs['save_dir'], saveas)
    if not 'fail_error' in kwargs:
        kwargs['fail_error'] = True
    
    ## username or password key(s) in kwargs
    if set(['username', 'password']).intersection(set(kwargs)):
        username = kwargs['username'] if 'username' in kwargs else ''
        password = kwargs['password'] if 'password' in kwargs else ''

    # Note that the urls is something like:
    # ssh://147.102.106.88/foo/bar/koko.rnx -- get the ip
    g=re.match(r'ssh://(([0-9]{1,3}\.?){4})', url)
    server = g.group(1)
    ## remote (path +)filename
    remote_pfn = os.path.join(url.replace(g.group(0),''), filename) 

    ssh = createSSHClient(server, 9785, username, password, 10)
    scp = SCPClient(ssh.get_transport())
    scp.get(remote_pfn)
    scp.close()

    os.rename(filename, saveas)
    return 0, url, saveas

def http_retrieve(url, filename=None, **kwargs):
    """
    :return: An integer denoting the download status; anything other than 0 
             denotes an error

    kwargs:
    username:  Use this username to access the url.
    password:  Use this password to access the url.
    save_as:  'foobar' Save remote file as 'foobar' (can include path)
    save_dir: 'foo/bar' Directory to save remote file; if both save_dir and 
               save_as are given, then the local file will be the concatenation
               of these two, aka os.path.join(save_dir, save_as)
    fail_error: True/False Throw exception if download fails. By default
               the function will throw if the download fails
  """
    if filename is None:
        url, filename = url_split(url)
    saveas = kwargs['save_as'] if 'save_as' in kwargs else filename
    if 'save_dir' in kwargs:
        if not os.path.isdir(kwargs['save_dir']):
            msg = '[ERROR] retrieve::http_retrieve Directory does not exist {:}'.format(
                kwargs['save_dir'])
            raise RuntimeError(msg)
        saveas = os.path.join(kwargs['save_dir'], saveas)
    if not 'fail_error' in kwargs:
        kwargs['fail_error'] = True

    use_credentials = False
    if set(['username', 'password']).intersection(set(kwargs)):
        use_credentials = True
        username = kwargs['username'] if 'username' in kwargs else ''
        password = kwargs['password'] if 'password' in kwargs else ''
        if (not username or username == '') and (not password or password == ''):
            use_credentials = False

    target = '{:}/{:}'.format(url, filename)

    status = 0
    if not use_credentials:  ## download with no credentials
        try:
            ## allow timeout with requests
            request = requests.get(target, timeout=20, stream=True)
            if request.status_code == 200:
              with open(saveas, 'wb') as fh:
                  for chunk in request.iter_content(1024 * 1024):
                      fh.write(chunk)

            if not os.path.isfile(saveas):
                status += 1
        except:
            status = 1
    else:  ## download with credentials (not sure if this works for python 2)
        try:
            with requests.get(target, auth=(username, password), timeout=20) as r:
                r.raise_for_status()
                if r.status_code == 200:
                  with open(saveas, 'wb') as f:
                      #shutil.copyfileobj(r.raw, f)
                      f.write(r.content)
                if not os.path.isfile(saveas):
                    status += 1
        except:
            status = 1

    if status > 0 and kwargs['fail_error'] == True:
        msg = '[ERROR] retrieve::http_retrieve Failed to download file {:}'.format(
            target)
        raise RuntimeError(msg)

    return status, target, saveas


def web_retrieve(url, **kwargs):
    # print('>> called web_retrieve with args: url={:}, kwargs={:}'.format(url, kwargs))
    filename = None if 'filename' not in kwargs else kwargs['filename']
    if url.startswith('http'):
        return http_retrieve(url, filename, **kwargs)
    elif url.startswith('ftp'):
        return ftp_retrieve(url, filename, **kwargs)
    elif url.startswith('ssh'):
        return scp_retrieve(url, filename, **kwargs)
    else:
        msg = '[ERROR] retrieve::web_retrieve Unknown url protocol {:}'.format(
            url)
        raise RuntimeError(msg)
