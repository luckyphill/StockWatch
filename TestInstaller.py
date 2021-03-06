## This file contains all the unit tests to make sure everything works as it is written

import os
import csv
import log
import sys
import pytest
import filecmp
import logging



G_ALL_CODES_FILE = 'all_codes.csv'

#PATH_FOR_INSTALLER = '/Users/Manda/StockWatch/development/'  ## home
PATH_FOR_INSTALLER = '/Users/phillipbrown/StockWatch/development/' ## Uni

DATA_PATH = PATH_FOR_INSTALLER + 'data/'
RAW_DATA = DATA_PATH + 'raw_data/'
STOCK_DATA = DATA_PATH +'stock_data/'
ZIP_DATA = DATA_PATH + 'zips/'
COMPARISON_FILES_PATH = PATH_FOR_INSTALLER + 'cmp_files/'
TEST_LOG_PATH = PATH_FOR_INSTALLER + 'logs/'
TEST_LOG_FILE = TEST_LOG_PATH + 'log_file.log'


COMPARISON_ALL_CODES_FILE =  COMPARISON_FILES_PATH + G_ALL_CODES_FILE
## Have chosen to only do APT for the data cleaning test
COMPARISON_CODE = 'APT'
COMPARISON_TIME_SERIES_FILE = COMPARISON_FILES_PATH + COMPARISON_CODE + "/time_series.csv"
TEST_ALL_CODES_FILE = PATH_FOR_INSTALLER + G_ALL_CODES_FILE

EMPTY_FOLDER = PATH_FOR_INSTALLER + 'empty/'

TEST_EARLIEST_YEAR = 2016


## Clear out the testing files so we know new files are being written
os.system('rm global_vars.py')
os.system("rm raw_data_dates.csv")
os.system("rm watch_list.csv")
os.system('rm -rf ' + STOCK_DATA)
os.system('rm -rf ' + ZIP_DATA)
os.system('rm -rf ' + TEST_LOG_PATH)
os.system('rm -rf ' + EMPTY_FOLDER)

import installer

#==========================================
# Use pytest to test things work correctly
# If you don't have pytest, get it using:
# pip install -U pytest
# and check your install using:
# pytest --version
#==========================================

class TestInstallation(object):

	def test_InstallationErrorCatch(self):
		with pytest.raises(Exception):
			## Folder not found
			inst = installer.Installer(PATH_FOR_INSTALLER,PATH_FOR_INSTALLER +'lemon/',TEST_EARLIEST_YEAR)

		os.makedirs(EMPTY_FOLDER)
		with pytest.raises(Exception):
			## No data in folder
			inst = installer.Installer(PATH_FOR_INSTALLER,empty_folder,TEST_EARLIEST_YEAR)
		os.system('rm -rf ' + EMPTY_FOLDER)
		
		## Make a global_vars.py file to fool the installer
		fake_global_vars_file = PATH_FOR_INSTALLER  + "global_vars.py"
		os.system('touch ' + fake_global_vars_file)
		with pytest.raises(Exception):
			## Global vars file already exists
			inst = installer.Installer(PATH_FOR_INSTALLER,RAW_DATA,TEST_EARLIEST_YEAR)
		os.system('rm ' + fake_global_vars_file)

	def test_TestEachStep(self):
		## This will do everything twice since __init__ now contains the full
		## full installation procedure
		##===================================================================
		inst = installer.Installer(PATH_FOR_INSTALLER,RAW_DATA,TEST_EARLIEST_YEAR)
		## Make sure the installer is instantiated correctly
		assert inst.GetPath() == PATH_FOR_INSTALLER
		assert inst.GetRawPath() == RAW_DATA
		assert inst.GetEarliestYear() == TEST_EARLIEST_YEAR

		##===================================================================
		#inst.GetInitialCodes()

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
		#inst.CleanRawData()

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

		written_ts_file = inst.STOCK_PATH + COMPARISON_CODE + '/time_series.csv'
		with open(written_ts_file, 'r') as csvfile:
			written_ts_reader = csv.reader(csvfile,delimiter=',')
			written_ts = list(written_ts_reader)

		assert written_ts[:100] == comp_ts[:100]

		##===================================================================
		#inst.WriteGlobalVariables()

		## Check that the global variables have been set properly
		## In the actual program will write from global_vars import *
		## but this is useful here so as to not write over things
		import global_vars
		assert global_vars.APP_PATH 		== PATH_FOR_INSTALLER
		assert global_vars.STOCK_PATH 		== STOCK_DATA
		assert global_vars.ALL_CODES_FILE 	== TEST_ALL_CODES_FILE
		assert global_vars.LOG_FILE			== TEST_LOG_FILE
		logger = logging.getLogger(global_vars.LOG)
		logger.info('TEST')
		with open(global_vars.LOG_FILE,'r') as test_file:
			log_line = test_file.readlines()

		assert log_line[0][-21:] == 'TestInstaller - TEST\n'





