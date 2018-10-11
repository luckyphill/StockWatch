## Updater class
## This is an abstract class with some implementations
## I have attempted to make an abstract class using ABC, but it doesn't quite
## work as expected. To get around this, each class needs to be declared
## separately (withou inheritance) and it must follow the template in Updater
## manually without the built in error catching

import requests
from bs4 import BeautifulSoup

import csv
import time
import datetime as dt

from global_vars import *

from abc import ABCMeta, abstractmethod

class Updater:
	__metaclass__ = ABCMeta

	@abstractmethod
	def __init___(self, code):
		self.code = code

	@abstractmethod
	def FetchNewData(self, last_date):
		pass

class FromBigCharts:#(Updater):
	def __init__(self, code):
		URL = 'http://bigcharts.marketwatch.com/quickchart/quickchart.asp?symb=AU%3A'
		URL_END = '&insttype=Stock&freq=1&show=&time=8'

		HISTORICAL_URL = 'http://bigcharts.marketwatch.com/historical/default.asp?symb=au%3A'
		HISTORICAL_URL_MID = '&closeDate='
		HISTORICAL_URL_END = '&x=37&y=26'

		self.MAX_YEARS_AGO_FOR_SCRAPING = 2

		self.code = code
		self.URL = URL + code + URL_END
		self.HISTORICAL_URL = HISTORICAL_URL + self.code + HISTORICAL_URL_MID
		self.HISTORICAL_URL_END = HISTORICAL_URL_END

	def FetchNewData(self, last_quote_date):
		## Gets the all the missing data from BigCharts or archives
		## last_quote_date will be provided from Stock, which will get it
		## directly from the file. This is the most recent data that exists
		## in data file
		logger = logging.getLogger(LOG)
		logger.info("Getting new data for %s", self.code)

		## A list to hold all the data retrieved
		new_data = []

		today = dt.date.today().strftime ("%Y%m%d")

		if last_quote_date == today: # make sure we haven't already got today's data
			
			logger.info("Data appears to be up to date.")
			new_data = False
		
		elif last_quote_date < today: # make sure we're adding the next date
			logger.info("Getting missing data")
			logger.info("Fetching most recent data for date %s", today)
			
			most_recent = self.FetchMostRecent()

			if most_recent == False:
				## Something has gone wrong with retrieval of todays data
				## This could happen if BigCharts doesn't list the stock
				## It could also happen if the website fails to load (i.e. no internet connection)
				## In this case the best approach is to abort the FetchNewData method
				logger.info("Data not retrieved for %s", self.code)
				return False

			most_recent_date = most_recent[0]

			if most_recent_date == last_quote_date:
				## Sometime BigCharts doesn't give an entry for today if there was no trading
				## It just shows the most recent actual trading day
				## So, if that data is already stored, we don't need it
				logger.info("We already have data for this date, discarding.")
				return False

			logger.info("Today's data received %s",most_recent)

			next_date = self.GetNextDate(last_quote_date)

			## If the next date after last_quote_date isn't most_recent_date
			## then we need to make sure the data in between exists
			## This while loop will always be triggered on a Monday so
			## need to skip the data fetching if next_date is a weekend

			## It can look back an arbitrary amount of time backwards
			## but it only grabs data from the web if it won't end up
			## grabbing more than MAX_YEARS_AGO_FOR_SCRAPING worth of data
			## If it's older than that, only looks in the archives
			## This might mean that data is missed if it is available
			## on the web not not in the archive
			logger.info("Checking for other missing dates")
			while next_date < most_recent_date:
				year 	= int(next_date[:4])
				month 	= int(next_date[4:6])
				day 	= int(next_date[6:])

				try:
					## This put in a try statement because GetNextDate is a simplified date checker
					## and it always assumes 29 days in Feb, therefore dt.date will throw an exception
					## since the date doesn't exist every year
					dt_next_date = dt.date(year,month,day)

					## If is is a weekday, then retrieve the data
					if dt_next_date.weekday()<5:				
						max_years_ago = dt.date.today() - dt.timedelta(days = 365 * self.MAX_YEARS_AGO_FOR_SCRAPING) 
						
						## Date is not more than MAX_YEARS_AGO_FOR_SCRAPING so can get from BigCharts
						## Else if it is too far long ago, then restrict to archives
						logger.info("Searching for data for %s on %s", self.code, next_date)
						if  dt_next_date > max_years_ago:
							data = self.FetchHistorical(next_date)
						else:
							raw_data_dates = self.GetRawDataDates()
							if next_date in raw_data_dates:
								data = self.FetchHistoricalFromRawData(next_date)
							else:
								logger.info("The date %s is not in the archive", next_date)
								data = False

						## If any data was retrieved, add it to new_data
						if data:
							logger.info("Retrieved data for %s, %s", next_date, data)
							new_data.append(data)
				except:
					## Date doesn't exist
					logger.info("February problem caught")
					
				next_date = self.GetNextDate(next_date)


			logger.info("All missing data retrieved for %s on %s, validating", self.code, today)
			new_data.append(most_recent)

			## Sometimes BigCharts puts today's data as yesterday's data
			## This is due to a time zone issue which can be grabbed in the first instance by the update scheduler
			## However the exact nature of the bug is no clear, so
			## add in a check to make sure the BigCharts bug hasn't happened
			## If it has, delete the data to preserve the accuracy of the stored data
			if len(new_data) > 1:
				## The following check will be triggered when there is no trading today and/or yesterday
				## so need to account for this case
				if new_data[-1][-1] != 0 and new_data[-2][-1] !=0:
					try:
						assert new_data[-1][1:5] != new_data[-2][1:5]
					except:
						logger.error("BigCharts time difference bug encountered for %s on %s. Removed the offending data.", self.code, most_recent_date)
						## Remove the last two lines of data
						del new_data[-2:]

		else:
			logger.error("Something has gone wrong, we appear to be adding old data for " + self.code)
			raise Exception("Something has gone wrong, we appear to be adding old data for " + self.code)
			return False

		logger.info("Data retrieval complete.")
		return new_data

	def FetchMostRecent(self):
		## This attempts to get the most recent data

		logger = logging.getLogger(LOG)

		## In a try statement because downloading from the internet.
		## There could be any number of reasons why it could fail
		try:

			logger.info("Retrieving most recent data from %s",self.URL)

			response = requests.get(self.URL)
			html = response.content
			soup = BeautifulSoup(html, "xml")
			table = soup.find('table', id="quote")

		except:
			logger.error("There was an issue retrieving EoD data for " + self.code + ", check that lxml is installed.")
			raise Exception("There was an issue retrieving EoD data for " + self.code + ", check that lxml is installed.")
			return False


		if table == None:
			## No data available on BigCharts, need to look elsewhere
			logger.info("BigCharts does not have data for %s", self.code)
			return False
		else:
			##=====================================================
			## The next section is specific to this website
			temp_data = []
			for row in table.findAll('tr'):
				for cell in row.findAll('td'):
					temp_data.append(cell.text)
			
			# clean the data according to how the website presented it
			date = temp_data[1].split(' ')[0]
			open_p = temp_data[9].split('\n')[2]
			high = temp_data[10].split('\n')[2]
			low = temp_data[11].split('\n')[2]
			close = temp_data[7].split('\n')[2]
			vol = temp_data[12].split('\n')[2].replace(',', '')

			[month,day,year] = date.split('/')
			proper_date = year + month.zfill(2) + day.zfill(2)

			

			logger.info("Retrieval complete, validating.")

			## If there has been no trading today, then BigCharts displays 'n\a' in the open high and low columns
			if open_p == 'n/a':
				## Cleaning the data to get rid of 'n/a'
				logger.info("Caught the no-trading-n/a issue.")
				eod_data = [proper_date, close, close, close, close, vol]

			else:
				## Everything has worked properly
				eod_data = [proper_date, open_p, high, low, close, vol]

		logger.info("Retrieval complete. Today's data obtained for %s.", self.code)
		
		return eod_data

	def FetchHistorical(self, date):
		## Decides which way to get historical data
		## either from the web, or the raw data archive
		logger = logging.getLogger(LOG)
		logger.info("Started search for historical data for %s on %s", self.code, date)

		new_data = False
		raw_data_dates = self.GetRawDataDates()
		
		if date in raw_data_dates:
			new_data = self.FetchHistoricalFromRawData(date)
			if not new_data:
				## Stock wasn't found in the archive data
				## This could be because it's not part of the archive - check online
				## or because it wasn't around at the date in question - it won't be online either
				new_data = self.FetchHistoricalFromBigCharts(date)
		else:
			new_data = self.FetchHistoricalFromBigCharts(date)

		if new_data:
			logger.info("Search complete. Data successfully retrieved for %s on %s", self.code, date)
		else:
			logger.info("Search complete. No data found for %s on %s", self.code, date)
		
		return new_data

	def FetchHistoricalFromBigCharts(self, date):
		## Uses the historical page on Big Charts to get the data from a specific date
		

		logger = logging.getLogger(LOG)
		date = str(date)
		

		year 	= date[:4]
		month 	= date[4:6]
		day 	= date[6:]

		hist_url = self.HISTORICAL_URL + month + '%2F' + day + '%2F' + year + self.HISTORICAL_URL_END
		logger.info("Searching online for %s on %s from %s",self.code, date, hist_url)
		
		try:
			response = requests.get(hist_url)
			html = response.content
			soup = BeautifulSoup(html, "xml")
			table = soup.find('table', id="historicalquote")

		except:
			logger.error("There was an issue retrieving EoD data for " + self.code + ". Check that lxml is installed.")
			raise Exception("There was an issue retrieving EoD data for " + self.code + ". Check that lxml is installed.")
			return False

		##=====================================================
		## The next section is specific to the historical part of Big Charts
		hist_data = []

		## table could be empty if there is no data
		if table:
			temp_data = []
			for row in table.findAll('tr'):
				for cell in row.findAll('td'):
					temp_data.append(cell.text)
			
			# clean the data according to how the website presented it
			open_p = temp_data[4]
			high = temp_data[5]
			low = temp_data[6]
			close = temp_data[3]
			vol = temp_data[7].replace(',', '')

			##=====================================================
			# all neatly tabulated ready for writing
			hist_data = [date, open_p, high, low, close, vol]

			if hist_data[-1] == 'n/a':
				logger.info('Caught day with no trading, fixing volume column')
				hist_data[-1] = 0
		else:
			logger.info("No data on %s", date)
			return False

		logger.info("Online historical data found!")
		return hist_data

	def FetchHistoricalFromRawData(self,date):
		## Get the data from pre-downloaded archive data in RAW_PATH
		## This will save querying BigCharts too much
		## It shouldn't cause an issue for small amounts,
		## but for lots of data it might get blocked with an IP ban for abusing the system
		logger = logging.getLogger(LOG)

		## In the data file are all stocks for that date,
		## need to get the specific one we're after
		data_file = RAW_PATH + date + '.txt'
		logger.info("Searching local archive for %s on %s",self.code, date)

		data = []

		try:
			with open(data_file,'r') as file:
				data_reader = csv.reader(file)
				for line in data_reader:
					if line[0] == self.code:
						data = line[1:]
						break
		except:
			logger.info("Error reading file %s", data_file)
			return False

		if data:
			logger.info("Local historical data found! %s", data)
			return data
		else:
			logger.info("No local historical data found. Either not in archive, or wasn't trading yet.")
			return False

	def GetNextDate(self,date):
		## Takes a date as a string in the format YYYYMMDD
		## Gives the next date assuming a max of 31 days and 12 months
		## It would probably be much smarter to use a datetime increment
		## but this works
		year 	= int(date[:4])
		month 	= int(date[4:6])
		day 	= int(date[6:])

		day = day + 1
		if day > 31 or (day > 30 and month in [4,6,9,11]) or (day > 29 and month == 2):
			day = 1
			month = month + 1
			if month > 12:
				month = 1
				year = year + 1

		new_date = str(year) + str(month).zfill(2) + str(day).zfill(2)
		return new_date
	
	def GetRawDataDates(self):
		## Looks in RAW_PATH and determines which dates we have data for
		dates = []

		with open(RAW_DATA_DATES_FILE, 'r') as file:
			data_reader = csv.reader(file)
			for entry in data_reader:
				dates.append(entry[0])

		return dates


