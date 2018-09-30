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
## PATH_FOR_INSTALLER = '/Users/phillipbrown/StockWatch/testing/' ## Uni

RAW_DATA = PATH_FOR_INSTALLER + 'raw_data/'

TEST_CODE = 'APT'
TEST_TIME_SERIES_FILE = PATH_FOR_INSTALLER + 'data/' + TEST_CODE + "/time_series.csv"

TEST_EARLIEST_YEAR = 2016

COMPARISON_CODE = 'APT'
COMPARISON_FILES_PATH = PATH_FOR_INSTALLER + 'cmp_files/'
COMPARISON_TIME_SERIES_FILE = COMPARISON_FILES_PATH + COMPARISON_CODE + "/time_series.csv"


def testBigChartsUpdater():
	upd = updater.FromBigCharts(TEST_CODE)

	## Will only work on 20180929
	data_20180928 = ['20180928','17.95','18.50','17.82','17.95','2053325']
	retrieved_data = upd.FetchNewData('20180927')
	print retrieved_data
	assert retrieved_data == data_20180928


