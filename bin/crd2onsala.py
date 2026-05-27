#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import os
import sys


def default_path(*parts):
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    return os.path.join(repo_root, *parts)


def parse_crd_records(crd_file):
    with open(crd_file, 'r') as fin:
        for line_no, line in enumerate(fin, start=1):
            if len(line.strip()) == 0:
                continue

            parts = line.split()
            if len(parts) < 5 or not parts[0].isdigit():
                continue

            try:
                x, y, z = [float(value) for value in line[20:66].split()]
            except (ValueError, IndexError):
                print('[WRNNG] Skipping malformed CRD line {:}: {:}'.format(line_no, line.rstrip()), file=sys.stderr)
                continue

            name = line[5:10].strip()
            if not name:
                print('[WRNNG] Skipping CRD line {:}: empty station name'.format(line_no), file=sys.stderr)
                continue

            yield name, x, y, z


def write_xyz(records, output_file):
    out_dir = os.path.dirname(os.path.abspath(output_file))
    if out_dir and not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    count = 0
    with open(output_file, 'w') as fout:
        for name, x, y, z in records:
            fout.write('{:<24s}  {:15.3f} {:15.3f} {:15.3f}\n'.format(name, x, y, z))
            count += 1
    return count


def main():
    parser = argparse.ArgumentParser(
        description='Convert a Bernese CRD coordinate file to fixed-width station X Y Z records.')
    parser.add_argument(
        '-i',
        '--input',
        default=default_path('data', 'NTUA54.CRD'),
        help='Input CRD file')
    parser.add_argument(
        '-o',
        '--output',
        default=default_path('data', 'NTUA54.ons'),
        help='Output fixed-width XYZ file for submit to Onsala BLQ')
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print('[ERROR] Input CRD file does not exist: {:}'.format(args.input), file=sys.stderr)
        return 1

    count = write_xyz(parse_crd_records(args.input), args.output)
    print('Wrote {:} station records to {:}'.format(count, args.output))
    return 0


if __name__ == '__main__':
    sys.exit(main())
