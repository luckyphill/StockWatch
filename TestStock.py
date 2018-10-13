import os
import csv
import log
import sys
import pytest
import filecmp
import datetime as dt

import stock
import installer
import updater

from global_vars import *

#PATH_FOR_INSTALLER = '/Users/Manda/StockWatch/development/'  ## home
PATH_FOR_INSTALLER = '/Users/phillipbrown/StockWatch/development/' ## Uni

TEST_CODE = 'CBA'
TEST_TIME_SERIES_FILE = PATH_FOR_INSTALLER + 'data/stock_data/' + TEST_CODE + "/time_series.csv"

TEST_EARLIEST_YEAR = 2016

COMPARISON_CODE = 'CBA'
COMPARISON_FILES_PATH = PATH_FOR_INSTALLER + 'cmp_files/'
COMPARISON_TIME_SERIES_FILE = COMPARISON_FILES_PATH + COMPARISON_CODE + "/time_series.csv"

class TestStock(object):

	def test_IntialiseStock(self):

		st = stock.Stock(TEST_CODE, updater.FromBigCharts)
		assert st.GetDataFile() == TEST_TIME_SERIES_FILE

	def test_GetStockData(self):
		#=============================================================
		## Check that data loads correctly
		## Will only work if the test installation is completely fresh
		st = stock.Stock(TEST_CODE, updater.FromBigCharts)
		data = st.GetStockData()

		data_comp = []
		with open(COMPARISON_TIME_SERIES_FILE,'r') as csvfile:
			data_reader = csv.reader(csvfile)
			for line in data_reader:
				data_comp.append([line[0], float(line[1]), float(line[2]), float(line[3]), float(line[4]), int(line[5])])

		print len(data_comp)
		assert data[:130] == data_comp[:130]

	def xtest_FindNewData(self):
		##============================================================
		## Check that update works, and GetLastDate returns the correct date
		## Only works on trading day after GMT -6
		st = stock.Stock(TEST_CODE, updater.FromBigCharts)
		st.FindNewData()
		last_date = st.GetLastDate()
		today = dt.date.today().strftime ("%Y%m%d")
		assert last_date == today

	def test_FindOldData(self):
		## Check that it grabs old data correctly
		os.system('rm ' + TEST_TIME_SERIES_FILE)
		fake_today = '20181012'
		fake_yesterday = '20181011'
		st = stock.Stock(TEST_CODE, updater.FromBigCharts)
		st.FindOldData(fake_today)
		last_date = st.GetLastDate()
		today = dt.date.today().strftime ("%Y%m%d")
		assert last_date == fake_yesterday
