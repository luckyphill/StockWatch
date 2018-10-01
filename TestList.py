## This file contains all the unit tests to make sure everything works as it is written

import os
import csv
import log
import sys
import pytest
import filecmp
import logging



G_ALL_CODES_FILE = 'all_codes.csv'

##PATH_FOR_INSTALLER = '/Users/Manda/StockWatch/testing/'  ## home
PATH_FOR_INSTALLER = '/Users/phillipbrown/StockWatch/testing/' ## Uni
sys.path.insert(0, PATH_FOR_INSTALLER)  ## For importing the global_vars.py so it can be checked

RAW_DATA = PATH_FOR_INSTALLER + 'raw_data/'
STOCK_DATA = PATH_FOR_INSTALLER +'data/'
COMPARISON_FILES_PATH = PATH_FOR_INSTALLER + 'cmp_files/'
TEST_LOG_PATH = PATH_FOR_INSTALLER + 'logs/'
TEST_LOG_FILE = TEST_LOG_PATH + 'log_file.log'


COMPARISON_ALL_CODES_FILE =  COMPARISON_FILES_PATH + G_ALL_CODES_FILE
## Have chosen to only do APT for the data cleaning test
COMPARISON_CODE = 'APT'
COMPARISON_TIME_SERIES_FILE = COMPARISON_FILES_PATH + COMPARISON_CODE + "/time_series.csv"
TEST_ALL_CODES_FILE = PATH_FOR_INSTALLER + G_ALL_CODES_FILE

TEST_EARLIEST_YEAR = 2016


## Clear out the testing file so we know new files are being written
os.system('rm ' + PATH_FOR_INSTALLER +'*')
os.system('rm -rf ' + STOCK_DATA)
os.system('rm -rf ' + TEST_LOG_PATH)

import installer

#==========================================
# Use pytest to test things work correctly
# If you don't have pytest, get it using:
# pip install -U pytest
# and check your install using:
# pytest --version
#==========================================

def testInstallationSteps():

	##===================================================================
	inst = installer.Installer(PATH_FOR_INSTALLER,RAW_DATA,TEST_EARLIEST_YEAR)
	## Make sure the installer is instantiated correctly
	assert inst.GetPath() == PATH_FOR_INSTALLER
	assert inst.GetRawPath() == RAW_DATA
	assert inst.GetEarliestYear() == TEST_EARLIEST_YEAR

	##===================================================================
	inst.GetInitialCodes()

	## Get the static files for comparison
	all_codes = []
	with open(COMPARISON_ALL_CODES_FILE, 'r') as csvfile:
		codes_reader = csv.reader(csvfile,delimiter=',')
		all_codes = list(codes_reader)

	## Must have the all_codes file, file must be identical and subsequent lists also
	assert os.path.isfile(TEST_ALL_CODES_FILE)
	assert filecmp.cmp(TEST_ALL_CODES_FILE,COMPARISON_ALL_CODES_FILE)
	assert all_codes.sort() == inst.initial_codes.sort()

	##===================================================================
	inst.CleanRawData()

	## Check that each path and each file has been created
	for code in inst.initial_codes:
		code_path = STOCK_DATA + code +'/'
		assert os.path.exists(code_path)
		time_series_file = code_path + "time_series.csv"
		assert os.path.isfile(time_series_file)
	
	## Check that the file for APT is correct
	with open(COMPARISON_TIME_SERIES_FILE, 'r') as csvfile:
		comp_ts_reader = csv.reader(csvfile,delimiter=',')
		comp_ts = list(comp_ts_reader)

	written_ts_file = inst.DATA_PATH + COMPARISON_CODE + '/time_series.csv'
	with open(written_ts_file, 'r') as csvfile:
		written_ts_reader = csv.reader(csvfile,delimiter=',')
		written_ts = list(written_ts_reader)

	assert written_ts == comp_ts

	##===================================================================
	inst.WriteGlobalVariables()

	## Check that the global variables have been set properly
	## In the actual program will write from global_vars import *
	## but this is useful here so as to not write over things
	import global_vars
	assert global_vars.APP_PATH 		== PATH_FOR_INSTALLER
	assert global_vars.DATA_PATH 		== STOCK_DATA
	assert global_vars.ALL_CODES_FILE 	== TEST_ALL_CODES_FILE
	assert global_vars.LOG_FILE			== TEST_LOG_FILE
	logger = logging.getLogger(global_vars.LOG)
	logger.info('TEST')
	with open(global_vars.LOG_FILE,'r') as test_file:
		log_line = test_file.readlines()

	assert log_line[0][-16:] == 'TestList - TEST\n'


def testInstallationErrorCatch():
	with pytest.raises(Exception):
		## Folder not found
		inst = installer.Installer(PATH_FOR_INSTALLER,PATH_FOR_INSTALLER +'lemon/',TEST_EARLIEST_YEAR)

	empty_folder = PATH_FOR_INSTALLER + 'empty/'

	os.system('rm -rf ' + empty_folder)
	os.makedirs(empty_folder)
	with pytest.raises(Exception):
		## No data in folder
		inst = installer.Installer(PATH_FOR_INSTALLER,empty_folder,TEST_EARLIEST_YEAR)

	## Make a global_vars.py file to fool the installer
	fake_global_vars_file = PATH_FOR_INSTALLER  + "global_vars.py"
	os.system('touch ' + fake_global_vars_file)
	with pytest.raises(Exception):
		## Global vars file already exists
		inst = installer.Installer(PATH_FOR_INSTALLER,RAW_DATA,TEST_EARLIEST_YEAR)
	os.system('rm ' + fake_global_vars_file)




