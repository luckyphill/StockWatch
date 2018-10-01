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
		## This will be slow and could sorely do with optimising
		stockData = self.GetStockData()
		return str(stockData[-1][0])

	def GetStockData(self):
		## Loads the data from file
		## Assumes that the data file is structured:
		## date,open,high,low,close,volume
		stockData = []
		with open(self.DATA_FILE,'r') as csvfile:
			data_reader = csv.reader(csvfile)
			for line in data_reader:
				## The line is date,open,high,low,close,volume
				## date and volume shold be ints, the rest floats
				stockData.append([line[0], float(line[1]), float(line[2]), float(line[3]), float(line[4]), int(line[5])])

		return stockData

	def GetNewData(self):
		## This will get the latest data at a time controlled by Tracker
		## The data is retrieved by an Updater object, then written to file

		## Need to implement a check to see if the stock is brand new without any data
		## in the DATA_PATH
		## There are three cases: 
		## 1. We have the data, but have ignored it (shouldn't happen with this implementation)
		## 2. We don't have the data and the stock has existed for some time
		## 3. We don't have the data because the stock has just floated
		
		new_data = self.updater.FetchNewData()
		
		## new_data is either a list with the new data or bool False
		if new_data:
			with open(self.DATA_FILE,'a') as csvfile:
				data_writer = csv.writer(csvfile)
				for row in new_data:
					data_writer.writerow(row)
