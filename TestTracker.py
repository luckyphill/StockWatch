import os
import csv
import log
import sys
import pytest
import filecmp

import stock
import installer
import updater
import tracker

import sys
#PATH_FOR_INSTALLER = '/Users/Manda/StockWatch/testing/'
PATH_FOR_INSTALLER = '/Users/phillipbrown/StockWatch/testing/'
sys.path.insert(0, PATH_FOR_INSTALLER)
from global_vars import *


RAW_DATA = PATH_FOR_INSTALLER + 'raw_data/'

TEST_CODE = 'APT'
TEST_TIME_SERIES_FILE = PATH_FOR_INSTALLER + 'data/' + TEST_CODE + "/time_series.csv"

TEST_EARLIEST_YEAR = 2016

COMPARISON_CODE = 'APT'
COMPARISON_FILES_PATH = PATH_FOR_INSTALLER + 'cmp_files/'
COMPARISON_TIME_SERIES_FILE = COMPARISON_FILES_PATH + COMPARISON_CODE + "/time_series.csv"

WATCH_LIST_FILE = COMPARISON_FILES_PATH + 'watch_list.csv'
class TestTracker(object):
	## testing each function of Tracker
	def test_GetWatchList(self):
		trk = tracker.Tracker(WATCH_LIST_FILE)
		cmp_wl = ['APT', 'CBA', 'NAB', 'ANZ', 'TRS', 'IFL', 'BHP', 'CSL', 'AMP', 'WOW']
		wl = trk.GetWatchList()
		assert wl.sort() == cmp_wl.sort()

	def test_GetWatchList_fails(self):
		trk = tracker.Tracker('/path/that/doesnt/exist')
		with pytest.raises(Exception):
			wl = trk.GetWatchList()

	def test_MakeStockDict(self):
		trk = tracker.Tracker(WATCH_LIST_FILE)
		trk.UpdateStockDict()
		stock_dict = trk.stocks
		cmp_wl = ['APT', 'CBA', 'NAB', 'ANZ', 'TRS', 'IFL', 'BHP', 'CSL', 'AMP', 'WOW']
		assert stock_dict.keys().sort() == cmp_wl.sort()

	def test_UpdateArchive(self):
		trk = tracker.Tracker(WATCH_LIST_FILE)
		trk.UpdateArchive()
		## Need to make some assert statements here


	def test_EoDUpdate(self):
		trk = tracker.Tracker(WATCH_LIST_FILE)

		trk.EoDUpdate()
		
