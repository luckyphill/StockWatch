## Updater class
## This is an abstract class with some implementations

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
	BIG_CHARTS_URL = 'http://bigcharts.marketwatch.com/quickchart/quickchart.asp?symb=AU%3A'
	BIG_CHARTS_URL_END = '&insttype=Stock&freq=1&show=&time=8'

	def __init__(self, code):
		BIG_CHARTS_URL = 'http://bigcharts.marketwatch.com/quickchart/quickchart.asp?symb=AU%3A'
		BIG_CHARTS_URL_END = '&insttype=Stock&freq=1&show=&time=8'
		self.code = code
		self.URL = BIG_CHARTS_URL + code + BIG_CHARTS_URL_END

	def FetchNewData(self, last_date):
		## Gets the most up to date data from BigCharts
		logger = logging.getLogger(LOG)
		logger.info("Getting new data for %s", self.code)

		if last_date == dt.date.today().strftime ("%Y%m%d"): # make sure we haven't already got today's data
			
			logger.info("Data appears to be up to date.")
		
		elif last_date < dt.date.today().strftime ("%Y%m%d"): # make sure we're adding the next date

			try:

				logger.info("Retrieving data from %s",self.URL)

				response = requests.get(self.URL)
				html = response.content
				soup = BeautifulSoup(html, "xml")
				table = soup.find('table', id="quote")

			except:
				logger.error("There was an issue retrieving EoD data for " + self.code)
				raise Exception("There was an issue retrieving EoD data for " + self.code)
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

			logger.info(" Retrieval complete")

			return eod_data

		else:
			logger.error("Something has gone wrong, we appear to be adding old data for " + self.code)
			raise Exception("Something has gone wrong, we appear to be adding old data for " + self.code)
			return False


class ForTesting(Updater):
	## For testing only. Gets new data from /testing/fake_new_data/
	def __init__(self, code):
		self.NEW = APP_PATH + 'fake_new_data/'


	def FetchNewData(self, last_date):

		files = sorted(os.listdir(self.RAW_PATH))

		

