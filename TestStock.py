import os
import csv
import log
import sys
import pytest
import filecmp

import stock
import installer
import updater

PATH_FOR_INSTALLER = '/Users/Manda/StockWatch/testing/'  ## home
#PATH_FOR_INSTALLER = '/Users/phillipbrown/StockWatch/testing/' ## Uni

RAW_DATA = PATH_FOR_INSTALLER + 'raw_data/'

TEST_CODE = 'APT'
TEST_TIME_SERIES_FILE = PATH_FOR_INSTALLER + 'data/' + TEST_CODE + "/time_series.csv"

TEST_EARLIEST_YEAR = 2016

COMPARISON_CODE = 'APT'
COMPARISON_FILES_PATH = PATH_FOR_INSTALLER + 'cmp_files/'
COMPARISON_TIME_SERIES_FILE = COMPARISON_FILES_PATH + COMPARISON_CODE + "/time_series.csv"

def testStockObjectSteps():
	## Test each stage in coding up the Stock object

	## Need some data first, so make sure we have an installation
	## This will abort if global_vars already exists
	try:
		inst = installer.Installer(PATH_FOR_INSTALLER,RAW_DATA,TEST_EARLIEST_YEAR)
	except:
		pass
	
	global_vars_file = PATH_FOR_INSTALLER + "global_vars.py"
	assert os.path.isfile(global_vars_file)

	##============================================================
	## We've definitely got global_vars.py, so assume there is an existing installation
	## First check that the stock object initialises properly

	st = stock.Stock(TEST_CODE, updater.FromBigCharts)
	assert st.GetDataFile() == TEST_TIME_SERIES_FILE

	#=============================================================
	## Check that data loads correctly
	## Will only work if the test installation is completely fresh
	data = st.GetStockData()

	data_comp = []
	with open(COMPARISON_TIME_SERIES_FILE,'r') as csvfile:
		data_reader = csv.reader(csvfile)
		for line in data_reader:
			data_comp.append([line[0]] + [float(i) for i in line[1:]])

	#assert data == data_comp

	##============================================================
	## Check that update works, and GetLastDate returns the correct date
	st.GetNewData()
	last_date = st.GetLastDate()
	assert last_date == '20181001'