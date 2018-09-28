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

class Installer:
	def __init__(self,path_inst_dir,path_raw_data):
		self.PATH_TO_INSTALL_DIRECTORY = path_inst_dir
		self.RAW_PATH = path_raw_data
		self.ALL_CODES_FILE = self.PATH_TO_INSTALL_DIRECTORY + 'all_codes.csv'

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
		all_codes = []

		latest_file = os.listdir(self.RAW_PATH)[0]
		for file in os.listdir(self.RAW_PATH)[1:]:
			if file > latest_file:
				latest_file = file

		path_to_latest_file = self.RAW_PATH + latest_file

		with open(path_to_latest_file, 'rU') as csvfile:
			code_reader = csv.reader(csvfile, dialect='excel')
			for code in code_reader:
				all_codes.append(code[0])

		with open(self.ALL_CODES_FILE,'w') as file:
			for code in all_codes:
				file.write(code + '\n')




