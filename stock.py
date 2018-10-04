## The stock object
## Should do all the handling of actual stock data

##=====================================================
## This section is only needed for testing
## It should be deleted before running properly
import sys
PATH_FOR_INSTALLER = '/Users/Manda/StockWatch/testing/'
#PATH_FOR_INSTALLER = '/Users/phillipbrown/StockWatch/testing/'
sys.path.insert(0, PATH_FOR_INSTALLER)
##=====================================================

import os
import csv
import datetime as dt
from tail import tail
from global_vars import *

class Stock:
	def __init__(self, code, updater_object):
		self.code = code
		self.DIRECTORY = DATA_PATH + code +'/'
		self.DATA_FILE = self.DIRECTORY + TIME_SERIES_FILE_NAME

		self.updater = updater_object(code)
		## Declaring the object

	def GetDataFile(self):
		return self.DATA_FILE

	def GetLastDate(self):
		## Get the most recent date that we have data for
		stockData = tail(self.DATA_FILE).split(',')
		return str(stockData[0])

	def GetStockData(self,days=False):
		## Loads the data from file
		## Assumes that the data file is structured:
		## date,open,high,low,close,volume
		stockData = []
		
		if os.path.isfile(self.DATA_FILE):
			with open(self.DATA_FILE,'r') as csvfile:
				data_reader = csv.reader(csvfile)
				for line in data_reader:
					## The line is date,open,high,low,close,volume
					## date should be a string, volume should be int, the rest floats
					stockData.append([line[0], float(line[1]), float(line[2]), float(line[3]), float(line[4]), int(line[5])])

		return stockData

	def GetNewData(self):
		## This will get the latest data at a time controlled by Tracker
		## The data is retrieved by an Updater object, then written to file

		if os.path.isfile(self.DATA_FILE):
			new_data = self.updater.FetchNewData(self.GetLastDate())
		else:
			## Collect 5 years worth of data if there is none
			## If there is no data in the archives, checks the maximum limit for web scraping
			## before it tried to download
			five_years_ago = dt.date.today() - dt.timedelta(days=5*365)
			earliest_date = five_years_ago.strftime ("%Y%m%d")
			new_data = self.updater.FetchNewData(earliest_date)
		
		## new_data is either a list with the new data or bool False
		if new_data:
			with open(self.DATA_FILE,'a') as csvfile:
				data_writer = csv.writer(csvfile)
				for row in new_data:
					data_writer.writerow(row)
