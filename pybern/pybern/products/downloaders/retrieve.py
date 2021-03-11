#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import re
import os
import shutil
from contextlib import closing
import requests

if sys.version_info.major == 3:
    import urllib.request
else:
    import urllib2


def url_split(target):
    return target[0:target.rindex('/')], target[target.rindex('/') + 1:]


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

    ## username or password key(s) in kwargs
    if set(['username', 'password']).intersection(set(kwargs)):
        username = kwargs['username'] if 'username' in kwargs else ''
        password = kwargs['password'] if 'password' in kwargs else ''
        __url = re.sub('^ftp:\/\/', '', filename)
        url = 'ftp://{:}:{:}@{:}'.format(username, password, __url)

    target = '{:}/{:}'.format(url, filename)

    status = 0
    try:
        if sys.version_info.major == 2:
            with closing(urllib2.urlopen(target)) as r:
                with open(saveas, 'wb') as f:
                    shutil.copyfileobj(r, f)
        else:
            with closing(request.urlopen(target)) as r:
                with open(saveas, 'wb') as f:
                    shutil.copyfileobj(r, f)
        if not os.path.isfile(saveas):
            status += 1
    except:
        status = 1

    if status > 0 and kwargs['fail_error'] == True:
        msg = '[ERROR] retrieve::ftp_retrieve Failed to download file {:}'.format(
            target)
        raise RuntimeError(msg)

    return status, target, saveas


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

    target = '{:}/{:}'.format(url, filename)

    status = 0
    if not use_credentials: ## download with no credentials
        try:
            if sys.version_info.major == 2:
                response = urllib2.urlopen(target)
                data = response.read()
                with open(saveas, 'wb') as f:
                    f.write(data)
            else:
                urllib.request.urlretrieve(target, saveas)
            if not os.path.isfile(saveas):
                status += 1
        except:
            status = 1
    else: ## download with credentials (not sure if this works for python 2)
        try:
            with requests.get(target, auth=(username, password)) as r:
                r.raise_for_status()
                with open(saveas, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
                if not os.path.isfile(saveas): status += 1
        except:
            status = 1

    if status > 0 and kwargs['fail_error'] == True:
        msg = '[ERROR] retrieve::http_retrieve Failed to download file {:}'.format(
            target)
        raise RuntimeError(msg)

    return status, target, saveas


def web_retrieve(url, **kwargs):
    filename = None if 'filename' not in kwargs else kwargs['filename']
    if url.startswith('http'):
        return http_retrieve(url, filename, **kwargs)
    elif url.startswith('ftp'):
        return ftp_retrieve(url, filename, **kwargs)
    else:
        msg = '[ERROR] retrieve::web_retrieve Unknown url protocol {:}'.format(
            url)
        raise RuntimeError(msg)
