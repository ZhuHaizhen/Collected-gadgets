#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhuhz
@file: blast_se.py
@time: 2020/6/23 13:30
"""

import os
import time

from selenium import webdriver


def setDriver(driver_path):
	# profile for downloading
	options = webdriver.ChromeOptions()
	prefs = {'download.prompt_for_download': False, 'profile.default_content_settings.popups': 0, 'download.default_directory': os.getcwd()}
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


def blastP(driver, seq, db='nr', max_target=10):
	driver.find_element_by_id('homeBlastp').click()
	driver.find_element_by_id('seq').send_keys(seq)
	# # choose database
	# if db == 'refseq':
	# 	js = "$('select[id=DATABASE]').attr('defval', 'refseq_protein')"
	# elif db == 'swissprot':
	# 	js = "$('select[id=DATABASE]').attr('defval', 'swissprot')"
	# else:
	# 	print('Default db: nr')
	# 	js = "$('select[id=DATABASE]').attr('defval', 'nr')"
	# driver.execute_script(js)
	# # set parameters
	# driver.find_element_by_class_name('ui-ncbitoggler-master-text').click()
	# if max_target == 50:
	# 	js = "$('select[id=NUM_SEQ]').attr('defval', 50)"
	# else:
	# 	print('Max target sequences: 10')
	# 	js = "$('select[id=NUM_SEQ]').attr('defval', 10)"
	# driver.execute_script(js)
	# send query
	driver.find_element_by_id('nw1').click()
	driver.find_element_by_id('b1').click()
	# change handle
	query_handle = driver.current_window_handle
	handles = driver.window_handles
	for handle in handles:
		if handle != query_handle:
			driver.switch_to.window(handle)


def downloadData(driver):
	driver.find_element_by_id('ulDnldAl').click()
	driver.find_element_by_css_selector('#allDownload > li:nth-child(2) > a:nth-child(1)').click()
	driver.find_element_by_id('ulDnldAl').click()
	driver.find_element_by_id('hitCvs').click()


if __name__ == '__main__':
	with open('JQ135_mut.fa', 'r') as f:
		fa = f.read()
	my_driver = setDriver('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
	blastP(my_driver, fa)
	# waiting the web loaded completely
	time.sleep(20)
	downloadData(my_driver)

