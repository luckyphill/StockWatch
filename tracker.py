## The stock tracker object

## There will be three lists:
## A code list that contains all the codes from the raw data files
## A watch list that conatins the stock codes that the user is interested in
## An ignore list that the user specifically does not want to be notified of

## The Tracker object handles the day-to-day management of the data
## It will determine when updates will occur, and handle notifying the user of interesting info
## I imagine it will be possible to have multiple trackers running with different watch lists, but I don't see why this should happen
## Perhaps running this as a singleton would be a good idea

from global_vars import *
import csv
import stock
import updater
import os
import urllib
import zipfile
import shutil

import datetime as dt
from dateutil.relativedelta import relativedelta, FR


class Tracker:
	def __init__(self, watch_list):
		self.watch_list = []
		self.WATCH_LIST_FILE = watch_list
		self.stocks = {}

		self.URL_HISTORICAL = 'https://www.asxhistoricaldata.com/data/'

	def GetWatchList(self):
		## Loads the watch_list from file
		logger = logging.getLogger(LOG)

		watch_list = []
		try:
			with open(self.WATCH_LIST_FILE,'r') as file:
				data_reader = csv.reader(file)
				for entry in data_reader:
					watch_list.append(entry[0])
		except:
			logger.error("Error with retrieving watch list")
			raise Exception("Error with retrieving watch list")

		logger.info("Retrieved watch list from %s", self.WATCH_LIST_FILE)
		return watch_list

	def UpdateStockDict(self):
		## Populates self.stocks with the stocks in the watch list
		watch_list = self.GetWatchList()

		for code in watch_list:
			if code not in self.stocks:
				self.stocks[code] = stock.Stock(code,updater.FromBigCharts)

	def EoDUpdate(self):
		## Updates each stock with the latest data
		self.UpdateStockDict()

		for stock in self.stocks:
			stock.GetNewData()

	def UpdateArchive(self):
		# This will run once a week
		logger = logging.getLogger(LOG)

		date = dt.datetime.now() + relativedelta(weekday=FR(-1))

		file_name = 'week' + date.strftime("%Y%m%d") + ".zip"
		online_file = self.URL_HISTORICAL + file_name
		save_file = ZIP_PATH + file_name

		extracted_location = ZIP_PATH + 'week' + date.strftime("%Y%m%d") + '/'
		
		if not os.path.exists(ZIP_PATH):
			os.makedirs(ZIP_PATH)

		if not os.path.isfile(save_file):
			try:
				logger.info("Downloading historical data from %s", online_file)
				urllib.urlretrieve (online_file, save_file)

			except:
				logger.info("Download process failed")
				# popupmsg('Auto Download', "Auto Download didn't work mate, try it manually " +  online_file)

			logger.info("Download successful")

			zip_ref = zipfile.ZipFile(save_file, 'r')

			logger.info("Unzipping archive data")
			zip_ref.extractall(ZIP_PATH)
			zip_ref.close()

			logger.info("Extraction successful")

			for file in os.listdir(extracted_location):
				file_to_move = extracted_location + file
				move_to_file = RAW_PATH + file
				shutil.move(file_to_move, move_to_file)

			os.rmdir(extracted_location)
			logger.info("Moving successful")

	def GetSignals(self):
		## For each stock, looks for signals
		pass

	def Notification(self):
		## Notifies the user of a signal
		pass	



