#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhuhz
@file: seq_select.py
@time:  12:33
"""

import pandas as pd
import argparse


def read_fasta(input):
    with open(input, 'r') as f:
        fasta = {}
        for line in f:
            line = line.strip()
            if line[0] == '>':
                header = line[1:11]
            else:
                seq = line
                fasta[header] = fasta.get(header, '') + seq
    return fasta


def select_seq(fasta, idx, output):
    with open(output, 'w') as f:
        for (k, v) in fasta.items():
            if k in idx:
                f.write('>' + k + '\n' + v + '\n')
            else:
                continue


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', type=str, help='input file in fasta format')
    parser.add_argument('--output', '-o', type=str, help='output file')
    parser.add_argument('--index', type=str, help='index file')
    args = parser.parse_args()

    fasta = read_fasta(args.input)
    idx = list(pd.read_csv(args.index, sep='\t', header=0).CDS)
    select_seq(fasta, idx, args.output)
