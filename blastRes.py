#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhuhz
@file: blastRes.py
@time: 2020/6/22 19:30
"""

from xml.etree import ElementTree
import pandas as pd


class ParseXML(object):
	def __init__(self, xmlpath):
		self.xmlpath = xmlpath

	def getRoot(self):
		tree = ElementTree.parse(self.xmlpath)
		return tree.getroot()

	def getAnno(self, root):
		acc_list = []
		for elem in root[8].iter(tag='Hit_accession'):
			acc_list.append(elem.text + '.1')
		anno_list = []
		for elem in root[8].iter(tag='Hit_def'):
			anno_list.append(elem.text)
		return acc_list, anno_list

	def getRes(self, outfile):
		root = self.getRoot()
		acc_list, anno_list = self.getAnno(root)
		res = pd.DataFrame({'subject id': acc_list, 'annotation': anno_list})
		res.to_csv(outfile, sep='\t', index=False)
		return res


class ParseCSV(object):
	def __init__(self, csvpath):
		self.csvpath = csvpath

	def readCSV(self):
		df = pd.read_csv(self.csvpath, names=['query id', 'subject id', 'identities', 'alignment length', 'mismatches', 'gap opens', 'qstart', 'qend', 'sstart', 'send', 'evalue', 'bit score'], header=0)
		return df

	def mergeRes(self, res, outfile):
		df = self.readCSV()
		merged = pd.merge(df, res, how='inner', on='subject id', sort=False, copy=False)
		merged.to_csv(outfile, sep='\t', index=False)
		return merged


if __name__ == '__main__':
	xmlparse = ParseXML('P37P4R6D016-Alignment.xml')
	res = xmlparse.getRes('acc_anno.txt')
	csvparse = ParseCSV('P37P4R6D016-Alignment-HitTable.csv')
	merged = csvparse.mergeRes(res, 'merged.txt')
