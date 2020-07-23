#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhuhz
@file: blast_se.py
@time: 2020/6/23 13:30
"""

import os
import argparse

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def setDriver(driver_path):
	# profile for downloading
	options = webdriver.ChromeOptions()
	prefs = {'download.prompt_for_download': False, 'profile.default_content_settings.popups': 0}
	options.add_experimental_option('prefs', prefs)

	# driver = webdriver.Firefox()
	driver = webdriver.Chrome(executable_path=driver_path, options=options)
	driver.maximize_window()
	driver.get('https://blast.ncbi.nlm.nih.gov/')

	# https://blog.csdn.net/weixin_41812940/article/details/82423892
	driver.command_executor._commands['send_command'] = ('POST', '/session/$sessionId/chromium/send_command')
	params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': os.getcwd()}}
	driver.execute('send_command', params)
	return driver


def blastN(driver, seq, db='nt', sub_db='nt', max_target=10):
	# send keys
	driver.find_element_by_id('homeBlastn').click()
	driver.find_element_by_id('seq').send_keys(seq)

	# choose database
	set_db = driver.find_element_by_xpath('//*[@id="genomeDbs"]')
	all_db = set_db.find_elements_by_tag_name('input')
	if db == 'nt':
		all_db[0].click()
		set_nt = driver.find_element_by_xpath('//*[@id="DATABASE"]')
		all_nt = set_nt.find_elements_by_tag_name('option')
		for nt in all_nt:
			if nt.get_attribute('value') == sub_db:
				nt.click()
	elif db == 'rRNA/ITS':
		all_db[1].click()
		set_rna = driver.find_element_by_xpath('//*[@id="DATABASE"]')
		all_rna = set_rna.find_elements_by_tag_name('option')
		for rna in all_rna:
			if rna.get_attribute('value') == sub_db:
				rna.click()
	elif db == 'genomic+transcript':
		all_db[2].click()
		set_genome = driver.find_element_by_xpath('//*[@id="DATABASE"]')
		all_genome = set_genome.find_elements_by_tag_name('option')
		for genome in all_genome:
			if genome.get_attribute('id') == sub_db:
				genome.click()
	elif db == 'betacov':
		all_db[3].click()
		set_beta = driver.find_element_by_xpath('//*[@id="DATABASE"]')
		all_beta = set_beta.find_elements_by_tag_name('option')
		for beta in all_beta:
			if beta.get_attribute('id') == sub_db:
				beta.click()
	else:
		raise ValueError('Database not found.')

	# set parameter
	driver.find_element_by_id('algPar').click()
	set_max = driver.find_element_by_xpath('//*[@id="NUM_SEQ"]')
	all_num = set_max.find_elements_by_tag_name('option')
	for num in all_num:
		if num.get_attribute('value') == str(max_target):
			num.click()

	# send query
	driver.find_element_by_id('nw1').click()
	driver.find_element_by_id('blastButton1').click()

	# change handle
	query_handle = driver.current_window_handle
	handles = driver.window_handles
	for handle in handles:
		if handle != query_handle:
			driver.switch_to.window(handle)


def blastP(driver, seq, db='nr', program='blastp', max_target=10):
	# send keys
	driver.find_element_by_id('homeBlastp').click()
	driver.find_element_by_id('seq').send_keys(seq)

	# choose database
	set_db = driver.find_element_by_xpath('//*[@id="DATABASE"]')
	all_db = set_db.find_elements_by_tag_name('option')
	for opt in all_db:
		if opt.get_attribute('abbr') == db:
			opt.click()


	# choose program
	set_program = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/form/div[6]/div/fieldset/div[2]/table/tbody')
	all_program = set_program.find_elements_by_tag_name('tr')
	for tr in all_program:
		td = tr.find_element_by_tag_name('td')
		if td.get_attribute('id') == program:
			td.click()
	driver.find_element_by_id('algPar').click()
	set_max = driver.find_element_by_xpath('//*[@id="NUM_SEQ"]')
	all_num = set_max.find_elements_by_tag_name('option')
	for num in all_num:
		if num.get_attribute('value') == str(max_target):
			num.click()

	# send query
	driver.find_element_by_id('nw2').click()
	driver.find_element_by_id('blastButton2').click()

	# change handle
	query_handle = driver.current_window_handle
	handles = driver.window_handles
	for handle in handles:
		if handle != query_handle:
			driver.switch_to.window(handle)


def downloadData(driver):
	# wait 60s in total, check every 5s
	WebDriverWait(driver, 60, 5).until(EC.presence_of_element_located((By.ID, 'ulDnldAl')))
	driver.find_element_by_id('ulDnldAl').click()
	driver.find_element_by_css_selector('#allDownload > li:nth-child(2) > a:nth-child(1)').click()
	driver.find_element_by_id('ulDnldAl').click()
	driver.find_element_by_id('hitCvs').click()
	driver.close()


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--seq', help='Input of query sequence', type=str, required=True)
	parser.add_argument('--type', help='BlastN or BlastP', type=str, choices=['BlastN', 'BlastP'], required=True)
	parser.add_argument('--max_target', help='Number of max targets', type=int, choices=[10, 50, 100, 250, 500, 1000, 5000, 10000, 20000])
	parser.add_argument('--db', help='Database for blast', type=str, choices=['nt', 'rRNA/ITS', 'genomic+transcript', 'betacov', 'nr', 'refseq_protein', 'landmark', 'swissprot', 'pataa', 'pdb', 'env_nr', 'tsa_nr'])
	parser.add_argument('--sub_db', help='Sub-database for blastN', type=str, choices=['nt', 'refseq_rna', 'refseq_representative_genomes', 'refseq_genomes', 'Whole_Genome_shotgun_contigs', 'est', 'sra', 'tsa_nt', 'htgs', 'patnt', 'pdbnt', 'genomic/9606/RefSeqGene', 'gss', 'sts', 'rRNA_typestrains/prokaryotic_16S_ribosomal_RNA', 'TL/18S_fungal_sequences', 'TL/28S_fungal_sequences', 'rRNA_typestrains/ITS_RefSeq_Fungi', 'Ohc', 'Omc', 'OvirB', 'OvirC'])
	parser.add_argument('--program', help='BlastP program', type=str, choices=['kmerBlastp', 'balstp', 'psiBlast', 'phiBlast', 'delstBlast'])
	args = parser.parse_args()
	with open(args.seq, 'r') as f:
		fa = f.read()
	my_driver = setDriver('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
	if args.type == 'BlastN':
		blastN(my_driver, fa, args.db, args.sub_db, args.max_target)
	elif args.type == 'BlastP':
		blastP(my_driver, fa, args.db, args.program, args.max_target)
	downloadData(my_driver)
