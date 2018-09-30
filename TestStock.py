import os
import csv
import log
import sys
import pytest
import filecmp

import stock

PATH_FOR_INSTALLER = '/Users/Manda/StockWatch/testing/'  ## home
## PATH_FOR_INSTALLER = '/Users/phillipbrown/StockWatch/testing/' ## Uni

RAW_DATA = PATH_FOR_INSTALLER + 'raw_data/'

TEST_CODE = 'APT'
TEST_TIME_SERIES_FILE = PATH_FOR_INSTALLER + 'data/' + TEST_CODE + "/time_series.csv"

TEST_EARLIEST_YEAR = 2016

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

	## We've definitely got global_vars.py, so assume there is an existing installation
	## First check that the stock object initialises properly

	st = stock.Stock(TEST_CODE)
	assert st.GetDataFile() == TEST_TIME_SERIES_FILE