class ForTesting:
	## For testing only. Gets new data from /testing/fake_new_data/
	## This is important for testing Tracker
	
	def __init__(self, code):
		self.NEW = APP_PATH + 'fake_new_data/'
		self.code = code

	def FetchNewData(self, last_quote_date, fake_today):
		## Gets the all the missing data from BigCharts
		## last_quote_date will be provided from Stock, which will get it
		## directly from the file.

		today = fake_today

		logger = logging.getLogger(LOG)
		logger.info("Getting new data for %s", self.code)

		## A list to hold all the data retrieved
		new_data = []

		if last_quote_date == today: # make sure we haven't already got today's data
			
			logger.info("Data appears to be up to date.")
		
		elif last_quote_date < today: # make sure we're adding the next date
			logger.info("Getting missing data")
			logger.info("Fetching most recent data for date %s", today)
			
			most_recent = self.FetchData(today)
			most_recent_date = today

			next_date = self.GetNextDate(last_quote_date)

			## If the next date after last_quote_date isn't most_recent_date
			## then we need to make sure the data in between exists
			## This while loop will always be triggered on a Monday so
			## need to skip the data fetching if next_date is a weekend
			logger.info("Checking for other missing dates")
			while next_date < most_recent_date and next_date < '20190000':
				year 	= int(next_date[:4])
				month 	= int(next_date[4:6])
				day 	= int(next_date[6:])

				try:
					if dt.datetime(year,month,day).weekday()<5:
						## Ignore weekends
						data = self.FetchData(next_date)
						
						if data:
							## Sometimes weekdays won't have data i.e. public holidays
							logger.info("Retrieved data for %s, %s", next_date, data)
							
							if data[-1] == 'n/a':
								logger.info('Caught day with no trading')
								data[-1] = 0
							
							new_data.append(data)
				except:
					logger.info("February problem caught")
				
				next_date = self.GetNextDate(next_date)


			new_data.append(most_recent)

		else:
			logger.error("Something has gone wrong, we appear to be adding old data for " + self.code)
			raise Exception("Something has gone wrong, we appear to be adding old data for " + self.code)
			return False

		return new_data
	
	def FetchData(self, date):
		logger = logging.getLogger(LOG)

		## In the data file are all stocks for that date,
		## need to get the specific one we're after
		data_file = self.NEW + date + '.txt'
		logger.info("Retrieving data for %s from %s",self.code, data_file)

		data = []

		try:
			with open(data_file,'r') as file:
				data_reader = csv.reader(file)
				for line in data_reader:
					if line[0] == self.code:
						data = line[1:]
						break
		except:
			data = False


		return data

	def GetNextDate(self,date):
		## Takes a date as a string in the format YYYYMMDD
		## Gives the next date assuming a max of 31 days and 12 months
		## It would probably be much smarter to use a datetime increment
		## but this works
		year 	= int(date[:4])
		month 	= int(date[4:6])
		day 	= int(date[6:])

		day = day + 1
		if day > 31 or (day > 30 and month in [4,6,9,11]) or (day > 29 and month == 2):
			day = 1
			month = month + 1
			if month > 12:
				month = 1
				year = year + 1

		new_date = str(year) + str(month).zfill(2) + str(day).zfill(2)
		return new_date








		

