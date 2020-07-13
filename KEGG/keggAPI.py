#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhuhz
@file: keggAPI.py
@time: 2020/6/16 13:58
"""

from Bio.KEGG import REST

pathways = REST.kegg_list('pathway').read()
# print(type(pathways))
res = 'ko' + '\t' + 'ko name' + '\t' + 'ko des' + '\t' + 'module' + '\t' + 'module name' + '\t' + 'map' + '\t' + 'map name' + '\t' + 'map class' + '\n'

for pathway in pathways.rstrip().split('\n'):
	map_entry, map_description = pathway.split('\t')
	# print(map_entry)
	map = REST.kegg_get(map_entry).read()
	# print(type(map))
	current_section = None
	for line in map.rstrip().split('\n'):
		section = line[:12].strip()
		if not section == '':
			current_section = section
		if current_section == 'NAME':
			map_name = line[12:]
		elif current_section == 'CLASS':
			map_class = line[12:]
		# elif current_section == 'PATHWAY_MAP':
		# 	map_des = line[22:]
		elif current_section == 'MODULE':
			modules = line[12:]
			for module in modules.rstrip().split('\n'):
				module_id, module_name = module.split('  ')
				module_entry = 'module:' + module_id
				module_info = REST.kegg_get(module_entry).read()
				module_section = None
				for module_line in module_info.rstrip().split('\n'):
					module_section = module_line[:12].strip()
					if not module_section == '':
						c_module_section = module_section
					if c_module_section == 'ORTHOLOGY':
						orthologies = module_line[12:]
						ko_list = []
						for orth in orthologies.rstrip().split('\n'):
							try:
								kos, ko_des = orth.split('  ')
							except ValueError:
								kos, ko_des = orth.split(' ', 1)
							if len(kos) > 6:
								if kos[6] == '+':
									if len(kos) > 13 and kos[13] == ',':
										ko_list.append(kos.split('+')[0])
										ko_list.extend(kos.split('+')[1].split(','))
									elif len(kos) > 35 and len(kos.split('+')[4]) > 6 and kos.split('+')[4][6] == '-':
										ko_list.extend(kos.split('+')[:4])
										ko_list.extend(kos.split('+')[4].split('-'))
										ko_list.append(kos.split('+')[5])
									else:
										ko_list.extend(kos.split('+'))
								else:
									ko_list.extend(kos.split(','))
							else:
								ko_list.append(kos)
							for ko in ko_list:
								ko_entry = 'orthology:' + ko
								ko_info = REST.kegg_get(ko_entry).read()
								ko_section = None
								for ko_line in ko_info.rstrip().split('\n'):
									ko_section = ko_line[:12].strip()
									if not ko_section == '':
										c_ko_section = ko_section
									if c_ko_section == 'NAME':
										ko_name = ko_line[12:]
									elif current_section == 'DEFINITION':
										ko_des = ko_line[12:]
									else:
										continue
									temp = ko + '\t' + ko_name + '\t' + ko_des + '\t' + module_id + '\t' + module_name + '\t' + map_entry + '\t' + map_name + '\t' + map_class + '\n'
									res += temp
		else:
			continue

with open('kos_pyAPI.txt', 'w') as f:
	f.write(res)
