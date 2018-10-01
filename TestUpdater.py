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


def xtestBigChartsUpdater():
	upd = updater.FromBigCharts(TEST_CODE)

	## Make sure months roll over correctly
	next_date = upd.GetNextDate('20180229')
	assert next_date == '20180301'

	next_date = upd.GetNextDate('20180430')
	assert next_date == '20180501'

	next_date = upd.GetNextDate('20180630')
	assert next_date == '20180701'

	next_date = upd.GetNextDate('20180930')
	assert next_date == '20181001'

	next_date = upd.GetNextDate('20181130')
	assert next_date == '20181201'

	## Make sure year rolls over correctly
	next_date = upd.GetNextDate('20181231')
	assert next_date == '20190101'


	## Will only work on 20180929
	data_20180928 = ['20180928','17.95','18.50','17.82','17.95','2053325']
	retrieved_data = upd.FetchNewData('20180927')
	print retrieved_data
	assert retrieved_data[0] == data_20180928

	## Gets correct historical data for APT
	old_data = upd.FetchHistorical('20180906')
	print old_data
	assert old_data == ['20180906', '16.52', '16.58', '15.32','16.00', '3844401']

	## Returns False for days with no trading
	no_data = upd.FetchHistorical('20180908')
	print no_data
	assert no_data == False

	## Returns False for dates that don't exist
	no_data = upd.FetchHistorical('20180230')
	print no_data
	assert no_data == False

	## Test that is grabs multiple dates correctly
	## Giving last date as a Thursday and giving current date the following Tuesday
	## Test should return Friday, ignore Sat and Sun, then return Mon and Tues
	upd = updater.FromBigCharts(TEST_CODE)

	multiple_dates = [ ['20180926', u'16.24', u'17.00', u'16.16', u'16.97', u'1524296'],
						['20180927', u'17.25', u'17.85', u'16.70', u'17.80', u'1846039'],
						['20180928', u'17.95', u'18.50', u'17.82', u'17.95', u'2053325']]
	retrieved_data = upd.FetchNewData('20180925')
	assert retrieved_data[:3] == multiple_dates

def testForTestingUpdater():
	upd = updater.ForTesting(TEST_CODE)

	## Will only work on 20180929
	data_20180112 = ['20180112','6.45','6.53','6.44','6.5','825978']
	retrieved_data = upd.FetchNewData('20180111','20180112')
	print retrieved_data
	assert retrieved_data[0] == data_20180112

	## Gets correct historical data for APT
	old_data = upd.FetchData('20180906')
	print old_data
	assert old_data == ['20180906', '16.52', '16.58', '15.32','16', '3844401']

	## Returns False for days with no trading
	no_data = upd.FetchData('20180908')
	print no_data
	assert no_data == False

	## Returns False for dates that don't exist
	no_data = upd.FetchData('20180230')
	print no_data
	assert no_data == False

	## Test that is grabs multiple dates correctly
	## Giving last date as a Thursday and giving current date the following Tuesday
	## Test should return Friday, ignore Sat and Sun, then return Mon and Tues
	upd = updater.ForTesting(TEST_CODE)

	multiple_dates = [ ['20180926', u'16.24', u'17', u'16.16', u'16.97', u'1524296'],
						['20180927', u'17.25', u'17.85', u'16.7', u'17.8', u'1846039'],
						['20180928', u'17.95', u'18.5', u'17.82', u'17.95', u'2053325']]
	retrieved_data = upd.FetchNewData('20180925','20180928')
	assert retrieved_data[:3] == multiple_dates

