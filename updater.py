## Updater class
## This is an abstract class with some implementations
## I have attempted to make an abstract class using ABC, but it doesn't quite
## work as expected. To get around this, each class needs to be declared
## separately (withou inheritance) and it must follow the template in Updater
## manually without the built in error catching

import requests
from bs4 import BeautifulSoup

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
	def __init__(self, code, last_date):
		URL = 'http://bigcharts.marketwatch.com/quickchart/quickchart.asp?symb=AU%3A'
		URL_END = '&insttype=Stock&freq=1&show=&time=8'

		self.code = code
		self.URL = URL + code + URL_END
		self.last_date = last_date

	def FetchNewData(self):
		## Gets the all the missing data from BigCharts
		logger = logging.getLogger(LOG)
		logger.info("Getting new data for %s", self.code)

		##
		new_data = []

		today = dt.date.today().strftime ("%Y%m%d")

		if self.last_date == today: # make sure we haven't already got today's data
			
			logger.info("Data appears to be up to date.")
		
		elif self.last_date < today: # make sure we're adding the next date
			logger.info("Getting missing data")
			logger.info("Fetching most recent data for date %s", today)
			
			most_recent = self.FetchMostRecent()
			most_recent_date = most_recent[0]

			next_date = self.GetNextDate(self.last_date)

			## If the next date after last_date isn't most_recent_date
			## then we need to make sure the data in between exists
			## This while loop will always be triggered on a Monday so
			## need to skip the data fetching if next_date is a weekend
			logger.info("Checking for other missing dates")
			while next_date < most_recent_date:
				year 	= int(next_date[:4])
				month 	= int(next_date[4:6])
				day 	= int(next_date[6:])

				if dt.datetime(year,month,day).weekday()<5:
					## Ignore weekends
					data = self.FetchHistorical(next_date)
					if data:
						## Sometime weekdays won't have data i.e. public holidays
						logger.info("Retrieved data for %s, %s", next_date, data)
						new_data.append(data)
				
				next_date = self.GetNextDate(next_date)


			new_data.append(most_recent)

			self.last_date = most_recent_date

		else:
			logger.error("Something has gone wrong, we appear to be adding old data for " + self.code)
			raise Exception("Something has gone wrong, we appear to be adding old data for " + self.code)
			return False

		return new_data

	def FetchMostRecent(self):
		## This attempts to get the most recent data

		logger = logging.getLogger(LOG)
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

		##=====================================================
		# all neatly tabulated ready for writing
		eod_data = [proper_date, open_p, high, low, close, vol]

		logger.info("Retrieval complete")

		return eod_data

	def FetchHistorical(self, date):
		## Uses the historical page on Big Charts to get the data from a specific date
		HISTORICAL_URL = 'http://bigcharts.marketwatch.com/historical/default.asp?symb=au%3A'
		HISTORICAL_URL_MID = '&closeDate='
		HISTORICAL_URL_END = '&x=37&y=26'

		logger = logging.getLogger(LOG)
		try:

			date = str(date)
			logger.info("Retrieving data from %s", date)

			year 	= date[:4]
			month 	= date[4:6]
			day 	= date[6:]

			hist_url = HISTORICAL_URL + self.code + HISTORICAL_URL_MID + month + '%2F' + day + '%2F' + year + HISTORICAL_URL_END

			response = requests.get(hist_url)
			html = response.content
			soup = BeautifulSoup(html, "xml")
			table = soup.find('table', id="historicalquote")

		except:
			logger.error("There was an issue retrieving EoD data for " + self.code + ", check that lxml is installed.")
			raise Exception("There was an issue retrieving EoD data for " + self.code + ", check that lxml is installed.")
			return False

		##=====================================================
		## The next section is specific to the historical part of Big Charts
		hist_data = []
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

			logger.info("Retrieval complete for %s", date)
		else:
			hist_data = False
			logger.info("No data on %s", date)

		return hist_data

	def GetNextDate(self,date):
		## Takes a date as a string in the format YYYYMMDD
		## Gives the next date assuming a max of 31 days and 12 months
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

class ForTesting(Updater):
	## For testing only. Gets new data from /testing/fake_new_data/
	def __init__(self, code):
		self.NEW = APP_PATH + 'fake_new_data/'


	def FetchNewData(self):

		files = sorted(os.listdir(self.RAW_PATH))

		

