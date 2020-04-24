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
				ko_list = []
				map_dict = json.load(f)
				maps = json.loads(json.dumps(map_dict['children']))
				# print(type(maps))
				for map in maps:
					# print(type(map['children']))
					map_name = map['name'][0:5] + '\t' + map['name'][6:]
					# print(map_name)
					for map_l_1 in map['children']:
						map_l_1_name = map_l_1['name'][0:5] + '\t' + map_l_1['name'][6:]
						# print(map_l_1_name)
						map_l_2 = json.loads(json.dumps(map_l_1))
						for pathway in map_l_2['children']:
							try:
								for genes in pathway['children']:
									pathway_name = pathway['name'][0:5] + '\t' + pathway['name'][6:]
									# print(genes['name'])
									k_num = genes['name'].split(sep='  ')[0]
									gene_name = genes['name'].split(sep='  ')[1].split(sep=';')[0]
									anno = genes['name'].split(sep='  ')[1].split(sep=';')[-1]
									try:
										pattern = re.compile('(.*)(\[EC:.*\])')
										product = re.search(pattern, anno).group(1)
										ec = re.search(pattern, anno).group(2)
										ko = k_num + '\t' + gene_name + '\t' + product + '\t' + ec
									except:
										ko = k_num + '\t' + gene_name + '\t' + anno
									# print(ko)
									info = map_name + '\t' + map_l_1_name + '\t' + pathway_name + '\t' + ko
									ko_list.append(info)
							except:
								continue
				return ko_list
		else:
			print('Error: Json file does not exist.')

	def save_data(self, result, file_name):
		for info in result:
			kos = ''.join(info) + '\n'
			with open(file_name, 'a', encoding='utf-8') as f:
				f.write(kos)


if __name__ == '__main__':
	map = 'ko00001.json'
	file_name = 'ko.txt'
	ko_json = KOParser(map)
	ko = ko_json.json_parser()
	ko_json.save_data(ko, file_name)

