#!/usr/bin/python3
# encoding: utf-8
"""
@author: zhuhz
@file: multi-line_to_single-line.py
@time: 2019/8/1 22:05
"""

import argparse


def read_fa(in_file):
    with open(in_file, 'r') as f:
        fasta = {}
        for line in f:
            line = line.strip()
            if line[0] == '>':
                header = line
            else:
                seq = line
                fasta[header] = fasta.get(header, '') + seq
    return fasta


if __name__ == '__main__':
    print('This short script reformats a multi-line fasta file into a single-line one.')

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', type=str, help='path of the input fasta file')
    parser.add_argument('--output', '-o', type=str, help='path of the output fasta file')
    args = parser.parse_args()

    fa = read_fa(args.input)

    with open(args.output, 'w') as f:
        for k, v in fa.items():
            f.write('{0}\n{1}\n'.format(k, v))

    print('Done!')
