#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhuhz
@file: koChecker.py
@time: 2020/4/30 8:59
"""

import pandas as pd
import os

def check(q_dir, target):
	q_list = os.listdir(q_dir)
	check_merge = target.ko
	# print(q_list)
	for f in q_list:
		query = pd.read_csv(f, usecols=[1], sep='\t')
		query = query.rename(columns=lambda x: x.replace(' ', '_'))
		# print(query.head())
		check = target.apply(lambda s: pd.Series({'ko': s.ko, f: s.ko in query.KO_ID.to_list()}), axis=1)
		# print(check.head())
		check_merge = pd.merge(check_merge, check, on='ko')
		# print(type(target.ko))
	return check_merge


if __name__ == '__main__':
	q_dir = 'E:/lab/6Dragon_shaped_water_system/LXD/LXD_genome'
	os.chdir(q_dir)
	target = pd.read_csv('E:/lab/6Dragon_shaped_water_system/LXD/ko50.txt', sep='\t')
	ko_check = check(q_dir, target)
	ko_check.to_csv('E:/lab/6Dragon_shaped_water_system/LXD/ko_check.txt', sep='\t', index=False)
