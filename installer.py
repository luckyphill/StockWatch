## An installer function
## Not sure the best way to do this, but will start off as an object

## In order to install, we need the data in a known location in a known format
## The assumed format will be that which comes from www.asxhistoricaldata.com
## Each trading day has a file name YYYYMMDD.txt
## In that file we have for each stock, the code price data, volume data and other stuff
## for that given day
## The data will be processed to be in the form of time series data for each stock
## This will be found in a folder structure StockWatch/data/CODE/time_series.txt
## Firstly this folder structure will be created - this means we need a list of codes
## Secondly, the data will be cleaned and placed in the appropriate file
## Thirdly, all the file paths for each stock, a watch list etc. will be written to a 
## data file which will serve as global variable holder type thing
## The installer will only run if this file does not exist, otherwise, things will be
## handled by the Tracker object

import os
import csv
G_ALL_CODES_FILE = 'all_codes.csv'

class Installer:
	def __init__(self,path_inst_dir,path_raw_data):
		self.PATH_TO_INSTALL_DIRECTORY = path_inst_dir
		self.RAW_PATH = path_raw_data
		self.ALL_CODES_FILE = self.PATH_TO_INSTALL_DIRECTORY + G_ALL_CODES_FILE
		self.initial_codes = []

	def install(self):
		## Performs the installation
		pass

	def write_installation_file(self):
		## Writes a file that will be used to track all the information about
		pass

	def GetPath(self):
		return self.PATH_TO_INSTALL_DIRECTORY

	def GetRawPath(self):
		return self.RAW_PATH

	def GetInitialCodes(self):
		## Reads the most recent of the raw_data files and grabs the stock codes

		latest_file = os.listdir(self.RAW_PATH)[0]
		for file in os.listdir(self.RAW_PATH)[1:]:
			if file > latest_file:
				latest_file = file

		path_to_latest_file = self.RAW_PATH + latest_file

		with open(path_to_latest_file, 'rU') as csvfile:
			code_reader = csv.reader(csvfile, dialect='excel')
			for code in code_reader:
				self.initial_codes.append(code[0])

		with open(self.ALL_CODES_FILE,'w') as file:
			for code in self.initial_codes:
				file.write(code + '\n')

	
	def CleanRawData(self):
		## This will take the raw data, and put it in the correct format
		## It will create the file structure as well

		assert self.initial_codes ## Can't run this unless codes GetInitialCodes() has run first

		##===============================================================

		stockPriceData = []
		latestYear = dt.date.today().year() + 1
		dates = []
		for year in xrange(EARLIEST_YEAR, latestYear):
			for month in xrange(1,13):
				for day in xrange(1,32):
					dates.append(year * 10000 + month * 100 + day)

		for date in dates:
			file_name = RAW_PATH + str(date) + ".txt"
			if os.path.isfile(file_name):
				print "Reading data from " + str(date)
				with open(file_name, 'r') as file:
					data_reader = csv.reader(file, dialect='excel')
					for row in data_reader:
						if row[0] not in stockPriceData and row[0] in codes:
							stockPriceData[row[0]] = []
						stockPriceData[row[0]].append(row[1:])

		# save the data into a csv file
		# make the folder if it doesn't exist
		if not os.path.exists(STOCK_PATH):
			os.makedirs(STOCK_PATH)
				
		for code in stockPriceData:
			file_name = STOCK_PATH + code + ".csv"
			LOG.write(str(dt.datetime.now()) + " Writing data for " + code + "\n")
			with open(file_name, 'wb') as csvfile:
				writer = csv.writer(csvfile, delimiter=',')
				for row in stockPriceData[code]:
					writer.writerow(row)




