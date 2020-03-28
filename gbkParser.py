#!/usr/bin/python3
# encoding: utf-8
"""
@author: zhuhz
@file: gbkParser.py
@time: 2020/3/3 22:54
"""

import os
import argparse
from Bio import SeqIO


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', type=str, help='path of genbank file')
    parser.add_argument('--output', '-o', type=str, help='path of outputs')
    parser.add_argument('--suffix', type=str, default='gbk', help='suffix of output files')
    args = parser.parse_args()

    cds = os.path.join(args.output, '_'.join([args.suffix, 'cds_list.txt']))
    cds_handle = open(cds, 'w')
    rRNA = os.path.join(args.output, '_'.join([args.suffix, 'rRNA_list.txt']))
    rRNA_handle = open(rRNA, 'w')
    tRNA = os.path.join(args.output, '_'.join([args.suffix, 'tRNA_list.txt']))
    tRNA_handle = open(tRNA, 'w')
    fna = os.path.join(args.output, '_'.join([args.suffix, 'seq.fna']))
    fna_handle = open(fna, 'w')
    ffn = os.path.join(args.output, '_'.join([args.suffix, 'cds.ffn']))
    ffn_handle = open(ffn, 'w')
    faa = os.path.join(args.output, '_'.join([args.suffix, 'cds.faa']))
    faa_handle = open(faa, 'w')

    gb_seq = SeqIO.read(args.input, 'genbank')
    complete_seq = str(gb_seq.seq)
    seq_fna = '>' + gb_seq.id + '\n' + complete_seq
    fna_handle.write(seq_fna)

    for ele in gb_seq.features:
        if ele.type == 'CDS':
            if 'pseudo' in ele.qualifiers.keys():
                break
            else:
                cds_stat = ele.qualifiers['locus_tag'][0] + '\t' + ele.qualifiers['product'][0] + '\t' + str(ele.location.start) + '\t' + str(ele.location.end) + '\t' + str(ele.location.strand) + '\n'
                cds_handle.write(cds_stat)
                ffn_handle.write('>%s, from %s protein_id=%s product=%s\n%s\n' % (
                    ele.qualifiers['locus_tag'][0],
                    gb_seq.name,
                    ele.qualifiers['protein_id'][0],
                    ele.qualifiers['product'][0],
                    complete_seq[ele.location.start:ele.location.end]
                ))
                faa_handle.write('>%s, from %s protein_id=%s product=%s\n%s\n' % (
                    ele.qualifiers['locus_tag'][0],
                    gb_seq.name,
                    ele.qualifiers['protein_id'][0],
                    ele.qualifiers['product'][0],
                    ele.qualifiers['translation'][0]
                ))
        elif ele.type == 'rRNA':
            rRNA_stat = ele.qualifiers['locus_tag'][0] + '\t' + ele.qualifiers['product'][0] + '\t' + str(ele.location.start) + '\t' + str(ele.location.end) + '\t' + str(ele.location.strand) + '\n'
            rRNA_handle.write(rRNA_stat)
        elif ele.type == 'tRNA':
            tRNA_stat = ele.qualifiers['locus_tag'][0] + '\t' + ele.qualifiers['product'][0] + '\t' + str(ele.location.start) + '\t' + str(ele.location.end) + '\t' + str(ele.location.strand) + '\n'
            tRNA_handle.write(tRNA_stat)

    cds_handle.close()
    rRNA_handle.close()
    tRNA_handle.close()
    fna_handle.close()
    ffn_handle.close()
    faa_handle.close()
