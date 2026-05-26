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

FILE_FORMAT = 'PCF (Bernese v5.4)'
VARIABLE_RE = re.compile(
    r'^(?P<name>\S+)\s*=\s*(?P<value>.*?)(?:;\s*DESCRIPTION=(?P<description>.*))?$'
)


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
        VARIABLE         DEFAULT        PARAMETERS
        """
        header_index = self.pcf_lines.index(
            'VARIABLE         DEFAULT        PARAMETERS')
        assert (
            header_index > -1 and self.pcf_lines[header_index + 1] ==
            '# General and model files:'
        )
        return header_index

    def parse_variable_line(self, line):
        """Parse a Bernese 5.4 PCF variable line."""
        stripped = line.lstrip()
        is_commented = stripped.startswith('#')
        if is_commented:
            stripped = stripped[1:].lstrip()

        match = VARIABLE_RE.match(stripped)
        if not match:
            return None

        return {
            'name': match.group('name').strip(),
            'description': (match.group('description') or '').strip(),
            'value': match.group('value').strip(),
            'is_commented': is_commented,
        }

    def format_variable_line(self, var_name, var_value, var_comment):
        if var_comment is None:
            var_comment = ''
        return '{:14s} = {:14s};  DESCRIPTION={:}'.format(
            var_name, var_value, var_comment)

    def parse_pcf(self, pcf_file):
        with open(pcf_file, 'r') as pcf:
            self.pcf_lines = [line.strip() for line in pcf.readlines()]

    def find_variable(self, var_name):
        ## search for the variable beyond this point
        idx = self.find_variable_header_line() + 2
        for pcf_line in self.pcf_lines[idx:]:
            parsed = self.parse_variable_line(pcf_line)
            if parsed and parsed['name'] == var_name:
                return idx, var_name, parsed['description'], parsed[
                    'value'], parsed['is_commented']
            idx += 1
        return -1, '', '', '', False

    def add_variable_line(self, var_name, var_value, var_comment):
        assert (len(var_value) <= 30)
        idx = self.find_variable_header_line() + 2
        insert_idx = idx
        for offset, vline in enumerate(self.pcf_lines[idx:]):
            if self.parse_variable_line(vline):
                insert_idx = idx + offset + 1
        self.pcf_lines.insert(insert_idx,
                              self.format_variable_line(
                                  var_name, var_value, var_comment))
        return insert_idx

    def comment_out_variable_line(self, var_name):
        var_found = 0
        idx = self.find_variable_header_line() + 2
        for offset, vline in enumerate(self.pcf_lines[idx:]):
            parsed = self.parse_variable_line(vline)
            if parsed and not parsed['is_commented'] and parsed[
                    'name'] == var_name:
                self.pcf_lines[idx + offset] = '#{:}'.format(vline.rstrip())
                var_found += 1
        return var_found

    def uncomment_variable_line(self, var_name, var_value, idx=None):
        if idx is not None:
            pcf_line = self.pcf_lines[idx]
            parsed = self.parse_variable_line(pcf_line)
            idx, name, cmnt, val, is_cmnt = idx, parsed['name'], parsed[
                'description'], parsed['value'], parsed['is_commented']
        else:
            idx, name, cmnt, val, is_cmnt = self.find_variable(var_name)
        assert (idx > -1 and name == var_name and is_cmnt)
        self.pcf_lines[idx] = self.format_variable_line(
            var_name, var_value, cmnt)
        return

    def change_variable_line(self, var_name, var_value, idx=None):
        if idx is not None:
            pcf_line = self.pcf_lines[idx]
            assert (not pcf_line.startswith('#'))
            parsed = self.parse_variable_line(pcf_line)
            idx, name, cmnt, val, is_cmnt = idx, parsed['name'], parsed[
                'description'], parsed['value'], parsed['is_commented']
        else:
            idx, name, cmnt, val, is_cmnt = self.find_variable(var_name)
        assert (idx > -1 and name == var_name and not is_cmnt)
        self.pcf_lines[idx] = self.format_variable_line(
            var_name, var_value, cmnt)
        return

    def set_variable(self, var_name, var_value, var_comment):
        """ There are 3 possibilities:
            1. The variable does not exist at all; in this case we add it
            2. The variable is commented out; in this case, uncomment and set
               the correct value
            3. The variable exists but has a different value; in this case just
               change the value
            Note that if 'var_value' is None, then it will be translated to an
            empty string.
        """
        if var_value is None: var_value = ''
        ## handle non-string values
        var_value = '{:}'.format(var_value)
        line_idx, name, cmnt, val, is_commented = self.find_variable(var_name)
        ## print('>> Searching for varible {:} returned index {:}'.format(var_name, line_idx))
        if line_idx == -1:  ## variable does not exist
            self.add_variable_line(var_name, var_value, var_comment)
        elif line_idx > -1 and is_commented:  ## variable exists but is commented out
            self.uncomment_variable_line(var_name, var_value, line_idx)
        elif line_idx > -1 and not is_commented:  ## variable exists; check and alter value
            # print('>> Variable {:} has same value as requested!'.format(var_name))
            if val != var_value:
                # print('>> Changing variable {:} from {:} to {:}'.format(var_name, val, var_value))
                self.change_variable_line(var_name, var_value, line_idx)
        else:
            raise RuntimeError('[ERROR] Cannot set/update variable!')

    def collect_variables(self):
        idx = self.find_variable_header_line() + 2
        var_dct = {}
        for line in self.pcf_lines[idx:]:
            parsed = self.parse_variable_line(line)
            if parsed and not parsed['is_commented']:
                var_name = parsed['name']
                var_comment = parsed['description']
                var_value = parsed['value']
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
#        if not self.check_variables_are_unique():
#            raise RuntimeError(
#                '[ERROR] Cannot write PCF file! Some variables are not unique')
        if outfile:
            f = open(outfile, 'w')
        else:
            f = sys.stdout
        for line in self.pcf_lines:
            print('{}'.format(line), file=f)
        if outfile:
            f.close()
