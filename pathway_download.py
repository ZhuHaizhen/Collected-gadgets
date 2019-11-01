#!/usr/bin/Python3
# -*- coding: utf-8 -*-

import os, sys, re
import urllib
import urllib.request

if len(sys.argv) != 3:
	print('\nuseage:\npython3 pathway_download.py <my.pathway_anno.result> <map_dir>\nexample:\npython3 pathway_download.py pathway_anno.txt ./map_download\n')
	exit()

pathway = open(sys.argv[1], 'r')
pathway.readline()
os.makedirs(sys.argv[2], exist_ok = True)
os.chdir(sys.argv[2])

for line in pathway:
	line = line.strip().split('\t')
	url = line[-1]
	html = urllib.request.urlopen(url).read()
	img = re.findall(re.compile('src="(.+?\.png)"'), html.decode('utf-8'))
	if img:
		urllib.request.urlretrieve('https://www.genome.jp' + img[0], line[-4] + '.png')

pathway.close()
