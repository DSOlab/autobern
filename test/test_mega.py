#! /usr/bin/python3

import os
import sys
from mega import Mega

## see https://github.com/odwyersoftware/mega.py

def create_dir_if_nonexistant(dir_path, mega_handle):
    dir_name = os.path.basename(dir_path)
    dir_path = os.path.dirname(dir_path)

    current_path = ''
    current_id   = None
    for d in dir_path.split('/'):
        current_path = os.path.join(current_path, d)
        did = mega_handle.find(current_path, exclude_deleted=True)
        if did is None:
            print('Path {:} does not exist, creating ...'.format(current_path))
            current_id = mega_handle.create_folder(d, current_id)
        else:
            current_id = did[0]
            print('Path {:} found with id={:}'.format(current_path, current_id))

# Create an instance of Mega.py
mega = Mega()

# Login
m = mega.login('autobpe.dso@gmail.com', 'gevdais;ia')

# get user details
#details = m.get_user()
#print('details:')
#print(details)

# get account disk quota
#quota = m.get_quota()
#print('quota:')
#print(quota)

# get account storage space (unit can be kilo, mega, gig)
#space = m.get_storage_space(mega=True)
#print('space:')
#print(space)

# get account files
#files = m.get_files()
#print('files:')
#print(files)

# check if folder exists (ommiting Trash folder)
root_folder='gnss/products'
folder = m.find(root_folder, exclude_deleted=True) ## a dictionary ...
print('folder found:')
print(folder)
if folder:
    print('Cloud folder {:} exists'.format(root_folder))
else:
    print('Cloud folder {:} does not exist'.format(root_folder))

root_folder='gnss/products/666'
folder = m.find(root_folder, exclude_deleted=True) ## None ...
print('folder found:')
print(folder)
if folder:
    print('Cloud folder {:} exists'.format(root_folder))
else:
    print('Cloud folder {:} does not exist'.format(root_folder))

create_dir_if_nonexistant('gnss/products/666/777/8888', m)

## create folder
#rand_folder='666'
#if not m.create_folder(rand_folder, m.find('gnss/products', exclude_deleted=True)[0]):
#    print('Failed to create folder!')
#rand_folder='667'
#if not m.create_folder(rand_folder, m.find('gnss/products', exclude_deleted=True)[0]):
#    print('Failed to create folder!')
