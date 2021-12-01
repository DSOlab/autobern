#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import os, sys
import datetime
import re
from pybern.products.errors.errors import FileFormatError
utils_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) +
             '/utils/')
sys.path.append(utils_dir)
from dctutils import merge_dicts

FILE_FORMAT = 'PCF (Bernese v5.2)'


class PcfFile:

    def __init__(self, input_pcf=None):
        self.pcf_lines = []
        if input_pcf:
            self.parse_pcf(input_pcf)

    def find_variable_header_line(self):
        if self.pcf_lines == []:
            raise RuntimeError(
                '[ERROR] No PCF files parsed! Cannot find variable header line for list'
            )
        """
        VARIABLE DESCRIPTION                              DEFAULT
        8******* 40************************************** 30****************************
        """
        header_index = self.pcf_lines.index(
            'VARIABLE DESCRIPTION                              DEFAULT')
        assert (
            header_index > -1 and self.pcf_lines[header_index + 1] ==
            '8******* 40************************************** 30****************************'
        )
        return header_index

    def parse_pcf(self, pcf_file):
        with open(pcf_file, 'r') as pcf:
            self.pcf_lines = [line.strip() for line in pcf.readlines()]

    def find_variable(self, var_name):
        ## search for the variable beyond this point
        idx = self.find_variable_header_line() + 2
        for pcf_line in self.pcf_lines[idx:]:
            if not pcf_line[0].lstrip() == '#':
                if pcf_line.strip()[0:8] == var_name:
                    return idx, var_name, pcf_line[9:40 + 9].strip(
                    ), pcf_line[40 + 9 + 1:40 + 9 + 30].strip(), False
            else:
                tmp_line = pcf_line.lstrip().strip('#').lstrip()
                if tmp_line[0:8].strip() == var_name:
                    return idx, var_name, tmp_line[9:40 + 9].strip(
                    ), tmp_line[40 + 9 + 1:40 + 9 + 30].strip(), True
            idx += 1
        return -1, '', '', '', False

    def add_variable_line(self, var_name, var_value, var_comment):
        assert (len(var_name) <= 8)
        assert (len(var_value) <= 30)
        if var_comment is None:
            var_comment = ''
        idx = self.find_variable_header_line() + 2
        for vline in self.pcf_lines[idx:]:
            if vline.lstrip().startswith('#'):
                break
            idx += 1
        self.pcf_lines.insert(
            idx, '{:8s} {:40s} {:30s}'.format(var_name, var_comment, var_value))
        return idx

    def comment_out_variable_line(self, var_name):
        assert (len(var_name) <= 8)
        var_found = 0
        idx = self.find_variable_header_line() + 2
        for offset, vline in enumerate(self.pcf_lines[idx:]):
            if vline.lstrip().startswith(var_name):
                self.pcf_lines[idx + offset] = '#{:}'.format(vline.rstrip())
                var_found += 1
        return var_found

    def uncomment_variable_line(self, var_name, var_value, idx=None):
        if idx is not None:
            pcf_line = self.pcf_lines[idx]
            tmp_line = pcf_line.lstrip().strip('#').lstrip()
            idx, name, cmnt, val, is_cmnt = idx, tmp_line[0:8].strip(
            ), tmp_line[9:40 + 9].strip(), tmp_line[40 + 9 + 1:40 + 9 +
                                                    30].strip(), True
        else:
            idx, name, cmnt, val, is_cmnt = self.find_variable(var_name)
        assert (idx > -1 and name == var_name and is_cmnt)
        self.pcf_lines[idx] = '{:8s} {:40s} {:30s}'.format(
            var_name, cmnt, var_value)
        return

    def change_variable_line(self, var_name, var_value, idx=None):
        if idx is not None:
            pcf_line = self.pcf_lines[idx]
            assert (not pcf_line.startswith('#'))
            idx, name, cmnt, val, is_cmnt = idx, pcf_line[0:8].strip(
            ), pcf_line[9:40 + 9].strip(), pcf_line[40 + 9 + 1:40 + 9 +
                                                    30].strip(), False
        else:
            idx, name, cmnt, val, is_cmnt = self.find_variable(var_name)
        assert (idx > -1 and name == var_name and not is_cmnt)
        self.pcf_lines[idx] = '{:8s} {:40s} {:30s}'.format(
            var_name, cmnt, var_value)
        return

    def set_variable(self, var_name, var_value, var_comment):
        """ There are 3 possibilities:
            1. The variable does not exist at all; in this case we add it
            2. The variable is commented out; in this case, uncomment and set
               the correct value
            3. The variable exists but has a different value; in this case just
               change the value
        """
        line_idx, name, cmnt, val, is_commented = self.find_variable(var_name)
        if line_idx == -1:  ## variable does not exist
            self.add_variable_line(var_name, var_value, var_comment)
        elif line_idx > -1 and is_commented:  ## variable exists but is commented out
            self.uncomment_variable_line(var_name, var_value, line_idx)
        elif line_idx > -1 and not is_commented:  ## variable exists; check and alter value
            if val != var_value:
                self.change_variable_line(var_name, var_value, line_idx)
        else:
            raise RuntimeError('[ERROR] Cannot set/update variable!')

    def collect_variables(self):
        idx = self.find_variable_header_line() + 2
        var_dct = {}
        for line in self.pcf_lines[idx:]:
            if not line.lstrip().startswith('#'):
                var_name, var_comment, var_value = [
                    x.strip()
                    for x in [line[0:8], line[9:40 + 9], line[40 + 9 + 1:]]
                ]
                if var_name in var_dct:
                    raise RuntimeError(
                        '[ERROR] Variable found more than once in PCF file; variable name: \'{:}\''
                        .format(var_name))
                var_dct[var_name] = {
                    'description': var_comment,
                    'value': var_value
                }
        return var_dct

    def check_variables_are_unique(self):
        try:
            self.collect_variables()
        except:
            return False
        return True

    def assert_variables(self, var_list, var_vals):
        assert (len(var_list) == len(var_vals))
        var_dct = self.collect_variables()
        for name, value in zip(var_list, var_vals):
            if not name in var_dct:
                raise RuntimeError(
                    '[ERROR] Requested variable {:} which is not in the PCF file'
                    .format(name))
            assert (value == var_dct[name]['value'])
        return True

    def dump(self, outfile=None):
        if not self.check_variables_are_unique():
            raise RuntimeError(
                '[ERROR] Cannot write PCF file! Some variables are not unique')
        if outfile:
            f = open(outfile, 'w')
        else:
            f = sys.stdout
        for line in self.pcf_lines:
            print('{}'.format(line), file=f)
        if outfile:
            f.close()
