## The stock object
## Should do all the handling of actual stock data

##=====================================================
## This section is only needed for testing
## It should be deleted before running properly
import sys
PATH_FOR_INSTALLER = '/Users/phillipbrown/StockWatch/testing/'
sys.path.insert(0, PATH_FOR_INSTALLER)
##=====================================================

import csv
from global_vars import *

class Stock:
	def __init__(self, code, updater_object):
		self.code = code
		self.DIRECTORY = DATA_PATH + code +'/'
		self.DATA_FILE = self.DIRECTORY + TIME_SERIES_FILE_NAME

		self.updater = updater_object(code, self.GetLastDate())
		## Declaring the object

	def GetDataFile(self):
		return self.DATA_FILE

	def GetLastDate(self):
		## Get the most recent date that we have data
		stockData = self.GetStockData()
		return stockData[-1][0]


	def GetStockData(self):
		## Loads the data from file
		## Assumes that the data file is structured:
		## date,open,high,low,close,volume

		stockData = []
		with open(self.DATA_FILE,'r') as csvfile:
			data_reader = csv.reader(csvfile)
			for line in data_reader:
				stockData.append([float(i) for i in line])

		return stockData



	def GetNewData(self):
		## This will get the latest data at a time controlled by Tracker
		## Since it uses an Updater object, we don't care about the implementation
		
		new_data = self.updater.FetchNewData()
		
		## new_data is either a list with the new data or bool False
		if new_data:
			with open(self.DATA_FILE,'a') as csvfile:
				data_writer = csv.writer(csvfile)
				for row in new_data:
					data_writer.writerow(row)



	def eod_update(self):
		## Manages all the updating procedures
		pass

	def get_latest_price(self):
		## Accesses the designated website to get the end of day data

		pass

	def initialise_stock(self):
		## Used when there is only raw data

		pass