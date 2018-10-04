## An installer function
## Not sure the best way to do this, but will start off as an object

## In order to install, we need the data in a known location in a known format
## The assumed format will be that which comes from www.asxhistoricaldata.com
## Each trading day has a file name YYYYMMDD.txt
## In that file we have for each stock, the code price data, volume data and 
## other stuff for that given day
## The data will be processed to be in the form of time series data for each 
## stock. This will be found in a folder structure 
## StockWatch/data/CODE/time_series.csv
## Firstly this folder structure will be created - this means we need a list of codes
## Secondly, the data will be cleaned and placed in the appropriate file
## Thirdly, global variable are written to global_vars.py including log file handling
## The installer will only be run if this file does not exist, otherwise, things will be
## handled by the Tracker object
## The installer is dumb and will blindly overwrite anything in the directory


import os
import re
import csv
import log
import logging
import datetime as dt


class Installer:
	def __init__(self, path_inst_dir, path_raw_data, earliest_year):
		self.PATH_TO_INSTALL_DIRECTORY = path_inst_dir
		self.RAW_PATH = path_raw_data
		self.DATA_PATH = self.PATH_TO_INSTALL_DIRECTORY + 'data/'
		self.ALL_CODES_FILE_NAME = 'all_codes.csv'
		self.TIME_SERIES_FILE_NAME = 'time_series.csv'
		self.RAW_DATA_REGEX_PATTERN = '\d{8}.txt'
		self.GLOBAL_VARS_FILE_NAME = 'global_vars.py'
		self.RAW_DATA_DATES_FILE_NAME = 'raw_data_dates.csv'
		
		self.RAW_DATA_DATES_FILE = self.PATH_TO_INSTALL_DIRECTORY + self.RAW_DATA_DATES_FILE_NAME
		self.ALL_CODES_FILE = self.PATH_TO_INSTALL_DIRECTORY + self.ALL_CODES_FILE_NAME
		self.GLOBAL_VARS_FILE = self.PATH_TO_INSTALL_DIRECTORY + self.GLOBAL_VARS_FILE_NAME
		self.LOG_PATH = self.PATH_TO_INSTALL_DIRECTORY + 'logs/'

		
		if not os.path.exists(self.LOG_PATH):
			os.makedirs(self.LOG_PATH)
		
		self.initial_codes = []

		self.INSTALL_LOG_FILE =  self.LOG_PATH + 'install.log'
		log.setup_custom_logger('root', self.INSTALL_LOG_FILE)

		self.EARLIEST_YEAR = earliest_year

		logger = logging.getLogger('root')

		try:
			assert os.path.exists(self.RAW_PATH)
		except:
			logger.critical("Path to raw data not found: %s", self.RAW_PATH)
			raise ValueError('Path to raw data not found. Please provide the absolute path to a folder with the specified data format.')

		if not os.listdir(self.RAW_PATH):
			logger.error("No files in the raw data path: %s", self.RAW_PATH)
			raise Exception("No files in the raw data path. Nothing can be done if there is no data!")
			

		if not os.path.exists(self.PATH_TO_INSTALL_DIRECTORY):
			logger.info("Install path does not exist. Creating now")
			os.makedirs(self.PATH_TO_INSTALL_DIRECTORY)

		self.install()

	def GetPath(self):
		return self.PATH_TO_INSTALL_DIRECTORY

	def GetRawPath(self):
		return self.RAW_PATH

	def GetEarliestYear(self):
		return self.EARLIEST_YEAR

	def install(self):
		logger = logging.getLogger('root')

		if os.path.isfile(self.GLOBAL_VARS_FILE):
			logger.error("%s detected. Assuming installation already exists", self.GLOBAL_VARS_FILE_NAME)
			raise Exception("It looks like you already have an installation. Aborting installation")


		logger.info('Getting initial codes from file')
		self.GetInitialCodes()
		logger.info("Initial codes retrieved")

		logger.info("Cleaning raw data")
		self.CleanRawData()
		logger.info("Raw data cleaned")

		logger.info("Writing global variables file")
		self.WriteGlobalVariables()
		logger.info("Global variables file written")

		logger.info("Writing raw data dates file")
		self.WriteRawDataDatesFile()
		logger.info("Raw data dates file written")

		logger.info("Installation complete")
		
	def GetInitialCodes(self):
		## Reads the most recent of the raw_data files and grabs the stock codes
		## This is so the installer has something to install
		logger = logging.getLogger('root')

		## Get only the files that match the pattern YYYMMDD.txt
		regex = re.compile(self.RAW_DATA_REGEX_PATTERN)
		files = [f for f in os.listdir(self.RAW_PATH) if regex.match(f)]

		logger.info('Detected %d files',len(files))
		latest_file = files[0]

		for file in files:
			if file > latest_file:
				latest_file = file

		path_to_latest_file = self.RAW_PATH + latest_file
		
		logger.info('Most recent date in raw data is %s',latest_file)

		with open(path_to_latest_file, 'rU') as csvfile:
			data_reader = csv.reader(csvfile, dialect='excel')
			for line in data_reader:
				code = line[0]
				if code not in self.initial_codes:
					self.initial_codes.append(code)

		logger.info('Now have a total of %d codes', len(self.initial_codes))
		with open(self.ALL_CODES_FILE,'w') as file:
			for code in self.initial_codes:
				file.write(code + '\n')
		logger.info('Codes written to the all_codes file')

	def CleanRawData(self):
		## This will take the raw data, and put it in the correct format
		## It will create the file structure as well
		logger = logging.getLogger('root')
		assert self.initial_codes ## Can't run this unless codes GetInitialCodes() has run first

		##===============================================================

		stockPriceData = {}
		latestYear = dt.date.today().year + 1
		dates = []
		for year in xrange(self.EARLIEST_YEAR, latestYear):
			for month in xrange(1,13):
				for day in xrange(1,32):
					dates.append(year * 10000 + month * 100 + day)

		## This presumes the format of raw data is YYYYMMDD.txt - ought to generalise
		for date in dates:
			file_name = self.RAW_PATH + str(date) + ".txt"
			if os.path.isfile(file_name):
				with open(file_name, 'r') as file:
					data_reader = csv.reader(file, dialect='excel')
					for row in data_reader:
						code = row[0]
						if code not in stockPriceData and code in self.initial_codes:
							stockPriceData[code] = []
						if code in self.initial_codes:	
							stockPriceData[code].append(row[1:])

		logger.info('Data from %d to %d read from file', self.EARLIEST_YEAR, latestYear)

		for code in stockPriceData:
			## File structure: /StockWatch/data/CODE/
			code_path = self.DATA_PATH + code +"/"
			
			if not os.path.exists(code_path):
				os.makedirs(code_path)
			
			file_name = code_path + self.TIME_SERIES_FILE_NAME
			with open(file_name, 'wb') as csvfile:
				writer = csv.writer(csvfile, delimiter=',')
				for row in stockPriceData[code]:
					writer.writerow(row)

		logger.info("Data for %d codes successfully cleaned and written to file", len(stockPriceData))
	
	def WriteRawDataDatesFile(self):
		## Writes a file that contains all the dates that are stored in RAW_PATH
		## This is to speed up accessing the archive data
		## The file will be updated by the Tacker object

		regex = re.compile(self.RAW_DATA_REGEX_PATTERN)
		dates = [f.split('.')[0] for f in os.listdir(self.RAW_PATH) if regex.match(f)]
		ordered_dates = sorted(dates)

		with open(self.RAW_DATA_DATES_FILE, 'w') as d_file:
			for date in ordered_dates:
				d_file.write(date + '\n')



	def WriteGlobalVariables(self):
		## Writes a file that will be used to track all the information about
		with open(self.GLOBAL_VARS_FILE, 'w') as gv_file:
			gv_file.write("## Automatically generated file. Modifying may break the installation\n\n")
			gv_file.write("APP_PATH 				= '%s'\n" % self.PATH_TO_INSTALL_DIRECTORY)
			gv_file.write("DATA_PATH 				= '%s'\n" % self.DATA_PATH)
			gv_file.write("RAW_PATH 				= '%s'\n" % self.RAW_PATH)
			gv_file.write("ALL_CODES_FILE 			= '%s'\n" % self.ALL_CODES_FILE)
			gv_file.write("RAW_DATA_DATES_FILE 	= '%s'\n" % self.RAW_DATA_DATES_FILE)
			gv_file.write("LOG_FILE 				= '%slog_file.log'\n" % self.LOG_PATH)
			gv_file.write("TIME_SERIES_FILE_NAME 	= '%s'\n" % self.TIME_SERIES_FILE_NAME)
			gv_file.write("LOG 					= 'log_reference' # Just some name to put in the variable\n")
			gv_file.write('\n#=================================================\n\n')
			gv_file.write("## Creating the global logger\n")
			gv_file.write('import logging\nimport log\n')
			gv_file.write("log.setup_custom_logger(LOG, LOG_FILE)\n")

class Uninstaller:
	def __init__(self, path_inst_dir):
		## Removes all the data in the installation path
		## Might be better implemented as a script writer in the Installer

		pass