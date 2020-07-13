#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhuhz
@file: keggAPI_v1.py
@time: 2020/6/17 9:13
"""

from Bio.KEGG import REST

orthologies = REST.kegg_list('orthology').read()
res = 'ko' + '\t' + 'ko name' + '\t' + 'ko des' + '\t' + 'map' + '\t' + 'map name' + '\t' + 'map class' + '\n'

for orth in orthologies.rstrip().split('\n'):
	ko_entry, ko_des = orth.strip().split('\t')
	ko_id = ko_entry.strip().split(':')[1]
	try:
		ko_name, ko_func = ko_des.strip().split('; ', 1)
	except ValueError:
		ko_name = ko_des
		ko_func = ko_des
	ko_info = REST.kegg_get(ko_entry).read()
	current_section = None
	for line in ko_info.rstrip().split('\n'):
		section = line[:12].strip()
		if not section == '':
			current_section = section
		if current_section == 'PATHWAY':
			maps = line[12:]
			for map in maps.rstrip().split('\n'):
				map_entry, map_name = ('path:' + map.strip().split('  ')[0]), map.strip().split('  ')[1]
				map_info = REST.kegg_get(map_entry).read()
				c_map_section = None
				for m_line in map_info.rstrip().split('\n'):
					map_section = m_line[:12].strip()
					if not map_section == '':
						c_map_section = map_section
					if c_map_section == 'CLASS':
						map_class = m_line[12:]
					else:
						continue
					temp = ko_id + '\t' + ko_name + '\t' + ko_func + '\t' + map + '\t' + map_name + '\t' + map_class + '\n'
					res += temp

with open('kos_pyAPIv1.txt', 'w') as f:
	f.write(res)
