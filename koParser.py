#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhuhz
@file: koParser.py
@time: 2020/4/24 13:35
"""


import os
import json
import re


class KOParser(object):
	def __init__(self, map):
		self.map = map

	def json_parser(self):
		# 判断文件存在
		if os.path.exists(self.map):
			with open(self.map, 'r') as f:
				# 将json转成字典
				ko = []
				map_dict = json.load(f)
				maps = json.loads(json.dumps(map_dict['children']))
				# print(type(maps))
				for map in maps:
					# print(type(map['children']))
					for map_l_1 in map['children']:
						map_l_2 = json.loads(json.dumps(map_l_1))
						for pathway in map_l_2['children']:
							try:
								for genes in pathway['children']:
										ko.append(genes['name'])
							except:
								continue
				# print(type(ko))
				return ko
		else:
			print('Json file does not exist.')

	def save_data(self, result, file_name):
		for genes in result:
			k_num = genes.split(sep='  ')[0]
			gene_name = genes.split(sep='  ')[1].split(sep=';')[0]
			anno = genes.split(sep='  ')[1].split(sep=';')[-1]
			try:
				pattern = re.compile('(.*)(\[EC:.*\])')
				product = re.search(pattern, anno).group(1)
				ec = re.search(pattern, anno).group(2)
				ko = k_num + '\t' + gene_name + '\t' + product + '\t' + ec
			except:
				ko = k_num + '\t' + gene_name + '\t' + anno
			kos = ''.join(ko) + '\n'
			with open(file_name, 'a', encoding='utf-8') as f:
				f.write(kos)


if __name__ == '__main__':
	map = 'ko00001.json'
	file_name = 'ko.txt'
	ko_json = KOParser(map)
	ko = ko_json.json_parser()
	ko_json.save_data(ko, file_name)

